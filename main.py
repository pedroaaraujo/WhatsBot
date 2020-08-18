from whatsbot import WhatsBot 
from configparser import SafeConfigParser
import requests

config = SafeConfigParser()
config.read('config.ini')

servidor = config.get('CONFIGURACAO', 'servidor')

bot = WhatsBot()
bot.MaximizarNavegador
mensagens = ['Olá', 'Esta é uma mensagem automatizada', 'Obrigado']
contato = ['5537991123000']
bot.EnviarMensagensNumero(contato, mensagens)
        