from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.models import Site
from .models import Post, Subscription
from django.db.models.signals import post_save


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    # Только для новых постов
    if not created:
        return

    category = instance.category
    # Получаем всех подписчиков этой категории
    subscribers = Subscription.objects.filter(category=category).select_related('user')
    # Собираем email (только те, у кого он есть)
    recipient_emails = [sub.user.email for sub in subscribers if sub.user.email]

    if not recipient_emails:
        return

    # Формируем абсолютную ссылку на пост
    # Используем Site framework для получения домена
    current_site = Site.objects.get_current()
    relative_url = instance.get_absolute_url()
    full_url = f"http://{current_site.domain}{relative_url}"

    # Отправляем письмо
    send_mail(
        subject=f'Новый пост в категории "{category}"',
        message=(
            f'Здравствуйте!\n\n'
            f'В категории "{category}" появился новый пост:\n'
            f'"{instance.heading}"\n\n'
            f'Читать: {full_url}'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_emails,
        fail_silently=True,  # чтобы не ломать создание поста при ошибке отправки
    )