from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

@app.route("/", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(first_name=request.form['first_name'], last_name=request.form['last_name'], email=request.form['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        resp = make_response(redirect('/welcome'))
        resp.set_cookie('first_name', request.form['first_name'])
        return resp
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    first_name = request.cookies.get('first_name')
    return render_template('welcome.html', first_name=first_name)

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('first_name')
    return resp

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
