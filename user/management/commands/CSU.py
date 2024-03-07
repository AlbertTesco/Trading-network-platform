from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    """
    Creates a superuser.

    Prompts the user to enter their email address, password, and password confirmation.
    If the passwords do not match, an error is displayed.
    If the superuser is created successfully, a success message is displayed.
    """

    def handle(self, *args, **options):
        email = input('Enter your email address: ')
        password = input('Enter your password: ')
        password2 = input('Confirm your password: ')

        if password != password2:
            self.stdout.write(self.style.ERROR('Passwords do not match.'))
            return

        user = User.objects.create_superuser(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )

        self.stdout.write(self.style.SUCCESS(f'Superuser {user.email} created successfully.'))
