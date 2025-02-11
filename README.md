# Available endpoints and methods
## /users
### GET
Returns all users from database
### POST
Creates new user
### PATCH
Updates user, send id in body
## /users/id
### DELETE
Removes users with selected id

## /login
### POST
Recieves email and passowrd, and verifys the user, returns a JWT

# Request content
**GET** method requires authorization

**PATCH** and **DELETE** are still missing authorization

## Schema
![alt text](userschema.png)

### Example request for the post method:
```
{
    "name": "Rainer Roiner",
    "email": "rainer.roiner5@test.com",
    "phone": "11887744235",
    "dob": "1993-01-01T00:00:00Z",
    "purchases": 3948,
    "updatedAt": "2025-01-30T11:50:07.975000Z"
}
```
# Responses
**GET** returns an array of user objects

**POST** returns the created user object

**PATCH** returns simple "User updated" string

**DELETE** returns simple "User deleted" string



# To-do

- MINERVA - fastAPI, Create login endpoint, (optionally github login)
- ELLEN - middleware authorization jwt
- IRIS - db connection och prisma schema, env (kan sättas i rahi2     users-service-api) (db, genetrator och model user) 
- SUSANNA - fastApi, Create Reigster endpoint, keep track on documentation (optinally med github)
- Everybody assignes their own issues (and puts them to main board) 

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