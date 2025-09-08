
class Use:
    def __init__(self) -> None:
        self.useApi = {}
        
    def drop_zipFile(self,ip):
        for filepath in self.useApi[ip].zipFileName:
            if filepath.is_file():
                filepath.unlink()
        
use = Use()