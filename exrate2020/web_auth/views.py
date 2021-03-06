from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from authentication.models import User
from validate_email import validate_email
import json
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError, smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import account_activation_token
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
import logging
from django.contrib.auth.signals import user_logged_in
from rolepermissions.roles import assign_role
from django.conf import settings
from django.utils import translation

logger = logging.getLogger("error_logger")


# Create your views here.

@receiver(user_logged_in)  # Decorator of receiving signal while user going to logged in
def on_login(sender, user, request, **kwargs):
    logger.error("after user login")
    request.session["fav_color"] = "blue"


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        parent_introcode = request.POST['introcode']

        if not parent_introcode:
            parent_introcode = settings.parent_introcode

        context = {
            'fieldValues': request.POST
        }

        logger.error("register new user: " + str(username))
        logger.error(context)

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                logger.error("read to register  ")
                user = User.objects.create_user(username=username,
                                                email=email,
                                                parent_introcode=parent_introcode,
                                                password=password)
                # user.set_password(password)
                # user.is_active = False
                # user.save()

                assign_role(user, "member")

                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('web_activate', kwargs={
                    'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://' + current_site.domain + link

                email = EmailMessage(
                    email_subject,
                    'Hi ' + user.username + ', Please the link below to activate your account \n' + activate_url,
                    'crs@nichiei.services',
                    [email],
                )
                # email.send(fail_silently=False)
                EmailThread(email).start()
                messages.success(request, 'Account successfully created')
                return redirect("web_login")

                return render(request, 'authentication/register.html')

            messages.error(request, "Email already exists!")
            return render(request, 'authentication/register.html')

        messages.error(request, "User already exists!")
        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('web_login' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('web_login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('web_login')

        except Exception as ex:
            pass

        return redirect('web_login')


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        try:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return redirect('web_login' + '?message=' + 'Not a valid reset password link')

            context_ = {
                "username": user.username,
                "app": "Lionhu"
            }
            return render(request, "authentication/set-newpasword.html", context_)

        except DjangoUnicodeDecodeError as identifier:
            pass

        messages.error(request, "userid:" + str(id))
        return redirect("web_login")

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]

        if not User.objects.filter(email=email).exists():
            messages.error(request, "no such user exist!")
            return render(request, "authentication/reset-password.html")

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        messages.success(request, "Password has been reset as your wish.")
        return redirect("web_login")


class PasswordResetView(View):

    def get(self, request):
        return render(request, "authentication/reset-password.html")

    def post(self, request):
        email = request.POST["email"]

        if not User.objects.filter(email=email).exists():
            messages.error(request, "no such user exist!")
            return render(request, "authentication/reset-password.html")

        user = User.objects.get(email=email)
        current_site = get_current_site(request)
        email_body = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(smart_bytes(user.id)),
            'token': PasswordResetTokenGenerator().make_token(user),
        }

        link = reverse('web_password-reset-confirm', kwargs={
            'uidb64': email_body['uid'], 'token': email_body['token']})

        email_subject = 'Reset your email'

        resetpassword_url = 'http://' + current_site.domain + link

        email = EmailMessage(
            email_subject,
            'Hi ' + user.username + ', Please the link below to reset your password \n' + resetpassword_url,
            'crs@nichiei.services',
            [email],
        )
        # email.send(fail_silently=False)
        EmailThread(email).start()
        messages.success(request, "Password Reset Notification mail has been sent to " + str(user.email))
        return render(request, "authentication/reset-password.html")


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        redirect_url = request.POST.get("redirect", "top")
        logger.error("login form POST:".format(request.POST))
        logger.error("login form username:".format(username))
        logger.error("login form password:".format(password))
        logger.error("login form redirect_url:".format(redirect_url))

        if username and password:
            logger.error("login username:".format(username))
            user = auth.authenticate(username=username, password=password)
            logger.error(user)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username + ' you are now logged in')

                    return redirect(redirect_url)
                    # return render(request, 'index.html', {"accessToken": "Bearer " + user.tokens()["access"]})
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('web_login')


@login_required(login_url="/webauth/login/")
def set_user_language(request, language="ja"):
    logger.error("set current language: "+language)
    logger.error("return path: "+request.META.get('HTTP_REFERER', '/'))
    if any(language in sub for sub in settings.LANGUAGES) :
        logger.error("language in settings.LANGUAGES")
        user = request.user
        user.language = language
        user.save()

        translation.activate(language)
        request.session[translation.LANGUAGE_SESSION_KEY] = language

    return redirect(request.META.get('HTTP_REFERER', '/'))
