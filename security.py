# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 00:31:16 2020

@author: shadm
"""

from models.user import UserModel
#from werkzeug.security import safe_str_cmp

def authenticate (username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user

def identity (payload):
    user_id = payload ['identity']
    return UserModel.find_by_userid(user_id)