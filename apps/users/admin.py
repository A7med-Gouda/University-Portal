from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django import forms
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export.formats.base_formats import CSV

from .models import CustomUser, Staff, Student
from apps.academics.models import College, Department

# ============ SECTION 2: EXCEL IMPORT UTILITIES ============

class UTF8BOMCSV(CSV):
    def get_title(self):
        return "csv (UTF-8 with BOM)"

    def export_data(self, dataset, **kwargs):
        data = super().export_data(dataset, **kwargs)
        return '\ufeff' + data

class CustomUserWidget(ForeignKeyWidget):
    """
    Auto-creates or updates a CustomUser based on national_id.
    Ensures password is set to national_id and normalizes numbers.
    """
    def __init__(self, model, field):
        super().__init__(model, field)

    def clean(self, value, row=None, *args, **kwargs):
        # Normalize national_id to avoid scientific notation
        if not value:
            return None
        try:
            nat = str(int(float(value)))
        except Exception:
            nat = str(value).strip().replace(',', '').replace(' ', '')

        # Lookup or create user
        user = CustomUser.objects.filter(national_id=nat).first()
        if not user:
            user = CustomUser(
                national_id=nat,
                name_ar=row.get('name_ar'),
                name_en=row.get('name_en'),
                email=row.get('email'),
                college=College.objects.filter(name=row.get('college')).first(),
                user_type=row.get('user_type') or ('staff' if 'disbursement_id' in row else 'student'),
                is_active=True,
            )
            user.set_password(nat)
            user.save()
        else:
            # Ensure password is usable
            if not user.has_usable_password():
                user.set_password(nat)
                user.save()
            # Update missing fields
            updated = False
            for attr in ('name_ar', 'name_en', 'email', 'user_type'):
                val = row.get(attr)
                if val and not getattr(user, attr):
                    setattr(user, attr, val)
                    updated = True
            if not user.college and row.get('college'):
                user.college = College.objects.filter(name=row.get('college')).first()
                updated = True
            if updated:
                user.save()
        return user

class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        exclude = ('password',)

class StaffResource(resources.ModelResource):
    user = fields.Field(
        column_name='national_id',
        attribute='user',
        widget=CustomUserWidget(CustomUser, 'national_id')
    )
    department = fields.Field(
        column_name='department',
        attribute='department',
        widget=ForeignKeyWidget(Department, 'name')
    )

    class Meta:
        model = Staff
        import_id_fields = ('disbursement_id',)
        fields = (
            'disbursement_id', 'basic_salary', 'appointment_type', 'status',
            'department', 'grade', 'job_title', 'payment_status',
            'primary_appointment_group', 'user'
        )

    def before_import_row(self, row, **kwargs):
        # Clean up national_id formatting before import
        nat = row.get('national_id')
        if isinstance(nat, float):
            row['national_id'] = str(int(nat))
        elif nat:
            row['national_id'] = str(nat).strip().replace(',', '').replace(' ', '')

class StudentResource(resources.ModelResource):
    user = fields.Field(
        column_name='national_id',
        attribute='user',
        widget=CustomUserWidget(CustomUser, 'national_id')
    )

    class Meta:
        model = Student
        import_id_fields = ('student_number',)
        fields = ('student_number', 'user')

    def before_import_row(self, row, **kwargs):
        # Clean up national_id formatting before import
        nat = row.get('national_id')
        if isinstance(nat, float):
            row['national_id'] = str(int(nat))
        elif nat:
            row['national_id'] = str(nat).strip().replace(',', '').replace(' ', '')

class UTF8BOMFormatMixin:
    """Mixin to apply BOM CSV export format."""
    def get_export_formats(self):
        formats = super().get_export_formats()
        for i, f in enumerate(formats):
            if isinstance(f, CSV):
                formats[i] = UTF8BOMCSV()
        return formats


# ============ SECTION 1: ADMIN INTERFACES ============
@admin.register(CustomUser)
class CustomUserAdmin(UTF8BOMFormatMixin, ImportExportModelAdmin, UserAdmin):
    resource_class = CustomUserResource
    list_display = ('national_id', 'email', 'name_en', 'name_ar', 'user_type', 'is_verified', 'is_active')
    search_fields = ('national_id', 'email', 'name_en', 'name_ar', 'username')
    ordering = ('national_id',)
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('user_type', 'national_id', 'college', 'profile_picture', 'date_of_birth', 'phone_number', 'is_verified')}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('user_type', 'national_id', 'college', 'profile_picture', 'date_of_birth', 'phone_number', 'is_verified')}),)


class StaffForm(forms.ModelForm):
    national_id = forms.CharField(required=True)
    user_type = forms.ChoiceField(required=True)
    email = forms.EmailField(required=True)
    name_ar = forms.CharField(required=False)
    name_en = forms.CharField(required=False)

    class Meta:
        model = Staff
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        national_id = cleaned_data.get('national_id')
        email = cleaned_data.get('email')

        if not national_id or not email:
            raise forms.ValidationError("National ID and Email are required to create the user.")

        return cleaned_data

    def save(self, commit=True):
        # Get or create CustomUser
        national_id = self.cleaned_data.get('national_id')
        email = self.cleaned_data.get('email')

        user, created = CustomUser.objects.get_or_create(
            national_id=national_id,
            defaults={
                'email': email,
                'name_ar': self.cleaned_data.get('name_ar'),
                'name_en': self.cleaned_data.get('name_en'),
                'user_type': self.cleaned_data.get('user_type'),
                'is_active': True
            }
        )

        if created:
            user.set_password(national_id)
            user.save()

        self.instance.user = user
        return super().save(commit)
