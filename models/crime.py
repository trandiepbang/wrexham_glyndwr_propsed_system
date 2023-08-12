from mongoengine import Document, StringField, ListField, FloatField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField

class Location(EmbeddedDocument):
    type = StringField(required=True)
    coordinates = ListField(FloatField(), required=True, min_length=2, max_length=2)

class Incident(Document):
    description = StringField(required=True)
    incident_type = StringField(required=True)
    summary = StringField(required=True)
    location = EmbeddedDocumentField(Location, required=True)
    source = StringField(required=False)
    occurred_at = DateTimeField(required=True)
