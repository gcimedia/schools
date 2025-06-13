import io
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from PIL import Image

from .config.urls import landing_url_config
from .decorators import (
    auth_page_required,
    auth_page_required_class,
    redirect_authenticated_users,
    redirect_authenticated_users_class,
)
from .forms import ContactUsForm, SignInForm, SignUpForm
from .models import BaseDetail, BaseImage, ContactEmail

# ============================================================================
# BASE VIEWS
# ============================================================================


class ManifestView(View):
    """
    Returns a dynamically generated web manifest file.
    Cached for performance but always up-to-date.
    """

    def dispatch(self, request, *args, **kwargs):
        # Apply caching only in production (when DEBUG is False)
        if not settings.DEBUG:  # Production
            cached_dispatch = cache_page(60 * 15)(super().dispatch)
            return cached_dispatch(request, *args, **kwargs)
        else:  # Development - no caching
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        manifest_data = self.generate_manifest_data()

        response = JsonResponse(
            manifest_data, json_dumps_params={"indent": 2, "ensure_ascii": False}
        )
        response["Content-Type"] = "application/manifest+json"
        return response

    def generate_manifest_data(self):
        """Generate manifest data from database"""
        # Get values first
        name_value = self._get_detail_value("base_name", "")
        short_name_value = self._get_detail_value("base_short_name", "")
        description = self._get_detail_value("base_description", "A Django application")
        theme_color = self._get_detail_value("base_theme_color", "#000000")

        # short_name falls back to name in both cases
        name = short_name_value or name_value or "My App"
        short_name = short_name_value or name_value or "My App"

        # Get icons
        icons = self._generate_icons()

        return {
            "name": name,
            "short_name": short_name,
            "description": description,
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": theme_color,
            "icons": icons,
            "categories": ["productivity", "utilities"],
            "orientation": "portrait-primary",
            "scope": "/",
            "lang": "en",
        }

    def _get_detail_value(self, name, default=""):
        """Get value from BaseDetail or return default"""
        try:
            detail = BaseDetail.objects.get(name=name)
            return detail.value or default
        except BaseDetail.DoesNotExist:
            return default

    def _generate_icons(self):
        """Generate icons array for manifest"""
        icons = []

        # Icon mappings: (model_name, sizes, type, purpose)
        icon_mappings = [
            ("base_favicon", "32x32", "image/png", "any"),
            ("base_apple_touch_icon", "180x180", "image/png", "any"),
            ("base_logo", "512x512", "image/png", "any"),
        ]

        for model_name, sizes, icon_type, purpose in icon_mappings:
            try:
                image_obj = BaseImage.objects.get(name=model_name)
                if image_obj.image:
                    # Get resized image URL
                    resized_url = self._get_resized_image_url(image_obj, model_name)
                    icons.append(
                        {
                            "src": resized_url,
                            "sizes": sizes,
                            "type": icon_type,
                            "purpose": purpose,
                        }
                    )
            except BaseImage.DoesNotExist:
                continue

        return icons

    def _get_resized_image_url(self, image_obj, image_type):
        """Return URL for resized image"""
        request = self.request
        resize_url = f"/core/resize-image/{image_obj.pk}/?type={image_type}"
        return request.build_absolute_uri(resize_url)


