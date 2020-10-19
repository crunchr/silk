import json
from urllib.parse import urlparse

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from silk.auth import login_possibly_required, permissions_possibly_required
from silk.models import Profile
from silk.views.code import _code_context, _code_context_from_request
from silk.models import Request


class CProfileView(View):

    @method_decorator(login_possibly_required)
    @method_decorator(permissions_possibly_required)
    def get(self, request, *_, **kwargs):
        request_id = kwargs['request_id']
        silk_request = Request.objects.get(pk=request_id)
        profile_url = urlparse(request.build_absolute_uri().replace('cprofile', 'speedscope-data'))
        context = {
            'silk_request': silk_request,
            'request': request,
            'profile_url': json.dumps({
                'scheme': profile_url.scheme,
                'netloc': profile_url.netloc,
                'path': profile_url.path,
            }),
        }

        return render(request, 'silk/cprofile.html', context)