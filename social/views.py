from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.forms import modelformset_factory
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.apps import apps

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from social.forms import PostForm, MediaForm, CommentForm
from social.models import Post, Media, Comment, Notification
# Create your views here.

# Cette vue permet de créer une publication avec des fichiers multimédias associés. 
# Il gère à la fois les données de formulaire et les fichiers téléchargés
# @login_required
# def create_post(request):
#     template_name = 'post/create_post.html'
#     context = {}
#     MediaFormset = modelformset_factory(Media, form=MediaForm, extra=2)
#     # si le formulaire a été soumis
#     if request.method == 'POST':
#         # recupère les données de chaque formulaire
#         form_post = PostForm(request.POST)
#         form_media = MediaFormset(request.POST, request.FILES, queryset=Media.objects.none())

#         # vérifie si les données soumises sont valides selon les règles de validation
#         if form_post.is_valid() and form_media.is_valid():
#             # sauveegarde l'instance(post) dans une variable sans la sauvegarder ds le DB
#             post = form_post.save(commit=False)
#             # ensuite associé la publication à l'utilisateur 
#             post.owner = request.user
#             # enfin sauvegarder dans la DB
#             post.save()

#             # Sauvegarder chaque formulaire dans le formset 
#             for form in form_media.cleaned_data:
#                 if form:
#                     image = form['image']
#                     # créé une instance Media pour chaque fichier
#                     Media.objects.create(post=post, image=image)
#             # affiche un message de succès si la publication est créée.
#             messages.success(request, 'Publication créée avec succès')
#             return redirect('post_list')
#         else:
#             messages.error(request, 'Une erreur est survenue, veuillez réessayer')
#     # sinon renvoie moi un formulaire vide
#     else:
#         form_post = PostForm()
#         # signifie qu'on ne veut rien recupérer au niveau de la DB
#         form_media = MediaFormset(queryset=Media.objects.none())
#         messages.info(request, 'Veuillez remplir le formulaire')
    
#     context['form_post'] = form_post
#     context['form_media'] = form_media
#     return render(request, template_name, context)

# @login_required
# def update_post(request, post_id):
#     template_name = 'post/create_post.html'
#     context = {}
#     post = get_object_or_404(Post, pk=post_id)
#     media = post.post_media.all()
#     MediaFormset = modelformset_factory(Media, form=MediaForm, extra=2, can_delete=True)

#     if request.method == 'POST':
#         form_post = PostForm(request.POST, instance=post)
#         form_media = MediaFormset(request.POST, request.FILES, queryset=media)

#         if form_post.is_valid() and form_media.is_valid():
#             post = form_post.save(commit=False)
#             post.owner = request.user
#             post.save()

#             for form in form_media:
#                 if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
#                     image = form.cleaned_data.get('image')
#                     if image:
#                         Media.objects.create(post=post, image=image)
#                 elif form.cleaned_data.get('DELETE'):
#                     if form.instance.pk:
#                         form.instance.delete()

#             messages.success(request, 'Publication mise à jour avec succès')
#             return redirect('post_list')
#         else:
#             messages.error(request, 'Une erreur est survenue, veuillez réessayer')
#     else:
#         form_post = PostForm(instance=post)
#         form_media = MediaFormset(queryset=media)
#         messages.info(request, 'Veuillez remplir le formulaire')

#     context['form_post'] = form_post
#     context['form_media'] = form_media
#     return render(request, template_name, context)

