from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Message

# Parollar
PASSWORDS = {
    'K': 'K',
    'D': 'D',
}

def login_view(request):
    """Login sahifasi"""
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        
        if user in PASSWORDS and PASSWORDS[user] == password:
            request.session['user'] = user
            return redirect('chat')
        else:
            return render(request, 'login.html', {'error': 'Noto\'g\'ri parol!'})
    
    return render(request, 'login.html')


def chat_view(request):
    """Chat sahifasi"""
    if 'user' not in request.session:
        return redirect('login')
    
    user = request.session['user']
    messages = Message.objects.all()
    
    # O'qilgan deb belgilash
    Message.objects.filter(sender__in=['K', 'D']).exclude(sender=user).filter(is_read=False).update(
        is_read=True,
        read_at=timezone.now()
    )
    
    return render(request, 'chat.html', {
        'user': user,
        'messages': messages,
    })


def get_new_messages(request):
    """Polling API - Yangi xabarlarni olish"""
    if 'user' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    user = request.session['user']
    last_id = int(request.GET.get('last_id', 0))
    
    # Yangi xabarlar
    messages = Message.objects.filter(id__gt=last_id).order_by('timestamp')[:50]
    
    # O'qilgan deb belgilash
    Message.objects.filter(
        sender__in=['K', 'D']
    ).exclude(sender=user).filter(is_read=False).update(
        is_read=True,
        read_at=timezone.now()
    )
    
    # O'qilgan statusni qaytarish
    my_messages = Message.objects.filter(sender=user, id__gt=last_id)
    read_updates = {}
    for msg in my_messages:
        read_updates[msg.id] = msg.is_read
    
    data = {
        'messages': [
            {
                'id': msg.id,
                'sender': msg.sender,
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%H:%M'),
                'is_read': msg.is_read,
            }
            for msg in messages
        ],
        'read_updates': read_updates,
    }
    
    return JsonResponse(data)


@csrf_exempt
def send_message(request):
    """Xabar yuborish API"""
    if 'user' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.session['user']
            content = data.get('message', '').strip()
            
            if not content:
                return JsonResponse({'error': 'Empty message'}, status=400)
            
            # Xabarni saqlash
            message = Message.objects.create(
                sender=user,
                content=content
            )
            
            return JsonResponse({
                'success': True,
                'message': {
                    'id': message.id,
                    'sender': message.sender,
                    'content': message.content,
                    'timestamp': message.timestamp.strftime('%H:%M'),
                    'is_read': message.is_read,
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)


def logout_view(request):
    """Chiqish"""
    if 'user' in request.session:
        del request.session['user']
    return redirect('login')
