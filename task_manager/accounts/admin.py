from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import CustomUser, UserAddress, UserPayment

# admin.site.register(CustomUser)
# admin.site.register(UserAddress)
admin.site.register(UserPayment)

class UserAddressInline(admin.StackedInline):
    model = UserAddress
    extra = 1
    fields = ('city', 'street', 'postal_code')

class UserPaymentInLine(admin.TabularInline):
    model = UserPayment
    extra = 0
    fields = ('amount', 'payment_date', 'payment_method')
    readonly_fields = ('payment_date',)


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'postal_code')
    list_filter = ('city', 'street')
    search_fields = ('user__email', 'city', 'street')

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserAddressInline, UserPaymentInLine]
    list_display = ('email', 'phone_number', 'is_active')
    list_filter = ('is_active', 'preferred_language')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
