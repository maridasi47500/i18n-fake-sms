# -*- coding: utf-8 -*-

import sys
import os
print(sys.argv[1])


filename=sys.argv[1].lower()
myclass=(filename).capitalize()
modelname=(filename).capitalize()
marouteget="\"/%s\"" % filename
maroutenew="\"/%s_new\"" % filename
maroutecreate="\"/%s_create\"" % filename
marouteget2="\\\"/%s\\\"" % filename
myhtml="my"+filename+"html"
myfavdirectory=filename
index = 2 
createtable=""
columns="("
formhtml="<form method=\"POST\">"
values="("
myparam=","
items=sys.argv
while index < (len(items)):

    try:
      print(index, items[index])
      paramname=items[index]
      print(items[(index+1)])
    except:
      myparam=""
    index += 1
    formhtml+="<div class=\"field\"><label>{paramname}</label><input name=\"{paramname}\"/></div>".format(myparam=myparam,paramname=paramname)
    columns+="{paramname}{myparam}".format(myparam=myparam,paramname=paramname)
    values+=":{paramname}{myparam}".format(myparam=myparam,paramname=paramname)
    createtable+="""        {paramname} text{myparam}
    """.format(myparam=myparam,paramname=paramname)
columns+=")"
values+=")"
mystr="""create table if not exists {filename}(
        id integer primary key autoincrement,
"""
mystr+=createtable

mystr+="""                );
"""
selectall= "select * from {filename}"

delete="""delete from {filename} where id = ?",(myid,)"""
selectone="""select * from {filename} where id = ?",(myid,)"""
addone="""@app.route("/add_one_{filename}", methods=["GET","POST"])
def add_one_{filename}():

    if request.method == 'POST':

        the_username = "anonyme"
        one_user = query_db("insert into {filename} {columns} values {values}",request.form)
        user = query_db('select * from {filename}')
        return render_template("{filename}form.html", {filename}s=user, one_user=one_user, the_title="add new {filename}")
    user = query_db('select * from {filename}')
    one_user = query_db("select * from {filename} limit 1", one=True)
    return render_template("{filename}form.html", {filename}s=user, one_user=one_user, the_title="add new {filename}")

"""


with open("app.py", "a") as myfile:
    myfile.write(addone.format(filename=filename,columns=columns,values=values))
with open("schema.sql", "a") as myfile:
    myfile.write(mystr.format(filename=filename))
with open("templates/hey.html", "a") as myfile:
    myfile.write("<a href=\"/add_one_{filename}\"> add one {filename}</a>".format(filename=filename))


with open("templates/"+filename+"form.html", "w") as myfile:
    myfile.write("{% extends 'base.html' %}{% block content %}"+formhtml.format(filename=filename)+"<div class=\"actions\"><input type=\"submit\"/></div></form>" + "{% for x in "+filename+"s %}{{"+ "x[\""+items[2]+"\"] }}{% endfor %}"+"{% endblock %}{% block liens %}<a href=\"/\">bienvenue</a>"+"<a href=\"/add_one_{filename}\"> add one {filename}</a>".format(filename=filename)+"{% endblock %}")



