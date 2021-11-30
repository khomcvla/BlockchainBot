import telebot
import random
import string
from uuid import uuid4
from random import randrange

from blockchain import Blockchain

TOKEN = "2147116231:AAElcotkDbwidWYV_VHvmhy-TaoAip6B2wA"
bot = telebot.TeleBot(TOKEN)
blockchain = Blockchain()
node_identifier = str(uuid4()).replace('-', '')


@bot.message_handler(commands=['mine'])
def mine(message):
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    bot.send_message(message.chat.id, f'New block generated: {str(response)}')


@bot.message_handler(commands=['full_chain'])
def full_chain(message):
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    bot.send_message(message.chat.id, str(response))


@bot.message_handler(commands=['full_transactions'])
def full_transactions(message):
    bot.send_message(message.chat.id, str(blockchain.current_transactions))


@bot.message_handler(commands=['random_transaction'])
def random_transaction(message):
    index = blockchain.new_transaction(
        ''.join(random.choice(string.ascii_lowercase) for i in range(15)),
        ''.join(random.choice(string.ascii_lowercase) for i in range(15)),
        randrange(10)
    )
    bot.send_message(message.chat.id, f'Successfully generated random transaction: {blockchain.last_transaction}')


bot.polling(none_stop=True)