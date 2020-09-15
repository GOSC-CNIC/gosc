"""

"""
from collections import namedtuple
from .inputs import CreateServerInput


AuthHeaderClass = namedtuple('AuthHeaderClass', ['header_name',         # example: 'Authorization'
                                                 'header_value'         # example: 'Token xxx', 'JWT xxx'
                                                 ])
AuthQueryClass = namedtuple('AuthQueryClass', ['query_name',            # example: 'token', 'jwt'
                                               'query_value'
                                               ])
AuthClass = namedtuple('AuthClass', ['style',       # 'token', 'jwt', ...
                                     'token',       # token value
                                     'header',      # AuthHeaderClass()
                                     'query',       # AuthQueryClass(); None if unsupported
                                     'expire',      # expire timestamp; type: int
                                     'username',
                                     'password'
                                     ])


class BaseAdapter:
    """
    不同类型的服务平台的api适配器的基类
    """
    def __init__(self,
                 endpoint_url: str,
                 api_version: str,
                 auth: AuthClass = None,
                 *args, **kwargs
                 ):
        self.endpoint_url = endpoint_url
        self.auth = auth
        self.api_version = api_version

    def authenticate(self, username, password):
        """
        认证获取 Token

        :param username:
        :param password:
        :return:
            AuthClass()

        :raises: exceptions.AuthenticationFailed
        """
        raise NotImplementedError('`authenticate()` must be implemented.')

    def server_create(self, params: CreateServerInput, **kwargs):
        """
        创建虚拟服务器
        """
        raise NotImplementedError('`vm_create()` must be implemented.')

    def server_delete(self, server_id, headers: dict = None):
        raise NotImplementedError('`server_delete()` must be implemented.')

    def server_action(self, server_id, op, headers: dict = None):
        """
        操作虚拟主机

        :param server_id:
        :param op: value in ['start', 'reboot', 'shutdown', 'poweroff', 'delete', 'delete_force']
        :param headers:
        :return:
        """
        raise NotImplementedError('`server_action()` must be implemented.')

    def server_status(self, server_id, headers: dict = None):
        raise NotImplementedError('`server_status()` must be implemented.')

    def server_vnc(self, server_id, headers: dict = None):
        raise NotImplementedError('`server_vnc()` must be implemented.')

    def list_images(self, region_id: str, headers: dict = None):
        """
        列举镜像

        :param region_id: 分中心id
        :param headers:
        :return:
        """
        raise NotImplementedError('`list_images()` must be implemented.')

    def list_networks(self, region_id: str, headers: dict = None):
        """
        列举子网

        :param region_id: 分中心id
        :param headers:
        :return:
        """
        raise NotImplementedError('`list_networks()` must be implemented.')

    def list_flavors(self, headers: dict = None):
        """
        列举配置样式

        :param headers:
        :return:
        """
        raise NotImplementedError('`list_flavors()` must be implemented.')

    def get_flavor(self, flavor_id, headers: dict = None):
        raise NotImplementedError('`get_flavor()` must be implemented.')

    def get_network(self, network_id, headers: dict = None):
        raise NotImplementedError('`get_network()` must be implemented.')

