from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    # UserChangeForm,
    UserCreationForm,
    UsernameField,
)

from .config.auth import auth_config
from .models import OrgDetail, OrgImage, SocialMediaLink


class UniqueChoiceFormMixin:
    choices_attr = None  # Will be set dynamically in subclass

    def __init__(self, *args, **kwargs):
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
    class _ModelForm(UniqueChoiceFormMixin, forms.ModelForm):
        choices_attr = choices_attr_name

        class Meta:
            model = model_class
            fields = "__all__"

    return _ModelForm


OrgDetailForm = generate_model_form(OrgDetail, "CHOICES")
OrgImageForm = generate_model_form(OrgImage, "CHOICES")


class SocialMediaLinkForm(UniqueChoiceFormMixin, forms.ModelForm):
    choices_attr = "SOCIAL_MEDIA_CHOICES"

    class Meta:
        model = SocialMediaLink
        fields = "__all__"
        exclude = ("icon",)


class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
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

    # remember_me = forms.BooleanField(
    #     required=False,
    #     initial=True,
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             "class": "form-check-input",
    #         }
    #     ),
    #     label="Remember Me",
    # )


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
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
