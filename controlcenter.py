################################################################
# File: controlcenter.py
# Purpose:
# - Activatemodel
#
# Martin Hummel
# 09.12.2023
################################################################


import sys, os, re
import subprocess
import threading  
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QTextEdit, QPushButton, QListWidget
from PyQt5.QtCore import QSize

from talkollama import AiTalk
from talkollama import LogEmitter


def cmdlineCommands(cmdlineparam, scriptpath):
	result = subprocess.run([cmdlineparam, scriptpath], shell=True, capture_output=True, text=True)
	s = result.stdout.strip()
	return s


def extract_name(data):
	pattern = re.compile(r'\b([\w-]+:[\w-]+)\b')
	matches = pattern.findall(data)
	return matches


class ControlCenter(QMainWindow):
	def __init__(self, parent=None):
	
		super(ControlCenter, self).__init__()

		path, fl = os.path.split(os.path.realpath(__file__))
		uiFilePath = os.path.join(path, "controlcenter.ui")
		mainWidget = uic.loadUi(uiFilePath, self)

		self.toggleOnOff 	= False
		self.model 		= None
		self.aitalk 		= None
		self.language 		= None
		
		self.startllmButton = self.findChild(QPushButton, 'startllmButton')
		self.startllmButton.clicked.connect(self.startllmButtonClicked)
		self.stopllmButton = self.findChild(QPushButton, 'stopllmButton')
		self.stopllmButton.clicked.connect(self.stopllmButtonClicked)
		self.dispStart = self.findChild(QLineEdit, 'dispStart')
		self.dispStart.setAlignment(QtCore.Qt.AlignCenter)
		self.dispStart.setText("NONE")
		self.textEdit = self.findChild(QTextEdit, 'dispInfo')
		

		cmdlineparam = "ollama list"
		scriptpath = ""
		result = cmdlineCommands(cmdlineparam, scriptpath)
		names = extract_name(result)

		# choose LLM
		self.listLLM = self.findChild(QListWidget, 'listLLM')
		self.listLLM.addItems(names)
		self.listLLM.setSelectionMode(QListWidget.SingleSelection)
		self.listLLM.itemPressed.connect(self.selLLMclicked)
		
		# choose Language
		names = {'en','de'}
		self.listLang = self.findChild(QListWidget, 'listLang')
		self.listLang.addItems(names)
		self.listLang.setSelectionMode(QListWidget.SingleSelection)
		self.listLang.itemPressed.connect(self.selLangclicked)
		
       

	def startllmButtonClicked(self):

		if self.toggleOnOff == False:
			s = "Model started: " + self.model
			self.dispStart.setText(s)

			# Start talking in a separate thread
			self.aitalk = AiTalk(self.model, self.language)
			self.aitalk.log_emitter.log_signal.connect(self.update_log_text)
			self.worker_thread = threading.Thread(target=self.start_aiprocess)
			self.worker_thread.start()

			self.toggleOnOff = True
		else:
			self.dispStart.setText("OFF")
			self.toggleOnOff = False
	
	
	def stopllmButtonClicked(self):
		self.stop_aiprocess()


	def selLLMclicked(self):
		selected_item = self.sender().selectedItems()[0]
		self.model = selected_item.text()
		

	def selLangclicked(self):
		#global  aitalk
		selected_item = self.sender().selectedItems()[0]
		self.language = selected_item.text()
		

	def update_log_text(self, message):
		# Slot to update the QTextEdit with log messages
		self.textEdit.append(message)


	def start_aiprocess(self):
		self.aitalk.aiprocess()
  
	def stop_aiprocess(self):
		self.aitalk.stop_aiprocess()

	


if __name__ == '__main__':
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
	app = QApplication(sys.argv)
	gui = ControlCenter()
	gui.show()
	sys.exit(app.exec_())

