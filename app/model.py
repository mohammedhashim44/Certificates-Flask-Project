import os 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.event import listens_for

basedir = os.path.abspath(os.path.dirname(__file__))
static_path = os.path.join(basedir, 'static')
user_images_path = os.path.join(static_path, 'user_images')
certificates_path = os.path.join(static_path, 'certificates')

db = SQLAlchemy()

def thumbgen_filename(filename):
    name, ext = os.path.splitext(filename)
    return '%s_thumb%s' % (name, ext)


# User table
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(64) , unique=True,nullable=False)
    password = db.Column(db.String(64),nullable=False)
    username = db.Column(db.String(64), unique=True,nullable=False)
    full_name = db.Column(db.String(70),nullable=False)
    image = db.Column(db.Unicode(),nullable=True)

# This is what happends after deleteing user record
@listens_for(User, 'after_delete')
def del_user(mapper, connection, target):
    # if the user has image , delete it
    if target.image:
        try:
            os.remove(os.path.join(user_images_path, target.image))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass
    
    # delete any certificates belong to this user 
    db.session.begin_nested()
    certificates = Certificate.query.filter(Certificate.user_id==1)

    # delete certificates image and the thumnails of it 
    for certif_ in certificates:
        try:  
            os.remove(os.path.join(certificates_path, certif_.image))
            os.remove(os.path.join(certificates_path, thumbgen_filename(certif_.image)))
        except OSError:
            pass
    try : 
        # delete certificates records 
        Certificate.query.filter(Certificate.user_id==1).delete()
        db.session.commit()
    except Exception:
        pass

# Certificate table 
class Certificate(db.Model):
    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    name = db.Column(db.String(),nullable=False) 
    about = db.Column(db.String(),nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)
    image = db.Column(db.Unicode(),nullable=False)

# This is what happends after deleteing certificate record
# delete certificate image and thumbnail 
@listens_for(Certificate, 'after_delete')
def del_certificate(mapper, connection, target):
    if target.image:
        try:
            os.remove(os.path.join(certificates_path, target.image))
            os.remove(os.path.join(certificates_path, thumbgen_filename(target.image)))

        except OSError:
            # Don't care if was not deleted because it does not exist
            pass
 