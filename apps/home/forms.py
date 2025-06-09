from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)

from .config.auth import auth_config
from .models import OrgDetail, OrgImage, SocialMediaLink


class UniqueChoiceFormMixin:
    """
    Mixin for forms that restricts the 'name' field choices to those not
    already used in the database, ensuring uniqueness.

    Expects `choices_attr` to be defined in subclasses, pointing to a list of allowed choices.
    """

    choices_attr = None  # Will be set dynamically in subclass

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and dynamically filters available 'name' choices
        based on which ones are not already used in the database.
        """
        super().__init__(*args, **kwargs)

        if self.instance.pk or not self.choices_attr:
            return

        model_choices = getattr(self._meta.model, self.choices_attr, [])
        existing_values = self._meta.model.objects.values_list("name", flat=True)

        available_choices = [
            choice for choice in model_choices if choice[0] not in existing_values
        ]

        self.fields["name"].choices = [(None, "")] + available_choices


def generate_model_form(model_class, choices_attr_name):
    """
    Generates a model form class using UniqueChoiceFormMixin, with dynamic filtering of choices.

    Args:
        model_class (Model): The Django model class to build the form for.
        choices_attr_name (str): The name of the class attribute containing the choice list.

    Returns:
        forms.ModelForm: A dynamically generated model form class.
    """

    class _ModelForm(UniqueChoiceFormMixin, forms.ModelForm):
        choices_attr = choices_attr_name

        class Meta:
            model = model_class
            fields = "__all__"

    return _ModelForm


# Form for OrgDetail with filtered unique name choices
OrgDetailForm = generate_model_form(OrgDetail, "CHOICES")

# Form for OrgImage with filtered unique name choices
OrgImageForm = generate_model_form(OrgImage, "CHOICES")


class SocialMediaLinkForm(UniqueChoiceFormMixin, forms.ModelForm):
    """
    Form for SocialMediaLink model, filtering out existing choices for 'name'.
    Excludes the 'icon' field from the form.
    """

    choices_attr = "SOCIAL_MEDIA_CHOICES"

    class Meta:
        model = SocialMediaLink
        fields = "__all__"
        exclude = ("icon",)


class SignInForm(AuthenticationForm):
    """
    Custom authentication form that applies dynamic labels and placeholders
    for the username field based on `auth_config`.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the login form with custom field widgets and labels.
        """
        super().__init__(*args, **kwargs)

        # Get username configuration from registry
        username_label = auth_config.get_username_label()
        username_placeholder = auth_config.get_username_placeholder()

        # Update the username field
        self.fields["username"] = UsernameField(
            label=username_label,
            widget=forms.TextInput(
                attrs={
                    "autofocus": True,
                    "class": "form-control",
                    "placeholder": username_placeholder,
                }
            ),
        )

        # Update password field
        self.fields["password"] = forms.CharField(
            label="Password",
            strip=False,
            widget=forms.PasswordInput(
                attrs={
                    "autocomplete": "current-password",
                    "class": "form-control",
                    "placeholder": "Your password",
                }
            ),
        )


class SignUpForm(UserCreationForm):
    """
    Custom user creation form that supports dynamic username labels/placeholders
    and styled input fields.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the registration form with dynamic username settings
        and customized password field widgets and help texts.
        """
        super().__init__(*args, **kwargs)

        # Get username configuration from registry
        username_label = auth_config.get_username_label()
        username_placeholder = auth_config.get_username_placeholder()

        # Update the username field
        self.fields["username"].label = username_label
        self.fields["username"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": username_placeholder,
            }
        )

        # Update password fields
        self.fields["password1"] = forms.CharField(
            strip=False,
            widget=forms.PasswordInput(
                attrs={
                    "autocomplete": "new-password",
                    "class": "form-control",
                    "placeholder": "Password",
                }
            ),
            help_text=password_validation.password_validators_help_text_html(),
        )
        self.fields["password2"] = forms.CharField(
            widget=forms.PasswordInput(
                attrs={
                    "autocomplete": "new-password",
                    "class": "form-control",
                    "placeholder": "Password confirmation",
                }
            ),
            strip=False,
            help_text="Enter the same password as before, for verification.",
        )

    class Meta:
        model = get_user_model()
        fields = ("username",)


# class AuthProfileUpdateForm(UserChangeForm):
#     current_password = forms.CharField(
#         label="Current Password",
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={
#                 "class": "form-control",
#                 "placeholder": "Current Password",
#             },
#         ),
#     )
#     new_password1 = forms.CharField(
#         label="New Password",
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={
#                 "class": "form-control",
#                 "placeholder": "New Password",
#             },
#         ),
#     )
#     new_password2 = forms.CharField(
#         label="Confirm New Password",
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={
#                 "class": "form-control",
#                 "placeholder": "New Password Confirmation",
#             },
#         ),
#     )

#     class Meta:
#         model = get_user_model()
#         fields = ("username", "image", "first_name", "last_name")
#         widgets = {
#             "username": forms.TextInput(
#                 attrs={
#                     "class": "form-control",
#                     "placeholder": "Phone number",
#                 }
#             ),
#             "first_name": forms.TextInput(
#                 attrs={
#                     "class": "form-control",
#                     "placeholder": "First name",
#                 }
#             ),
#             "last_name": forms.TextInput(
#                 attrs={
#                     "class": "form-control",
#                     "placeholder": "Last name",
#                 }
#             ),
#             "image": forms.ClearableFileInput(
#                 attrs={
#                     "class": "form-control-file",  # Adjust class as needed
#                 }
#             ),
#         }

#     def clean_current_password(self):
#         current_password = self.cleaned_data.get("current_password")
#         if not self.instance.check_password(current_password):
#             raise forms.ValidationError("Incorrect current password.")
#         return current_password

#     def clean_new_password2(self):
#         new_password1 = self.cleaned_data.get("new_password1")
#         new_password2 = self.cleaned_data.get("new_password2")
#         if new_password1 and new_password2 and new_password1 != new_password2:
#             raise forms.ValidationError("New passwords do not match.")
#         return new_password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         new_password = self.cleaned_data.get("new_password1")
#         if new_password:
#             user.set_password(new_password)
#         if commit:
#             user.save()
#         return user
