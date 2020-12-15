from app import ma
from app.models import Message, User
from app import ma
from marshmallow_sqlalchemy.fields import Nested


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
    
    sender = Nested(UserSchema, exclude=("about_me", "id", "password_hash", "location", "last_seen"))
    