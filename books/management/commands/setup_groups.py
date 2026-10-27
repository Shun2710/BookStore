
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = "Create user groups and assign book permissions"

    def handle(self, *args, **options):
        managers, _ = Group.objects.get_or_create(name="Managers")
        Group.objects.get_or_create(name="Customers")

        content_type = ContentType.objects.get_for_model(Book)
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                "add_book",
                "change_book",
                "delete_book",
                "view_book",
            ],
        )

        managers.permissions.add(*permissions)

        self.stdout.write(
            self.style.SUCCESS("Groups and permissions configured successfully")
        )
