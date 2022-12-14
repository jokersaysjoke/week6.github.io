from flask import Flask, request, redirect, render_template, session
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="", #輸入密碼
    database="WEBSITE"
)


cursor = connection.cursor()

app=Flask(__name__, static_folder="static", static_url_path="/")

app.secret_key="99TSLA"

#首頁
@app.route("/")  
def homePage():
    return render_template("logIn.html")

#註冊
@app.route("/signUp", methods=['POST','GET'])
def signUp():
    if request.method=='GET':
        return redirect("/")
    else:
        userid = request.form['userid']
        username = request.form['username']
        userpassword = request.form['password']
        cursor.execute("SELECT * FROM MEMBER WHERE USERNAME=%s",(username,))
        record = cursor.fetchone()
        if record is None:
            cursor.execute("INSERT INTO MEMBER(name, username, password) VALUES (%s,%s,%s)",(userid,username,userpassword))
            connection.commit()
            return  redirect("/")
        else:
            return redirect("/error?message=帳號已經被註冊")

#登入
@app.route("/signIn", methods=['POST','GET'])
def signIn():
    if request.method=='POST':
       
        username=request.form['username']
        password=request.form['password']
        cursor.execute('SELECT * FROM MEMBER WHERE USERNAME=%s ',(username,))
        record = cursor.fetchone()
        if record:
            if password == record[3]:
                session['userid']=record[1]
                session['username']=username
                session['password']=password
                return redirect("/member")
            else: 
                return redirect("/error?message=密碼錯誤")
        else:
            return redirect("/error?message=查無此帳號")

    else:
        return redirect("/")

# #登出
@app.route("/signOut")
def signOut():
    session.pop("username",None)
    session.pop("password",None)
    return redirect("/")
#會員畫面
@app.route("/member")
def member():
    if "username" in session:
        message=session['userid']
        return render_template("member.html",message=message)
    else:
        return redirect("/")
#錯誤
@app.route("/error")
def error():
    message=request.args.get("message")
    return render_template("error.html",errorMessage=message)

app.run(port=3000)

