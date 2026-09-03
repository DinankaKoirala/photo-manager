import os
from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from auth import get_service, list_accounts
from downloader import get_photos_list, download_file

app = Flask(__name__)
app.secret_key = "temp"

@app.route("/")
def index():
    accounts = list_accounts()
    return render_template("index.html", accounts=accounts)

@app.route("/login/<account_name>")
def login(account_name):
    get_service(account_name)
    return redirect(url_for("index"))

@app.route("/photos/<account_name>")
def photos(account_name):
    service,creds = get_service(account_name)
    photos_list = get_photos_list(service)
    session["photos"] = photos_list
    session["account"] = account_name
    session["current"] = 0

    return redirect(url_for("swipe"))

@app.route("/swipe")
def swipe():
    photos = session.get("photos" , [])
    current = session.get("current", 0)
    account = session.get("account", "")

    if current >= len(photos):
        return redirect(url_for("done"))

    photo = photos[current]
    return render_template("swipe.html", photo=photo, current=current, total=len(photos), account=account)

@app.route("/keep")
def keep():
    session["current"] = session.get("current", 0)+1
    return redirect(url_for("swipe"))

@app.route("/delete")
def delete():
    photos = session.get("photos",[])
    current = session.get("current", 0)

    deleted = session.get("deleted", [])
    deleted.append(photos[current])
    session["deleted"] = deleted

    session["current"] = current + 1
    return redirect(url_for("swipe"))

@app.route("/done")
def done():
    deleted = session.get("deleted", [])
    account = session.get("account", "")
    return render_template("done.html",deleted=deleted, account=account)

@app.route("/confirm_delete", methods=["POST"])
def confirm_delete():
    service, creds = get_service(session.get("account",""))
    deleted = session.get("deleted", [])

    for photo in deleted:
        service.files().delete(fileId=photo["id"]).execute()

    session.clear()
    return redirect(url_for("index"))

@app.route("/clear")
def clear():
    session.clear()
    return redirect(url_for("index"))    

if __name__ == "__main__":
    app.run(debug=True)