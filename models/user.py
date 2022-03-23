from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    mobile_number = db.Column(db.String(256))
    username = db.Column(db.String(256))
    password = db.Column(db.String(256))
    otp = db.Column(db.String(256))

    def __init__(self,full_name,email,mobile_number, username, password):
        self.full_name = full_name
        self.email = email
        self.mobile_number = mobile_number
        self.username = username
        self.password = password
        


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()    

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
          

    @classmethod 
    def find_by_id(cls, _id):
       return cls.query.filter_by(id = _id).first()    

    @classmethod 
    def find_by_email(cls, email):
       return cls.query.filter_by(email = email).first()   

    @classmethod 
    def find_my_mobile_number(cls, mobile_number):
        return cls.query.filter_by(mobile_number = mobile_number).first()


