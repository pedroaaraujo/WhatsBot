from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import time	

class WhatsBot:
	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('lang=pt-br')
		options.add_argument("--user-data-dir=chrome-data")		
		self.driver = webdriver.Chrome(
			executable_path=r'./chromedriver', chrome_options=options)
		self.driver.get('https://web.whatsapp.com')
		time.sleep(15)
		pickle.dump( self.driver.get_cookies() , open("cookies.pkl","wb"))
		cookies = pickle.load(open("cookies.pkl", "rb"))
		for cookie in cookies:
			self.driver.add_cookie(cookie)			
		self.ativo = True

	def __ChatBox(self):
		chat_box = self.driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')		
		chat_box.click()
		return chat_box

	def __BuscarChat(self, grupo_contato):
		try:
			contato = self.driver.find_element(By.XPATH, '//span[@title="{}"]'.format(grupo_contato))
			contato.click()
			return True
		except:
			pass
		
		#percorre a lista de conversas caso nao seja
		#possivel encontrar o contato pela rotina anterior	
		conversas = self.__GetConversas()
		for contato in conversas:
			texto = contato.text
			if (texto.find(grupo_contato) != -1):
				contato.click()
				return True			
		return False		

	def __GetConversas(self):
		conversas = self.driver.find_elements(By.XPATH, '//div[@class="_2kHpK"]')
		return conversas

	def __UltimaMensagemEnviada(self, grupo_contato):
		if self.__BuscarChat(grupo_contato):
			try:
				mensagens = self.driver.find_elements(By.XPATH, '//div[@class="_2hqOq message-out focusable-list-item"]')
				mensagem = mensagens[-1].text
				return mensagem				
			except:
				return ''

	def __UltimaMensagemRecebida(self, grupo_contato):
		if self.__BuscarChat(grupo_contato):	
			try:
				mensagens = self.driver.find_elements(By.XPATH, '//div[@class="_2hqOq message-in focusable-list-item"]')
				mensagem = mensagens[-1].text
				return mensagem
			except:
				return ''

	def __TextoUltimaMensagem(self, grupo_contato):
		if self.__BuscarChat(grupo_contato):	
			try:
				mensagens = self.driver.find_elements(By.XPATH, '//span[@class="_3Whw5 selectable-text invisible-space copyable-text"]')
				mensagem = mensagens[-1].text
				return mensagem
			except:
				return ''

	def ListaConversas(self):
		lista = []
		conversas = self.__GetConversas()
		for conversa in conversas:
			nome = conversa.text
			nome = nome[:nome.find("\n")]
			lista.append(nome)
		return lista	

	def Encerrar(self):
		self.driver.close
		self.ativo = False

	def MinimizarNavegador(self):
		self.driver.minimize_window()

	def MaximizarNavegador(self):
		self.driver.maximize_window()		

	def EnviarMensagensNumero(self, numero, mensagem):
		self.numero = numero
		self.mensagem = mensagem	
		for I in self.numero:
			print("Enviando mensagem para {}".format(I))
			self.driver.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(I))
			time.sleep(5)
			try:
				self.driver.switch_to_alert().accept()
			except Exception as e:
				print(e)
				pass	
			chat_box = self.__ChatBox()
			time.sleep(1)
			chat_box.click()
			for m in self.mensagem:
				chat_box.send_keys(m)      
				chat_box.send_keys("\n")
				time.sleep(1)								 	

	def EnviarMensagensGrupoContato(self, grupo_contato, mensagem):
		self.grupo_contato = grupo_contato
		self.mensagem = mensagem		
		for I in self.grupo_contato:
			print("Enviando mensagem para {}".format(I))
			if self.__BuscarChat(grupo_contato):
				for m in self.mensagem:
					chat_box = self.__ChatBox()
					chat_box.send_keys(m)      
					chat_box.send_keys("\n")
					time.sleep(1)				

	def AguardandoResposta(self, grupo_contato):
		return self.__TextoUltimaMensagem(grupo_contato) == self.TextoUltimaMensagemRecebida(grupo_contato)

	def Respondido(self, grupo_contato):
		return self.__TextoUltimaMensagem(grupo_contato) == self.TextoUltimaMensagemEnviada(grupo_contato)	

	def TextoUltimaMensagemRecebida(self, grupo_contato):
		try:
			return self.__UltimaMensagemRecebida(grupo_contato)[0:-6]
		except:
			return ''			

	def HoraUltimaMensagemRecebida(self, grupo_contato):
		try:
			return self.__UltimaMensagemRecebida(grupo_contato)[-6:]
		except:
			return ''

	def TextoUltimaMensagemEnviada(self, grupo_contato):
		try:
			return self.__UltimaMensagemEnviada(grupo_contato)[0:-6]
		except:
			return ''			

	def HoraUltimaMensagemEnviada(self, grupo_contato):
		try:
			return self.__UltimaMensagemEnviada(grupo_contato)[-6:]
		except:
			return ''			

	def ResponderContato(self, grupo_contato, mensagem):
		if self.__BuscarChat(grupo_contato):
			self.ResponderContatoAtivo(mensagem)

	def ResponderContatoAtivo(self, mensagem):
		chat_box = self.__ChatBox()		
		chat_box.send_keys(mensagem)      
		chat_box.send_keys("\n")
		time.sleep(1) 			