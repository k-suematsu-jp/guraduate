from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from datetime import datetime
# splite3をimportする
# flaskをimportしてflaskを使えるようにする
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。


app = Flask(__name__)


@app.route("/")
def top_picture():
    # dbtest.dbに接続
    conn = sqlite3.connect("mappin_good.db")
    # データベースの中身が見えるようにする
    c = conn.cursor()
    # sqlを実行する
    c.execute("select picture,comment from picture where picture_id =1")
    # fetchoneはタプル型
    top_img = c.fetchone()
    print(top_img)
    # 接続終了
    c.close()
    # 接続終了
    return render_template("index.html", top_img=top_img)


@app.route("/login",methods=["GET"])
def login_get():
    if "user_id" in session:
        return redirect("/user_page")
    else:
        return render_template("login.html")

@app.route("/login",methods=["POST"])
def login_post():
    # 入力フォームから値を取得
    name = request.form.get("name")
    password = request.form.get("password")
    # dbtest.dbに接続
    conn = sqlite3.connect("mappin_good.db")
    # データベースの中身が見れるようにする
    c = conn.cursor()
    # SQL文を実行する
    c.execute("select user_id from users where username=? and password=?",(name,password))

    user_id = c.fetchone()
    #IDが取得できているのかの確認
    print(user_id)
    # 接続終了
    c.close()

    if user_id is None:
        return redirect("/login")
    else:
        session["user_id"] = user_id
        return redirect("/user_page")


@app.route("/register",methods=["GET"])
def regist_get():
    if "user_id" in session:
        return redirect("/user_page")
    else:
        return render_template("register.html")


@app.route("/register",methods=["POST"])
def regist_post():
    # 入力フォームから値を取得
    name = request.form.get("name")
    password = request.form.get("password")
    site_name = request.form.get("site_name")
    nickname = request.form.get("nickname")
    # dbtest.dbに接続
    conn = sqlite3.connect("mappin_good.db")
    # データベースの中身が見れるようにする
    c = conn.cursor()
    # SQL文を実行する
    c.execute("insert into users values(null,?,?,?,?)",(name,password,site_name,nickname))
    # 変更を適用
    conn.commit()
    # 接続終了
    c.close()
    return redirect("/user_page/<nickname>")


@app.route("/user_page/<nickname>")
def greet(nickname):
    return nickname + "さん　のページ"





if __name__ == "__main__":
    app.run(debug=True)
