from src.package.database import BaseService
from fastapiUtils import cwd_path

class Service(BaseService):
    def __init__(self, DO):
        super().__init__(DO, rf"{cwd_path}\config.json")
