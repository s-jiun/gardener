from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, userid, name, password=None):
        if not email:
            raise ValueError(('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email),
            userid=userid,
            password=password,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, userid, name, password):
        user = self.create_user(
            email=email,
            password=password,
            userid=userid,
            name=name
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class GeneralUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
    )
    userid = models.CharField(
        verbose_name='userid',
        max_length=30,
        unique=True
    )
    name = models.CharField(
        verbose_name='Name',
        max_length=30
    )
    is_seller = models.BooleanField(
        verbose_name='Is seller',
        default=False
    )
    gender = models.BooleanField(
        verbose_name='Gender',
        blank=True,
        null=True
    )

    point = models.IntegerField(
        verbose_name='Point',
        default=0,
    )
    Image = models.ImageField(
        default='base/baseimg.png', upload_to='profile/%y/%m/%d/')

    profile = models.TextField(
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['email', 'name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.userid

    # def get_full_name(self):
    #     return self.userid

    # def get_short_name(self):
    #     return self.userid

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser
