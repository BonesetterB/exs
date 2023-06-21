from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Application
from telegram.ext import ContextTypes
from telegram.ext import ChatJoinRequestHandler
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

# for person in session.query(Person).all():
#     print(f"Айді --- {person.id_user_tg}, Ім'я === {person.name}")


TOKEN="5815046882:AAEda4DeKsDr3N2TadHINxuqW_De1CwYONc"
BOT_username='@Sar_vivi_bot'

async def send_messeng(chat_id,update):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    params={
        'chat_id': chat_id,
        'text': "HELLO ITS ME MARIOO"
    }
    print(type(chat_id))
    response = requests.post(url, params)
    if response.status_code == 200:
        new_person = Person(name=update.effective_user.first_name, id_user_tg=update.effective_user.id)
        session.add(new_person)
        session.commit()
        print('Повідомлення успішно надіслано!')
    else:
        print('Помилка при надсиланні повідомлення.')

async def join_request(update, context):
    await context.bot.approve_chat_join_request(
            chat_id=update.effective_chat.id, user_id=update.effective_user.id
        )
    await send_messeng(update.effective_user.id,update)

async def update_bace():
    pass
async def start_comand(update:Updater,context:ContextTypes.DEFAULT_TYPE):
    print('HI!')
    await update.message.reply_text('Привіт, що робиш?')

async def help_comand(update:Updater,context:ContextTypes.DEFAULT_TYPE):
    print('HEELP')
    await update.message.reply_text('Чим можу допомгти?')

async def custom_comand(update:Updater,context:ContextTypes.DEFAULT_TYPE):
    print('CustomSEXS')
    await update.message.reply_text('Кастомна команда, я крутий')

def handler(text):
    pass


if __name__=='__main__':
    app=Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',start_comand))
    app.add_handler(CommandHandler('help',help_comand))
    app.add_handler(CommandHandler('custom',custom_comand))
    app.add_handler(ChatJoinRequestHandler(join_request))
    app.run_polling(poll_interval=3)
