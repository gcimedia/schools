from django.shortcuts import render


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
