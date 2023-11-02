from flask import Flask, render_template,url_for,request,redirect,flash,session

from flask_mysqldb import MySQL
import re

app=Flask(__name__)

app.secret_key="abc123"

#Mysql connection
app.config["MYSQL_HOST"]= "localhost"
app.config["MYSQL_USER"]= "root"
app.config["MYSQL_PASSWORD"]= "787889"
app.config["MYSQL_DB"]= "crud"
app.config["MYSQL_CURSORCLASS"]= "DictCursor"
mysql=MySQL(app)

#loading home page
@app.route('/')
def home():
    con=mysql.connection.cursor()
    sql="SELECT * FROM users"
    con.execute(sql)
    res=con.fetchall()
    con.close()

    return render_template("home.html",datas=res)

#New user
@app.route('/addusers',methods=['GET','POST'])
def addusers():
    if request.method=='POST':

        name=request.form['name']
        if name == "":
            flash("Enter Name.!")
            return redirect(url_for("addusers"))
        # Check if the name already exists in the database
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM users WHERE name=%s", (name,))
        user = con.fetchone()
        # print(user)
        con.close()
        if user:
            flash("Username already exists, give another name.!")
            return redirect(url_for("addusers"))  
          
        age=request.form['age']
        if not age.isnumeric(): 
            flash("Enter the Age in integer type!") 
            return redirect(url_for("addusers"))
        a = int(age)
        if a < 18:
            flash("Age must be greater than 18.!")
            return redirect(url_for("addusers"))
        
        city=request.form['city']
        if len(city)<3:
            flash("City needs atleast 3 characters.!")
            return redirect(url_for("addusers"))
        
        mobile=request.form['mobile']
        # print(type(mobile[0]))
        if mobile[0] not in ['9','8','7','6'] or len(mobile)!=10:
            flash("invalid mobile number.! \n Pls Check start with number 6789 and must 10 Digit")
            return redirect(url_for("addusers"))
        if not mobile.isnumeric(): 
            flash("Enter the mobile in integer type!") 
            return redirect(url_for("addusers"))
            
        con=mysql.connection.cursor()
        con.execute("SELECT * FROM users WHERE mobile=%s", (mobile,))
        mob = con.fetchone()
        if mob:
            flash("Usermob already exists, give another number.!")
            return redirect(url_for("addusers"))
        
        #email method correction
        email=request.form['email']
        pattern = r'([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        x=re.match(pattern,email)
        if not x:
            flash("invalid email id")
            return redirect(url_for("addusers"))
        
        con=mysql.connection.cursor()
        con.execute("select * from users where email=%s", (email,))
        em=con.fetchone()
        print(em)
        if em:
            flash("User email already exists, give another email.!")
            return redirect(url_for("addusers"))
    
        con=mysql.connection.cursor() #open the  connection
        sql="insert into users (NAME,CITY,AGE,Mobile,email) values (%s,%s,%s,%s,%s)"
        con.execute(sql,(name,city,age,mobile,email))
        mysql.connection.commit()
        con.close()
        flash('User Details  Added')
        return redirect(url_for("home"))
    
    return render_template("addusers.html")

#update User
@app.route("/editUser/<string:id>",methods=['GET','POST'])

def editUser(id):
    con=mysql.connection.cursor()  #open the connection
    if request.method=='POST':
        name=request.form['name']
        if name == "":
            flash("Enter Name.!")
            return redirect(url_for("editUser", id=id))
        
        con = mysql.connection.cursor()
        con.execute("SELECT * FROM users WHERE name=%s and id !=%s", (name, id))
        user = con.fetchone()
        # print(user)
        if user:
            flash("Username already exists, give another name.!")
            return redirect(url_for("editUser",id=id))

        age=request.form['age']
        if not age.isnumeric(): 
            flash("Enter the Age in integer type!") 
            return redirect(url_for("editUser",id=id))
        a = int(age)
        if a < 18:
            flash("Age must be greater than 18.!")
            return redirect(url_for("editUser",id=id))

        city=request.form['city']
        if len(city)<3:
            flash("City needs atleast 3 characters.!")
            return redirect(url_for("editUser",id=id))
        
        mobile=request.form['mobile']
        if not mobile.isnumeric():
            flash('Enter the mobile in integer type!')
            return redirect(url_for('editUser',id=id))
        if mobile[0] not in ['9','8','7','6'] or len(mobile)!=10:
            flash("invalid mobile number.! \n Pls Check start with number 6789 and must 10 Digit")
            return redirect(url_for("editUser",id=id))
        
        #Already exist Mobile
        con=mysql.connection.cursor()
        con.execute("SELECT * FROM users WHERE mobile = %s AND id != %s", (mobile, id))
        phone=con.fetchone()
        if phone:
            flash("UserMobile already exists, give another Mobile.!")
            return redirect(url_for("editUser",id=id))
       
        email=request.form['email']
        pattern = r'([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        x=re.match(pattern,email)
        if not x:
            flash("invalid email id")
            return redirect(url_for("editUser",id=id))
        
        #Already exits Email
        con=mysql.connection.cursor()
        con.execute("select * from users where email=%s and id!=%s",(email,id))
        em=con.fetchone()
        if em:
            flash("UserEmail already exists, give another Email.!")
            return redirect(url_for("editUser",id=id))


        sql="update users set NAME=%s,CITY=%s,AGE=%s,Mobile=%s,email=%s where ID=%s"
        con.execute(sql,(name,city,age,mobile,email,id))
        mysql.connection.commit()
        con.close()
        flash('User Details  Updated')
        return redirect(url_for("home"))
    
        
    con=mysql.connection.cursor()
    sql="select * from users where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    con.close()
    return render_template("editUser.html",datas=res)

#Delete User
@app.route("/deleteUser/<string:id>",methods=['GET','POST'])
def deleteUser(id):
    con=mysql.connection.cursor()
    sql="delete from users where ID=%s"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    flash('User Details Deleted')
    return redirect(url_for("home"))

#Login

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        session["name"]=request.form["name"]
        mobile = request.form['mobile']
        cur = mysql.connection.cursor()
        cur.execute("select * from users where name=%s and mobile=%s",(name,mobile))
        
        data = cur.fetchone()
        cur.close()
        if data:
            flash("login Successfully")
            return redirect(url_for('show_user_details',name=name,mobile=mobile))
        else:
            flash("User not found!")
            return redirect(url_for("login"))
    return render_template("login.html")

#show
@app.route("/show/<string:name>/<string:mobile>")

def show_user_details(name, mobile):
    if "name" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE name = %s AND mobile = %s", (name, mobile))
        user_data = cur.fetchone()
        cur.close()
        print(user_data)

        if user_data:
            return render_template("show.html", user=user_data)
    else:
        flash("Pls login...!!!")
        return redirect(url_for('login'))

#Logout    
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))   
 
    

if __name__=='__main__':
    
    app.run(debug=True)

