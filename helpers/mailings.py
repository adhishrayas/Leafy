from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
from leafy.settings import EMAIL_HOST_USER
from Authmodules.models import CustomUser
from django.template.loader import render_to_string

@receiver(post_save,sender = CustomUser)
def send_verification_mail(sender,instance,**kwargs):
    htmly = "email.html"
    recipient = instance.email
    user = CustomUser.objects.get(email = recipient)
    html_content = render_to_string(htmly,{
        'url':f"Verification_mail/{user.id}"
    })
    mail = EmailMultiAlternatives(
        subject = "Verification mail",
        body = html_content,
        from_email=EMAIL_HOST_USER,
        bcc = [recipient],
        reply_to=[EMAIL_HOST_USER],
    )
    mail.content_subtype = "html"
    mail.send()