
from model import User , db

class DatabaseHelper():

    def __init__(self):
        pass

    def getUserData(self,email,password):
        res = User.query.filter(User.email==email , User.password==password)
        if res.count() != 1 :
            return -1
        res = res.first() 
        data = {"id":res.id,"username" : str(res.username) , "image": res.image}
        return data
 
    def insertIntoUsers(self,args):
        try :
            user = User()
            user.full_name = args[0]
            user.username =  args[1]
            user.email = args[2]
            user.password = args[3]
            
            db.session.add(user)
            db.session.commit()
            return 1 
        except Exception as e :
            print(str(e))
            return -1
