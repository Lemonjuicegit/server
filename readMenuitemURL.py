import json,os
from pathlib import Path
from src.package.utils import re_json
class Config:
    def __init__(self) -> None:
        # self.cwd_path = r"E:\exploitation\collection\server"
        self.cwd_path = os.getcwd()
        self.path = Path(f"{self.cwd_path}\\menuitemURL.json")
        self.menuitemURL = re_json(self.path)
        self.routerName = list(self.menuitemURL)
        self.routerName = list(filter(lambda x:x not in ['utils'],self.routerName))
        self.re_routerName = []
    def upmenuitem(self):
        with open(f"{self.cwd_path}\\menuitemURL.json", 'w',encoding='utf-8') as f:
            f.write(json.dumps(self.menuitemURL))
    
    def getMenuitem(self):
        self.menuitemURL = json.loads(self.path.read_text(encoding="utf-8"))
        return self.menuitemURL
        
config = Config()
