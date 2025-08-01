from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id)
            return store
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the store.")

    def delete(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id)
            db.session.delete(store)
            db.session.commit()
            return {"message": "Store deleted"}
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the store.")

@blp.route("/store")
class StoreList(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, request_data): 
        try:
            store = StoreModel(**request_data)
            db.session.add(store)
            db.session.commit()
            return store
        except IntegrityError:
            abort(400, message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store.")

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        try:
            return StoreModel.query.all()
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching stores.")