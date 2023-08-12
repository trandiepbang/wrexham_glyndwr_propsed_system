from mongoengine import Document, StringField, ListField, FloatField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField

class Location(EmbeddedDocument):
    type = StringField(required=True)
    coordinates = ListField(FloatField(), required=True, min_length=2, max_length=2)

class User(Document):
    email = StringField(required=True)
    password = StringField(required=True)
    resetPasswordToken = StringField()
    resetPasswordExpires = DateTimeField()
    currentLocation = EmbeddedDocumentField(Location, required=False)
    endpoint_arn = StringField()