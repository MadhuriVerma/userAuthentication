from flask_restful import Resource,reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
import math
import random
import jwt
import re


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('full_name', 
    type=str,
    required=True,
    help="This field cannot be blank."
    )
    parser.add_argument('email', 
    type=str,
    required=True,
    help="This field cannot be blank."
    )
    parser.add_argument('mobile_number', 
    type=str,
    required=True,
    help="This field cannot be blank."
    )
    parser.add_argument('username', 
    type=str,
    required=True,
    help="This field cannot be blank."
    )
    parser.add_argument('password', 
    type=str,
    required=True,
    help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"},400
        else:
            email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

            if email_regex.match(data['email']):
                pass
            else:
                return {"Error":"Please enter a valid email address"}
         
        if UserModel.find_my_mobile_number(data['mobile_number']):
            return {"message": "A user with that number already exists"},400   
        else:
            number = re.fullmatch('[6-9][0-9]{9}',data['mobile_number'])

            if number != None:
                pass
            else:
                return {"message": "Please enter a valid mobile number"},400
   

        user = UserModel(**data)
        user.save_to_db()


        return {"message": "User registration successful."}, 201


class Login(Resource):
     parser = reqparse.RequestParser()
     parser.add_argument('username', 
     type=str,
     required=True,
     help="This field cannot be blank."
     )
     parser.add_argument('password', 
     type=str,
     required=True,
     help="This field cannot be blank."
     )

     def post(self):
         data = Login.parser.parse_args()

         user = UserModel.find_by_username(data['username'])
         if user and safe_str_cmp(user.password, data['password']):
             digits = "0123456789"
             otp = ""
             for i in range(6):
                 otp += digits[math.floor(random.random() * 10)]

             user.otp = str(otp)
             user.save_to_db()

             return f"User successfully login. Your OTP is: {user.otp}", 200

         else:
             return ({"message": "Invalid username and password"}), 400


class OTPVerification(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
     type=str,
     required=True,
     help="This field cannot be blank."
     )
    parser.add_argument('otp', 
     type=str,
     required=True,
     help="This field cannot be blank."
     )

    def post(self):
         data = OTPVerification.parser.parse_args()

         user = UserModel.find_by_username(data['username'])

         if user and safe_str_cmp(user.otp, data['otp']):
             payload = {
                 "username": "username",
                 "password": "password"
             }
             tokens = jwt.encode (
                 payload = payload,
                 key= 'zehn_key')
             return ({"message": f"Your OTP verification successfully completed.",
             "username": f"{data['username']}",
             "Full Name": f"{user.full_name}",
             "Mobile Number": f"{user.mobile_number}", 
             "Email Address": f"{user.email}",
             "access token": f"{tokens}",
             })

         else:
            return ({"message": "Invalid  OTP"})     


class UpdatePassword(Resource):
     parser = reqparse.RequestParser()
     parser.add_argument('username', 
     type=str,
     required=True,
     help="This field cannot be blank."
     )
     parser.add_argument('current password', 
     type=str,
     required=True,
     help="This field cannot be blank."
     )
     parser.add_argument('new password', 
     type=str,
     required=True,
     help="This field cannot be blank."
     )

     
     def post(self):
         data = UpdatePassword.parser.parse_args()

         user = UserModel.find_by_username(data['username'])
         if user and safe_str_cmp(user.password, data['current password']):
             user.password = data['new password']
             user.save_to_db()
             return f"Your password successfully updated", 200

         else:
             return ({"message": "Can not change your password, please check your username and password"}), 400
    

class ForgotPassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
     type=str,
     required=True,
     help="This field cannot be blank."
     )

    def post(self):
        data = ForgotPassword.parser.parse_args()


        user = UserModel.find_by_username(data['username'])

        if user:
            payload = {
                "username" : data['username']
             }
            token = jwt.encode (
                 payload = payload,
                 key= 'madhuri_key')
            access_token = token.decode("utf-8")     

            return ({"message": f"Username verified successfully",
            "reset_token": f"{access_token}"})

        else:
            return ({"message": "Username does not exist"})    

class ResetPassword(Resource):
     parser = reqparse.RequestParser()
     parser.add_argument('access token',
      type=str,
     required=True,
     help="This field cannot be blank."
     )
     parser.add_argument('new password', 
     type=str,
     required=True,
     help="This field cannot be blank."
     )
     parser.add_argument('confirm password',
      type=str,
     required=True,
     help="This field cannot be blank."
     )
    

     def post(self):
        data = ResetPassword.parser.parse_args()
        

        if data:
            token = data['access token']
            token_data = jwt.decode(token,key='madhuri_key',algorithms=['HS256',])
            username = token_data['username']

        username = UserModel.find_by_username(username)

        if username is None:
            return {"message": "Invalid token"}, 401

        elif data['new password'] == data['confirm password']:
            username.password = data['new password']

        else:
            return {"message": "New password and confirmation password are not the same"}

        username.save_to_db()

        return {"message": "Password changed successfully, now you can login using new password!"}, 201



       