@admin.register(Staff)
class StaffAdmin(UTF8BOMFormatMixin, ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = StaffResource
    form = StaffForm
    list_display = ('user', 'disbursement_id', 'appointment_type', 'status', 'department')
    search_fields = ('user__national_id', 'disbursement_id', 'user__name_en')

    # List all fields from Staff model including 'user'
    fieldsets = (
        (None, {
            'fields': (
                'user', 'disbursement_id', 'basic_salary', 'appointment_type', 'status', 'department', 'grade',
                'job_title', 'payment_status', 'primary_appointment_group', 'date_joined', 'facebook',
                'x', 'instagram', 'bio', 'qualifications', 'tasks', 'researches', 'cv', 'key_user',
                'google_schoolar', 'linkedin', 'related_sectors'
            )
        }),
        ('User Info', {
            'fields': ('national_id', 'email', 'name_ar', 'name_en', 'user_type')  # CustomUser fields
        }),
    )

    # Optionally, you can define choices for the user_type field in the form if it's a choice field
    def get_form(self, request, obj=None, **kwargs):
        # First get the standard form from ImportExportModelAdmin/ModelAdmin
        FormClass = super().get_form(request, obj, **kwargs)

        # If you want to define choices for user_type
        FormClass.base_fields['user_type'].choices = [
            ('staff', 'Staff'),
            ('employee', 'Employee'),
        ]

        # If editing, ensure that `national_id`, `name_ar`, and other fields are available
        if obj:
            FormClass.base_fields['national_id'].initial = obj.user.national_id
            FormClass.base_fields['email'].initial = obj.user.email
            FormClass.base_fields['name_ar'].initial = obj.user.name_ar
            FormClass.base_fields['name_en'].initial = obj.user.name_en
            FormClass.base_fields['user_type'].initial = obj.user.user_type

        return FormClass

    def save_model(self, request, obj, form, change):
        # Access cleaned_data from the form to get the new values
        if not obj.user:
            nat_id = form.cleaned_data.get('national_id')  # Use cleaned_data to get form fields
            user, created = CustomUser.objects.get_or_create(
                national_id=nat_id,
                defaults={
                    'email': form.cleaned_data.get('email'),
                    'name_ar': form.cleaned_data.get('name_ar'),
                    'name_en': form.cleaned_data.get('name_en'),
                    'user_type': form.cleaned_data.get('user_type'),
                    'is_active': True
                }
            )
            if created:
                user.set_password(nat_id)
                user.save()
            obj.user = user
        else:
            # If the user already exists, update the user model with new values from the form
            user = obj.user
            user.email = form.cleaned_data.get('email')
            user.name_ar = form.cleaned_data.get('name_ar')
            user.name_en = form.cleaned_data.get('name_en')
            user.user_type = form.cleaned_data.get('user_type')

            # Save the updated user model
            user.save()

        # Ensure user_type is set to 'staff' if it's empty
        if not obj.user.user_type:
            obj.user.user_type = 'staff'
            obj.user.save()

        # Save the staff object itself
        super().save_model(request, obj, form, change)

@admin.register(Student)
class StudentAdmin(UTF8BOMFormatMixin, ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = StudentResource
    form = StaffForm
    list_display = ('user', 'student_number')
    search_fields = ('user__national_id', 'student_number')

    fieldsets = (
        (None, {
            'fields': ('user','student_number', 'job_title', 'date_joined', 'facebook', 'x', 'instagram', 'bio',
                       'qualifications', 'tasks', 'researches', 'cv', 'key_user', 'google_schoolar', 'linkedin')
        }),
        ('User Info', {
            'fields': ('national_id', 'email', 'name_ar', 'name_en', 'user_type')  # CustomUser fields
        }),
        )

    def get_form(self, request, obj=None, **kwargs):
        # First get the standard form from ImportExportModelAdmin/ModelAdmin
        FormClass = super().get_form(request, obj, **kwargs)

        # If editing, ensure that `national_id`, `name_ar`, and other fields are available
        if obj and obj.user:
            FormClass.base_fields['national_id'].initial = obj.user.national_id
            FormClass.base_fields['email'].initial = obj.user.email
            FormClass.base_fields['name_ar'].initial = obj.user.name_ar
            FormClass.base_fields['name_en'].initial = obj.user.name_en
        # If you want to define choices for user_type
        FormClass.base_fields['user_type'].choices = [
            ('student', 'Student'),
        ]
        return FormClass

    def save_model(self, request, obj, form, change):
        # Access cleaned_data from the form to get the new values
        if not obj.user:
            nat_id = form.cleaned_data.get('national_id')
            user, created = CustomUser.objects.get_or_create(
                national_id=nat_id,
                defaults={
                    'username': nat_id,
                    'name_ar': form.cleaned_data.get('name_ar'),
                    'name_en': form.cleaned_data.get('name_en'),
                    'user_type': 'student',
                    'email': form.cleaned_data.get('email'),
                    'is_active': True
                }
            )
            if created:
                user.set_password(nat_id)  # Use student number as the default password
                user.save()
            obj.user = user
        else:
            # If the user already exists, update the user model with new values from the form
            user = obj.user
            user.email = form.cleaned_data.get('email')
            user.name_ar = form.cleaned_data.get('name_ar')
            user.name_en = form.cleaned_data.get('name_en')
            user.user_type = 'student'

            # Save the updated user model
            user.save()

        # Save the student object itself
        super().save_model(request, obj, form, change)