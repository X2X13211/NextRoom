import base64
import datetime
import json
import secrets
import urllib.request
import urllib.error

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Q, Count

from .models import Room, Message, UserProfile, AIIntegration, RoomAIIntegration, RoomInvitation, AI_PROVIDER_CHOICES

AI_COMMAND_ALIASES = {provider: label for provider, label in AI_PROVIDER_CHOICES}

YOO_KASSA_API_URL = 'https://api.yookassa.ru/v3'


def get_user_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def get_ai_bot_user():
    bot_username = 'nextroom_ai'
    bot_email = 'bot@nextroom.local'
    bot_user, created = User.objects.get_or_create(username=bot_username, defaults={
        'email': bot_email,
        'password': User.objects.make_random_password(32)
    })
    return bot_user


def get_room_ai_integration_for_user(user, room, alias):
    profile = get_user_profile(user)
    integration = profile.integrations.filter(provider=alias).first()
    if integration:
        return integration

    if room.creator != user:
        room_enabled = room.ai_integrations.filter(provider=alias).first()
        if room_enabled:
            creator_profile = get_user_profile(room.creator)
            return creator_profile.integrations.filter(provider=alias).first()

    return None


def yookassa_request(method, endpoint, payload=None):
    api_key = getattr(settings, 'YOOKASSA_SECRET_KEY', None)
    if not api_key:
        raise ValueError('YOOKASSA_SECRET_KEY is not configured in settings.')

    url = f'{YOO_KASSA_API_URL}/{endpoint.lstrip("/")}'
    auth_token = base64.b64encode(f'{api_key}:'.encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_token}',
        'Content-Type': 'application/json',
        'Idempotence-Key': secrets.token_urlsafe(16),
        'Accept': 'application/json',
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode('utf-8')

    request_obj = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request_obj, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            return json.loads(error_body)
        except Exception:
            raise


def parse_ai_command(content):
    stripped = content.strip()
    if stripped.startswith('@'):
        parts = stripped.split(maxsplit=1)
        alias = parts[0][1:].lower()
        question = parts[1].strip() if len(parts) > 1 else ''
        return alias, question
    return None, None


def fetch_ai_response(alias, prompt, integration):
    if not prompt:
        return f'Пожалуйста, укажите запрос после команды @{alias}. Например: @{alias} расскажи анекдот.'

    if alias == 'gpt':
        try:
            return fetch_openai_response(prompt, integration.api_key)
        except Exception as exc:
            return f'Ошибка при обращении к ChatGPT: {str(exc)}'

    return f'Интеграция с {AI_COMMAND_ALIASES.get(alias, alias).title()} настроена, но внешнее API пока обрабатывается локально. Запрос: {prompt}'


def fetch_openai_response(prompt, api_key):
    url = 'https://api.openai.com/v1/chat/completions'
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 400,
        'temperature': 0.8,
    }
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
    if 'choices' in result and result['choices']:
        return result['choices'][0]['message']['content'].strip()
    raise ValueError('Неверный ответ от OpenAI API.')


def create_yookassa_payment(request):
    shop_id = getattr(settings, 'YOOKASSA_SHOP_ID', None)
    if not shop_id:
        raise ValueError('YOOKASSA_SHOP_ID is not configured in settings.')

    return_url = request.build_absolute_uri(reverse('subscription_confirm'))
    payment_body = {
        'amount': {
            'value': '199.00',
            'currency': 'RUB'
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': return_url
        },
        'capture': True,
        'description': 'NextRoom Premium подписка на 199 рублей в месяц',
        'metadata': {
            'user_id': request.user.id,
        }
    }
    return yookassa_request('POST', 'payments', payment_body)


def update_premium_status(profile, months=1):
    now = timezone.now()
    expiry = profile.premium_until or now
    if expiry < now:
        expiry = now
    profile.premium_until = expiry + datetime.timedelta(days=30 * months)
    profile.subscription_plan = 'premium'
    profile.save()


