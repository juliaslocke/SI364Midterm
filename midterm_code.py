import requests
import json
from flask import Flask, request, render_template, redirect, url_for, flash, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this key is a secret'
app.debug = True

@app.errorhandler(404)
def not_found(e):
	return render_template('404error.html'), 404

@app.errorhandler(500)
def internal_error(e):
	return render_template('500error.html'), 500

class WelcomeForm(FlaskForm):
	myname = StringField("What is your name?")
	songname = StringField("What is your favorite song?")
	next = SubmitField("Next")

@app.route('/')
def homepage():
	return render_template('homepage.html')

@app.route('/welcomepg/<imgchoice>')
def get_assignments(imgchoice):
	newform = WelcomeForm()
	cookie_img = request.cookies.get('imgchoice')
	return render_template('form.html', form=newform, img=imgchoice, cookie_img=cookie_img)

@app.route('/songchoice', methods=['GET', 'POST'])
def choose_msg():
	res = WelcomeForm(request.form)
	if request.method == 'POST':
		me = res.myname.data
		song = res.songname.data
		params = {'media':'music', 'format':'json', 'term':song, 'limit':10}
		info = requests.get('https://itunes.apple.com/search?', params = params)
		data = json.loads(info.text)
		return render_template('message_form.html', me = me, song=song, data=data['results'])
	flash('Oops, your name must be filled out!')
	return redirect(url_for('get_assignments', imgchoice = request.cookies.get('imgchoice')))

@app.route('/display', methods=['GET', 'POST'])
def show_image():
	if request.method == 'GET':
		result = request.args
		artist = result.get('coverart')
		params = {'media':'music', 'format':'json', 'term':artist}
		info = requests.get('https://itunes.apple.com/search?', params = params)
		data = json.loads(info.text)
		return render_template('displaying.html', artist=artist, data = data['results'])

@app.route('/createcookie')
def cookie():
	response = make_response(render_template('cookie.html'))
	response.set_cookie('imgchoice', value='cookie')
	return response
