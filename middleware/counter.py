import random
from api.models import Counter


class IncreaseCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        random.seed(0)
        self.min = 10
        self.max = 100

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        counter = None
        try:
            counter = Counter.objects.get(type="website")
        except Counter.DoesNotExist as ex:
            pass
        else:
            counter.count = str(int(counter.count) + random.randint(self.min, self.max))
            counter.save()
        response = self.get_response(request)
        return response
