# base_app/migrations/0002_populate_initial_data.py (or similar filename)

from django.db import migrations
from datetime import date

def create_initial_data(apps, schema_editor):
    # Get the models by name from the apps registry
    Project = apps.get_model('base_app', 'Project')
    Task = apps.get_model('base_app', 'Task')
    User = apps.get_model('auth', 'User')

    # --- USER SETUP (ADJUST THESE IDS IF NECESSARY) ---
    try:
        manager_user = User.objects.get(pk=1) # User ID 1 for Manager
        assignee_user = User.objects.get(pk=7) # User ID 2 for Assignee
    except User.DoesNotExist:
        # Fallback if users 1 and 2 don't exist
        print("Warning: User IDs 1 and 2 not found. Skipping data population.")
        return


    # =========================================================
    # 1. CREATE PROJECTS
    # =========================================================

    p1 = Project.objects.create(
        name="Rift Valley Folktales Collection",
        description="A 6-month initiative to collect, digitize, and translate 50 oral folktales from Kalenjin, Maasai, and Turkana communities.",
        client="Ministry of Culture, Kenya",
        start_date=date(2025, 10, 1),
        due_date=date(2026, 3, 31),
        budget=2500000.00,
        status='I', # In Progress
        manager=manager_user,
    )

    p2 = Project.objects.create(
        name="Kenya Digital Nomad Guide (2025)",
        description="Comprehensive online guide covering visa application, co-working spaces in Nairobi/Mombasa, and local business registration (KEPCO).",
        client="Self-Funded (Internal IP)",
        start_date=date(2025, 11, 1),
        due_date=date(2026, 1, 30),
        budget=450000.00,
        status='P', # Planning
        manager=assignee_user,
    )


    # =========================================================
    # 2. CREATE TASKS
    # =========================================================

    # Project 1 Tasks
    Task.objects.create(
        project=p1,
        title="Audio-to-Text Transcription of Interviews",
        description="Transcribe the first 10 recorded oral history interviews from the Maasai community. Ensure speaker identification is clear.",
        assigned_to=assignee_user,
        priority='H',
        due_date=date(2025, 11, 5),
        status='TD', # To Do
        estimated_time=50
    )
    
    Task.objects.create(
        project=p1,
        title="Reconcile Q4 Field Trip Expenses",
        description="Compile all receipts and mileage logs for the initial field trip phase (Oct-Dec) and log them against the project budget in the financial tracking sheet.",
        assigned_to=manager_user,
        priority='M',
        due_date=date(2026, 1, 5),
        status='TD', # To Do
        estimated_time=8
    )

    Task.objects.create(
        project=p1,
        title="Secure Field Interview Permits",
        description="Contact local chiefs and county officials in Baringo and Kajiado to obtain necessary permissions for field recordings.",
        assigned_to=assignee_user,
        priority='H',
        due_date=date(2025, 10, 15),
        status='IP', # In Progress
        estimated_time=15
    )
    
    Task.objects.create(
        project=p1,
        title="Final Review of Swahili Translations",
        description="Proofread and quality check all 25 Swahili translated stories before passing to the English team.",
        assigned_to=manager_user,
        priority='M',
        due_date=date(2025, 12, 1),
        status='TD', # To Do
        estimated_time=20
    )

    # Project 2 Tasks
    Task.objects.create(
        project=p2,
        title="Research New Kenya Startup Visa Rules",
        description="Document all legal requirements, fees, and processing times for the new Digital Nomad/Startup Visa.",
        assigned_to=assignee_user,
        priority='C', # Critical
        due_date=date(2025, 11, 15),
        status='DO', # Done
        estimated_time=10
    )
    
    Task.objects.create(
        project=p2,
        title="Schedule & Execute Nairobi Co-Working Photoshoot",
        description="Arrange access and take high-quality, licensed photos of three major Nairobi co-working spaces (iHub, Nairobi Garage).",
        assigned_to=manager_user,
        priority='L',
        due_date=date(2025, 12, 30),
        status='TD', # To Do
        estimated_time=40
    )
    
    Task.objects.create(
        project=p2,
        title="Finalize Landing Page Wireframe",
        description="Design the high-fidelity wireframe and style guide for the main Digital Nomad Guide landing page before passing it to the frontend developer.",
        assigned_to=manager_user,
        priority='H',
        due_date=date(2025, 11, 25),
        status='IP', # In Progress
        estimated_time=25
    )
    
    Task.objects.create(
        project=p2,
        title="Curate Top 5 Mombasa Co-Working Spaces",
        description="Research and verify contact information, pricing, and amenities for the top five co-working spaces in the Mombasa/Nyali area.",
        assigned_to=assignee_user,
        priority='M',
        due_date=date(2025, 12, 15),
        status='TD', # To Do
        estimated_time=6
    )


class Migration(migrations.Migration):

    dependencies = [
        # This dependency must be the previous migration file in your base_app
        # Example: ('base_app', '0001_initial'), 
        # You MUST include the migration that created the Project and Task models
        ('base_app', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]