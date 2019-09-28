#!/usr/bin/env python

from flask import Flask, render_template, request
from process import val
app = Flask(_name_)

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        image = request.files['image_file']
        print("================================================================"+image.filename)
        
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/lock")
def lock():
    return render_template("lock.html")

@app.route("/recovery")
def recovery():
    return render_template("password-recovery.html")
@app.route("/insert")
def insert():
    json_format = val(img_link)
@app.route("/check")
def check():   
    #DB * QUERY  
    #dist = np.sum(np.square(f1-f2))
    json_format = val(TEST_IMG)

app.run()