from django.contrib import admin

from embed_video.admin import AdminVideoMixin
from home.models import Content,Userprofile

# Register your models here.


class ContentAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


class UserprofileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Content,ContentAdmin)
admin.site.register(Userprofile,UserprofileAdmin)


