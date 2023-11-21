from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app=Flask(__name__)
app.secret_key="Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:787889@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db=SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

#create database table
class Data(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    #after create the constructor this class
    def __init__(self,name,email,phone):
        self.name=name
        self.email=email
        self.phone=phone

@login_manager.user_loader
def load_user(user_id):
    return Data.query.get(int(user_id))        

# Create the table within the application context
with app.app_context():
    db.create_all()
    


@app.route('/')
def index():
    data = Data.query.all() 
    # print(data)
    return render_template("index.html", result=data)


@app.route('/addEmployee', methods=['POST','GET'])
def addEmployee():

    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        my_data=Data(name,email,phone)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template("addEmployee.html")

#editEmployee
@app.route('/editemployee/<id>', methods=['POST','GET'])
def editEmployee(id):
    data = Data.query.get(id)
    print(data.name, data.email, data.phone)
    # print(data)
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        data.name = name
        data.email = email
        data.phone = phone

        db.session.commit()
        return redirect("/")

    return render_template("editEmployee.html", result=data)

#delete
@app.route("/delete/<id>", methods=["GET", "POST"])
def delete(id):
    data = Data.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect("/")

#Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        user = Data.query.filter_by(name=name, phone=phone).first()

        if user:
            login_user(user)  # Log in the user
            flash("Login Successful")
            return redirect(url_for('show_user_details'))

        flash("User not found or incorrect credentials!")
        return redirect(url_for("login"))

    return render_template("login.html")

#show
@app.route("/show")
@login_required
def show_user_details():
    return render_template("show.html", user=current_user)


@app.route("/logout")
def logout():
    logout_user()  # Log the user out
    return redirect(url_for("login"))


if __name__=='__main__':
    app.run(debug=True)



