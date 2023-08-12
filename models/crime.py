from mongoengine import Document, StringField, PointField, DateTimeField


class Incident(Document):
    description = StringField(required=True)
    incident_type = StringField(required=True)
    summary = StringField(required=True)
    location = PointField()  # This will store the coordinates as [longitude, latitude]
    meta = {
        'indexes': [
            {
                'fields': [('location', '2dsphere')]
            }
        ]
    }
    source = StringField(required=False)
    occurred_at = DateTimeField(required=True)
