from flask import Flask,render_template,redirect,url_for,request,flash
from login import Login,RegisterForm,ContactForm,Reminder,Showrem,Modifyremd,Modifyrems,Modifyremn,IDform
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_login import LoginManager,UserMixin,login_user,logout_user
from flask_login import current_user,login_required
from flask_mail import Message, Mail



app = Flask(__name__)


app.secret_key = 'development key'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'blackhatal@gmail.com'
app.config["MAIL_PASSWORD"] = 'LpJt2HK4@&Evgl'
#app.config.from_pyfile('config.cfg')

mail = Mail(app)


app = Flask(__name__)
app.secret_key = 'development key'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
login_manager.login_view='login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"




class Reminderdb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date= db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120),nullable=True)
    name = db.Column(db.String(120), nullable=False)
    discript = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    sms= db.Column(db.Integer, nullable=False)
    rmn = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"







@app.route("/register",methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('success'))
    form= RegisterForm()
    if form.validate_on_submit():
        hpass = bcrypt.generate_password_hash(form.pswd.data).decode('utf-8')
        user= User(username=form.username.data,email=form.email.data,password=hpass)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return render_template('registerfail.html')
        return redirect(url_for('login'))
    return render_template("register.html",title="register",form=form)


@app.route("/")
def home():
    return redirect(url_for('login'))





@app.route('/mail')
@login_required
def Mail():
      posts = Reminderdb.query.filter_by(date=datetime.now()).first()
      msg = Message("remindermail",sender='reminder@gmail.com')
     # msg.recipients= posts.email
      msg.body="{}{}{}.format(posts.subject,posts.discript)"
      mail.send(msg)

      return 'Form posted.'










@app.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('success'))
    form= Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if  user and bcrypt.check_password_hash(user.password,form.pswd.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('success',name=form.email.data.split('@')[0]))
        else:
            return redirect(url_for('fail'))
    return render_template("login.html",title="register",form=form)





@app.route("/showrem1",methods=['POST','GET'])
@login_required
def show():            #getdate():
    form= Showrem()
    if form.validate_on_submit():
            allrems =Reminderdb.query.filter(Reminderdb.date >= form.sdate.data).filter(Reminderdb.date <= form.ldate.data).filter(Reminderdb.subject == form.subject.data)
            return render_template('selectdate.html',title="New Reminder",form=form,posts=allrems)
    allrems = Reminderdb.query.all()
    return render_template('selectdate.html',title="New Reminder",form=form,posts=allrems)





@app.route("/modify",methods=['POST','GET'])
@login_required
def modify():
        form = Modifyremd()
        if form.validate_on_submit():
            posts =Reminderdb.query.filter_by(date=form.date.data)
            return render_template('modify.html',posts=posts,form=form)
        return render_template('modify.html',title="Modify Reminder",form=form)#,posts=rems)


@app.route("/modifynow",methods=['POST','GET'])
@login_required
def modifynow():
    form= Reminder()
    form.id.data=134
    if form.validate_on_submit():
        tomodity =Reminderdb.query.filter(Reminderdb.date== form.date.data).filter(Reminderdb.subject == form.subject.data).filter(Reminderdb.name == form.name.data).first()
        tomodity.discript=form.discript.data
        tomodity.email=form.email.data
        tomodity.contact=form.contact.data
        tomodity.sms=form.sms.data
        tomodity.rmn=form.recur.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('modify2.html',title="Modify Reminder",form=form)





@app.route("/disable",methods=['POST','GET'])
@login_required
def disable():
        form = Modifyremd()
        if form.validate_on_submit():
            posts =Reminderdb.query.filter_by(date=form.date.data)
            return render_template('disable.html',posts=posts,form=form)
        return render_template('disable.html',title="Disable Reminder",form=form)#,posts=rems)

@app.route("/disablenow",methods=['POST','GET'])
@login_required
def disablenow():
    form= IDform()
    if form.validate_on_submit():
         posts =Reminderdb.query.filter_by(id=form.id.data).first()
         posts.status="Disable"
         db.session.commit()
         return redirect(url_for('success'))
    return render_template('disablenow.html',title="Modify Reminder",form=form)


@app.route("/enable",methods=['POST','GET'])
@login_required
def enable():
        form = Modifyremd()
        if form.validate_on_submit():
            posts =Reminderdb.query.filter_by(date=form.date.data)
            return render_template('enable.html',posts=posts,form=form)
        return render_template('enable.html',title="Disable Reminder",form=form)#,posts=rems)

@app.route("/enablenow",methods=['POST','GET'])
@login_required
def enablenow():
    form= IDform()
    if form.validate_on_submit():
         posts =Reminderdb.query.filter_by(id=form.id.data).first()
         posts.status="enabled"
         db.session.commit()
         return redirect(url_for('success'))
    return render_template('enablenow.html',title="Modify Reminder",form=form)




@app.route("/delete",methods=['POST','GET'])
@login_required
def delete():
        form = Modifyremd()
        if form.validate_on_submit():
            posts =Reminderdb.query.filter_by(date=form.date.data)
            return render_template('delete.html',posts=posts,form=form)
        return render_template('delete.html',title="Disable Reminder",form=form)#,posts=rems)

@app.route("/deletenow",methods=['POST','GET'])
@login_required
def deletenow():
    form= IDform()
    if form.validate_on_submit():
         posts =Reminderdb.query.filter_by(id=form.id.data).first()
         db.session.delete(posts)
         db.session.commit()
         return redirect(url_for('success'))
    return render_template('deletenow.html',title="Modify Reminder",form=form)


@app.route("/fail")
def fail():
             return render_template('loginfail.html')

@app.route("/logout")
def logout():
             logout_user()
             return render_template("logout.html")

@app.route("/success")
@login_required
def success():
          return render_template("home.html",time=datetime.now())


@app.route('/showrem/<form>')
def showrem(form):
    return render_template('showrem.html',posts=allrems)


@app.route("/account")
def account():
    return render_template('account.html',title='account')


@app.route('/newreminder', methods = ['GET', 'POST'])
@login_required
def rem():
    form = Reminder()
    form.id.data=123
    if form.validate_on_submit():
         remind = Reminderdb(name=form.name.data,date=form.date.data,email=form.email.data,subject=form.subject.data,discript=form.discript.data,contact=form.contact.data,sms=form.sms.data,rmn=form.recur.data,user_id=56)
         db.session.add(remind)
         db.session.commit()
         return redirect(url_for('success'))
    return render_template('remcreated.html',title="New Reminder",form=form)





if __name__=='__main__':
    app.run(host="localhost",port=5000,debug=True)
