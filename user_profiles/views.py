from django.shortcuts import render


def user_profile(request):
    """ """
    template = 'profiles/profile.html'
    context = {

    }

    return render(request, template, context)
