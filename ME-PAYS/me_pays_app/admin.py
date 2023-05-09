from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from me_pays_app.models.users import *
from django.contrib.auth.models import Group    
from django.contrib.auth.models import Permission

class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # ('Personal info', {'fields': ('first_name', 'last_name', 'contact_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    filter_horizontal = ['groups', 'user_permissions']
    search_fields = ('email',)
    ordering = ('email',)

    


class CustomGroupAdminForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Permissions', False),
        required=False,
    )

    class Meta:
        model = Group
        fields = '__all__'

# Custom GroupAdmin that uses the CustomGroupAdminForm
class CustomGroupAdmin(GroupAdmin):
    form = CustomGroupAdminForm

admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EndUser)