def landing(request):
    """Landing/Welcome page with beautiful visuals and stats."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Calculate some stats for the landing page
    active_rooms = Room.objects.filter(messages__isnull=False).distinct().count()
    online_users = User.objects.filter(last_login__gte=timezone.now() - datetime.timedelta(minutes=5), is_active=True).distinct().count()
    total_messages = Message.objects.count()
    total_rooms = Room.objects.count()
    
    # Top 3 active rooms based on message count
    featured_rooms = Room.objects.annotate(
        msg_count=Count('messages')
    ).filter(is_private=False).order_by('-msg_count')[:3]

    context = {
        'active_rooms': active_rooms,
        'online_users': online_users,
        'total_messages': total_messages,
        'total_rooms': total_rooms,
        'featured_rooms': featured_rooms,
    }
    return render(request, 'chat/landing.html', context)

def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        if not username or not password:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
        elif email and User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Пользователь с такой почтой уже существует.')
        elif password != password_confirm:
            messages.error(request, 'Пароли не совпадают.')
        elif len(password) < 6:
            messages.error(request, 'Пароль должен быть не менее 6 символов.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, f'Добро пожаловать в NextRoom, {username}!')
            return redirect('dashboard')
            
    return render(request, 'chat/register.html')

def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'С возвращением, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
            
    return render(request, 'chat/login.html')

def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, 'Вы вышли из системы. До встречи!')
    return redirect('landing')

@login_required
def dashboard(request):
    """Dashboard view listing all rooms with search, filters, and statistics."""
    profile = get_user_profile(request.user)
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()
    room_type = request.GET.get('type', 'all').strip() # all, public, private
    
    rooms = Room.objects.all().annotate(msg_count=Count('messages'))
    
    # Apply search filter
    if query:
        rooms = rooms.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(creator__username__icontains=query)
        )
        
    # Apply category filter
    if category_filter and category_filter != 'all':
        rooms = rooms.filter(category=category_filter)
        
    # Apply room type filter
    if room_type == 'public':
        rooms = rooms.filter(is_private=False)
    elif room_type == 'private':
        rooms = rooms.filter(is_private=True)
        
    # Get stats
    total_rooms = Room.objects.count()
    my_rooms_count = Room.objects.filter(creator=request.user).count()
    total_messages = Message.objects.count()
    
    categories = Room.CATEGORY_CHOICES

    context = {
        'rooms': rooms,
        'categories': categories,
        'query': query,
        'selected_category': category_filter,
        'selected_type': room_type,
        'stats': {
            'total_rooms': total_rooms,
            'my_rooms': my_rooms_count,
            'total_messages': total_messages,
        },
        'profile': profile,
        'room_limit_reached': my_rooms_count >= profile.room_limit,
        'max_rooms': profile.room_limit,
    }
    return render(request, 'chat/dashboard.html', context)

@login_required
def create_room(request):
    """Endpoint or form to create a new room."""
    if request.method == 'POST':
        profile = get_user_profile(request.user)
        current_rooms = Room.objects.filter(creator=request.user).count()
        if current_rooms >= profile.room_limit:
            messages.error(request, f'Вы достигли лимита комнат для текущей подписки ({profile.room_limit}). Обновите до Premium, чтобы создать больше комнат.')
            return redirect('dashboard')

        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category', 'general').strip()
        is_private = request.POST.get('is_private') == 'true'
        access_code = request.POST.get('access_code', '').strip() if is_private else ''
        
        if not name:
            messages.error(request, 'Имя комнаты не может быть пустым.')
            return redirect('dashboard')
            
        if Room.objects.filter(name=name).exists():
            messages.error(request, f'Комната с именем "{name}" уже существует.')
            return redirect('dashboard')
            
        if is_private and not access_code:
            messages.error(request, 'Для приватной комнаты необходимо указать код доступа.')
            return redirect('dashboard')
            
        # Create the room
        room = Room.objects.create(
            name=name,
            description=description,
            category=category,
            creator=request.user,
            is_private=is_private,
            access_code=access_code if is_private else None
        )
        
        messages.success(request, f'Комната "{name}" успешно создана!')
        return redirect('room_detail', slug=room.slug)
        
    return redirect('dashboard')

@login_required
def delete_room(request, slug):
    """Delete a room (only allowed for creator)."""
    room = get_object_or_404(Room, slug=slug)
    if room.creator != request.user:
        messages.error(request, 'У вас нет прав на удаление этой комнаты.')
        return redirect('dashboard')
        
    room_name = room.name
    room.delete()
    messages.success(request, f'Комната "{room_name}" была успешно удалена.')
    return redirect('dashboard')

@login_required
def profile(request):
    profile = get_user_profile(request.user)
    my_rooms = Room.objects.filter(creator=request.user).annotate(msg_count=Count('messages'))
    visited_rooms = profile.visited_rooms.all()
    integrations = profile.integrations.all()
    available_providers = AI_PROVIDER_CHOICES

    context = {
        'profile': profile,
        'my_rooms': my_rooms,
        'visited_rooms': visited_rooms,
        'integrations': integrations,
        'available_providers': available_providers,
    }
    return render(request, 'chat/profile.html', context)

@login_required
def add_ai_integration(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    provider = request.POST.get('provider', '').strip().lower()
    api_key = request.POST.get('api_key', '').strip()
    profile = get_user_profile(request.user)
    if not profile.is_premium:
        messages.error(request, 'Добавление API ключей доступно только для Premium-подписки.')
        return redirect('profile')
    if provider not in [choice[0] for choice in AI_PROVIDER_CHOICES] or not api_key:
        messages.error(request, 'Выберите модель и укажите корректный API ключ.')
        return redirect('profile')

    integration, created = AIIntegration.objects.update_or_create(
        profile=profile,
        provider=provider,
        defaults={'api_key': api_key}
    )
    messages.success(request, f'Интеграция @{provider} сохранена.')
    return redirect('profile')

@login_required
def create_yookassa_subscription(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')
    try:
        payment = create_yookassa_payment(request)
    except Exception as exc:
        messages.error(request, f'Не удалось создать платеж: {str(exc)}')
        return redirect('profile')

    if 'confirmation' in payment and 'confirmation_url' in payment['confirmation']:
        request.session['pending_yookassa_payment'] = payment.get('id')
        return redirect(payment['confirmation']['confirmation_url'])

    messages.error(request, 'Не удалось получить ссылку на оплату.')
    return redirect('profile')

@login_required
def confirm_subscription(request):
    payment_id = request.GET.get('paymentId') or request.GET.get('payment_id') or request.session.get('pending_yookassa_payment')
    if not payment_id:
        messages.error(request, 'Не удалось определить платеж.')
        return redirect('profile')

    try:
        payment = yookassa_request('GET', f'payments/{payment_id}')
    except Exception as exc:
        messages.error(request, f'Ошибка проверки платежа: {str(exc)}')
        return redirect('profile')

    if payment.get('status') == 'succeeded':
        profile = get_user_profile(request.user)
        update_premium_status(profile)
        messages.success(request, 'Подписка Premium успешно активирована на 30 дней!')
    else:
        messages.error(request, 'Платеж не подтвержден. Попробуйте снова.')
    return redirect('profile')

@login_required
def create_room_invite(request, slug):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    room = get_object_or_404(Room, slug=slug)
    if room.creator != request.user:
        messages.error(request, 'У вас нет прав на создание приглашения для этой комнаты.')
        return redirect('room_detail', slug=room.slug)

    profile = get_user_profile(request.user)
    invite_limit = profile.invite_limit
    invitation_count = room.invitations.count()
    if invite_limit is not None and invitation_count >= invite_limit:
        messages.error(request, f'Вы достигли лимита приглашений ({invite_limit}) для этой комнаты.')
        return redirect('room_detail', slug=room.slug)

    RoomInvitation.objects.create(room=room, invited_by=request.user)
    messages.success(request, 'Приглашение создано. Отправьте код приглашения участникам, чтобы они могли войти.')
    return redirect('room_detail', slug=room.slug)

@login_required
def manage_room_ai_integrations(request, slug):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    room = get_object_or_404(Room, slug=slug)
    if room.creator != request.user:
        messages.error(request, 'Только создатель комнаты может управлять доступными моделями.')
        return redirect('room_detail', slug=room.slug)

    profile = get_user_profile(request.user)
    available_providers = {integration.provider for integration in profile.integrations.all()}
    selected_providers = [provider for provider in request.POST.getlist('providers') if provider in available_providers]

    RoomAIIntegration.objects.filter(room=room).exclude(provider__in=selected_providers).delete()
    for provider in selected_providers:
        RoomAIIntegration.objects.get_or_create(room=room, provider=provider)

    messages.success(request, 'Список доступных моделей для комнаты обновлен.')
    return redirect('room_detail', slug=room.slug)


@login_required
def room_detail(request, slug):
    """Display the chat room. Verifies access code for private rooms."""
    room = get_object_or_404(Room, slug=slug)
    
    # Handle private room access code verification
    session_key = f'room_auth_{room.id}'
    is_authorized = session_key in request.session or room.creator == request.user or not room.is_private
    
    if room.is_private and not is_authorized:
        if request.method == 'POST':
            entered_code = request.POST.get('access_code', '').strip()
            if entered_code == room.access_code or RoomInvitation.objects.filter(room=room, invite_code=entered_code).exists():
                request.session[session_key] = True
                messages.success(request, 'Доступ разрешен!')
                return redirect('room_detail', slug=room.slug)
            else:
                messages.error(request, 'Неверный код доступа.')
        
        return render(request, 'chat/room_unlock.html', {'room': room})
        
    # Mark the room as visited for the current user
    if request.user != room.creator:
        profile = get_user_profile(request.user)
        profile.visited_rooms.add(room)

    # Retrieve last 100 messages
    chat_messages = room.messages.all().select_related('user')[:100]
    
    # Get active/recent participants in this room
    recent_members = User.objects.filter(
        messages__room=room
    ).distinct()[:10]
    
    room_invites = room.invitations.order_by('-created_at')[:10]
    profile = get_user_profile(request.user)
    can_create_invites = (profile.invite_limit is None or room.invitations.count() < profile.invite_limit) and request.user == room.creator
    enabled_room_providers = list(room.ai_integrations.values_list('provider', flat=True))
    available_room_providers = []
    if request.user == room.creator:
        available_room_providers = [integration.provider for integration in profile.integrations.all()]

    context = {
        'room': room,
        'chat_messages': chat_messages,
        'recent_members': recent_members,
        'room_invites': room_invites,
        'can_create_invites': can_create_invites,
        'invite_limit': profile.invite_limit,
        'ai_aliases': AI_COMMAND_ALIASES,
        'enabled_room_providers': enabled_room_providers,
        'available_room_providers': available_room_providers,
    }
    return render(request, 'chat/room_detail.html', context)

@login_required
def get_messages(request, slug):
    """JSON API endpoint to poll messages for real-time update."""
    room = get_object_or_404(Room, slug=slug)
    
    # Verify access to private room
    session_key = f'room_auth_{room.id}'
    is_authorized = session_key in request.session or room.creator == request.user or not room.is_private
    if not is_authorized:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    after_id = request.GET.get('after_id')
    
    # Query messages
    queryset = room.messages.all().select_related('user')
    if after_id:
        queryset = queryset.filter(id__gt=int(after_id))
        
    messages_data = []
    for msg in queryset:
        messages_data.append({
            'id': msg.id,
            'username': msg.user.username,
            'is_me': msg.user == request.user,
            'content': msg.content,
            'timestamp': msg.created_at.strftime('%H:%M'),
        })
        
    return JsonResponse({'messages': messages_data})

@login_required
def send_message(request, slug):
    """JSON API endpoint to send a message."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    room = get_object_or_404(Room, slug=slug)
    
    # Verify access to private room
    session_key = f'room_auth_{room.id}'
    is_authorized = session_key in request.session or room.creator == request.user or not room.is_private
    if not is_authorized:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    try:
        data = json.loads(request.body)
        content = data.get('content', '').strip()
    except json.JSONDecodeError:
        content = request.POST.get('content', '').strip()
        
    if not content:
        return JsonResponse({'error': 'Message content cannot be empty'}, status=400)

    alias, prompt = parse_ai_command(content)
    if alias in AI_COMMAND_ALIASES:
        integration = get_room_ai_integration_for_user(request.user, room, alias)
        if not integration:
            return JsonResponse({'error': f'Для использования @{alias} добавьте ключ API в личном кабинете или включите модель для комнаты.'}, status=400)

        user_message = Message.objects.create(room=room, user=request.user, content=content)
        bot_user = get_ai_bot_user()
        bot_content = fetch_ai_response(alias, prompt, integration)
        bot_message = Message.objects.create(room=room, user=bot_user, content=bot_content)

        return JsonResponse({
            'status': 'success',
            'message': {
                'id': user_message.id,
                'username': user_message.user.username,
                'is_me': True,
                'content': user_message.content,
                'timestamp': user_message.created_at.strftime('%H:%M'),
            },
            'bot_message': {
                'id': bot_message.id,
                'username': bot_message.user.username,
                'is_me': False,
                'content': bot_message.content,
                'timestamp': bot_message.created_at.strftime('%H:%M'),
            }
        })

    message = Message.objects.create(
        room=room,
        user=request.user,
        content=content
    )
    
    return JsonResponse({
        'status': 'success',
        'message': {
            'id': message.id,
            'username': message.user.username,
            'is_me': True,
            'content': message.content,
            'timestamp': message.created_at.strftime('%H:%M'),
        }
    })
