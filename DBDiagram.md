## MongoDB Diagram

### User 
```json
{
    "type": "object",
    "properties": {
        "username": {
            "type": "string"
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string"
        },
        "resetPasswordToken": {
            "type": "string"
        },
        "resetPasswordExpires": {
            "type": "string",
            "format": "date-time"
        },
        "currentLocation": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string"
                },
                "coordinates": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    },
                    "minItems": 2,
                    "maxItems": 2
                }
            },
            "required": [
                "type",
                "coordinates"
            ]
        },
       "endpoint_arn": {
            "type": "string",
            "description": "The Amazon SNS endpoint ARN associated with the user."
        }
    },
    "required": [
        "username",
        "email",
        "password",
        "currentLocation"
    ]
}
```

"username": This is a string that represents the username of a user. It's a unique identifier that a user uses to log in to the system.

"email": This is a string that represents the user's email address. It can also serve as a unique identifier and a way to contact the user. This field should follow the email format.

"password": This is a string that represents the user's password. This is used along with the username or email for authenticating the user during login. In a real-world scenario, it would be stored as a hashed value for security reasons.

"currentLocation": This is an object that represents the user's current geographical location. It consists of two properties: "type" and "coordinates". The "type" is expected to be the string "Point" to denote that the location data is a point in the 2D space. The "coordinates" is an array of exactly two numbers representing longitude and latitude of the location.



### Crime Incident DB
```json
{
    "type": "object",
    "properties": {
        "description": {
            "type": "string"
        },
        "incident_type": {
            "type": "string"
        },
        "summary": {
            "type": "string"
        },
        "location": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string"
                },
                "coordinates": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    },
                    "minItems": 2,
                    "maxItems": 2
                }
            },
            "required": [
                "type",
                "coordinates"
            ]
        },
        "occurred_at": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": [
        "description",
        "incident_type",
        "summary",
        "location",
        "occurred_at"
    ]
}
```

"description": This is a string that provides a detailed account of the crime incident.

"incident_type": This is a string that categorizes the type of crime incident, such as "theft", "assault", etc.

"summary": This is a string that provides a brief overview or summary of the crime incident.

"location": Similar to the User Schema, this is an object that represents the geographical location where the crime incident occurred. It also contains "type" and "coordinates" fields representing a point in the 2D space.

"occurred_at": This is a string in date-time format which records when the crime incident happened. The format would usually be an ISO 8601 date-time string like 'YYYY-MM-DDTHH:MM:SS'.
