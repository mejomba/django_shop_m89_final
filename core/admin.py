from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin
from . import models


class CustomUserAdmin(UserAdmin):
    ordering = ('id',)
    list_display = ['email', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'profile_image')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_deleted')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

    def get_queryset(self, request):
        return self.model.objects.filter(is_deleted=False)

    def delete_queryset(self, request, queryset):
        for user in queryset:
            user.is_deleted = True
            user.save()


class AdminAddress(admin.ModelAdmin):
    fields = ('country', 'province', 'city', 'street', 'zip_code', 'pelak', 'full_address', 'user', 'is_deleted')

    def get_queryset(self, request):
        return self.model.objects.filter(is_deleted=False)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(AdminAddress, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].queryset = models.User.objects.filter(is_deleted=False)
        return form

    def delete_queryset(self, request, queryset):
        for address in queryset:
            address.is_deleted = True
            address.save()


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Address, AdminAddress)