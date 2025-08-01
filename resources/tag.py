from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import StoreModel, TagModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("tags", __name__, description="Operations on tags")

@blp.route("/store/<int:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id)
            return store.tags.all()
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching tags.")

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        try:
            tag = TagModel(**tag_data, store_id=store_id)
            db.session.add(tag)
            db.session.commit()
            return tag
        except IntegrityError:
            abort(400, message="A tag with that name already exists in this store.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")
            
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        try:
            tag = TagModel.query.get_or_404(tag_id)
            return tag
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the tag.")

    @blp.response(202, description="Delete a tag if not linked to any items.", example={"message": "Tag deleted"})
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(400, description="Tag cannot be deleted because it is linked to items.")
    def delete(self, tag_id):
        try:
            tag = TagModel.query.get_or_404(tag_id)
            if not tag.items:
                db.session.delete(tag)
                db.session.commit()
                return {"message": "Tag deleted"}
            abort(400, message="Tag cannot be deleted because it is linked to items.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the tag.")

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            tag = TagModel.query.get_or_404(tag_id)
            if item.store_id != tag.store_id:
                abort(400, message="Tag does not belong to the item's store.")
            item.tags.append(tag)
            db.session.commit()
            return tag
        except SQLAlchemyError:
            abort(500, message="An error occurred while linking the tag to the item.")  

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            tag = TagModel.query.get_or_404(tag_id)
            item.tags.remove(tag)
            db.session.commit()
            return {"message": "Tag unlinked from item", "item" : item, "tag": tag}
        except SQLAlchemyError:
            abort(500, message="An error occurred while unlinking the tag from the item.")