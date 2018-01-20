import collections
from singleton_decorator import singleton

# get list of proxies and rotate
@singleton
class ProxyRotator:
    def __init__(self, file_name=None):
        """
        Rotator default constructor
        :param file_name: name of the proxy file
        :type file_name: file (txt)
        """
        print('initiating proxy rotator')
        print('proxy file name: {file}'.format(file=file_name))
        self.proxy_file_name = file_name
        self.proxies = []

        if self.get_proxies():
            self.proxy_queue = collections.deque(self.proxies)
        else:
            self.proxy_queue = None

    def get_proxies(self):
        """
        Read list of proxies from file
        :return:
        """
        print('reading proxy file: {file}'.format(file=self.proxy_file_name))

        if self.proxy_file_name is not None:
            try:
                proxy_file = open(self.proxy_file_name, 'r')
                proxy_list = [line.strip() for line in proxy_file.readlines()]

                for proxy in proxy_list:
                    content = proxy.split()
                    proxy = {
                        'http': 'http://{user}:{passwd}@{ip}:{port}'.format(user=content[0], passwd=content[1],
                                                                            ip=content[2], port=content[3]),
                        'https': 'socks5://{user}:{passwd}@{ip}:{port}'.format(user=content[0], passwd=content[1],
                                                                             ip=content[2], port=content[4])
                    }
                    self.proxies.append(proxy)
                proxy_file.close()
                return True
            except Exception as e:
                print('{exception}'.format(exception=e))
                return False
        else:
            print('using singleton obj')

    def get_proxy(self):
        """
        Get first proxy from queue and rotate the queue
        :return: proxy
        """
        if self.proxy_queue is not None:
            proxy = self.proxy_queue[0]
            self.proxy_queue.rotate(1)
            print('generating proxy: {proxy}'.format(proxy=proxy))
            return proxy
        else:
            return None