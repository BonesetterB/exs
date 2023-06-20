from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Application
from telegram.ext import ContextTypes
from telegram.ext import ChatJoinRequestHandler
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

TOKEN="5815046882:AAEda4DeKsDr3N2TadHINxuqW_De1CwYONc"

engine = create_engine('sqlite:///base.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'
    id=Column(Integer,primary_key=True)
    id_user_tg = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)


Base.metadata.create_all(engine)
Base.metadata.bind = engine

def send_messeng():
    x=input('Введіть пост для розсилки --- ')
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    for person in session.query(Person).all():
        params={
                'chat_id': int(person.id_user_tg),
                'text': x
            }
        requests.post(url, params)

if __name__=='__main__':
    send_messeng()


