import pandas as pd
import numpy as np

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords,wordnet

import string
import re
stop=set(stopwords.words('english'))


def reverseWords(input):

    inputWords = input.split(" ")


    inputWords=inputWords[-1::-1]

    output = ' '.join(inputWords) 
    return output

def key_cleaning(str1):
	str2=""
	count=0
	for each in str1.split():
		if each.lower()  in stop or each.isdigit()==True:
			continue
		else:
			count+=1
			str2+=each
			str2+=" "
	strdemo=[]
	for each in str2.split():
		if each.title() not in strdemo:
			strdemo.append(each.title())
	str3=""
	for each in strdemo:
		str3+=each
		str3+=" "

	if count<=8 and ',' not in str3:
		return str3

	else:
		return ""


def find_keys_for_is_a(i,textlist):
	str1=""
	for j in range(i,0,-1):
		if textlist[j][-1]=='.' or textlist[j][-1]==':':
			break
		else:
			str1+=textlist[j]
			str1+=" "
		str1=reverseWords(str1)
		str1=key_cleaning(str1)
	return str1

def find_keys_for_called(i,textlist):
	str1=""
	for j in range(i,len(textlist),1):
		if textlist[j] in stop:
			continue
		elif textlist[j][-1]!='.' and textlist[j][-1]!=',':
			str1+=textlist[j]
			str1+=" "
		elif textlist[j][-1]=='.' or textlist[j][-1]==',':
			str1+=textlist[j][:-1]
			break
		else:
			break
	return str1




class dictionarycreation:
	def __init__(self,text):
		self.text=text
		self.result_dictionary={}
		self.textlist=np.asarray(text.split())


	def called_extraction(self):
		count=0
		for i in range(len(self.textlist)):
			if self.textlist[i]=='called':
				str1=""
				count=0
				for j in range(i-1,0,-1):
					count+=1
					if (self.textlist[j][-1]=='-' or self.textlist[j][-1]=='.') and count>4:
						break;
					else:
						str1+=self.textlist[j]
						str1+=" "
				x=find_keys_for_called(i+1,self.textlist)
				if len(x.split())<6 and x not in self.result_dictionary.keys():
					self.result_dictionary[x.title()]=reverseWords(str1)+" called "+x.upper()

	def is_a_extraction(self):
		for i in range(len(self.textlist)):
			if self.textlist[i]=="is" and self.textlist[i+1]=="a":
				str1=""
				count=0
				for j in range(i+2,len(self.textlist),1):
					if (self.textlist[j][-1]=='.'):
						count+=1
						str1+=self.textlist[j]
						break;
					else:
						count+=1
						str1+=self.textlist[j]
						str1+=" "
				str2=find_keys_for_is_a(i-1,self.textlist)
				if str2 not in self.result_dictionary.keys() and str2!="" and count>3 and str2[0].isupper() and len(str2.split())<5:
					self.result_dictionary[str2.title()]=str2.upper()+" is a "+str1

	def is_known_extraction(self):
		for i in range(len(self.textlist)):
			if  self.textlist[i]=="known" and self.textlist[i+1]=="as":
				str1=""
				count=0
				for j in range(i-1,0,-1):
					count+=1
					if(self.textlist[j][-1]=="-" or self.textlist[j][-1]=='.' or self.textlist[j][-1]=="") and count>4:
						break
					else:
						str1+=self.textlist[j]
						str1+=" "
				x=find_keys_for_called(i+2,self.textlist)
				if len(x.split())<6 and x not in self.result_dictionary.keys():
					self.result_dictionary[x.title()]=reverseWords(str1)+" is known as "+x.upper()
	def repattern_1(self):
		patterns=re.findall("\([A-Z][A-Z]+\)",self.text)
		l=[]
		for i in self.text.split():
			if i.endswith('.') or i.endswith(','):
				l.append(i[:len(i)-1])
				l.append('.')
			else:
				l.append(i)
		d={}
		dd={}
		for i in patterns:
			try:
				keyind=l.index(i)
				k=l[keyind-len(i)+2:keyind+1]
				startind=keyind+1
				l1=l[startind:].index('.')
				endind=l[startind:].index('.')
				d[" ".join(k)]=" ".join(l[startind:endind])
			except:
				pass
		def mykey(each):
			for key in d.keys():
				if each in key.split():
					return key.title()


		for each in patterns:
			for i in range(len(self.textlist)):
				if self.textlist[i]==each:
					defination=""
					for j in range(i+2,len(self.textlist)):
						if self.textlist[j][-1]!='.':
							defination+=self.textlist[j]
							defination+=" "
						else:
							defination+=self.textlist[j]
							break
					self.result_dictionary[mykey(each)]=defination


	def get_dictionary(self):

		return self.result_dictionary


	def antonym_synm(self):
		List = list(map(lambda x:x[:len(x)-1],filter(lambda x:len(x.split())==1,self.result_dictionary.keys())))
		service_synonym={}
		service_antonym={}
		for genre in List: 
			synonyms = set()
			antonyms = set()
			for syn in wordnet.synsets(genre):
				for l in syn.lemmas(): 
					synonyms.add(l.name()) 
					if l.antonyms(): 
						antonyms.add(l.antonyms()[0].name())
			if len(synonyms)!=0:
				service_synonym[genre]=synonyms
			if len(antonyms)!=0:
				service_antonym[genre]=antonyms
		return service_antonym,service_synonym

def dictionary_convertor(text):
	dict1=dictionarycreation(text)
	dict1.called_extraction()
	dict1.is_known_extraction()
	dict1.is_a_extraction()
	dict1.repattern_1()
	return dict1.get_dictionary()

def antonym_synm(l):
		List = list(map(lambda x:x[:len(x)-1],filter(lambda x:len(x.split())==1,l.keys())))
		service_synonym={}
		service_antonym={}
		for genre in List: 
			synonyms = []
			antonyms = []
			for syn in wordnet.synsets(genre):
				for l in syn.lemmas(): 
					synonyms.append(l.name()) 
					if l.antonyms(): 
						antonyms.append(l.antonyms()[0].name())
			if len(synonyms)!=0:
				service_synonym[genre]=synonyms
			if len(antonyms)!=0:
				service_antonym[genre]=antonyms
		return service_antonym,service_synonym
