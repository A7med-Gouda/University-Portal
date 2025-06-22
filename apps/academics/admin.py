import uuid
from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import College, Department, Program

class CollegeResource(resources.ModelResource):
    id = fields.Field(attribute='id', readonly=True)

    class Meta:
        model = College
        fields = ('name', 'chairman', 'address')
        export_order = ('id', 'name', 'chairman', 'address')

    def before_import_row(self, row, **kwargs):
        """Generate UUID for new records during import."""
        if not row.get('id'):
            row['id'] = str(uuid.uuid4())

class DepartmentResource(resources.ModelResource):
    id = fields.Field(attribute='id', readonly=True)
    college = fields.Field(attribute='college', column_name='college')

    class Meta:
        model = Department
        fields = ('name', 'head', 'college')
        export_order = ('id', 'name', 'head', 'college')

    def before_import_row(self, row, **kwargs):
        if not row.get('id'):
            row['id'] = str(uuid.uuid4())

class ProgramResource(resources.ModelResource):
    id = fields.Field(attribute='id', readonly=True)
    department = fields.Field(attribute='department', column_name='department')

    class Meta:
        model = Program
        fields = ('name', 'head', 'department')
        export_order = ('id', 'name', 'head', 'department')

    def before_import_row(self, row, **kwargs):
        if not row.get('id'):
            row['id'] = str(uuid.uuid4())

# Admin classes
@admin.register(College)
class CollegeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CollegeResource
    list_display = ('name', 'chairman_email', 'address')
    search_fields = ('name', 'chairman__email', 'chairman__name_en', 'address')
    autocomplete_fields = ['chairman']

    def chairman_email(self, obj):
        return obj.chairman.email if obj.chairman else None
    chairman_email.short_description = 'Chairman Email'

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DepartmentResource
    list_display = ('name', 'head_email', 'college_name')
    search_fields = ('name', 'head__email', 'head__name_en', 'college__name')
    list_filter = ('college',)
    autocomplete_fields = ['head', 'college']

    def head_email(self, obj):
        return obj.head.email if obj.head else None
    head_email.short_description = 'Head Email'

    def college_name(self, obj):
        return obj.college.name if obj.college else None
    college_name.short_description = 'College Name'

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