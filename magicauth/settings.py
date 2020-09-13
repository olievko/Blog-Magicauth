from django.conf import settings as django_settings
#################
# Email settings
#################
EMAIL_SUBJECT = getattr(django_settings, "MAGICAUTH_EMAIL_SUBJECT", "Lien de connexion")
EMAIL_HTML_TEMPLATE = getattr(django_settings, "MAGICAUTH_EMAIL_HTML_TEMPLATE", "magicauth/email.html")
EMAIL_TEXT_TEMPLATE = getattr(django_settings, "MAGICAUTH_EMAIL_TEXT_TEMPLATE", "magicauth/email.txt")
FROM_EMAIL = getattr(django_settings, "MAGICAUTH_FROM_EMAIL")

###########################
# View templates and urls
###########################
# Login view :

LOGIN_URL = getattr(django_settings, "MAGICAUTH_LOGIN_URL", "login/")

# Template for the login view if you want to customise it. It has to contain a form, with a field
# with type="email" and name="email".
LOGIN_VIEW_TEMPLATE = getattr(django_settings, "MAGICAUTH_LOGIN_VIEW_TEMPLATE", "magicauth/login.html")

# Name of the field in your User model that contains the email
EMAIL_FIELD = getattr(django_settings, "MAGICAUTH_EMAIL_FIELD", "username")

# Email sent view :
# shown when the user has entered their email successfully and the email has been sent.
EMAIL_SENT_VIEW_TEMPLATE = getattr(
    django_settings, "MAGICAUTH_EMAIL_SENT_VIEW_TEMPLATE", "magicauth/email_sent.html"
)
EMAIL_SENT_URL = getattr(django_settings, "MAGICAUTH_EMAIL_SENT_URL", "email-envoyé/")

# Wait view :
# The emailed links point to this url. It shows a wait message, makes the user wait for
# WAIT_SECONDS, and then redirects them to the VALIDATE_TOKEN_URL (see below).
# Why do we have this view? Because some mail clients visit links their find in email, to check them for spam,
# phishing, etc. So that when the user clicks the link in the email, the antispam bot has already "clicked" it first.
# Adding this intermediary view avoids having the antispam bot invalidate the token and block the user login : the bot
# visits the view but does not wait long enough, so the login is not triggered.
WAIT_VIEW_TEMPLATE = getattr(
    django_settings, "MAGICAUTH_WAIT_VIEW_TEMPLATE", "magicauth/wait.html"
)
# The view will look for the token in the "key" variable.
WAIT_URL = getattr(django_settings, "MAGICAUTH_WAIT_URL", "chargement/code/<str:key>/")

# Validate token view :
# validates the token in the url, does the login, and redirects to LOGGED_IN_REDIRECT_URL_NAME.
VALIDATE_TOKEN_URL = getattr(django_settings, "MAGICAUTH_VALIDATE_TOKEN_URL", "code/<str:key>/")

# Logged in redirect view :
# view on which the user lands once logged in.
LOGGED_IN_REDIRECT_URL_NAME = getattr(django_settings, "MAGICAUTH_LOGGED_IN_REDIRECT_URL_NAME")

# Logout view :
LOGOUT_URL_NAME = getattr(django_settings, "MAGICAUTH_LOGOUT_URL_NAME", "logout")

#################
# Other settings
#################

# When using an expired token, user will be prompted to get a new one.
TOKEN_DURATION_SECONDS = getattr(django_settings, "MAGICAUTH_TOKEN_DURATION_SECONDS", 5 * 60)

# The default just raises an error whose message gets displayed on the login page.
EMAIL_UNKNOWN_CALLBACK = getattr(
    django_settings, "MAGICAUTH_EMAIL_UNKNOWN_CALLBACK", "magicauth.utils.raise_error"
)

# this message will be displayed when an unknown email is entered.
EMAIL_UNKNOWN_MESSAGE = getattr(django_settings, "MAGICAUTH_EMAIL_UNKNOWN_MESSAGE", "No user found.")

# How long the user will wait on the WAIT_URL page before doing the actual login.
WAIT_SECONDS = getattr(django_settings, "MAGICAUTH_WAIT_SECONDS", 3)