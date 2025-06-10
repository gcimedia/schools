class AuthConfig:
    def __init__(self):
        self._enabled_pages = {
            "signin": True,
            "signup": True,
            "profile_update": True,
            "password_reset": False,
            "email_verification": False,
            "logout": True,
        }
        self._page_configs = {}
        # Global auth configuration
        self._global_config = {
            "username_field_label": "Username",
            "username_field_placeholder": "Enter your username",
        }
        # Role registry for project-specific roles
        self._roles = []
        self._role_staff_status = {}  # Track which roles should be staff
        self._default_role = None

    def enable_page(self, page_name, **config):
        """Enable an auth page with optional configuration."""
        if page_name in self._enabled_pages:
            self._enabled_pages[page_name] = True
            if config:
                self._page_configs[page_name] = config
        else:
            raise ValueError(f"Unknown auth page: {page_name}")

    def disable_page(self, page_name):
        """Disable an auth page."""
        if page_name in self._enabled_pages:
            self._enabled_pages[page_name] = False
            self._page_configs.pop(page_name, None)
        else:
            raise ValueError(f"Unknown auth page: {page_name}")

    def is_enabled(self, page_name):
        """Check if an auth page is enabled."""
        return self._enabled_pages.get(page_name, False)

    def get_enabled_pages(self):
        """Get list of all enabled auth pages."""
        return [page for page, enabled in self._enabled_pages.items() if enabled]

    def get_page_config(self, page_name):
        """Get configuration for a specific page."""
        return self._page_configs.get(page_name, {})

    def configure_page(self, page_name, **config):
        """Configure an auth page without changing its enabled status."""
        if page_name in self._enabled_pages:
            self._page_configs[page_name] = config
        else:
            raise ValueError(f"Unknown auth page: {page_name}")

    def get_all_pages_status(self):
        """Get status of all auth pages."""
        return {
            page: {"enabled": enabled, "config": self._page_configs.get(page, {})}
            for page, enabled in self._enabled_pages.items()
        }

    def bulk_configure(self, pages_config):
        """Configure multiple pages at once."""
        for page_name, config in pages_config.items():
            if page_name not in self._enabled_pages:
                raise ValueError(f"Unknown auth page: {page_name}")

            if "enabled" in config:
                self._enabled_pages[page_name] = config["enabled"]
                config = {k: v for k, v in config.items() if k != "enabled"}

            if config:
                self._page_configs[page_name] = config

    def configure_username_field(self, label=None, placeholder=None):
        """Configure the username field globally."""
        if label is not None:
            self._global_config["username_field_label"] = label
        if placeholder is not None:
            self._global_config["username_field_placeholder"] = placeholder

    def get_username_config(self):
        """Get username field configuration."""
        return self._global_config.copy()

    def get_username_label(self):
        """Get the configured username field label."""
        return self._global_config["username_field_label"]

    def get_username_placeholder(self):
        """Get the configured username field placeholder."""
        return self._global_config["username_field_placeholder"]

    def set_global_config(self, **config):
        """Set global configuration options."""
        self._global_config.update(config)

    def get_global_config(self, key=None):
        """Get global configuration."""
        if key:
            return self._global_config.get(key)
        return self._global_config.copy()

    # ================== ROLE MANAGEMENT METHODS ==================

    def register_roles(self, roles, default_role=None):
        """Register roles for this project.

        Args:
            roles (list): List of role names, tuples (name, display_name),
                         or dicts with role configuration
            default_role (str): Default role to assign to new users
        """
        self._roles = []
        for role in roles:
            if isinstance(role, dict):
                # Full role configuration: {"name": "admin", "display_name": "Administrator", "is_staff": True}
                role_name = role["name"]
                display_name = role.get("display_name", role_name.title())
                is_staff = role.get("is_staff", False)

                self._roles.append({"name": role_name, "display_name": display_name})
                self._role_staff_status[role_name] = is_staff

            elif isinstance(role, tuple):
                role_name, display_name = role
                self._roles.append({"name": role_name, "display_name": display_name})
                # Default to False for staff status if not specified
                self._role_staff_status[role_name] = False
            else:
                # Just role name as string
                self._roles.append({"name": role, "display_name": role.title()})
                self._role_staff_status[role] = False

        if default_role:
            if not self.is_valid_role(default_role):
                raise ValueError(
                    f"Default role '{default_role}' not in registered roles"
                )
            self._default_role = default_role

    def add_role(self, role_name, display_name=None, is_staff=False):
        """Add a single role to the registry."""
        if self.is_valid_role(role_name):
            raise ValueError(f"Role '{role_name}' already exists")

        self._roles.append(
            {"name": role_name, "display_name": display_name or role_name.title()}
        )

        self._role_staff_status[role_name] = is_staff

    def remove_role(self, role_name):
        """Remove a role from the registry."""
        self._roles = [r for r in self._roles if r["name"] != role_name]
        self._role_staff_status.pop(role_name, None)
        if self._default_role == role_name:
            self._default_role = None

    def get_roles(self):
        """Get all registered roles."""
        return [role["name"] for role in self._roles]

    def get_roles_display(self):
        """Get roles with display names for forms/UI."""
        return [(role["name"], role["display_name"]) for role in self._roles]

    def is_valid_role(self, role_name):
        """Check if a role is registered."""
        return role_name in self.get_roles()

    def get_default_role(self):
        """Get the default role for new users."""
        return self._default_role

    def set_default_role(self, role_name):
        """Set the default role for new users."""
        if not self.is_valid_role(role_name):
            raise ValueError(f"Role '{role_name}' not registered")
        self._default_role = role_name

    def set_role_staff_status(self, role_name, is_staff):
        """Set whether a role should have staff status."""
        if not self.is_valid_role(role_name):
            raise ValueError(f"Role '{role_name}' not registered")
        self._role_staff_status[role_name] = is_staff

    def get_role_staff_status(self, role_name):
        """Get whether a role should have staff status."""
        return self._role_staff_status.get(role_name, False)

    def get_staff_roles(self):
        """Get all roles that should have staff status."""
        return [role for role, is_staff in self._role_staff_status.items() if is_staff]

    def create_groups_if_needed(self):
        """Create Django groups for all registered roles (call this in apps.py)."""
        from django.contrib.auth.models import Group

        created_groups = []
        for role in self._roles:
            group, created = Group.objects.get_or_create(name=role["name"])
            if created:
                created_groups.append(role["name"])

        return created_groups

    def update_user_staff_status(self, user):
        """Update a user's staff status based on their role."""
        try:
            user_role = user.get_role()
            if user_role and user_role != "No role assigned":
                should_be_staff = self.get_role_staff_status(user_role)
                if user.is_staff != should_be_staff:
                    user.is_staff = should_be_staff
                    user.save(update_fields=["is_staff"])
                    return True
        except Exception:
            pass
        return False

    def bulk_update_staff_status(self):
        """Update staff status for all users based on their roles."""
        from django.contrib.auth import get_user_model

        User = get_user_model()
        updated_count = 0

        try:
            for user in User.objects.all():
                if self.update_user_staff_status(user):
                    updated_count += 1
        except Exception:
            pass

        return updated_count

    def get_role_info(self):
        """Get complete role information."""
        return {
            "roles": self._roles,
            "default_role": self._default_role,
            "staff_status": self._role_staff_status,
        }


