from django.shortcuts import render


def home(request):
    extra_context = {
        "page_title": "Welcome",
        "show_hero": True,
        "header_navigation": False,
    }

    return render(request, "landing/index.html", extra_context)
