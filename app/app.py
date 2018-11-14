import os
from flask import Flask, url_for, request,  flash ,render_template , session , redirect , send_file 
from flask_admin import Admin 
from DatabaseHelper import DatabaseHelper 
import model 
from model import db as database
import myAdmin
from flask_uploads import UploadSet , IMAGES , configure_uploads

### Define variables and pathes

basedir = os.path.abspath(os.path.dirname(__file__))
static_path = os.path.join(basedir, 'static')
user_images_path = os.path.join(static_path, 'user_images')
certificates_path = os.path.join(static_path, 'certificates')
database_path = os.path.join(basedir, 'my-database.sqlite')

# initiate flask app 
app = Flask(__name__,)

# change the secret key
app.secret_key = "secret key"
app.config['SECRET_KEY'] = 'my secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# helper object for sqlalchemy
helper = DatabaseHelper()

# configure uploads for uploading profile images 
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = user_images_path 
configure_uploads(app, photos)


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html",session=session) 


@app.route('/login' , methods=['GET' , 'POST'])
def login():
    if request.method == 'POST' :
        email = request.form["email"] 
        password = request.form["password"]

        if not (email and password ):
            flash("Fill all the fileds!")
            return redirect(url_for("home"))

        data = helper.getUserData(email,password)
        if  data == -1 :
            flash("Email or password incorrect .")
            return redirect(url_for("home"))
        else:
            session["image"] = data["image"]
            session["username"] = data["username"]
            session["id"] = data["id"]
            return redirect(url_for("profile"))
    else :
        return redirect(url_for("home"))

@app.route('/sign_up' , methods=['GET' , 'POST'])
def sign_up():

    # when entreing sign up data 
    if request.method == 'POST' :
        full_name = request.form["full_name"] 
        password =  request.form["password"] 
        re_password = request.form["re_password"]
        email = request.form["email"]
        username = request.form["username"]

        if not (full_name and password and re_password and email and username):
            flash("Fill all the fileds!")
            return redirect(url_for("home"))

        if password != re_password : 
            flash("Passwords not match")
            return redirect(url_for("home"))
     
        data = helper.insertIntoUsers((full_name , username , email  ,password))
        if data == -1 : 
            flash("Username or email already taken !")
            return redirect(url_for("home"))
        else:
            flash("Sign up done !")
            return redirect(url_for('home'))

    else :
        return redirect(url_for("home")) 
    
@app.route('/profile',methods=['GET' , 'POST'])
def profile():
    # if the user is not logged , he will return to home page
    if not "id" in session :
        flash("You have to log in first !")
        return redirect(url_for("home"))

    # when upload image
    if request.method == "POST" : 
        image = request.files["image"]
        image_name = image.filename
        image_name = ('ID-%s-%s' % (session["id"],image_name))
        image_name = photos.save(request.files['image'],name=image_name )
        
        if image_name : # delete the old image and replace it with the new one 
            user= model.User.query.filter_by(id=session["id"]).first()
            if user.image : 
                try:
                    os.remove(os.path.join(user_images_path, user.image))
                except Exception :
                    pass 
            
            try:
                user.image = image_name 
                user= model.User.query.filter_by(id=session["id"]).first()
                database.session.commit()
                session["image"] = image_name 
            except Exception :
                return "ERROR"
                pass 

    # get all certificaetes to this user
    certificates = model.Certificate.query.filter(model.Certificate.user_id==session["id"])
    n = certificates.count() 
 
    # the user image  
    image = None 
    if session["image"] == None :
        image = 'no_image.jpg'
    else:
        image = session["image"] 

    return render_template("profile.html",username=session["username"],
                                        image=image ,
                                    n=n, 
                                    certificates=certificates)


def send_image(path , filename):
    filename = os.path.join(path, filename)
    return send_file(filename , mimetype='image/gif')

@app.route('/user_images/<path:filename>')
def user_images(filename):
    # if the image is "no_image" the user can see it 
    # and if the admin is logged , he can see any image 
    if "admin" in session or filename == "no_image.jpg" :
        return send_image(user_images_path , filename)
    
    # if the user is not loged in , he can't view any images 
    if not "id" in session :
        return "You don't have permission" 
    # to authorize the user , each image have a prefix conatins user id that the image belong to 
    # for example "img.jpg" becomes "ID-1-img.jpg" for the user with id "1" 
    # if anyone wants to see it , we comapare his ID whit the ID in the image , if there is a match he can see it , 
    # else , he has no premission 
    authorized = False
    s = "ID-"+ str(session["id"]) 
    if filename[0:len(s)] == s :
        authorized = True
    if authorized :
        return send_image(user_images_path , filename)
    else :
        return "You don't have permission"


@app.route('/certificates/<path:filename>')
def certificates(filename):
    # the same as before 
    if "admin" in session :
        return send_image(certificates_path,filename)

    if not "id" in session : 
        return "You don't have permission"
    
    authorized = False
    s = "ID-"+ str(session["id"]) 
    if filename[0:len(s)] == s :
        authorized = True
    if authorized :
        return send_image(certificates_path,filename)
    else :
        return "You don't have permission"



@app.route('/logout' , methods=['GET' , 'POST'])
def logout():
    if "username" in session : 
        session.pop("id",None)
        session.pop("username" , None)
        session.pop("image",None)
    return redirect(url_for('home'))

# admin login 
@app.route('/dashboard_login',methods=['GET' , 'POST'])
def dashboard_login():
    if request.method == 'POST':
        email = request.form["email"] 
        password = request.form["password"]
        if not ( email == "admin@admin.com" and password == "admin" ) :
            flash ("Admin email or password incorrect")
            return redirect(url_for('dashboard_login'))
        else : 
            session["admin"] = True 
            return redirect(url_for("admin.index"))
    return render_template("dashboard_login.html")


@app.route('/admin_logout')
def admin_logout():
    if "admin" in session :
        session.pop("admin",None) 
    return redirect(url_for('dashboard_login'))

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found"

# Delete database and create new one
def build_sample_db(database):
    database.drop_all()
    database.create_all()
    database.session.commit()


if __name__ == '__main__':

    database.app=app
    database.init_app(app)
    
    admin = Admin(app,index_view=myAdmin.MyHomeView())
    admin.add_view(myAdmin.UserView(model.User,database.session))
    admin.add_view(myAdmin.CertificateView(model.Certificate,database.session))
    admin.add_link(myAdmin.MenuLink(name='Logout', category='', url='/admin_logout'))

    # if the database not exists 
    if not os.path.exists(database_path)  :
        build_sample_db(database)
        usernames = [
            {"username":"davis","email":"test11@test.com","password":"test","full_name":"Davis Backer"}, 
            {"username":"irwin","email":"test22@test.com","password":"test","full_name":"Irwin Smith"}]
        for u in usernames:
            user = model.User()
            user.username = u["username"]
            user.email = u["email"]
            user.password = u["password"]
            user.full_name = u["full_name"]
            database.session.add(user)
            database.session.commit()
        
    app.run(debug=True)

    
