from flask import Flask,render_template,request,url_for,flash,redirect,session

from flask_sqlalchemy import SQLAlchemy



# from flask_login import LoginManager, UserMixin


app=Flask(__name__)
app.secret_key="Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:787889@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db=SQLAlchemy(app)


#create database table
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    #after create the constructor this class
    def __init__(self,name,email,phone):
        self.name=name
        self.email=email
        self.phone=phone

# Create the table within the application context
with app.app_context():
    db.create_all()
    


@app.route('/')
def index():
    data = Data.query.all() 
    print(data)
    return render_template("index.html")


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
            flash("login Successfi")
            return redirect(url_for('show_user_details', name=name, phone=phone))

        else:
            flash("User not found or incorrect credentials!")
            return redirect(url_for("login"))

    return render_template("login.html")

#Show
@app.route("/show/<string:name>/<string:phone>")
def show_user_details(name, phone):

    user = Data.query.filter_by(name=name, phone=phone).first()

    if user:
        
        return render_template("show.html", user=user)
    else:
        flash("User not found")
        return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True,port=5001)



