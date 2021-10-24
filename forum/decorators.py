from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

#decorator that restricts page access - accessible only for the group manager
def forum_group_manager(req_func):
    def wrapper(request, *args, **kwargs):
        perms = User.get_all_permissions(request.user)
        if 'forum.add_forumgroup' in perms:
            return req_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("<h2>Permission denied - please contact the administrator</h2>")
    return wrapper
