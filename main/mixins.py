from .models import ViewCount
from modules.services.utils import get_client_ip


class ViewCountMixin:
    def get_object(self):
        obj = super().get_object()
        ip_address = get_client_ip(self.request)
        ViewCount.objects.get_or_create(quote=obj, ip_address=ip_address)
        return obj