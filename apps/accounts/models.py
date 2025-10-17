from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser


class UserManager(BaseUserManager):
    """
        Менеджер для створення користувачів та суперкористувачів.

        Менеджер користувача, що розширює BaseUserManager для роботи
        з кастомною моделлю User, яка використовує email замість username
        як ідентифікатор.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
            Створює звичайного користувача.

            Args:
                email (str): Email адресу користувача (має бути унікальною).
                password (str, optional): Пароль користувача. Defaults to None.
                **extra_fields: Додаткові поля для моделі User.

            Returns:
                User: Створений об'єкт користувача.

            Raises:
                ValueError: Якщо email не надано.

            Example:
                >>> user = UserManager.create_user(
                ... email="user@example.com",
                ... password="secure_password"
                ... )
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
            Створює суперкористувача (адміністратора).

            Args:
                email (str): Email адреса адміністратора.
                password (str, optional): Пароль адміністратора. Defaults to None.
                **extra_fields: Додаткові поля для моделі User.

            Returns:
                User: Створений об'єкт суперкористувача.

            Example:
                >>> admin = UserManager.create_superuser(
                ... email="admin@example.com",
                ... password="admin_password"
                ... )
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
        Модель користувача системи.

        Використовує email як унікальний ідентифікатор замість username.
        Наслідує AbstractBaseUser для кастомізації аутентифікації.

        Attributes:
            email (EmailField): Унікальна email адреса
            username (CharField): Унікальне ім'я користувача
            is_staff (BooleanField): Чи є користувач співробітником
            is_superuser (BooleanField): Чи є користувач суперадміністратором
            is_active (BooleanField): Чи активний обліковий запис
            date_joined (DateTimeField): Дата реєстрації
    """
    email = models.EmailField(max_length=128, unique=True)
    username = models.CharField(max_length=128, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
