from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

from social.forms import PostForm, MediaForm
from social.models import Post, Media
# Create your views here.

# Cette vue permet de créer une publication avec des fichiers multimédias associés. 
# Il gère à la fois les données de formulaire et les fichiers téléchargés
def create_post(request):
    template_name = 'post/create_post.html'
    context = {}
    MediaFormset = modelformset_factory(Media, form=MediaForm, extra=2)
    # si le formulaire a été soumis
    if request.method == 'POST':
        # recupère les données de chaque formulaire
        form_post = PostForm(request.POST)
        form_media = MediaFormset(request.POST, request.FILES, queryset=Media.objects.none())

        # vérifie si les données soumises sont valides selon les règles de validation
        if form_post.is_valid() and form_media.is_valid():
            # sauveegarde l'instance(post) dans une variable sans la sauvegarder ds le DB
            post = form_post.save(commit=False)
            # ensuite associé la publication à l'utilisateur 
            post.owner = request.user
            # enfin sauvegarder dans la DB
            post.save()

            # Sauvegarder chaque formulaire dans le formset 
            for form in form_media.cleaned_data:
                if form:
                    image = form['image']
                    # créé une instance Media pour chaque fichier
                    Media.objects.create(post=post, image=image)
            # affiche un message de succès si la publication est créée.
            messages.success(request, 'Publication créée avec succès')
            return redirect('post_list')
        else:
            messages.error(request, 'Une erreur est survenue, veuillez réessayer')
    # sinon renvoie moi un formulaire vide
    else:
        form_post = PostForm()
        # signifie qu'on ne veut rien recupérer au niveau de la DB
        form_media = MediaFormset(queryset=Media.objects.none())
        messages.info(request, 'Veuillez remplir le formulaire')
    
    context['form_post'] = form_post
    context['form_media'] = form_media
    return render(request, template_name, context)


@login_required
def post_list(request):
    template_name = 'post/post_list.html'
    context = {}
    # recupère toutes les posts avec leurs propriétaires et leurs users qui les aiment
    posts = Post.objects.select_related('owner').prefetch_related('users_like').all()
    context['posts'] = posts
    return render(request, template_name, context)
