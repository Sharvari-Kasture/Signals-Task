from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def send_post_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New Post Created'
        message = f'Your post "{instance.title}" has been created successfully.'
        recipient_email = instance.author.email
        send_mail(subject, message, 'your_email@example.com', [recipient_email])