# Global config instance
auth_config = AuthConfig()

if __name__ == "__main__":
    print("=== AuthConfig with Role Management Examples ===\n")

    # ================== ROLE REGISTRATION EXAMPLES ==================
    print("1. ROLE REGISTRATION EXAMPLES")
    print("-" * 40)

    # Example 1: Register roles with simple names
    auth_config.register_roles(
        ["student", "instructor", "admin"], default_role="student"
    )
    print("Simple roles registered:", auth_config.get_roles())
    print("Default role:", auth_config.get_default_role())

    # Example 2: Register roles with display names
    auth_config.register_roles(
        [
            ("student", "Student"),
            ("instructor", "Course Instructor"),
            ("admin", "System Administrator"),
            ("principal", "School Principal"),
        ],
        default_role="student",
    )

    print("\nRoles with display names:")
    for role_name, display_name in auth_config.get_roles_display():
        print(f"  - {role_name}: {display_name}")

    # Example 3: Add individual roles
    auth_config.add_role("librarian", "School Librarian")
    auth_config.add_role("counselor", "School Counselor")

    print(f"\nAll roles after additions: {auth_config.get_roles()}")

    # ================== STAFF STATUS EXAMPLES ==================
    print("\n2. STAFF STATUS EXAMPLES")
    print("-" * 40)

    # Set staff status for different roles
    auth_config.set_role_staff_status("admin", True)
    auth_config.set_role_staff_status("principal", True)
    auth_config.set_role_staff_status("instructor", False)
    auth_config.set_role_staff_status("student", False)

    print("Role staff status:")
    for role in auth_config.get_roles():
        is_staff = auth_config.get_role_staff_status(role)
        print(f"  {role}: {'Staff' if is_staff else 'Non-staff'}")

    print(f"\nStaff roles: {auth_config.get_staff_roles()}")

    # ================== PAGE CONFIGURATION EXAMPLES ==================
    print("\n3. PAGE CONFIGURATION EXAMPLES")
    print("-" * 40)

    # Configure pages with role-specific settings
    auth_config.configure_page(
        "signin",
        redirect_url="/dashboard",
        remember_me=True,
        allowed_roles=["student", "instructor", "admin"],
    )

    auth_config.configure_page(
        "signup",
        require_email_verification=True,
        default_role="student",
        allowed_roles=["student"],  # Only students can self-register
    )

    auth_config.configure_page(
        "profile_update",
        fields=["email", "first_name", "last_name"],
        role_specific_fields={
            "instructor": ["email", "first_name", "last_name", "bio", "office_hours"],
            "student": ["email", "first_name", "last_name", "student_id"],
            "admin": ["email", "first_name", "last_name", "phone", "department"],
        },
    )

    print("Page configurations:")
    for page in auth_config.get_enabled_pages():
        config = auth_config.get_page_config(page)
        print(f"  {page}: {config}")

    # ================== BULK CONFIGURATION EXAMPLES ==================
    print("\n4. BULK CONFIGURATION EXAMPLES")
    print("-" * 40)

    # Bulk configure for different project types

    # School Management System Configuration
    school_config = {
        "signin": {
            "redirect_url": "/school-dashboard",
            "require_role_verification": True,
            "allowed_roles": ["student", "instructor", "admin", "principal"],
        },
        "signup": {
            "enabled": False  # Disable public signup for schools
        },
        "profile_update": {
            "role_based_access": True,
            "instructor_fields": ["bio", "qualifications", "subjects"],
            "student_fields": ["grade", "section", "parent_contact"],
        },
        "password_reset": {"enabled": True, "require_admin_approval": True},
    }

    auth_config.bulk_configure(school_config)

    print("Bulk configuration applied for school system")

    # ================== GLOBAL CONFIGURATION EXAMPLES ==================
    print("\n5. GLOBAL CONFIGURATION EXAMPLES")
    print("-" * 40)

    # Different username field configurations for different systems

    # School system
    auth_config.configure_username_field(
        label="Student/Staff ID", placeholder="Enter your School ID"
    )

    auth_config.set_global_config(
        username_field_label="Student/Staff ID",
        username_field_placeholder="Enter your School ID",
        password_min_length=8,
        require_uppercase=True,
        require_numbers=True,
        session_timeout=7200,  # 2 hours
        role_based_redirects={
            "student": "/student-dashboard",
            "instructor": "/teacher-dashboard",
            "admin": "/admin-dashboard",
            "principal": "/principal-dashboard",
        },
    )

    print("Global config for school system:")
    for key, value in auth_config.get_global_config().items():
        print(f"  {key}: {value}")

    # ================== ROLE VALIDATION EXAMPLES ==================
    print("\n6. ROLE VALIDATION EXAMPLES")
    print("-" * 40)

    # Check role validity
    test_roles = ["student", "teacher", "invalid_role", "admin"]
    for role in test_roles:
        is_valid = auth_config.is_valid_role(role)
        print(f"  {role}: {'✓ Valid' if is_valid else '✗ Invalid'}")

    # ================== COMPLETE ROLE INFO EXAMPLES ==================
    print("\n7. COMPLETE ROLE INFORMATION")
    print("-" * 40)

    role_info = auth_config.get_role_info()
    print("Complete role information:")
    print(f"  Registered roles: {len(role_info['roles'])}")
    print(f"  Default role: {role_info['default_role']}")
    print(f"  Staff roles: {len([r for r in role_info['staff_status'].values() if r])}")

    print("\nDetailed role info:")
    for role in role_info["roles"]:
        is_staff = role_info["staff_status"].get(role["name"], False)
        print(
            f"  - {role['name']} ({role['display_name']}): {'Staff' if is_staff else 'Non-staff'}"
        )

    # ================== PROJECT-SPECIFIC EXAMPLES ==================
    print("\n8. PROJECT-SPECIFIC CONFIGURATION EXAMPLES")
    print("-" * 50)

    print("Example 1: E-Learning Platform")
    print("- Roles: student, instructor, content_creator, admin")
    print("- Default role: student")
    print("- Features: Public signup, email verification, role-based dashboards")

    print("\nExample 2: Hospital Management")
    print("- Roles: patient, nurse, doctor, admin, receptionist")
    print("- Default role: patient")
    print("- Features: 2FA for staff, medical record access control")

    print("\nExample 3: Corporate System")
    print("- Roles: employee, manager, hr, admin, executive")
    print("- Default role: employee")
    print("- Features: Department-based access, hierarchy permissions")

    # ================== USAGE IN DJANGO APPS ==================
    print("\n9. USAGE IN DJANGO APPS.PY")
    print("-" * 40)

    example_apps_py = """
# In your apps/schools/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class SchoolsConfig(AppConfig):
    name = "apps.schools"
    
    def ready(self):
        from apps.home.config.auth import auth_config
        
        # Register school-specific roles
        auth_config.register_roles([
            ('student', 'Student'),
            ('teacher', 'Teacher'),
            ('admin', 'School Administrator'),
            ('principal', 'Principal')
        ], default_role='student')
        
        # Set staff status for roles
        auth_config.set_role_staff_status('admin', True)
        auth_config.set_role_staff_status('principal', True)
        
        # Configure auth pages
        auth_config.disable_page('signup')  # No public signup
        auth_config.configure_username_field(
            label='School ID',
            placeholder='Enter your School ID'
        )
        
        # Create groups after migrations
        post_migrate.connect(create_school_groups, sender=self)

def create_school_groups(sender, **kwargs):
    from apps.home.config.auth import auth_config
    auth_config.create_groups_if_needed()
    """

    print("Example apps.py configuration:")
    print(example_apps_py)

    print("\n=== End of Examples ===")
