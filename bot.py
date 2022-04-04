from typing import Optional
import requests
# from misc import token
from yobit import get_btc
from time import sleep

my_message = ''
my_answer = ''
token = ''

try:
    from misc import token
    from my_message import *

except ImportError:
    pass


URL = f'https://api.telegram.org/bot{token}/'

# если возникает необходимость хранения промежуточных состояний (id последнего элемента), то это знак, что нужно использовать класс
global update_id
update_id = 0


def get_updates() -> dict:
    """ Get data about messages from user """
    url = f'{URL}getupdates'
    response = requests.get(url)
    return response.json()


def get_message() -> Optional[dict]:
    """ Get a last message from user """
    data = get_updates()
    last_update_id = data['result'][-1]['update_id']
    global update_id
    if update_id != last_update_id:
        update_id = last_update_id
        chat_id = data['result'][-1]['message']['chat']['id']
        text = data['result'][-1]['message']['text']
        message = {'chat_id': chat_id,
                   'text': text}
        return message
    return None


def send_message(chat_id, text='Wait a second, please...'):
    """ Send a mesage to user """
    url = f'{URL}sendmessage?chat_id={chat_id}&text={text}'
    requests.get(url)


def main():
    """ Start bot """
    while True:
        message = get_message()
        if message is not None:
            chat_id = message['chat_id']
            text = message['text']
            if text == '/btc':
                send_message(chat_id, get_btc())
            elif text == my_message:
                send_message(chat_id, my_answer)
            # else:
            #     send_message(chat_id, 'I don\'t understand')
        else:
            continue
        sleep(2)


if __name__ == '__main__':
    main()
