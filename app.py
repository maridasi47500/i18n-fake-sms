from flask import Flask, render_template, request
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
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
@app.route("/add_one_sms", methods=["GET","POST"])
def add_one_sms():

    if request.method == 'POST':

        the_username = "anonyme"
        one_user = query_db("insert into sms (from,to,content,datetime,place_id) values (:from,:to,:content,:datetime,:place_id)",request.form)
        user = query_db('select * from sms')
        return render_template("smsform.html", smss=user, one_user=one_user, the_title="add new sms")
    user = query_db('select * from sms')
    one_user = query_db("select * from sms limit 1", one=True)
    return render_template("smsform.html", smss=user, one_user=one_user, the_title="add new sms")

@app.route("/add_one_place", methods=["GET","POST"])
def add_one_place():

    if request.method == 'POST':

        the_username = "anonyme"
        one_user = query_db("insert into place (name,lat,lon) values (:name,:lat,:lon)",request.form)
        user = query_db('select * from place')
        return render_template("placeform.html", places=user, one_user=one_user, the_title="add new place")
    user = query_db('select * from place')
    one_user = query_db("select * from place limit 1", one=True)
    return render_template("placeform.html", places=user, one_user=one_user, the_title="add new place")

