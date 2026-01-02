from django.contrib import admin
from django.contrib.auth.models import User
from .models import Turf


@admin.register(Turf)
class TurfAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'owner',
        'location',
        'area_sqft',
        'is_active',
        'created_at',
    )

    list_filter = ('is_active', 'location')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-created_at',)

    # 🔒 IMPORTANT: show only OWNER users in owner dropdown
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "owner":
            kwargs["queryset"] = User.objects.filter(profile__role="OWNER")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
