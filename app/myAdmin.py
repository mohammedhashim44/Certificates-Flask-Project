import os

from flask import  redirect , url_for , render_template

from flask_admin import   expose ,form , AdminIndexView  
from flask_admin.contrib.sqla import ModelView , fields 
from flask_admin.menu import MenuLink 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import ForeignKey  

from wtforms import  validators
from wtforms.fields import  PasswordField 
from sqlalchemy.event import listens_for
from flask_admin.form import Select2Widget 
from jinja2 import Markup

from app import session , user_images_path , certificates_path , static_path
import model

# the home page for admin 
class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if "admin" in session : 
            if session["admin"] :
                return render_template('admin_base.html')
                return self.render('admin/index.html')
        return redirect('/dashboard_login')


class UserView(ModelView):
    # Only accessible for admin 
    def is_accessible(self):
        if "admin" in session : 
            if session["admin"] : 
                return True
        return False
    
    # Show tumbs for user image if he has one 
    def _list_thumbnail(view, context, model, name):
        if not model.image :
            return 'No image'

        return Markup(
            
            """
            <img src="%s" width="100px" height="100px">""" %
            url_for('user_images',

                    filename=model.image)
        )

    # Show download button for user image if he has one 
    def download(view, context, model, name):
        if model.image == None :
            return Markup(
            '<p>No image</p>')            
        
        return Markup(
            '<a href=%s>Donwload</a>'% 
            url_for('user_images',
                    filename=model.image    )
        )

    # Add prefix to image -> ID-{{user_id}}-imageName
    def prefix_name(obj, file_data):
        id = obj.id
        return ('ID-%s-%s' % (id,file_data.filename))
    
    # Can't edit user record 
    can_edit = False 

    # What appear in records
    column_list = ['full_name','username' , 'email' ,'image','download']

    column_searchable_list = ('full_name', 'email')
    column_default_sort = ('full_name', True)
    column_filters = ('full_name', 'email' )

    # What appear whan creating new record
    form_columns = ('full_name' ,'username', 'email', 'password', 'image') 


    column_formatters = {
        'image': _list_thumbnail ,
        'download' : download
    }

    form_extra_fields = {
        'password': PasswordField('Password',  validators=[validators.DataRequired()]) ,
        'image': form.ImageUploadField('Image',
                                      base_path=user_images_path,
                                      namegen=prefix_name
                                      )
    }


class CertificateView(ModelView):

    # Only accessible for admin 
    def is_accessible(self):
        if "admin" in session : 
            if session["admin"] : 
                return True
        return False

    # Show tumbs for certificates  
    def _list_thumbnail(view, context, model, name):
        if not model.image :
            return 'No image'

        return Markup(
            '<img src="%s" width="150px" height="100px">' %
            url_for('certificates',
                    filename=form.thumbgen_filename(model.image))
        )

    # Show download button for certificate
    def download(view, context, model, name):

        if model.image == None :
            return Markup(
            '<p>No file</p>')            
        
        return Markup(
            '<a href=%s>Donwload</a>'% 
            url_for('certificates',
                    filename=model.image)
        )

    # get email from certificate.user 
    def get_email(view, context, model, name):
        return model.user.email

    # same as in User View 
    def prefix_name(obj, file_data):
        id = obj.user.id
        return ('ID-%s-%s' % (id,file_data.filename))
        
    # What appear in records
    column_list = ['name','about' ,'user' ,'image','download']

    # What appear when creating or editing records 
    form_columns = ('name' ,'about', 'user', 'image') 

    
    column_labels = dict(name="Certificate" ,user="Email")
    column_sortable_list = ('name' , 'about','user')
    column_formatters = {
        'user': get_email ,
        'image': _list_thumbnail ,
        'download' : download
    }

    form_extra_fields = {
        # Add drop down list contains the emails if all registered users 
        'user': fields.QuerySelectField( validators=[validators.DataRequired()] ,
            query_factory=lambda: model.User.query.all(),
            widget=Select2Widget() , 
            get_label="email"
        ),
        'image': form.ImageUploadField('Image', validators=[validators.DataRequired()] ,
                                      base_path=certificates_path,
                                      thumbnail_size=(150, 100, True),
                                      namegen=prefix_name
                                      )                         
    }

