from django.shortcuts import render


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def privacy(request):
    """ A view to return the privacy policy """

    return render(request, 'home/privacy_policy.html')
