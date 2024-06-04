from sqlalchemy import create_engine, Column, Integer, String, Sequence, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from environs import Env
from datetime import datetime

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
class User(Base): #пользователи
    __tablename__ = 'users'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    step = Column(Integer, nullable=False)
    message_sent = Column(Boolean, nullable=True)
    no_stat = Column(Boolean, nullable = True)
    disable_mess = Column(Boolean, nullable = True)

class Links(Base): #ссылки
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(255), nullable=True)

class time_loop(Base): #временная шкала для отчетов
    __tablename__ = "time_loop"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    step2 = Column(String(50), nullable=True)
    step3 = Column(String(50), nullable=True)
    step4 = Column(String(50), nullable=True)
    step5 = Column(String(50), nullable=True)
    step6 = Column(String(50), nullable=True)
    step7 = Column(String(50), nullable=True)
    step10 = Column(String(50), nullable=True)
    no_stat = Column(Boolean, nullable = True)



#create_table
Base.metadata.create_all(engine)



#смена шага
def user_step_change(name, step) -> None:
    Session = sessionmaker()
    session = Session(bind = engine)
    user = session.query(User).filter(User.username == name).first()
    if user is None:
        new_user = User(username = name, step = step, no_stat = False)
        session.add(new_user)
        session.commit()
    else:
        if user.step < step:
            user.step = step
            session.add(user)
            session.commit()
    session.close()
    return 

# все офферы
def all_link() -> list[str]:
    arr = []
    Session = sessionmaker()
    session = Session(bind = engine)
    users = session.query(Links).all()
    session.close()
    for i in users:
        arr.append(i.link)
    return arr

# на каком шаге пользователь в воронке
def user_step_check(name) -> int:
    Session = sessionmaker()
    session = Session(bind = engine)
    user = session.query(User).filter(User.username == name).first()
    session.close()
    if user is None:
        return 0
    return user.step

# работа с бд для рассылок
def for_th(name):
    Session = sessionmaker()
    session = Session(bind = engine)
    user = session.query(User).filter(User.username == name).first()
    if user.message_sent:
        return False
    user.message_sent = True
    session.commit()
    session.close()
    return True

#обработка временной шкалы шагов
def loop(user, step): 
    date = datetime.now()
    date = datetime.strftime(date, "%Y.%m.%d %H:%M:%S")
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(time_loop).filter(time_loop.username == user).first()
    if curr is None:
       new = time_loop(username = user, no_stat = False)
       session.add(new)
       session.commit()
    curr = session.query(time_loop).filter(time_loop.username == user).first()
    if step == 2:
        if curr.step2 == None:
            curr.step2 = date
    if step == 3:
        if curr.step3 == None:
            curr.step3 = date
    if step == 4:
        if curr.step4 == None:
            curr.step4 = date
    if step == 5:
        if curr.step5 == None:
            curr.step5 = date
    if step == 6:
        if curr.step6 == None:
            curr.step6 = date
    if step == 7:
        if curr.step7 == None:
            curr.step7 = date
    if step == 10:
        if curr.step10 == None:
            curr.step10 = date
    session.commit()
    session.close()


def disable_messages(username):
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(User).filter(User.username == username).first()
    curr.disable_mess = True
    session.commit()
    session.close()

def is_disabled(username):
    Session = sessionmaker()
    session = Session(bind = engine)
    curr = session.query(User).filter(User.username == username).first()
    session.close()
    return curr.disable_mess








