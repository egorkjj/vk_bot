from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from environs import Env

#read_env
env = Env()
env.read_env(".env")
user = env.str("DB_USER")
passw = env.str("DB_PASSWORD")
host = env.str("DB_HOST")
name = env.str("DB_NAME")

# Подключение к базе данных PostgreSQL
DATABASE_URL = f"postgresql+psycopg2://{user}:{passw}{host}/{name}"

# Создание объекта Engine
engine = create_engine(DATABASE_URL)

# Создание базового класса для моделей
Base = declarative_base()

# Определение модели User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    step = Column(Integer, nullable=False)

class Links(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(255), nullable=True)

#create_table
Base.metadata.create_all(engine)

#check if user is not on last step
def db_check(name) -> bool:
    Session = sessionmaker()
    session = Session(bind = engine)
    user = session.query(User).filter(User.username == name).first()
    session.close()
    if user is None:
        return True
    if user.step == 10:
        return False
    return True


#change step
def user_step_change(name, step) -> None:
    Session = sessionmaker()
    session = Session(bind = engine)
    user = session.query(User).filter(User.username == name).first()
    if user is None:
        new_user = User(username = name, step = step)
        session.add(new_user)
        session.commit()
    else:
        user.step = step
        session.add(user)
        session.commit()
    session.close()
    return 


def all_link() -> list[str]:
    arr = []
    Session = sessionmaker()
    session = Session(bind = engine)
    users = session.query(Links).all()
    session.close()
    for i in users:
        arr.append(i.link)
    return arr







