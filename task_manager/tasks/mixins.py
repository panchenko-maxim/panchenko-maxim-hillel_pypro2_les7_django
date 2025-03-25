from django.http import HttpResponseNotAllowed

class OwnerOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            return HttpResponseNotAllowed(content='Only author can perform some actions', permitted_methods=('GET',))
        return super().dispatch(request, *args, **kwargs)