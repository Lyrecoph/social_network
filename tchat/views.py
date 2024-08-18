from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required


from .models import Conversation, Message
from accounts.models import CustomUser as User
# Create your views here.

# Vue pour la page d'accueil du tchat
@login_required
def tchat_home(request, username):
    template_name = 'tchat/tchat.html'
    try:
        user_to = get_object_or_404(User, username=username, is_active=True)
        following_users = request.user.follow_user.all()
        
        following_with_status = []
        for following in following_users:
            is_online = any(conv.is_user_online(following) for conv in following.conversation_set.all())
            following_with_status.append({
                'username': following.username,
                'is_online': is_online
            })
        print("Les utilisateurs en ligne", following_with_status )

        # Déterminer si user_to est en ligne
        is_user_to_online = any(conv.is_user_online(user_to) for conv in user_to.conversation_set.all())
        # récupere quand l'utilisateur s'est déconnecté
        last_seen = user_to.last_seen
    except Exception as e:
        print(e)
        return HttpResponseForbidden("Vous devez suivre un utilisateur avant d'envoyer un message")
    
    context = {
        'user_to': user_to,
        'user': request.user,
        'following_users': following_with_status,
        'is_user_to_online': is_user_to_online,
        'last_seen': last_seen
    }
    return render(request, template_name, context)

# Vue pour récupérer les messages de la conversation
@login_required
def get_conversation_messages(request, conversation_name):
    conversation = get_object_or_404(Conversation, name=conversation_name)
    # récupère le paramètre page de la requête GET. Si ce paramètre n'est pas fourni,
    # la valeur par défaut est 1. La valeur est ensuite convertie en entier.
    page = int(request.GET.get('page', 1))
    # nombre de messages à charger par page est défini à 10.
    page_size = 10
    offset = (page - 1) * page_size
    messages = conversation.messages.all().order_by('-created_at')[offset:offset+page_size]
    messages_data = [{
        'id': message.id,
        'content': message.content,
        'from_user': {'username': message.from_user.username},
        'to_user': {'username': message.to_user.username},
        'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    } for message in messages]
    return JsonResponse({'messages': messages_data})

