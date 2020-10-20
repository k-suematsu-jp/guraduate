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
    # print(top_img)

    c.execute("select picture,comment from picture order by time desc ")
    new_imgs = c.fetchmany(size=4)

    # print(new_imgs)

    c.execute("select site_name from site")
    site_name = c.fetchall()

    # 接続終了
    c.close()
    # 接続終了
    return render_template("index.html", top_img=top_img, new_imgs=new_imgs, site_name=site_name)


@app.route('/junru/<string:junru>')
def brows(junru):
    conn = sqlite3.connect('mappin_good.db')
    c = conn.cursor()
    print(junru)
    c.execute(
        "select * from picture where junru_name = ? order by time desc", (junru,))
    brows_list = []
    for row in c.fetchall():
        brows_list.append({"picture_id": row[0], "user_id": row[1], "comment": row[2], "picture": row[3],
                           "time": row[4], "location_no": row[5], "good_count": row[6], "site_name": row[7], "junru_name": row[8], })
    c.close()
    print(brows_list)
    return render_template("browsing_junru.html", junru=junru, brows_list=brows_list)


@app.route('/kouku/<string:kouku>')
def brows_kouku(kouku):
    conn = sqlite3.connect('mappin_good.db')
    c = conn.cursor()
    print(kouku)
    c.execute(
        "select * from picture where site_name = ? order by time desc", (kouku,))
    brows_list = []
    for row in c.fetchall():
        brows_list.append({"picture_id": row[0], "user_id": row[1], "comment": row[2], "picture": row[3],
                           "time": row[4], "location_no": row[5], "good_count": row[6], "site_name": row[7], "junru_name": row[8], })
    c.close()
    print(brows_list)
    return render_template("browsing_kouku.html", kouku=kouku, brows_list=brows_list)

@app.route('/personal_page/<string:name>')
def brows_person(name):
    conn = sqlite3.connect('mappin_good.db')
    c = conn.cursor()
    print(name)
    c.execute(
        "select * from picture where user_id = ? order by time desc", (name,))
    brows_list = []
    for row in c.fetchall():
        brows_list.append({"picture_id": row[0], "user_id": row[1], "comment": row[2], "picture": row[3],
                           "time": row[4], "location_no": row[5], "good_count": row[6], "site_name": row[7], "junru_name": row[8], })
    
    c.execute("select nickname,site_name from users where username = ? ", (name,))
    profile=c.fetchall()
    c.close()
    print(profile)
    return render_template("personal_page.html", name=name, brows_list=brows_list, profile=profile)

@app.route('/picture/<int:picture_id>')
def picture(picture_id):
    conn = sqlite3.connect('mappin_good.db')
    c = conn.cursor()
    print(picture_id)
    c.execute("select * from picture where picture_id = ? ", (picture_id,))
    img_profile=c.fetchall()

    c.execute("select nickname,site_name from users where username = ? ", (img_profile[0][1],))
    name=c.fetchall()
    c.close()
    return render_template("picture.html", img_profile=img_profile,name=name)


if __name__ == "__main__":
    app.run(debug=True)
