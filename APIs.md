## API Design
###  POST /users/register
This endpoint is used to create a new user. The request body should include the username, email, and password for the new user. 
Request Body:
```json
{
    "username": "user1",
    "email": "user1@example.com",
    "password": "user1password"
}
```

Response: A successful response would return a 201 status code along with a confirmation message or the created user data.


### POST /users/login
used to authenticate a user. The request body should contain the username (or email) and password of the user. Request Body:

Request Body:
```json
{ 
   "username": "user1", 
   "password": "user1password" 
}
```


Response: A successful response would return a 200 status code along with an access token or user data.

### POST /users/forgot_password
This endpoint is used when a user forgets their password. The request body should contain the email of the user. The server will then generate a reset token, save it in the database with an expiration time, and send it to the user's email.

Request Body:
```json
{ "email": "user1@example.com" }
```

Response: A successful response would return a 200 status code along with a confirmation message.

### POST /users/reset_password/:token
This endpoint is used to update the user's password. It should be used in combination with the reset token sent to the user's email. The request body should contain the new password.

Request Body:
```json
{ "password": "newPassword" }
```

Response: A successful response would return a 200 status code along with a confirmation message.

### PUT /users/update_location
This endpoint is used to update the user's current location. The request body should contain the new currentLocation object which includes type and coordinates. 

Request Body:
```json
{ "currentLocation": { "type": "Point", "coordinates": [-0.1276474, 51.5072955] } }
```

Response: A successful response would return a 200 status code along with a confirmation message or the updated user data.

