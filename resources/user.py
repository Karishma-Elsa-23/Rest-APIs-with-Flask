from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from passlib.hash import pbkdf2_sha256

from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import UserModel
from schemas import UserSchema
from blocklist import BLOCKLIST

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @jwt_required()
    @blp.arguments(UserSchema)
    def post(self, user_data):
        try:
            user = UserModel(
                username = user_data["username"],
                password = pbkdf2_sha256.hash(user_data["password"])  
            )
            db.session.add(user)
            db.session.commit()
            return {"message": "User created successfully"}, 201
        except IntegrityError:
            abort(400, message="A user with that username already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the user.")

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token" : access_token, "refresh_token": refresh_token}, 200
        abort(401, message = "Invalid Credentials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_access_token}, 200
    

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jwt = get_jwt()
        BLOCKLIST.add(jwt["jti"])
        return {"message": "Successfully logged out"}, 200


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        try:
            user = UserModel.query.get_or_404(user_id)
            return user
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the user.")

    @jwt_required()
    def delete(self, user_id):
        try:
            user = UserModel.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted"}, 200
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the user.")