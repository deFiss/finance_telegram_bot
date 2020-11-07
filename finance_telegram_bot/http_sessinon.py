from requests import Session
import os


class HttpSession(Session):
    def __init__(self):
        super().__init__()

        self.headers.update({'Authorization': f'Bearer {os.getenv("BACKEND_HOST_TOKEN")}'})
        self.base_path = f'http://{os.getenv("BACKEND_HOST_IP")}:{os.getenv("BACKEND_HOST_PORT")}/api/v1/'

    def request(self, *args, **kwargs):
        # add base path
        args = list(args)
        args[1] = self.base_path + args[1]

        return super().request(*args, **kwargs)