# Vue pour créer et mettre à jour les publications
@method_decorator(login_required, name='dispatch')
class PostCreateUpdateView(View):
    template_name = 'post/create_post.html'
    
    def get(self, request, post_id=None):
        if post_id:
            post = get_object_or_404(Post.objects.select_related('owner')\
                                    .prefetch_related('users_like').all(), pk=post_id)
            media = post.post_media.all()
            form_post = PostForm(instance=post)
            MediaFormset = modelformset_factory(Media, form=MediaForm, extra=2, can_delete=True)
            form_media = MediaFormset(queryset=media)
            messages.info(request, 'Veuillez remplir le formulaire pour mettre à jour la publication.')
        else:
            form_post = PostForm()
            MediaFormset = modelformset_factory(Media, form=MediaForm, extra=2)
            form_media = MediaFormset(queryset=Media.objects.none())
            messages.info(request, 'Veuillez remplir le formulaire pour créer une nouvelle publication.')
        
        context = {
            'form_post': form_post,
            'form_media': form_media,
            'session' : 'post'
        }
        return render(request, self.template_name, context)
    
    def post(self, request, post_id=None):
        if post_id:
            post = get_object_or_404(Post.objects.select_related('owner')\
                                    .prefetch_related('users_like').all(), pk=post_id)
            media = post.post_media.all()
            form_post = PostForm(request.POST, instance=post)
            MediaFormset = modelformset_factory(Media, form=MediaForm, extra=2, can_delete=True)
            form_media = MediaFormset(request.POST, request.FILES, queryset=media)
        else:
            post = None
            form_post = PostForm(request.POST)
            MediaFormset = modelformset_factory(Media, form=MediaForm, extra=2)
            form_media = MediaFormset(request.POST, request.FILES, queryset=Media.objects.none())

        if form_post.is_valid() and form_media.is_valid():
            post = form_post.save(commit=False)
            post.owner = request.user
            post.save()
            
            for form in form_media:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    image = form.cleaned_data.get('image')
                    if image:
                        Media.objects.create(post=post, image=image)
                elif form.cleaned_data.get('DELETE'):
                    if form.instance.pk:
                        form.instance.delete()

            # Enregistrer la notification
            action = 'mis à jour une publication' if post_id else 'créé une nouvelle publication'
            # Notification.objects.create(user=request.user, action=action)
            add_notification(request.user, action, post)
            
            messages.success(request, 'Publication mise à jour avec succès' if post_id else 'Publication créée avec succès')
            return redirect('post_list')
            
        else:
            messages.error(request, 'Une erreur est survenue, veuillez réessayer')
        
        context = {
            'form_post': form_post,
            'form_media': form_media,
            'session' : 'post'
        }
        return render(request, self.template_name, context)

# Cette fonction est chargée d'affiché la liste des publications
@login_required
def post_list(request):
    template_name = 'post/post_list.html'
    template_ajax = 'post/ajax_post_list.html'

    context = {}
    # recupère toutes les posts avec leurs propriétaires et leurs users qui les aiment
    posts = Post.objects.select_related('owner').prefetch_related('users_like').all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    page_only = request.GET.get('page_only')
    # récupère toutes les notifications hormis ceux de l'utilisateur connecté
    notifications = Notification.objects.select_related('user', 'content_type').exclude(user_id=request.user.id)
    # récupèrer les utilisateurs que suit l'utilisateur actuellement connecté
    following_ids = request.user.follow_user.values_list('id', flat=True)
    # récupère moi les notifications de l'utilisateur qui se trouve dans la liste des utilisateurs
    # qui suit l'utilisateur actuellement connecté
    notifications = notifications.filter(user_id__in=following_ids)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # si la requête est de type ajax
        if page_only:
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    context['posts'] = posts
    context['notifications'] = notifications
    context['session'] = 'home'


    if page_only:
        return render(request, template_ajax, context)   
    return render(request, template_name, context)

# N'est plus,utiliser est remplacé par add_ajax_comment
# applique le décorateur login_required à toutes les méthodes de la vue. 
@method_decorator(login_required, name='dispatch')
# Cette classe est chargé de la creation et de la modification d'un commentaire
class CommentCreateUpdateView(View):
    template_name = 'comment/form_comment.html'
    
    def get(self, request, post_id=None, comment_id=None):
        context = {}
        post = get_object_or_404(Post.objects.select_related('owner').prefetch_related('users_like').all(), pk=post_id)
        if comment_id:
            comment = get_object_or_404(Comment.objects.select_related('owner').prefetch_related('users_like').all(), pk=comment_id)
            comment_form = CommentForm(instance=comment)
            context['page_title'] = 'Modifier un commentaire'
        else:
            comment_form = CommentForm()
            context['page_title'] = 'Ajouter un commentaire'
        context['form_comment'] = comment_form
        return render(request, self.template_name, context)

    def post(self, request, post_id=None, comment_id=None):
        context = {}
        post = get_object_or_404(Post.objects.select_related('owner').prefetch_related('users_like').all(), pk=post_id)
        if comment_id:
            comment = get_object_or_404(Comment.objects.select_related('owner').prefetch_related('users_like').all(), pk=comment_id)
            comment_form = CommentForm(request.POST, instance=comment)
            context['page_title'] = 'Modifier un commentaire'
        else:
            comment_form = CommentForm(request.POST)
            context['page_title'] = 'Ajouter un commentaire'
            
        if comment_form.is_valid() and post:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.owner = request.user
            comment.save()

            # Enregistrer la notification
            # action = 'commenté une publication'
            # notification = Notification.objects.create(user=request.user, action=action)
            # add_notification(request.user, action, comment)

            messages.success(request, 'Commentaire ajouté avec succès' if not comment_id else 'Commentaire mis à jour avec succès')
            return redirect('post_list')
        else:
            messages.error(request, 'Une erreur est survenue, veuillez réessayer')
        context['form_comment'] = comment_form
        return render(request, self.template_name, context)

  
