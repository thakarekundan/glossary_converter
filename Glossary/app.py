from flask import Flask,render_template,url_for,request,send_file,redirect,session
from werkzeug.utils import secure_filename
import textconversion
import dictionaryconversion
import json
import time




app = Flask(__name__)
app.secret_key = "super secret key"
@app.route("/")
def index():

    return render_template('index.html')

@app.route("/test.html")
def services():

    return render_template('test.html')


@app.route("/#aboutapp")
def about():
	return redirect('#aboutapp')



@app.route("/analyze",methods=['GET','POST'])
def analyze():
	start=time.time()
	if request.method == 'POST':
		rawtext = request.files['rawtext']
		if rawtext.filename=='':
			return render_template('index.html',input="file not selected")
		rawtext.save(secure_filename(rawtext.filename))
		textfile=textconversion.pdf_to_text(rawtext.filename)
		dictionary=dictionaryconversion.dictionary_convertor(textfile.get_text())
		anto,syno=dictionaryconversion.antonym_synm(dictionary)
		end=time.time()
		final_time=end-start
		s=json.dumps(dictionary)
		with open(rawtext.filename.split('.')[0]+"_glossary.json","w") as f:
			f.write(s)
		t=json.dumps(anto)
		with open(rawtext.filename.split('.')[0]+"_anto_syno.json","w") as f1:
			f1.write(t)
		t1=json.dumps(syno)
		with open(rawtext.filename.split('.')[0]+"_anto_syno.json","a") as f2:
			f2.write(t1)
		session['file_anto_syno']=rawtext.filename.split('.')[0]+"_anto_syno.json"
		
	return render_template('index.html',ctext=rawtext.filename,final_time=final_time,final_summary=dictionary,text1="Successfully extracted!!! Download Your Glossary File")




@app.route("/download",methods=['GET','POST'])
def download():
	file_input = request.values['file']
	filename=file_input.split('.')[0]+"_glossary.json"
	return send_file(filename,as_attachment=True)




@app.route("/download1",methods=['GET','POST'])
def download1():
	file_input = session.get('file_anto_syno',None)
	filename=file_input
	return send_file(filename,as_attachment=True)


app.run(debug=True)
