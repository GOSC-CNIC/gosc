class AdapterBase:
    def __init__(self,
                 endpoint_url: str,
                 api_version: str,
                 auth=None,  # type tuple (username, password)
                 *args, **kwargs
                 ):
        self.endpoint_url = endpoint_url
        self.auth = auth
        self.api_version = api_version

    def authenticate(self, username, password, style: str = 'token'):
        """
        认证获取 Token

        :param username:
        :param password:
        :param style: 'token', 'jwt'
        :return:
            ['token', 'token str']
            ['jwt', 'jwt str']

        :raises: exceptions.AuthenticationFailed
        """
        raise NotImplementedError('`authenticate()` must be implemented.')

    def server_create(self, image_id: str, flavor_id: str, region_id: str, network_id: str = None, headers={},
                      extra_kwargs={}):
        """
        创建虚拟服务器

        :param image_id: 系统镜像id
        :param flavor_id: 配置样式id
        :param region_id: 区域/分中心id
        :param network_id: 子网id
        :param headers: 标头
        :param extra_kwargs: 其他参数
        :return:
        """
        raise NotImplementedError('`vm_create()` must be implemented.')

    def server_delete(self, server_id, headers={}):
        raise NotImplementedError('`server_delete()` must be implemented.')

    def server_action(self, server_id, op, headers={}):
        """
        操作虚拟主机

        :param server_id:
        :param op: value in ['start', 'reboot', 'shutdown', 'poweroff', 'delete', 'delete_force']
        :param headers:
        :return:
        """
        raise NotImplementedError('`server_action()` must be implemented.')

    def server_status(self, server_id, headers={}):
        raise NotImplementedError('`server_status()` must be implemented.')

    def server_vnc(self, server_id, headers={}):
        raise NotImplementedError('`server_vnc()` must be implemented.')

    def list_images(self, region_id: str, headers={}):
        """
        列举镜像

        :param region_id: 分中心id
        :param headers:
        :return:
        """
        raise NotImplementedError('`list_images()` must be implemented.')

    def list_networks(self, region_id: str, headers={}):
        """
        列举子网

        :param region_id: 分中心id
        :param headers:
        :return:
        """
        raise NotImplementedError('`list_networks()` must be implemented.')

    def list_flavors(self, headers={}):
        """
        列举配置样式

        :param headers:
        :return:
        """
        raise NotImplementedError('`list_flavors()` must be implemented.')
