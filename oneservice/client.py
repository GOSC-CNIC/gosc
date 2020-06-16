from .evcloud.adapter import EVCloudAdapter
from .exceptions import UnsupportedServiceType
from .base import AdapterBase


SERVICE_TYPE_EVCLOUD = 'evcloud'
SERVICE_TYPE_OPENSTACK = 'openstack'


def get_adapter_class(style: str = 'evcloud'):
    """
    获取适配器

    :param style: in ['evcloud', 'openstack']
    :return:
        subclass of base.AdapterBase

    :raises: UnsupportedServiceType
    """
    if style.lower() == SERVICE_TYPE_EVCLOUD:
        return EVCloudAdapter

    raise UnsupportedServiceType()


class OneServiceClient:
    def __init__(self, adapter: AdapterBase):
        self.adapter = adapter

    def __getattr__(self, attr):
        try:
            return getattr(self.adapter, attr)
        except AttributeError:
            return self.__getattribute__(attr)

    def authenticate(self, *args, **kwargs):
        return self.adapter.authenticate(*args, **kwargs)

    def server_create(self, *args, **kwargs):
        return self.adapter.server_create(*args, **kwargs)

    def server_delete(self, *args, **kwargs):
        return self.adapter.server_delete(*args, **kwargs)

    def server_action(self, *args, **kwargs):
        return self.adapter.server_action(*args, **kwargs)

    def server_status(self, *args, **kwargs):
        return self.adapter.server_status(*args, **kwargs)

    def server_vnc(self, *args, **kwargs):
        return self.adapter.server_vnc(*args, **kwargs)

    def list_images(self, *args, **kwargs):
        return self.adapter.list_images(*args, **kwargs)

    def list_networks(self, *args, **kwargs):
        return self.adapter.list_networks(*args, **kwargs)

    def list_flavors(self, *args, **kwargs):
        return self.adapter.list_flavors(*args, **kwargs)
