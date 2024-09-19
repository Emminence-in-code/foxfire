from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model


UserModel = get_user_model()


def send_password_token(reciever_name, token, email):

    context = {"receiver_name": reciever_name, "token": token}



    convert_to_html_content = render_to_string(
        template_name="forgot_password.html", context=context
    )
    plain_message = strip_tags(convert_to_html_content)

    x = send_mail(
        subject="Password Verification Code",
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],  # recipient_list is self explainatory
        html_message=convert_to_html_content,
        fail_silently=False,  # Optional
    )
    print(x, email)


# def mail_admin(url):

#     template_name = "admin_email.html"
#     convert_to_html_content = render_to_string(
#         template_name=template_name, context={"url": url}
#     )
#     plain_message = strip_tags(convert_to_html_content)
#     super_user = UserModel.objects.filter(is_superuser=True).first()
#     x = send_mail(
#         subject="A User just Uploaded an app",
#         message=plain_message,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[
#             # settings.EMAIL_HOST_USER,
#             super_user.email
#         ],  # recipient_list is self explainatory
#         html_message=convert_to_html_content,
#         fail_silently=False,  # Optional
#     )


# def confirm_app_uploaded_mail(url, user: CustomUser):

#     template_name = "upload_email.html"
#     convert_to_html_content = render_to_string(
#         template_name=template_name, context={"name": user.username}
#     )
#     plain_message = strip_tags(convert_to_html_content)
#     x = send_mail(
#         subject="Your app Was uploaded Succesfully",
#         message=plain_message,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[
#             # settings.EMAIL_HOST_USER,
#             user.email
#         ],  # recipient_list is self explainatory
#         html_message=convert_to_html_content,
#         fail_silently=False,  # Optional
#     )
