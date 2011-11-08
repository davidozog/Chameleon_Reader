from django.core.mail import send_mail

send_mail('Subject here', 'Here is the message.', 'from@example.com',
    ['gozo311@gmail.com'], fail_silently=False)
