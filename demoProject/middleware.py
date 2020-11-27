import time
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin


def timing(get_response):
    def middleware(request):
        request.current_time = datetime.now()
        t1 = time.time()
        response = get_response(request)
        t2 = time.time()
        print("TOTAL TIME:", (t2 - t1))
        return response

    def process_exception(request, exception):
        # Do something useful with the exception
        pass

    middleware.process_exception = process_exception
    return middleware


class BCMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        # Add the header. Or do other things, my use case is to send a monitoring metric
        response["X-Page-Generation-Duration-ms"] = int(duration * 1000)
        print("DURATION:", duration)
        return response

    def process_request(self, request):
        #request._request_time = datetime.now()
        pass

    def process_template_response(self, request, response):

        # response_time = datetime.now() - request._request_time
        # response.context_data['response_time'] = response_time
        return response
