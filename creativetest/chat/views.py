from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Message

# Parollar
PASSWORDS = {
    'K': '01092007',  # K foydalanuvchi uchun parol
    'D': 'K',  # D foydalanuvchi uchun parol
}

def login_view(request):
    """Login sahifasi"""
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        
        # Parolni tekshirish
        if user in PASSWORDS and PASSWORDS[user] == password:
            request.session['user'] = user
            return redirect('chat')
        else:
            return render(request, 'login.html', {'error': 'No\'malum yoki tugallangan test!'})
    
    return render(request, 'login.html')


def chat_view(request):
    """Chat sahifasi"""
    # Session tekshirish
    if 'user' not in request.session:
        return redirect('login')
    
    user = request.session['user']
    messages = Message.objects.all()
    
    # Boshqa foydalanuvchidan kelgan xabarlarni o'qilgan deb belgilash
    Message.objects.filter(sender__in=['K', 'D']).exclude(sender=user).filter(is_read=False).update(
        is_read=True,
        read_at=timezone.now()
    )
    
    return render(request, 'chat.html', {
        'user': user,
        'messages': messages,
    })


def mark_as_read(request):
    """Xabarlarni o'qilgan deb belgilash (AJAX)"""
    if 'user' not in request.session:
        return JsonResponse({'status': 'error'}, status=401)
    
    user = request.session['user']
    
    # Boshqa foydalanuvchidan kelgan xabarlarni o'qilgan qilish
    updated = Message.objects.filter(
        sender__in=['K', 'D']
    ).exclude(sender=user).filter(is_read=False).update(
        is_read=True,
        read_at=timezone.now()
    )
    
    return JsonResponse({'status': 'ok', 'updated': updated})


def logout_view(request):
    """Chiqish - sessionni tozalash"""
    if 'user' in request.session:
        del request.session['user']
    return redirect('login')
