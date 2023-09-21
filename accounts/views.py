from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
import datetime
from django.contrib.auth.models import User
from django.contrib import messages


# 404 Error Page.
def custom_page_not_found(request, exception=None):
    return render(request, 'dashboard/404.html', status=404)

# 403 Error Page.
def custom_page_forbidden(request, exception=None):
    return render(request, 'dashboard/403.html', status=403)

# 500 Error Page.
def custom_server_not_found(request, exception=None):
    return render(request, 'dashboard/500.html', status=500)

def index(request):

    context = {
        'page_title':'Dashboard',
    }
    return render(request, 'accounts/index.html', context)