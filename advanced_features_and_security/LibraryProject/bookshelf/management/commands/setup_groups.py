"""
Management command to set up user groups with permissions.

This command creates three groups (Viewers, Editors, Admins) and assigns
appropriate permissions to each group based on the Book model's custom permissions.

Usage:
    python manage.py setup_groups
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Creates user groups (Viewers, Editors, Admins) and assigns permissions'

    def handle(self, *args, **options):
        # Get the ContentType for the Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        # Get all Book permissions
        can_view = Permission.objects.get(
            codename='can_view',
            content_type=content_type
        )
        can_create = Permission.objects.get(
            codename='can_create',
            content_type=content_type
        )
        can_edit = Permission.objects.get(
            codename='can_edit',
            content_type=content_type
        )
        can_delete = Permission.objects.get(
            codename='can_delete',
            content_type=content_type
        )
        
        # Create or get Viewers group (can only view)
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        viewers_group.permissions.clear()
        viewers_group.permissions.add(can_view)
        if created:
            self.stdout.write(self.style.SUCCESS('Created Viewers group'))
        else:
            self.stdout.write(self.style.SUCCESS('Updated Viewers group'))
        
        # Create or get Editors group (can view, create, and edit)
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editors_group.permissions.clear()
        editors_group.permissions.add(can_view, can_create, can_edit)
        if created:
            self.stdout.write(self.style.SUCCESS('Created Editors group'))
        else:
            self.stdout.write(self.style.SUCCESS('Updated Editors group'))
        
        # Create or get Admins group (all permissions)
        admins_group, created = Group.objects.get_or_create(name='Admins')
        admins_group.permissions.clear()
        admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admins group'))
        else:
            self.stdout.write(self.style.SUCCESS('Updated Admins group'))
        
        self.stdout.write(self.style.SUCCESS('\nGroups setup completed successfully!'))
        self.stdout.write(self.style.SUCCESS('\nGroup Permissions:'))
        self.stdout.write('  - Viewers: can_view')
        self.stdout.write('  - Editors: can_view, can_create, can_edit')
        self.stdout.write('  - Admins: can_view, can_create, can_edit, can_delete')

