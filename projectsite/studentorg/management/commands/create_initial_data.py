"""
Management command to create initial/seeding data for development.

Usage:
    python manage.py create_initial_data --orgs 10 --students 50 --members 20

The command is idempotent where possible: colleges/programs are created only if
missing, and Student/Organization/OrgMember creations use get_or_create to avoid
duplicates.
"""

from django.core.management.base import BaseCommand
from faker import Faker
from django.db import IntegrityError, transaction
from studentorg.models import College, Program, Organization, Student, OrgMember


class Command(BaseCommand):
    help = 'Create initial data for the application. Idempotent where possible.'

    def add_arguments(self, parser):
        parser.add_argument('--orgs', type=int, default=10, help='Number of organizations to create')
        parser.add_argument('--students', type=int, default=50, help='Number of students to create')
        parser.add_argument('--members', type=int, default=10, help='Number of memberships to create')

    def handle(self, *args, **options):
        orgs = options.get('orgs')
        students = options.get('students')
        members = options.get('members')

        # Ensure there is at least one college and program to relate to
        self.ensure_seed_relations()

        self.create_organization(orgs)
        self.create_students(students)
        self.create_membership(members)

    def ensure_seed_relations(self):
        # Create a default college and program if none exist
        fake = Faker()
        if not College.objects.exists():
            College.objects.create(name='Default College')
            self.stdout.write(self.style.WARNING('Created Default College'))

        if not Program.objects.exists():
            Program.objects.create(name='General Program', college=College.objects.first())
            self.stdout.write(self.style.WARNING('Created General Program'))

    def create_organization(self, count):
        fake = Faker()
        created = 0
        for _ in range(count):
            words = [fake.word() for _ in range(2)]
            organization_name = ' '.join(words).title()
            college = College.objects.order_by('?').first()
            obj, was_created = Organization.objects.get_or_create(
                name=organization_name,
                defaults={'college': college, 'description': fake.sentence()}
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Organizations created: {created} (attempted {count})'))

    def create_students(self, count):
        fake = Faker('en_PH')
        created = 0
        for _ in range(count):
            sid = f"{fake.random_int(2020,2025)}-{fake.random_int(1,8)}-{fake.random_number(digits=4)}"
            program = Program.objects.order_by('?').first()
            defaults = {
                'lastname': fake.last_name(),
                'firstname': fake.first_name(),
                'middlename': fake.last_name(),
                'program': program
            }
            student, was_created = Student.objects.get_or_create(student_id=sid, defaults=defaults)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Students created: {created} (attempted {count})'))

    def create_membership(self, count):
        fake = Faker()
        created = 0
        students_qs = list(Student.objects.all())
        orgs_qs = list(Organization.objects.all())

        if not students_qs or not orgs_qs:
            self.stdout.write(self.style.ERROR('No students or organizations available to create memberships'))
            return

        import random

        for _ in range(count):
            student = random.choice(students_qs)
            organization = random.choice(orgs_qs)
            date_joined = fake.date_between(start_date='-2y', end_date='today')
            try:
                with transaction.atomic():
                    obj, created_flag = OrgMember.objects.get_or_create(
                        student=student,
                        organization=organization,
                        defaults={'date_joined': date_joined}
                    )
                    if created_flag:
                        created += 1
            except IntegrityError:
                # Skip duplicates or constraint failures
                continue

        self.stdout.write(self.style.SUCCESS(f'Memberships created: {created} (attempted {count})'))
