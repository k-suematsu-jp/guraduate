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


if __name__ == "__main__":
    app.run(debug=True)
