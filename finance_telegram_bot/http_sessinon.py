from requests import Session
import os


class HttpSession(Session):

    def request(self, *args, **kwargs):
        self.headers.update({'Authorization': f'Bearer {os.getenv("BACKEND_HOST_TOKEN")}'})
        base_path = f'http://{os.getenv("BACKEND_HOST_IP")}:{os.getenv("BACKEND_HOST_PORT")}/api/v1/'

        args = list(args)
        args[1] = base_path + args[1]

        if args[1][-1] != '/':
            args[1] = args[1] + '/'

        return super().request(*args, **kwargs)
