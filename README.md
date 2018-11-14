# Certificates

A small website built with flask.There is users and an admin.
The admin can add certificates to the users so they can login and download their certificates.

## Getting Started

### Prerequisites
 python 3 

### Installing
 Clone the project : 
 
 
 
```
 git clone https://github.com/mohammedhashim44/Certificates-Flask-Project.git
```

 Install the libraries listed in requirements.txt file .

```
 pip3 install -r requirements.txt
```

## Running the project

to run the project , do :

```
 cd Certificates-Flask-Project 
 cd app 
 python3 app.py 
```

## How to use 
  #### The user end
  -When you run the project , the server will be running on localhost:5000 <br/>
  -Open the browser and go ```http://localhost:5000/```<br/>
  -You can sign in with example account ```email:test11@test.com  password:test``` <br/>
  -You will be directed to the profile page  <br/>
  -You can upload your image <br/>
  -You can view your certificates and download them <br/>
  


  
  #### The admin end
  -Go to ```http://localhost:5000/admin```<br/>
  -Sign in with the account ```email:admin@admin.com  password:admin``` <br/>
  -You will be directed to the dashboard  <br/>
  -You can create , edit or delete users and certificates  <br/>
  -To add user , go to user tab and press create and fill the form  <br/>
  -To add certificate to certain user , go to certificates tab and press create and fill the form <br/>


### example

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/) - Dashboard extension
* [Flask_SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) - Sqlalchemy database
* [Jinja2](http://jinja.pocoo.org/docs/2.10/) - Template engine
* [Flask-Uploads](https://pythonhosted.org/Flask-Uploads/) - Upload files
* [WTForms](https://github.com/wtforms/wtforms) - Forms validation and rendering
* [W3schools.com](https://www.w3schools.com/) - HTML templates

 
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details




