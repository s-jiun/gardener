from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


from django.utils.translation import gettext_lazy as _
from allauth.account.utils import user_email, user_field, user_username
from allauth.utils import (
    valid_email_or_none,
)

class customSocialAccountAdapter(DefaultSocialAccountAdapter):
        def populate_user(self, request, sociallogin, data):
            print(data)
            username = data.get("username")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            email = data.get("email")
            name = data.get("name")
            print('username:',username)
            print('name', name)
            user = sociallogin.user
            user_username(user, username or "")
            if first_name != None:
                user_field(user, 'name', last_name + first_name)
            else:
                user_field(user,'name', username)
            user_email(user, valid_email_or_none(email) or "")
            name_parts = (name or "").partition(" ")
            user_field(user, "first_name", first_name or name_parts[0])
            user_field(user, "last_name", last_name or name_parts[2])
            return user
