# wrexham_glyndwr_propsed_system
### How to start MongoDB 
docker run -d  -p 27017:27017  --name mongodb -v mongo-data:/data/db  -e MONGODB_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_DATABASE=crime_db  -e MONGODB_INITDB_ROOT_PASSWORD=admin mongo:latest
