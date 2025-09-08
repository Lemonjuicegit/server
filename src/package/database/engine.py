from sqlmodel import create_engine, Session
from src.package.utils import re_json
from fastapiUtils import cwd_path

# conf = re_json(rf"{cwd_path}\config.json")

# sqlite_file_name = conf["database"]["server"]
# server = f"sqlite:///{sqlite_file_name}"


def getEngine(
    drivers=None,
    ip=None,
    port=None,
    user=None,
    password=None,
    database=None,
    conf=None,
):
    if conf:
        config = re_json(conf)["database"]
    else:
        config = {
            "drivers": drivers,
            "ip": ip,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
        }
    match config["drivers"]:
        case "mysql":
            server = f"mysql+pymysql://{config['user']}:{config['password']}@{config['ip']}:{config['port']}/{config['database']}"
            return create_engine(server)
        case "sqlite":
            server = f"{config['drivers']}:///{config['ip']}"
            connect_args = {"check_same_thread": False}
            return create_engine(server, connect_args=connect_args)
        case "postgresql":
            server = f"postgresql://{config['user']}:{config['password']}@{config['ip']}:{config['port']}/{config['database']}"
            return create_engine(server)


def getSession(
    drivers=None,
    ip=None,
    port=None,
    user=None,
    password=None,
    database=None,
    conf=None,
):
    return Session(getEngine(drivers, ip, port, user, password, database, conf))
