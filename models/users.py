from mongoengine import Document, StringField, PointField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField

class User(Document):
    email = StringField(required=True)
    password = StringField(required=True)
    resetPasswordToken = StringField()
    resetPasswordExpires = DateTimeField()
    currentLocation = PointField()
    endpoint_arn = StringField()