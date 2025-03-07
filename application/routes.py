from application import app, db
from flask import render_template,request,Response,json,redirect,flash,url_for
from application.models import Course, Enrollment,User
from application.forms import LoginForm, RegisterForm
courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html",index = True )

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data

        user = User.objects(email=email).first()
        if user and password == user.password:
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/course")
@app.route("/course/<term>")
def course(term="Spring 2020"):
    return render_template("course.html",courseData = courseData , course = True, term = term)

@app.route("/register",methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id  = User.objects.count()
        user_id  += 1
        email       = form.email.data
        password    = form.password.data 
        first_name  = form.first_name.data
        last_name   = form.last_name.data
      
        user = User(user_id = user_id, email = email, first_name = first_name, last_name = last_name)
        # user.check_password_hash(password)
        # user.save()
        print("..................---------------------------------")
        print("..................",user_id)
        print("..................",form.email.data)
        print("..................",form.password.data )
        print("..................",form.first_name.data)
        print("..................",form.last_name.data)
        flash("You are successfully registered","Successfull")
        return redirect(url_for('index'))
    return render_template("register.html",title="Register", register = True, form=form) 

@app.route("/enrollment",methods = ['GET','POST'])
def enrollment():
    id = request.form.get('courseID')
    title = request.form.get('title')
    term = request.form.get('term')
    return render_template("enrollment.html", enrollment = True, data = {"id":id, "title":title, "term":term})  

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]

    return Response(json.dumps(jdata), mimetype="application/json")        


@app.route("/user")
def user():
   # User(user_id=1, first_name="Christian", last_name="Hur", email="christian@uta.com", password="abc1234").save()
    #User(user_id=2, first_name="Mary", last_name="Jane", email="mary.jane@uta.com", password="password123").save()
    users = User.objects.all()
    print("users-----------456y---",users)
    return render_template("user.html", users=users)    