# cette fonction permet de liker un commentaire soite un publication
@login_required
@require_POST
def like_item(request):
    # recupère l'action si c'est un like ou delike
    action = request.POST.get('action')
    # recupère l'id de l'element à liker ou deliker
    item_id = request.POST.get('item_id')
    # recupère le model de l'element à liker ou deliker
    model = request.POST.get('model')
    # permet d'obtenir un label à partir d'un model
    item = apps.get_model('social', model)

    if action and item_id:
        try:
            # Tente de récupérer le post correspondant à l'id fourni
            obj = item.objects.get(id=item_id)
            if action == 'like':
                # Ajoute l'utilisateur courant à la liste des utilisateurs qui aiment ce post
                obj.users_like.add(request.user)
                add_notification(request.user, action, obj)
            else:
                 # Supprime l'utilisateur courant de la liste des utilisateurs qui aiment ce post
                obj.users_like.remove(request.user)
                add_notification(request.user, action, obj)
            # Retourne une réponse JSON indiquant le succès de l'opération
            return JsonResponse({'status':'success','message': 'Action effectuée avec succès'})
        except item.DoesNotExist:
            return JsonResponse({'status': 'error','message': 'Cet élément n\'existe pas'})

    return JsonResponse({'status': 'error','message': 'Une erreur est survenue'})


# Vue pour ajouter des commentaires via AJAX
@login_required
@require_POST
def add_ajax_comment(request):
    # recupère l'id du post
    post_id = request.POST.get('id')
    # recupère le commentaire
    content = request.POST.get('comment')
    template_name = 'partial/comment_list.html'
    # si l'id et le contenu du post existe
    if post_id and content:
        try:
            # Tente de récupérer le post correspondant à l'id fourni
            post = Post.objects.get(id=post_id)
            comment = Comment.objects.create(post=post, content=content, owner=request.user)
            
            # Créer une notification pour le commentaire ajouté
            add_notification(request.user, 'commenté', post)
            
            context = {'comment': comment}
            return render(request, template_name, context)
        except Post.DoesNotExist:
            return HttpResponse('error')
    return HttpResponse('error')

def add_notification(user, action, target):
    notif = Notification(user=user, action=action, target=target)
    notif.save()

# @login_required
# def add_comment(request, post_id):
#     template_name = 'comment/form_comment.html'
#     context = {}
#     post = get_object_or_404(Post.objects.select_related('owner').prefetch_related('users_like').all(), pk=post_id)
    
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid() and post:
#             comment_form = comment_form.save(commit=False)
#             comment_form.post = post
#             comment_form.owner = request.user
#             comment_form.save()
#             messages.success(request, 'Commentaire ajouté avec succès')
#             return redirect('post_list')
#         else:
#             messages.error(request, 'Une erreur est survenue, veuillez réessayer')
#     else:
#         comment_form = CommentForm()
#         context['form_comment'] = comment_form
#     return render(request, template_name, context)

# @login_required
# def update_comment(request, post_id, comment_id):
#     template_name = 'comment/form_comment.html'
#     context = {}
#     post = get_object_or_404(Post.objects.select_related('owner').prefetch_related('users_like').all(), pk=post_id)
#     comment = get_object_or_404(Comment.objects.select_related('owner').prefetch_related('users_like').all(), pk=comment_id)
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST, instance=comment)
#         if comment_form.is_valid() and post:
#             comment_form = comment_form.save(commit=False)
#             comment_form.post = post
#             comment_form.owner = request.user
#             comment_form.save()
#             messages.success(request, 'Commentaire ajouté avec succès')
#             return redirect('post_list')
#         else:
#             messages.error(request, 'Une erreur est survenue, veuillez réessayer')
#     else:
#         comment_form = CommentForm(instance=comment)
#         context['form_comment'] = comment_form
#     return render(request, template_name, context)
        