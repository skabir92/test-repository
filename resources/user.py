# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 00:29:45 2020

@author: shadm
"""
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Do not leave this empty")
    
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Do not leave this empty")
    
    def post(self):    
        data = UserRegistration.parser.parse_args() 
        
        if UserModel.find_by_username(data['username']):
            return {"message" : "A user with name '{}' already exists".format(data['username'])}, 400
    
        user = UserModel(**data)
        user.save_to_db()
        
        return {"message" : "User created successfully"}, 201
    