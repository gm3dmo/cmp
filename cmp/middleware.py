from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

class MgmtAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/mgmt/') and not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        return self.get_response(request) 