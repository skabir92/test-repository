# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 23:03:24 2020

@author: shadm
"""

from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    @jwt_required()
    def get(self, name):        
        store = StoreModel.find_by_name(name)
        
        if store:
            return store.json()
        return {"message" : "Store not found"}, 404
    
    def post(self, name):            
        if StoreModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
            
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message" : "Error occured creating store"}, 500
        
        return store.json(), 201
    
    def delete (self, name):
        store = StoreModel.find_by_name(name)
        
        if store:           
            store.delete_from_db()
              
        return {'message' : 'item deleted {}'.format(name)}
   
    
class StoreList(Resource):
    def get(self): 
        return {'stores' : list(map(lambda x: x.json(), StoreModel.query.all()))}
        #return {"items" : [item.json() for item in ItemModel.query.all()]}
    