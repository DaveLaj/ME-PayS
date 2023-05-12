from django.db import migrations
from django.contrib.auth.models import Group, Permission
from me_pays_app.perm import *

def add_permissions_to_group(group, permissions):
    """
    Helper function to add permissions to a group.
    """
    for permission in permissions:
        group.permissions.add(permission)


def create_groups_and_permissions(apps, schema_editor):
    """
    Creates groups and assigns permissions to them.
    """
    # Get the models
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Create groups
    enduser_group = Group.objects.create(name='enduser')
    cashier_group = Group.objects.create(name='cashier')
    pos_group = Group.objects.create(name='pos')
    admin_group = Group.objects.create(name='admin')

    enduser_group
    cashier_group
    pos_group
    admin_group

    # Get permissions
    # add_product_permission = Permission.objects.get(codename='add_product')
    # view_product_permission = Permission.objects.get(codename='view_product')
    # change_product_permission = Permission.objects.get(codename='change_product')
    # delete_product_permission = Permission.objects.get(codename='delete_product')

    # Assign permissions to groups
    # add_permissions_to_group(enduser_group, [view_product_permission])
    # add_permissions_to_group(cashier_group, [add_product_permission, view_product_permission, change_product_permission, delete_product_permission])


class Migration(migrations.Migration):

    dependencies = [
        ('me_pays_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions),
    ]
