from django.contrib import admin
from .models import College, Program, Organization, Student, OrgMember


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	ordering = ('name',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
	list_display = ('name', 'college')
	search_fields = ('name', 'college__name')
	list_filter = ('college',)
	ordering = ('college__name', 'name')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
	list_display = ('name', 'college')
	search_fields = ('name', 'college__name')
	list_filter = ('college',)
	ordering = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ('student_id', 'lastname', 'firstname', 'program')
	search_fields = ('student_id', 'lastname', 'firstname')
	list_filter = ('program',)
	ordering = ('lastname', 'firstname')


@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
	list_display = ('student', 'organization', 'date_joined')
	search_fields = ('student__student_id', 'student__lastname', 'organization__name')
	list_filter = ('organization', 'date_joined')
	date_hierarchy = 'date_joined'
	ordering = ('-date_joined',)
