import os
from flask import Flask, render_template, redirect, url_for, session, jsonify, request
from auth import get_credentials, list_accounts
from downloader import get_photos_list, download_file

app = Flask(__name__)
app.secret_key = "temp"
photos_store = {}

@app.route("/")
def index():
    accounts = list_accounts()
    return render_template("index.html", accounts=accounts)

@app.route("/login/<account_name>")
def login(account_name):
    get_credentials(account_name)
    return redirect(url_for("index"))

@app.route("/photos/<account_name>")
def photos(account_name):
    creds = get_credentials(account_name)
    photos_list = get_photos_list(creds)

    photos_store[account_name] = photos_list

    session["account"] = account_name
    session["current"] = 0
    session["downloaded"] = []

    return redirect(url_for("swipe"))

@app.route("/swipe")
def swipe():
    current = session.get("current", 0)
    account = session.get("account", "")
    photos = photos_store.get(account, [])

    if current >= len(photos):
        return redirect(url_for("done"))

    photo = photos[current]
    return render_template("swipe.html", photo=photo, current=current, total=len(photos), account=account)

@app.route("/keep")
def keep():
    account = session.get("account", "")
    current = session.get("current", 0)
    photos = photos_store.get(account, [])

    photo = photos[current]
    creds = get_credentials(account)
    download_file(creds, photo["baseUrl"], photo["filename"])

    downloaded = session.get("downloaded", [])
    downloaded.append(photo["filename"])
    session["downloaded"] = downloaded
    session["current"] = current + 1
    return redirect(url_for("swipe"))

@app.route("/skip")
def skip():
    session["current"] = session.get("current", 0) + 1
    return redirect(url_for("swipe"))

@app.route("/done")
def done():
    downloaded = session.get("downloaded", [])
    account = session.get("account", "")
    return render_template("done.html", downloaded=downloaded, account=account) 

@app.route("/clear")
def clear():
    session.clear()
    return redirect(url_for("index"))    

if __name__ == "__main__":
    app.run(debug=True)