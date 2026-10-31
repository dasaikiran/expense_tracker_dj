from tracker.models import RequestLogs


class RequestLogging:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_info = vars(request)
        print(request.method, request.path)

        RequestLogs.objects.create(
            request_path=request.path,
            request_method=request.method,
            request_info=request_info,
        )

        return self.get_response(request)
