# wrexham_glyndwr_propsed_system
### How to start MongoDB 
docker run -d  -p 27017:27017  --name mongodb -v mongo-data:/data/db  -e MONGODB_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_DATABASE=crime_db  -e MONGODB_INITDB_ROOT_PASSWORD=admin mongo:latest

### Main flow Summary
- Client sends a request to the API Gateway with location coordinates and a token.
- API Gateway authenticates the request and forwards the user information and location to the Main App.
- Main App routes the request to the Location Handler.
- Location Handler checks with the Database to determine if the given location is a high-risk area.
- Location Handler updates the user's location in the Database.
- If the location is high-risk, the Location Handler sends a push notification back to the Client.

