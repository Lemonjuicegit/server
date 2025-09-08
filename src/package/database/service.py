import csv
from sqlmodel import Session, select, delete, SQLModel
from .engine import getSession
from types import FunctionType

class Service:
    """
    数据库服务类，用于执行与数据库相关的操作。
    
    参数:
    - DO: SQLModel的子类，代表数据库中的一个表。
    - session_conf: 字典或字符串，配置Session的参数。
    """
    def __init__(self, DO: SQLModel, session_conf: dict | str):
        self.DO = DO
        self.session_conf = session_conf
        self.initSession()

    def initSession(self):
        """
        初始化数据库会话。
        
        根据session_conf的类型（字典或字符串）来获取数据库会话。
        """
        if isinstance(self.session_conf, dict):
            self.session = getSession(**self.session_conf)
        elif isinstance(self.session_conf, str):
            self.session = getSession(conf=self.session_conf)

    def insert(self, data:list[dict]):
        """
        批量插入数据到数据库中。
        
        参数:
        - data: 列表，包含多个字典，每个字典代表一条记录。
        """
        self.session.bulk_insert_mappings(self.DO, data)
        self.session.commit()

    def insert_one(self, data):
        """
        插入单条数据到数据库中。
        
        参数:
        - data: 字典，代表一条记录。
        """
        self.session.add(data)
        self.session.commit()

    def select_all(self):
        """
        查询表中的所有数据。
        
        返回:
        - res: 列表，包含查询到的所有记录。
        """
        statement = select(self.DO)
        res = self.session.exec(statement).all()
        return res

    def select(self, row:dict|FunctionType)-> list[SQLModel]:
        """
        根据条件查询数据。
        
        参数:
        - row: 字典，包含查询条件。
        
        返回:
        - res: 列表，包含查询到的记录。
        """


        statement = select(self.DO)
        if isinstance(row, FunctionType):
            statement = row(statement)
        elif isinstance(row, dict):
            for key, value in row.items():
                statement = statement.where(getattr(self.DO, key) == value)
        res = self.session.exec(statement).all()
        return res

    def limit(self, count: int = 1000) -> list[SQLModel]:
        """
        查询前N条记录，默认为前1000条。
        
        参数:
        - count: 整数，要查询的记录数量，默认为1000。
        
        返回:
        - res: 列表，包含查询到的记录。
        """
        statement = select(self.DO).limit(count)
        res = self.session.exec(statement).all()
        return res

    def update(self, data):
        """
        更新数据。
        
        参数:
        - data: 字典或列表，包含要更新的数据。
        """
        if isinstance(data, dict):
            up_data = self.select({"id": data["id"]})[0]
            for key, value in data.items():
                if key != "id":
                    setattr(up_data, key, value)
        elif isinstance(data, list):
            self.session.bulk_update_mappings(self.DO, data)
        self.session.commit()

    def delete(self, ids: list[int]):
        """
        删除指定ID的数据。
        
        参数:
        - ids: 列表，包含要删除的记录的ID。
        """
        dele = delete(self.DO).where(self.DO.id.in_(ids))
        self.session.exec(dele)
        self.session.commit()

    def to_csv(self, where=None, file_path=None, encoding="utf-8"):
        """
        将查询到的数据导出为CSV文件。
        
        参数:
        - where: 字典，包含查询条件。
        - file_path: 字符串，CSV文件的路径。
        - encoding: 字符串，文件的编码方式，默认为"utf-8"。
        """
        if where:
            data = self.select(where)
        else:
            data = self.select_all()
        fields = list(self.DO.__fields__.keys())
        if file_path:
            with open(f"{file_path}.csv", "w", encoding=encoding, newline="") as f:
                write = csv.DictWriter(f, fields)
                write.writeheader()
                write.writerows([v.model_dump() for v in data])
        else:
            with open("data.csv", "w", encoding=encoding, newline="") as f:
                write = csv.DictWriter(f, fields)
                write.writeheader()
                write.writerows([v.model_dump() for v in data])

    def up_fidld(self, before, after, callable, where=None):
        """
        更新字段值。
        
        参数:
        - before: 字符串，更新前的字段名。
        - after: 字符串，更新后的字段名。
        - callable: 可调用对象，用于处理字段值。
        - where: 字典，包含查询条件。
        """
        if where:
            statement = self.select(where)
        else:
            statement = self.select_all()
        up_data = []
        for item in statement:
            item_data = {}
            item_data["id"] = item.id
            res = callable(dict(item)[before])
            if res:
                item_data[after] = res
            up_data.append(item_data)

        self.update(up_data)
    
    def close(self):
        """
        关闭数据库会话。
        """
        self.session.close()