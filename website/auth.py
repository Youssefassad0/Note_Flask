from flask import Blueprint,render_template,request,flash

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('login')
        password = request.form.get('password')
    return render_template("login.html")
@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('login')
        name = request.form.get('name')
        role = request.form.get('role')
        password = request.form.get('password')
        if len(email) <=4:
            flash('Login Must be greater than 4 caratcters .',category='error')
        elif len(name) <=2:
            pass
        elif len(password) <=6:
            pass
        elif role =="":
            pass
        else:
            # add user to database
            pass
    return render_template("signup.html")

@auth.route('/Logout')
def logout():
    return 'logout'