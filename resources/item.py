from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):   
        try:
            item = ItemModel.query.get_or_404(item_id)
            return item
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the item.")

    @jwt_required(fresh=True)
    def delete(self, item_id):
        try:
            jwt = get_jwt()
            if jwt.get("is_admin", False) is False:
                abort(401, message="Admin privileges required to delete an item.")
            item = ItemModel.query.get_or_404(item_id)
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item deleted"}
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the item.")

    @jwt_required(fresh=True)
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
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        try:
            return ItemModel.query.all()
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching items.")
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, request_data):
        try:
            item = ItemModel(**request_data)
            db.session.add(item)
            db.session.commit()
            return item
        except SQLAlchemyError as e:
            abort(500, message="An error occurred while inserting the item. error: {}".format(str(e)))
