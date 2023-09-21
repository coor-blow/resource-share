from django.conf import settings
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from apps.core.logging import Logging

logging = Logging(str(settings.BASE_DIR / "logs" / "req_res_logs.txt"))


def simple_logging_middleware(get_response):
    def middleware(request):
        # : pre-processing -> HTTPRequest
        http_method = request.method
        url = request.get_full_path()
        host_port = request.get_host()
        content_type = request.headers["Content-Type"]
        user_agent = request.headers["User-Agent"]

        msg = f"{http_method} | {host_port}{url} | {content_type} | {user_agent}"
        logging.info(msg)

        response = get_response(request)  # next middleware or the view

        # : post-processing -> HTTPResponse
        # TODO: Investigate the response and decide on what to log
        # TODO: Formulate your message
        # TODO: log the message using the info level method

        return response

    return middleware


class ViewExecutionTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Pre-processing
        # START TIMER
        start_time = timezone.now()

        response = self.get_response(request)

        # Post-processing
        # STOP TIMER
        total_time = timezone.now() - start_time
        http_method = request.method
        url = request.get_full_path()
        host_port = request.get_host()
        msg = f"EXECUTION TIME {total_time} >> {http_method} | {host_port}{url}"

        # Interesting to do
        # - Set a limit for the time your views should take to execute
        # - Compare the total time to this limit and call the respective level method
        logging.info(msg)

        return response


class ViewExecutionTime2Middleware(MiddlewareMixin):
    def process_request(self, request):
        """Called during pre-processing"""

        request.start_time = timezone.now()

    def process_response(self, request, response):
        """Called during post-processing"""

        total_time = timezone.now() - request.start_time
        http_method = request.method
        url = request.get_full_path()
        host_port = request.get_host()
        msg = f"EXECUTION TIME {total_time} >> {http_method} | {host_port}{url}"
        logging.info(msg)

        return response
