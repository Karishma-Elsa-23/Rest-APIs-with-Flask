import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):   
        try:
            item = ItemModel.query.get_or_404(item_id)
            return item
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the item.")

    def delete(self, item_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item deleted"}
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the item.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = ItemModel.query.get(item_id)
            if item:
                item.price = item_data["price"] 
                item.name = item_data["name"]
            else:
                item = ItemModel(id = item_id, **item_data)
            db.session.add(item)
            db.session.commit()
            return item
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the item.")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        try:
            return ItemModel.query.all()
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching items.")
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, request_data):
        try:
            item = ItemModel(**request_data)
            db.session.add(item)
            db.session.commit()
            return item
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
