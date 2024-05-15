from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import UserRegistration
# Create your views here.

# ce decorateur empêche les utilisateurs non connectés de voir la page
@login_required
def profile(request):
    template_name='accounts/profile.html'
    context = {'session': 'profile'}
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