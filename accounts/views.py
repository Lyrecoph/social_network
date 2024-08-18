
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import User


from django.forms import modelformset_factory
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.apps import apps

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from social.forms import PostForm, MediaForm, CommentForm
from social.models import Post, Media, Comment, Notification
from accounts.models import Follow
from accounts.forms import UserRegistration
from accounts.models import CustomUser as User
# Create your views here.

# ce decorateur empêche les utilisateurs non connectés de voir la page
@login_required
def profile(request):
    template_name='accounts/profile.html'
    post_list = Post.objects.all()
    context = {'session': 'profile', 'post_list': post_list}
    return render(request, template_name, context)

@login_required
def updateProfile(request, username):
    template_name='user/update.html'
    user = get_object_or_404(Post, username=username)
    # if request.method == 'POST':
        



# Affiche la liste des utilisateurs
@login_required
def user_list(request):
    template_name = 'user/list.html'
    # récupère les utilisateurs actives et exclut celui qui est connecter dans un queryset(user_list)
    user_list = User.objects.filter(is_active=True).exclude(id=request.user.id)
    # parcours mon queryset et compte moi le nbre d'utilisateur qui suit un utilisateur lambda
    # et met la réponse dans la variable follow_count
    for user in user_list:
        user.follow_count = user.followers.count()
    context = {'session': 'user', 'user_list': user_list}
    return render(request, template_name, context)

# Affiche les détails d'un utilisateur
@login_required
def user_detail(request, username, email):
    template_name = 'user/detail.html'
    user = get_object_or_404(User, username=username, is_active=True)
    context = {'session': 'user', 'user': user}
    return render(request, template_name, context)

# Cette fonction permet de nous générer le formulaire d'enregistrement 
# d'un nouvel utilisateur
def register(request):
    # si un formulaire a été soumis
    if request.method == 'POST':
        # recupère les données du formulaire
        register_form = UserRegistration(request.POST)
        # si les données sont valides alors
        if register_form.is_valid():
            # prepare à sauvegarder les données
            # (cela permet de manipuler l'objet avant de le sauvegarder)
            new_user = register_form.save(commit=False)
            # hacher le pwd recupérer saisi par user dans le formulaire après que 
            # le nettoyage des données a été effectué pour s'assurer qu'elles sont 
            # valides et sécurisées avant de l'enregistrer
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        register_form = UserRegistration()
    return render(request, 'accounts/register.html', {'register_form': register_form})

@login_required
@require_POST
def follow_user(request):
    # récupèrer l'id de l'utilisateur que l'on veut suivre ou ne pas suivre
    user_to_id = request.POST.get('id')
    # récuperer l'action qui peut être un follow ou unfollow
    action = request.POST.get('action')
    # si ces deux variables existent
    if user_to_id and action:
        try:
            # récupère moi l'utilisateur qui corespond à cet id
            user_to = User.objects.get(id=user_to_id)
            if action == 'follow':
                Follow.objects.get_or_create(user_from=request.user, user_to=user_to)
            else:
                Follow.objects.filter(user_from=request.user, user_to=user_to).delete()
            return JsonResponse({'status':'success','message': 'Action effectuée avec succès'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error','message': 'Cet élément n\'existe pas'})

    return JsonResponse({'status': 'error','message': 'Une erreur est survenue'})