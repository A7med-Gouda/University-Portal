import uuid

from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import College, Department, Program

class CollegeResource(resources.ModelResource):
    id = fields.Field(attribute='id', readonly=True)  # Read-only for imports

    class Meta:
        model = College
        fields = ('name', 'chairman', 'address')  # ID excluded from import
        export_order = ('id', 'name', 'chairman', 'address')  # ID included in export

    def before_import_row(self, row, **kwargs):
        """
        Called before each Excel row is imported. We insert a fresh UUID
        into the row data so that when ModelResource builds the instance,
        the `uuid` field is populated.
        """
        # generate a hex string or leave as uuid.UUID
        row['uuid'] = str(uuid.uuid4())

    def get_instance(self, instance_loader, row):
        """
        Prevent matching on UUID (since it's brand new). Always create new.
        """
        return None
class DepartmentResource(resources.ModelResource):
    id = fields.Field(attribute='id', readonly=True)

    class Meta:
        model = Department
        fields = ('name', 'head', 'college')
        export_order = ('id', 'name', 'head', 'college')
    def before_import_row(self, row, **kwargs):
        row['uuid'] = str(uuid.uuid4())
    def get_instance(self, instance_loader, row):
        return None
class ProgramResource(resources.ModelResource):
    id = fields.Field(attribute='id', readonly=True)

    class Meta:
        model = Program
        fields = ('name', 'head', 'department')
        export_order = ('id', 'name', 'head', 'department')
    def before_import_row(self, row, **kwargs):
        row['uuid'] = str(uuid.uuid4())
    def get_instance(self, instance_loader, row):
        return None
# Admin classes
@admin.register(College)
class CollegeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CollegeResource
    list_display = ('name', 'chairman_email', 'address')
    search_fields = ('name', 'chairman__email', 'chairman__name_en', 'address')
    autocomplete_fields = ['chairman']  # Enables search for chairman (CustomUser)

    def chairman_email(self, obj):
        return obj.chairman.email if obj.chairman else None
    chairman_email.short_description = 'Chairman Email'

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DepartmentResource
    list_display = ('name', 'head_email', 'college_name')
    search_fields = ('name', 'head__email', 'head__name_en', 'college__name')
    list_filter = ('college',)  # Filter departments by college
    autocomplete_fields = ['head', 'college']  # Search for head (CustomUser) and college

    def head_email(self, obj):
        return obj.head.email if obj.head else None
    head_email.short_description = 'Head Email'

    def college_name(self, obj):
        return obj.college.name if obj.college else None
    college_name.short_description = 'College Name'

class ProgramResource(resources.ModelResource):
    class Meta:
        model = Program

@admin.register(Program)
class ProgramAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProgramResource
    list_display = ('name', 'head_email', 'department_college', 'department_name')
    search_fields = (
        'name',
        'head__email',
        'head__name_en',
        'department__name',
        'department__college__name'
    )
    autocomplete_fields = ['head', 'department']
    list_filter = (
        ('department', admin.RelatedOnlyFieldListFilter),
        ('department__college', admin.RelatedOnlyFieldListFilter),
    )

    def head_email(self, obj):
        return obj.head.email if obj.head else None
    head_email.short_description = 'Program Coordinator Email'

    def department_name(self, obj):
        return obj.department.name if obj.department else None
    department_name.short_description = 'Department'

    def department_college(self, obj):
        return obj.department.college.name if obj.department and obj.department.college else None
    department_college.short_description = 'College'