# from .tokens import account_activation_token
# from django.http import HttpResponse
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import get_user_model

# User = get_user_model()

# def register(request):
#     if request.method == 'POST':
#         # Process your HTML form data
#         # ...

#         # Assuming you have obtained the user data from the form
#         user = User.objects.create_user(username='labeep', email='jafars4@gmail.com', password='12345678')
#         user.is_active = False
#         user.save()

#         current_site = get_current_site(request)
#         mail_subject = 'Activate your account'
#         try:
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             to_email = 'jafars4ab@gmail.com'
#             email = EmailMessage(
#                 mail_subject, message, to=[to_email]
#             )
#             email.send()
#         except(TypeError):
#             print('something went wrong', TypeError)

#         # Redirect or return a response as needed
#         return HttpResponse("Please check your email to complete the registration.")

#     # Render your HTML form template for GET requests
#     return render(request, 'signup.html')


import smtplib
import ssl
from email.message import EmailMessage


from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from store.models import Customer
from .tokens import account_activation_token
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.contrib import messages


User = get_user_model()


def activate(request, uidb64, token):
    uid = None
    user = None
    try:
        # uid = str(urlsafe_base64_decode(uidb64))
        # user = User.objects.get(pk=uid)

        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        uid = int(uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = False
        user.save()
        messages.success(
            request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link.')
        return render(request, 'activation_invalid.html')


def register(request):

    if request.method == 'POST':

        # Define email sender and receiver
        email_sender = 'jafars4ab@gmail.com'
        email_password = 'txahcupztwcyjkii'
        email_receiver = 'jafars4ab@gmail.com'

        # Set the subject and body of the email
        user = User.objects.create_user(
            username='jaf007', email='jafars4@gmail.com', password='12345678')
        current_site = get_current_site(request)
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        subject = 'Verify Your Email!'
        body = """
        I've just published a new video on YouTube: https://youtu.be/2cZzP9DLlkg
        """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(message)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        return HttpResponse("Please check your email to complete the registration.")
    else:
        return render(request, 'signup.html')


def forgot_account(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(pk=1)
        print('print user ', user.username)
        if user != None:
            # Define email sender and receiver
            email_sender = 'jafars4ab@gmail.com'
            email_password = 'txahcupztwcyjkii'
            email_receiver = email

            # Set the subject and body of the email
            # user = User.objects.create_user(username='jaf007', email='jafars4@gmail.com', password='12345678')
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            subject = 'Check out my new video!'
            body = """
            I've just published a new video on YouTube: https://youtu.be/2cZzP9DLlkg
            """

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(message)

            # Add SSL (layer of security)
            context = ssl.create_default_context()

            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
            return HttpResponse("Please check your email to complete your email recovery.")

        else:
            print('This user is not found in our database')
            return
    return render(request, 'forgot_account.html')


def forgot_account_link(request, uidb64, token):
    uid = None
    user = None
    try:
        # uid = str(urlsafe_base64_decode(uidb64))
        # user = User.objects.get(pk=uid)

        email = urlsafe_base64_decode(uidb64).decode('utf-8')
        # uid = int(uid)
        # user = User.objects.get(email=email)
        user = Customer.objects.get(email=email)
    except (TypeError, ValueError, OverflowError):
        user = None

    if user and account_activation_token.check_token(user, token):
        #     user.is_active = False
        #     user.save()
        #     messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect(f'/recover_account/{uidb64}/{token}')
    else:
        messages.error(request, 'Invalid activation link.')
        return render(request, 'activation_invalid.html')


def recover_account(request, userId, token):
    # email = email
    print('get user User: ', userId)
    # uid = urlsafe_base64_decode(userId).decode('utf-8')
    # print('get user Id: ', uid)
    if request.method == 'POST':
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassowrd')
        userId = request.POST.get('userId')
        print('get user User: ', userId)
        uid = urlsafe_base64_decode(userId).decode('utf-8')
        print('get user Id: ', uid)
        if password == cpassword:
            user = User.objects.get(pk=uid)
            if user != None:
                user.password = password
                user.save()
                print('account updated successfully')
                return redirect('login')
            print('No user found')
            return
        print('password do not match')
        return
    context = {
        "userId": userId,
        "token": token
    }
    return render(request, 'recover_account.html', context)
