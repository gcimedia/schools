from django.shortcuts import render




def landing(request):
    """
    Render the public landing page with hero section and minimal header navigation.
    """
    extra_context = {
        "page_title": "Welcome",
        "header_navigation": False,
        "show_hero": True,
        "show_contact": True,
        "contact_map": False,
    }

    return render(request, "home/index.html", extra_context)
