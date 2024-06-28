from django.contrib import admin

from .models import Group, GroupMaterial, UserGroup

admin.site.register(Group)
admin.site.register(GroupMaterial)
admin.site.register(UserGroup)