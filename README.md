# user-service

# To-do

### Create a "Users" table in DB (id [unique, automatic], names [String], email [unique String], adress [String], hashed pass [String] created at [timestamp] etc.)
- create and define the User schema in Prisma 
- migrate it

### Connect the DB through Prisma 
- Set up Prisma in FastAPI (database.py or so)
- add the startup and shutoff events in main (db conection calls)

### Environment 
- Everyone creates an .env file (with db url, jwt secret etc.)
    - We can start with a shared one? e.g sample.env (without sensitive values)

### Create endpoint (POST /login)
- verify user 
- return JWT on login (pyJWT) (authorization in middleware folder)
- create a test file (users.http) to test the method 

### OBS Swagger UI updates automatically and works as our documentation, so the endpoint can be tested there as well. 


