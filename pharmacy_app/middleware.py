from django.utils.deprecation import MiddlewareMixin
from pharmacy_app.utils.thread_local import set_current_user

class CurrentUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            set_current_user(request.user)