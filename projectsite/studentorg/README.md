Usage
-----

This app includes a management command `create_initial_data` to seed development data.

Run it from the project root (use virtualenv python if needed):

    python projectsite\manage.py create_initial_data --orgs 10 --students 50 --members 20

Options:
  --orgs     Number of organizations to create (default: 10)
  --students Number of students to create (default: 50)
  --members  Number of memberships to create (default: 10)

Notes:
- The command will create a default College and Program if none exist.
- Student and Organization creation uses get_or_create to avoid duplicates.
- Membership creation will skip duplicates if the student is already a member of the organization.
