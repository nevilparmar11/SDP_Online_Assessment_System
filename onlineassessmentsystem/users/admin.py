from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

# To store password from Admin Panel in HashedForm instead of storing directly
class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('isStudent' ,'profilePicture')}),
    )

admin.site.register(User, MyUserAdmin)