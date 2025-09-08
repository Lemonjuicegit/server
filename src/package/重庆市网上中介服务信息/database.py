from src.package.database.service import Service
from .DO import CgggDO,JgggDO,ZjjgDO

conf = {
    "drivers": 'postgresql',
    "ip": '192.168.2.71',
    "port": 5432,
    "user": 'postgres',
    "password": '123456',
    "database": 'zjjgxx',
}
cggg_service = Service(CgggDO,conf)
jggg_service = Service(JgggDO,conf)
zjjg_service = Service(ZjjgDO,conf)