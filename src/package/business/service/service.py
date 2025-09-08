from package.database import BaseService


class Service(BaseService):
    def __init__(self, DO):
        self.conf = {
            "drivers": "postgresql",
            "ip": "192.168.2.202",
            "port": 5432,
            "user": "business",
            "password": "JIAyu123456",
            "database": "business",
        }
        super().__init__(DO, self.conf)