class BaseImageResizeView(View):
    """
    Dynamically resize and serve images with compression.
    Preserves transparency and original background colors.
    """

    # Size mappings for different image types (removed hero image)
    SIZE_MAPPING = {
        "base_logo": (512, 512),
        "base_favicon": (32, 32),
        "base_apple_touch_icon": (180, 180),
    }

    def get(self, request, image_id):
        try:
            image_obj = BaseImage.objects.get(pk=image_id)
            image_type = request.GET.get("type", image_obj.name)

            if not image_obj.image:
                return HttpResponse("Image not found", status=404)

            # Get target size
            target_size = self.SIZE_MAPPING.get(image_type, (512, 512))

            # Process the image
            processed_image = self._resize_and_compress_image(
                image_obj.image, target_size, image_type
            )

            # All images are PNG now (no more JPEG hero)
            content_type = "image/png"

            # Create response
            response = HttpResponse(processed_image, content_type=content_type)
            response["Cache-Control"] = "public, max-age=86400"  # Cache for 24 hours

            return response

        except BaseImage.DoesNotExist:
            return HttpResponse("Image not found", status=404)
        except Exception as e:
            return HttpResponse(f"Error processing image: {str(e)}", status=500)

    def _resize_and_compress_image(self, image_field, target_size, image_type):
        """
        Resize and compress image while preserving transparency and background colors.
        """
        # Open the image
        img = Image.open(image_field)

        # All remaining image types should preserve transparency
        preserve_transparency = True

        # Convert palette images to RGBA if they have transparency
        if img.mode == "P" and "transparency" in img.info:
            img = img.convert("RGBA")
        elif img.mode == "P":
            img = img.convert("RGB")

        # Calculate resize ratio maintaining aspect ratio
        img_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]

        if img_ratio > target_ratio:
            # Image is wider than target ratio
            new_width = target_size[0]
            new_height = int(target_size[0] / img_ratio)
        else:
            # Image is taller than target ratio
            new_height = target_size[1]
            new_width = int(target_size[1] * img_ratio)

        # Resize the image
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Center the image if it's smaller than target size
        if new_width < target_size[0] or new_height < target_size[1]:
            # Create new image with appropriate mode
            if preserve_transparency and img.mode == "RGBA":
                padded_img = Image.new("RGBA", target_size, (0, 0, 0, 0))  # Transparent
            else:
                # Use white background for non-transparent images
                padded_img = Image.new("RGB", target_size, (255, 255, 255))

            # Paste the resized image in the center
            paste_x = (target_size[0] - new_width) // 2
            paste_y = (target_size[1] - new_height) // 2

            if img.mode == "RGBA":
                padded_img.paste(img, (paste_x, paste_y), img)
            else:
                padded_img.paste(img, (paste_x, paste_y))

            img = padded_img

        # Save to BytesIO as PNG (simplified - no more JPEG logic)
        output = io.BytesIO()

        if img.mode in ("RGBA", "LA"):
            # Save as PNG to preserve transparency
            img.save(output, format="PNG", optimize=True, compress_level=6)
        else:
            # Save as PNG for all other image types
            img.save(output, format="PNG", optimize=True, compress_level=6)

        output.seek(0)
        return output.getvalue()


# ============================================================================
# CONTACT VIEWS
# ============================================================================


@csrf_exempt
@require_POST
def contact(request):
    """Handle contact form submission via AJAX"""
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)

        # Create form instance with the data
        form = ContactUsForm(data)

        if form.is_valid():
            # Extract cleaned data
            sender_name = form.cleaned_data["name"]
            sender_email = form.cleaned_data["email"]
            sender_subject = form.cleaned_data["subject"]
            sender_message = form.cleaned_data["message"]

            try:
                recipient_email = (
                    ContactEmail.objects.filter(is_primary=True).only("email")
                    if ContactEmail._meta.db_table
                    in connection.introspection.table_names()
                    else None,
                )

                email_context = {
                    "name": sender_name,
                    "email": sender_email,
                    "subject": sender_subject,
                    "message": sender_message,
                    "url": request.build_absolute_uri(
                        reverse(landing_url_config.get_landing_url_name())
                    ),
                }

                text_content = render_to_string("core/mail/contact.txt", email_context)
                html_content = render_to_string("core/mail/contact.html", email_context)

                msg = EmailMultiAlternatives(
                    sender_subject,
                    text_content,
                    sender_email,
                    [recipient_email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Thank you for your message! We will get back to you soon.",
                    }
                )

            except Exception:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "There was an error sending your message. Please try again later.",
                    },
                    status=500,
                )

        else:
            # Form is not valid, return errors
            return JsonResponse(
                {
                    "success": False,
                    "message": "Please correct the errors below.",
                    "errors": form.errors,
                },
                status=400,
            )

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Invalid JSON data."}, status=400
        )

    except Exception:
        return JsonResponse(
            {
                "success": False,
                "message": "An unexpected error occurred. Please try again.",
            },
            status=500,
        )


# ============================================================================
# USER VIEWS
# ============================================================================


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
                return redirect(landing_url_config.get_landing_url_name())
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
    return render(request, "core/index.html", extra_context)


@require_POST
def signout(request):
    """
    Log out the current user and redirect to the landing page
    with a success message.
    """
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect(landing_url_config.get_landing_url_name())


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
    template_name = "core/index.html"
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
