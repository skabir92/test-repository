# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 23:25:24 2020

@author: shadm
"""

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Do not leave this empty")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")
    
    @jwt_required()
    def get(self, name):        
        item = ItemModel.find_by_username(name)
        
        if item:
            return item.json()
        return {"message" : "Item not found"}, 404
    
    def post(self, name):            
        if ItemModel.find_by_username(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        
        data = Item.parser.parse_args()
        
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message" : "Error occured insterting item"}, 500
        
        return item.json(), 201
    
    def delete (self, name):
        item = ItemModel.find_by_username(name)
        
        if item:           
            item.delete_from_db()
              
        return {'message' : 'item deleted {}'.format(name)}
        
    def put (self, name):      
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_username(name)
        
        if item is None:
            try:
                item = ItemModel(name, data['price'], data['store_id'])
            except:
                return {"message" : "Error occured insterting item"}, 500
        else:
            try:
                item.price = data['price'] 
            except:
                return {"message" : "Error occured updating item"}, 500        
            
        item.save_to_db()
        
        return item.json()
   
    
class ItemList(Resource):
    def get(self): 
        return {'items' : list(map(lambda x: x.json(), ItemModel.query.all()))}
        #return {"items" : [item.json() for item in ItemModel.query.all()]}
    