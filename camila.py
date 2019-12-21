import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

#Instance variables
dir_path = os.getcwd()

#chatbot = ChatBot('camila',
#    logic_adapters=[
#        'chatterbot.logic.MathematicalEvaluation',
#        'chatterbot.logic.TimeLogicAdapter'
#    ]    
#)
chatbot = ChatBot('camila')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.portuguese')
trainerer = ListTrainer(chatbot)

def treina(diretorio):
    for treino in os.listdir(diretorio):
        conversas = open(diretorio+'/'+treino, 'r').readlines()
        trainerer.train(conversas)

treina(dir_path + '/treinos')


lastMessage = ''

options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir="+dir_path+"\profile\wpp")

#app start
driver = webdriver.Chrome(dir_path + '/chromedriver', chrome_options=options)
driver.get('http://web.whatsapp.com/')
driver.implicitly_wait(15)

caixa_de_pesquisa = driver.find_element_by_class_name('_2zCfw')
nome_contato = input('Nome Contato: ')
caixa_de_pesquisa.send_keys(nome_contato)
time.sleep(2)

contato = driver.find_element_by_xpath('//span[@title = "{}"]'.format(nome_contato))

contato.click()
time.sleep(2)



#comunication functions

def pegaConversa():
    try:
        post = driver.find_elements_by_css_selector('div[class=_12pGw]')[-1].text

        print('recebida: ' + post)
        
        return post.lower()
    except Exception as e:
        print('Ops!')
        print(e)
        pass

def processMessage(message):
    return str(chatbot.get_response(message))

def enviaMensagem(mensagem):
    inputField = driver.find_element_by_class_name('_3u328')

    inputField.click()
    inputField.send_keys(mensagem)

    time.sleep(1)

    driver.find_element_by_class_name('_3M-N-').click()


while True:
    message = pegaConversa()
    print(message)
    print(lastMessage)
    if message != lastMessage.lower():
        lastMessage = processMessage(message)
        time.sleep(1)
        enviaMensagem(lastMessage)