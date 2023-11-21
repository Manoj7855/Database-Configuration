from flask import Flask, render_template,url_for,request,redirect,flash

from flask_mysqldb import MySQL

app=Flask(__name__)
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
        age=request.form['age']
        city=request.form['city']
        con=mysql.connection.cursor() #open the  connection
        sql="insert into users (NAME,CITY,AGE) values (%s,%s,%s)"
        con.execute(sql,(name,city,age))
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
        city=request.form['city']
        age=request.form['age']
        sql="update users set NAME=%s,CITY=%s,AGE=%s where ID=%s"
        con.execute(sql,(name,city,age,id))
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

if __name__=='__main__':
    app.secret_key="abc123"
    app.run(debug=True)

