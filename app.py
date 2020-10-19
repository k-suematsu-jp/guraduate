from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from datetime import datetime
# splite3をimportする
# flaskをimportしてflaskを使えるようにする
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。

# appという名前でFlaskを使いますよ
app = Flask(__name__)
# secret key を設定
app.secret_key = "sunabaco"

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
    c.execute("insert into users values(null,?,?,?,?)",(name,password,nickname,site_name))
    # 変更を適用
    conn.commit()
    # 接続終了
    c.close()
    return redirect("/login")


# login状態でないと見れないページには、
# if "user_id" in session:
#        return 
#    else:
#        return 
# でその動作部分全体を囲ってあげる

@app.route("/user_page")
def greet():
    if "user_id" in session:
        user_id = session["user_id"][0]
        print(user_id)
        conn = sqlite3.connect("mappin_good.db")
        c = conn.cursor()
        c.execute("select nickname from users where user_id=?",(user_id,))
        nickname = c.fetchone()
        nickname = nickname[0]
        print(nickname)
        c.close()
        return render_template("/user_page.html",nickname = nickname)
    else:
        return render_template("login.html")

@app.route("/edit")
def edit():
    if "user_id" in session:
        user_id = session["user_id"][0]
        print(user_id)
        conn = sqlite3.connect("mappin_good.db")
        c = conn.cursor()
        c.execute("select * from users where user_id=?",(user_id,))
        name_edit = c.fetchone()
        print(name_edit)
        c.close()
        return render_template("edit.html",nickname = nickname)
    else:
        return render_template("login.html")


@app.route("/upload", methods=["POST"])
def do_upload():
    # bbs.tplのinputタグ name="upload" をgetしてくる
    upload = request.files["upload"]
    # uploadで取得したファイル名をlower()で全部小文字にして、ファイルの最後尾の拡張子が'.png', '.jpg', '.jpeg'ではない場合、returnさせる。
    if not upload.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return "png,jpg,jpeg形式のファイルを選択してください"
    # 下の def get_save_path()関数を使用して "./static/img/" パスを戻り値として取得する。
    save_path = get_save_path()
    # パスが取得できているか確認
    print(save_path)
    # ファイルネームをfilename変数に代入
    filename = upload.filename
    # 画像ファイルを./static/imgフォルダに保存。 os.path.join()は、パスとファイル名をつないで返してくれます。
    upload.save(os.path.join(save_path,filename))
    # ファイル名が取れることを確認、あとで使うよ
    print(filename)
    
    # アップロードしたユーザのIDを取得
    user_id = session["user_id"][0]
    comment = request.form.get("comment")
    conn = sqlite3.connect("mappin_good.db")
    c = conn.cursor()
    # update文
    print(user_id)
    # 上記の filename 変数ここで使うよ
    c.execute("insert into picture values(null,?,?,?,null,null,null,null,null)",(user_id,comment,filename))
    conn.commit()
    conn.close()

    return redirect ("/user_page")

#課題4の答えはここも
def get_save_path():
    path_dir = "static/img"
    return path_dir 

@app.route("/logout", methods=["GET"])
def logout():
    #セッションからユーザ名を取り除く (ログアウトの状態にする)
    session.pop("user_id", None)
    # ログインページにリダイレクトする
    return redirect("/")





if __name__ == "__main__":
    app.run(debug=True)
