from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Create a user with the given email, password and extra fields.
        """

        extra_fields.update(is_staff=False, is_superuser=False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a superuser with the given email, password and extra fields.
        """

        extra_fields.update(is_staff=True, is_superuser=True)
        return self._create_user(email, password, **extra_fields)
