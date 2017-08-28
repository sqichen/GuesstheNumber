
import random

from flask import Flask, render_template, flash, redirect, url_for, session
from flask_wtf import Form
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very hard to guess string'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)


class GuessNumberForm(Form):
	number = IntegerField(u'Please enter an integer between 0 and 1000', validators=[
		DataRequired(u'Please enter a valid integer!'), 
		NumberRange(0, 1000, u'Please enter an integer between 0 and 1000!')])
	submit = SubmitField(u'Submit')


@app.route('/')
def index():
	#generate a random integer between 0 and 1000, and store the number into session
	session['number'] = random.randint(0, 1000)
	session['times'] = 10
	return render_template('index.html')


@app.route('/guess', methods=['GET', 'POST'])
def guess():
	times = session['times']
	result = session['number']
	form = GuessNumberForm()
	if form.validate_on_submit():
		times -= 1
		session['times'] = times
		if times == 0:
			flash(u'Oops, you lose...>~~<', 'danger')
			return redirect(url_for('index'))
		answer = form.number.data
		if answer > result:
			flash(u'Your guess is too big! %s chances left.' % times, 'warning')
		elif answer < result:
			flash(u'Your guess is too small! %s chances left.' % times, 'info')
		else:
			flash(u'Congrats! You win!', 'success')
			return redirect(url_for('index'))
		return redirect(url_for('guess'))
	return render_template('guess.html', form=form)

if __name__ == '__main__':
	app.run()
	