import secrets
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

AI_PROVIDER_CHOICES = [
    ('gpt', 'ChatGPT'),
    ('grok', 'Grok'),
    ('deepseek', 'DeepSeek'),
    ('qwen', 'Qwen'),
    ('claude', 'Claude'),
]

SUBSCRIPTION_PLANS = [
    ('free', 'Free'),
    ('premium', 'Premium'),
]

class Room(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'Общее'),
        ('games', 'Игры'),
        ('movies', 'Фильмы'),
        ('music', 'Музыка'),
        ('social', 'Общение'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name="Room Name")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(max_length=300, blank=True, verbose_name="Description")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    is_private = models.BooleanField(default=False, verbose_name="Private Room")
    access_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Access Code")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or 'room'
            slug = base_slug
            counter = 2
            while Room.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    subscription_plan = models.CharField(max_length=20, choices=SUBSCRIPTION_PLANS, default='free')
    premium_until = models.DateTimeField(null=True, blank=True)
    api_keys = JSONField(default=dict, blank=True)
    visited_rooms = models.ManyToManyField(Room, related_name='visited_by', blank=True)

    def __str__(self):
        return f'{self.user.username} profile'

    @property
    def is_premium(self):
        from django.utils import timezone
        return self.subscription_plan == 'premium' and self.premium_until and self.premium_until >= timezone.now()

    @property
    def room_limit(self):
        return 30 if self.is_premium else 5

    @property
    def invite_limit(self):
        return None if self.is_premium else 10

    @property
    def active_plan(self):
        return 'Premium' if self.is_premium else 'Free'

class AIIntegration(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='integrations')
    provider = models.CharField(max_length=30, choices=AI_PROVIDER_CHOICES)
    api_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'provider')

    def __str__(self):
        return f'{self.provider} integration for {self.profile.user.username}'

class RoomAIIntegration(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='ai_integrations')
    provider = models.CharField(max_length=30, choices=AI_PROVIDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'provider')

    def __str__(self):
        return f'{self.provider} enabled for {self.room.name}'


class RoomInvitation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    invite_code = models.CharField(max_length=16, unique=True)
    invited_username = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = secrets.token_urlsafe(10)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Invite {self.invite_code} for {self.room.name}'

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(verbose_name="Message Content")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]} in {self.room.name}"

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
