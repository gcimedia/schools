from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView

from .config.landing import get_landing_url_name
from .decorators import (
    auth_page_required,
    auth_page_required_class,
    redirect_authenticated_users,
    redirect_authenticated_users_class,
)
from .forms import SignInForm, SignUpForm


def landing(request):
    """
    Render the public landing page with hero section and minimal header navigation.
    """
    extra_context = {
        "page_title": "Welcome",
        "show_hero": True,
        "header_navigation": False,
    }

    return render(request, "home/index.html", extra_context)


@auth_page_required("signin")
@redirect_authenticated_users
def signin(request):
    """
    Handle user sign-in.

    - Redirects authenticated users via decorator.
    - On GET, render the sign-in form.
    - On POST, authenticate the user and log them in if credentials are valid.
    - If authentication fails, show an error message.
    """

    extra_context = {
        "page_title": "Login",
        "header_auth_btn": False,
        "header_navigation": False,
        "show_auth": "signin",
    }

    next = request.GET.get("next", "")
    back = request.GET.get("back", "")
    extra_context["next"] = next
    extra_context["back"] = back

    if request.method == "POST":
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.POST.get("next", "")
                if next:
                    return redirect(next)
                return redirect(get_landing_url_name())
            else:
                messages.error(
                    request, "Invalid username or password.", extra_tags="signin"
                )
        else:
            messages.error(
                request, "Invalid username or password.", extra_tags="signin"
            )
    else:
        form = SignInForm()

    extra_context["loginform"] = form
    return render(request, "home/index.html", extra_context)


@require_POST
def signout(request):
    """
    Log out the current user and redirect to the landing page
    with a success message.
    """
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect(get_landing_url_name())


@auth_page_required_class("signup")
@redirect_authenticated_users_class
class SignUpView(CreateView):
    """
    Handle user registration.

    - Displays the signup form on GET.
    - Creates and logs in the user on valid POST.
    - Displays an error message on form error.
    - Redirects to the next page if specified or to the sign-in page otherwise.
    """

    form_class = SignUpForm
    template_name = "home/index.html"
    extra_context = {
        "page_title": "Sign up",
        "header_auth_btn": False,
        "header_navigation": False,
        "show_auth": "signup",
    }

    def get_context_data(self, **kwargs):
        """
        Add extra context including navigation flow (next/back).
        """
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        context["next"] = self.request.GET.get("next", "")
        context["back"] = self.request.GET.get("back", "")
        return context

    def form_invalid(self, form):
        """
        Display error message if form submission is invalid.
        """
        messages.error(
            self.request,
            "There was an error with your submission. Please check the form.",
            extra_tags="signup",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        """
        Create the user, log them in, and redirect based on flow.
        """
        user = form.save()
        user.backend = settings.AUTHENTICATION_BACKENDS[0]  # Optional but useful
        login(self.request, user)

        next = self.request.POST.get("next", "")
        if next:
            return redirect(next)

        return redirect("signin")


# class ProfileUpdate(LoginRequiredMixin, UpdateView):
#     """
#     View for updating user profile details and credentials.
#     Includes handling of password updates and post-submission feedback.
#     """
#     model = get_user_model()
#     form_class = ProfileUpdateForm
#     template_name = "home/index.html"
#     success_url = reverse_lazy("profile_update")

#     def get_object(self, queryset=None):
#         return self.request.user

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["authentication_active"] = "active"
#         context["profileupdate_active"] = "active"
#         context["profileupdateinterface"] = "Update your credentials here"
#         return context

#     def form_invalid(self, form):
#         messages.error(
#             self.request,
#             "There was an error with your submission. Please check the form.",
#         )
#         return super().form_invalid(form)

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         new_password = form.cleaned_data.get("new_password1")
#         if new_password:
#             user.set_password(new_password)
#         user.save()
#         messages.success(
#             self.request, "Profile updated successfully! Kindly log in again."
#         )
#         return redirect(self.success_url)

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().post(request, *args, **kwargs)
