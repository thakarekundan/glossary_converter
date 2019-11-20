
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import string
import re
stop=set(stopwords.words('english'))


class pdf_to_text:
	def __init__(self,input_file):
		self.file_path=input_file
		self.text=""
		fp=open(self.file_path,'rb')
		rsrcmgr=PDFResourceManager()
		retstr=StringIO()
		codec='utf-8'
		laparams=LAParams()
		device=TextConverter(rsrcmgr,retstr,codec=codec,laparams=laparams)
		interpreter=PDFPageInterpreter(rsrcmgr,device)
		for page in PDFPage.get_pages(fp,pagenos=set(),maxpages=0,password="",caching=True,check_extractable=True):
			interpreter.process_page(page)
		self.text=retstr.getvalue()
		fp.close()
		device.close()
		retstr.close()
	def get_text(self):
		return self.text



    	