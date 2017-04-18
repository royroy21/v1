import json

from django.contrib.auth import authenticate
from django.http import HttpResponse

from restless.constants import UNAUTHORIZED


class TokenMiddleware(object):

    def process_request(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META.get('HTTP_AUTHORIZATION', '')
            parts = auth.split()

            if parts:
                try:
                    user = authenticate(token=parts[1])
                except Exception as auth_exc:
                    response_json = json.dumps({
                        'error': auth_exc.detail
                    })
                    return HttpResponse(
                        response_json,
                        status=UNAUTHORIZED,
                        content_type='application/json'
                    )
                except IndexError:
                    response_json = json.dumps({
                        'error': 'JWT Authorization missing token'
                    })
                    return HttpResponse(
                        response_json,
                        status=UNAUTHORIZED,
                        content_type='application/json'
                    )

                if user:
                    request.user = user