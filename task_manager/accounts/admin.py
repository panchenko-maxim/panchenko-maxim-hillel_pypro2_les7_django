from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils import timezone
from accounts.models import CustomUser, UserAddress, UserPayment

# admin.site.register(CustomUser)
# admin.site.register(UserAddress)
admin.site.register(UserPayment)

class DateInput(forms.DateInput):
    input_type = 'data'

class UserAddressInline(admin.StackedInline):
    model = UserAddress
    extra = 1
    fields = ('city', 'street', 'postal_code')

class UserPaymentInLine(admin.TabularInline):
    model = UserPayment
    extra = 0
    fields = ('amount', 'payment_date', 'payment_method')
    readonly_fields = ('payment_date',)

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'date_of_birth')
        widgets = {'date_of_birth': DateInput()}

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and (password1 != password2):
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Current password', help_text='Encrypting version of password')
    new_password1 = forms.CharField(
        label='New_password',
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank if you don't want to change your password"
    )
    new_password2 = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError('Passwords do not match')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password1 = self.cleaned_data.get("new_password1")
        if new_password1:
            user.set_password(new_password1)
        if commit:
            user.save()
        return user


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'postal_code')
    list_filter = ('city', 'street')
    search_fields = ('user__email', 'city', 'street')

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    inlines = [UserAddressInline, UserPaymentInLine]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'full_name', 'phone_number', 'is_active', 'payment_total')
    list_filter = ('is_active', 'preferred_language')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    actions = ['activate_users', 'deactivate_users']

    fieldsets = (
        (None, {'fields': ('email', 'is_active',)}),
        ('Edit password', {'fields': ('new_password1', 'new_password2',), 'classes': ('collapse',)}),
        ('Roots', {'fields': ('is_staff', 'is_superuser'), 'classes': ('collapse',)}),
        ('Personal data', {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_of_picture'),
                           'classes': ('wide',)}),


    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2', 'first_name', 'last_name', 'date_of_birth',)
        }),
    )

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full name'

    def payment_total(self, obj):
        total = sum(payment.amount for payment in obj.payments.all())
        return f'{total} grn'
    payment_total.short_description = 'Total sum payments'

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Deactivate {updated} users')
    deactivate_users.short_description = "Deactivate select users"

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Activate {updated} users')
    activate_users.short_description = "Activate select users"

    class Media:
        js = ('admin/js/admin_custom.js')

