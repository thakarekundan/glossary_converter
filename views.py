import textconversion
import dictionaryconversion
import json_download
textfile=textconversion.pdf_to_text('se.pdf')
dictionary=dictionaryconversion.dictionary_convertor(textfile.get_text())
s=json_download.json_downloaded(dictionary)
