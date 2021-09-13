from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.base import Model
from django.db.models.deletion import CASCADE


class UserManager(BaseUserManager):
    def create_user(self, userid, email, name, password=None):
        if not email:
            raise ValueError(('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email),
            userid=userid,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userid, email, name, password):
        user = self.create_user(
            email=email,
            password=password,
            userid=userid,
            name=name
        )

        user.is_admin = True
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
        default='../static/images/default_profile.svg', upload_to='profile/%y/%m/%d/')

    profile = models.TextField(
        blank=True
    )

    # django usermodel의 필수 필드
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.userid

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_admin


class Follow(models.Model):
    user = models.ForeignKey(
        GeneralUser, on_delete=CASCADE, related_name='following')
    following_user = models.ForeignKey(
        GeneralUser, related_name='followers', on_delete=CASCADE)


class MyPlant(models.Model):
    user = models.ForeignKey(
        GeneralUser, on_delete=CASCADE, related_name='user'
    )

    plant_name = models.CharField(
        verbose_name='PlantName',
        max_length=100
    )

    Image = models.ImageField(
        blank=True, null=True, upload_to='plants/%y/%m/%d/')
