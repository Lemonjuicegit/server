from package.database.business.DO import SystemDictionaryDO
from .service import Service


class SystemDictionaryService(Service):
    def __init__(self) -> None:
        super().__init__(SystemDictionaryDO)


systemDictionaryService = SystemDictionaryService()
