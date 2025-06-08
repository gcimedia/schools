from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView

from .decorators import auth_page_required, auth_page_required_class
from .forms import SignInForm, SignUpForm
from .registry.home import get_home_url_name


class HomeRedirectView(RedirectView):
    permanent = False  # Use 302 redirect by default

    def get_redirect_url(self, *args, **kwargs):
        """Get the registered home URL or fall back to root."""
        try:
            from .registry.home import get_home_url

            return get_home_url()
        except Exception:
            # Fallback to root if home registry fails
            return "/"


class PermanentHomeRedirectView(HomeRedirectView):
    """
    Permanent (301) version of HomeRedirectView.
    """

    permanent = True


@auth_page_required("signin")
def signin(request):
    if request.user.is_authenticated:
        return redirect(get_home_url_name())

    extra_context = {
        "page_title": "Login",
        "header_auth_btn": False,
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
                return redirect(get_home_url_name())
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
    return render(request, "base/index.html", extra_context)


@require_POST
def signout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect(get_home_url_name())


@auth_page_required_class("signup")
class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "base/index.html"
    extra_context = {
        "page_title": "Sign up",
        "header_auth_btn": False,
        "show_auth": "signup",
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("base:signin")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        context["next"] = self.request.GET.get("next", "")
        context["back"] = self.request.GET.get("back", "")
        return context

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error with your submission. Please check the form.",
            extra_tags="signup",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.save()
        user.backend = settings.AUTHENTICATION_BACKENDS[0]  # Optional
        login(self.request, user)

        next = self.request.POST.get("next", "")
        if next:
            return redirect(next)

        return redirect("base:signin")


# class ProfileUpdate(LoginRequiredMixin, UpdateView):
#     model = get_user_model()
#     form_class = ProfileUpdateForm
#     template_name = "base/index.html"  # Create this template
#     success_url = reverse_lazy("profile_update")  # Redirect back to the same page

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
#         user.save()  # Save the form with the uploaded image
#         messages.success(
#             self.request, "Profile updated successfully! Kindly log in again."
#         )
#         return redirect(self.success_url)

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().post(request, *args, **kwargs)
