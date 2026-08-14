from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_language", methods=["GET","POST"])
def add_one_language():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into language (name,shortname) values (:name,:shortname)",hey)
        user = query_db('select * from language')

        return render_template("languageform.html", languages=user, one_user=one_user, the_title="add new language")


    user = query_db('select * from language')
    one_user = query_db("select * from language limit 1", one=True)
    return render_template("languageform.html", languages=user, one_user=one_user, the_title="add new language")

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,phone,country_id,email) values (:username,:phone,:country_id,:email)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','phone','country_id','email']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','phone','country_id','email']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','phone','country_id','email']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_place", methods=["GET","POST"])
def add_one_place():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into place (name,lat,lon) values (:name,:lat,:lon)",hey)
        user = query_db('select * from place')

        return render_template("placeform.html", places=user, one_user=one_user, the_title="add new place")


    user = query_db('select * from place')
    one_user = query_db("select * from place limit 1", one=True)
    return render_template("placeform.html", places=user, one_user=one_user, the_title="add new place")

@app.route("/add_one_postcard", methods=["GET","POST"])
def add_one_postcard():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        touslesplace= query_db("select * from place")

        touslesuser= query_db("select * from user")

        tousleslanguage= query_db("select * from language")

        one_user = query_db("insert into postcard (place_id,pic,recipient,message,user_id,language_id) values (:place_id,:pic,:recipient,:message,:user_id,:language_id)",hey)
        user = query_db('select * from postcard')

        return render_template("postcardform.html", postcards=user, one_user=one_user, the_title="add new postcard", touslesplace=touslesplace, touslesuser=touslesuser, tousleslanguage=tousleslanguage)


    touslesplace= query_db("select * from place")

    touslesuser= query_db("select * from user")

    tousleslanguage= query_db("select * from language")

    user = query_db('select * from postcard')
    one_user = query_db("select * from postcard limit 1", one=True)
    return render_template("postcardform.html", postcards=user, one_user=one_user, the_title="add new postcard", touslesplace=touslesplace, touslesuser=touslesuser, tousleslanguage=tousleslanguage)

@app.route("/add_one_letter", methods=["GET","POST"])
def add_one_letter():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        tousleslanguage= query_db("select * from language")

        touslesuser= query_db("select * from user")

        one_user = query_db("insert into letter (recipient,language_id,user_id,message) values (:recipient,:language_id,:user_id,:message)",hey)
        user = query_db('select * from letter')

        return render_template("letterform.html", letters=user, one_user=one_user, the_title="add new letter", tousleslanguage=tousleslanguage, touslesuser=touslesuser)


    tousleslanguage= query_db("select * from language")

    touslesuser= query_db("select * from user")

    user = query_db('select * from letter')
    one_user = query_db("select * from letter limit 1", one=True)
    return render_template("letterform.html", letters=user, one_user=one_user, the_title="add new letter", tousleslanguage=tousleslanguage, touslesuser=touslesuser)

@app.route("/add_one_email", methods=["GET","POST"])
def add_one_email():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        tousleslanguage= query_db("select * from language")

        one_user = query_db("insert into email (recipient,user_id,subject,body,language_id) values (:recipient,:user_id,:subject,:body,:language_id)",hey)
        user = query_db('select * from email')

        return render_template("emailform.html", emails=user, one_user=one_user, the_title="add new email", touslesuser=touslesuser, tousleslanguage=tousleslanguage)


    touslesuser= query_db("select * from user")

    tousleslanguage= query_db("select * from language")

    user = query_db('select * from email')
    one_user = query_db("select * from email limit 1", one=True)
    return render_template("emailform.html", emails=user, one_user=one_user, the_title="add new email", touslesuser=touslesuser, tousleslanguage=tousleslanguage)

@app.route("/add_one_sms", methods=["GET","POST"])
def add_one_sms():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        tousleslanguage= query_db("select * from language")

        touslesuser= query_db("select * from user")

        one_user = query_db("insert into sms (recipient,language_id,user_id,message) values (:recipient,:language_id,:user_id,:message)",hey)
        user = query_db('select * from sms')

        return render_template("smsform.html", smss=user, one_user=one_user, the_title="add new sms", tousleslanguage=tousleslanguage, touslesuser=touslesuser)


    tousleslanguage= query_db("select * from language")

    touslesuser= query_db("select * from user")

    user = query_db('select * from sms')
    one_user = query_db("select * from sms limit 1", one=True)
    return render_template("smsform.html", smss=user, one_user=one_user, the_title="add new sms", tousleslanguage=tousleslanguage, touslesuser=touslesuser)

@app.route("/add_one_calendar_entry", methods=["GET","POST"])
def add_one_calendar_entry():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        tousleslanguage= query_db("select * from language")

        touslesplace= query_db("select * from place")

        one_user = query_db("insert into calendar_entry (date,user_id:reference,title,description,time,language_id,place_id) values (:date,:user_id:reference,:title,:description,:time,:language_id,:place_id)",hey)
        user = query_db('select * from calendar_entry')

        return render_template("calendar_entryform.html", calendar_entrys=user, one_user=one_user, the_title="add new calendar_entry", tousleslanguage=tousleslanguage, touslesplace=touslesplace)


    tousleslanguage= query_db("select * from language")

    touslesplace= query_db("select * from place")

    user = query_db('select * from calendar_entry')
    one_user = query_db("select * from calendar_entry limit 1", one=True)
    return render_template("calendar_entryform.html", calendar_entrys=user, one_user=one_user, the_title="add new calendar_entry", tousleslanguage=tousleslanguage, touslesplace=touslesplace)

