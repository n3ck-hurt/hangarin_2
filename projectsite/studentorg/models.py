from django.db import models


class College(models.Model):
	name = models.CharField(max_length=200, unique=True)

	def __str__(self):
		return self.name


class Program(models.Model):
	name = models.CharField(max_length=200)
	college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='programs')

	def __str__(self):
		return self.name


class Organization(models.Model):
	name = models.CharField(max_length=200)
	college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name


class Student(models.Model):
	student_id = models.CharField(max_length=32, unique=True)
	lastname = models.CharField(max_length=100)
	firstname = models.CharField(max_length=100)
	middlename = models.CharField(max_length=100, blank=True)
	program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return f"{self.student_id} - {self.lastname}, {self.firstname}"


class OrgMember(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
	date_joined = models.DateField()

	class Meta:
		unique_together = (('student', 'organization'),)

	def __str__(self):
		return f"{self.student} -> {self.organization}"
