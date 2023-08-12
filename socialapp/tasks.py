from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task
from django.template import Template


@shared_task
def sendVerificationEmail(email):
    subject = "This email is from social project to verify your account..."
    from_email = settings.EMAIL_HOST_USER
    to = [email,]
    
    html_template = render_to_string('socialapp/email_template.html', {'email':email})
    # email_text_content = strip_tags(html_template)
    actual_email = EmailMultiAlternatives(
        subject, 
        html_template,
        from_email,
        to
    )
    actual_email.attach_alternative(html_template, 'text/html')
    
    actual_email.send()
    print("email send")
    return email


