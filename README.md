# Available endpoints and methods
## /users
### GET
Returns all users from database

Returns an array of user objects

### POST
Creates new user

Returns the created user object
The data and address fields always have to be sent, either with information or as empty dictionaries.

#### Example request for the post method:

###### Option 1
Data and Adress can be anything you want it to be
```
{
    "name": "Rainer Roiner",
    "email": "rainer.roiner5@test.com",
    "password": "password123",
    "phone": "11887744235",
    "dob": "1993-01-01T00:00:00Z"
    "address": {
          "street": "123 Main St",
          "zipcode": "12345",
          "city": "yayLand",
          "country": "Country"
    },
    "data": {
          "gender": "female",
          "height": "180cm",
          "weight": "100kg"
    }
}
```

###### Option 2
```
{
    "name": "Rainer Roiner",
    "email": "rainer.roiner5@test.com",
    "password": "password123",
    "phone": "11887744235",
    "dob": "1993-01-01T00:00:00Z"
}
```
### PATCH
Updates user
Normal user can only update themselves, admin can update anyone. 

Returns simple "User updated" string

## /users/id
### DELETE
Removes users with selected id
Normal user can only delete themselves, admin can delete anyone. 

Returns simple "User deleted" string

**GET**, **PATCH** and **DELETE** methods require authorization. 

## /login
### POST
Recieves email and password, then verifies the user, and returns a JWT. 
Login POST example:

```
POST {{apiURL}}/login
Content-Type: application/json

{
    "email": "user@email.com",
    "password": "password"
}
```
Login response example:
```
{
  "access_token": "eyJhbGciOiJIUzI1NnR5cCI6IkpXVCJ9.eyJzdWIiOiIxNSIsImBza3V0dCIsImVtYWlsIjoiLmNvbSIsImV4cCI6MTc0MDAzODM1OX0.0PJz-nosI7pHkmZXkID5z41aSHEuVnpRw5EPHk",
  "token_type": "bearer"
}
```
# DATABASE
Every user has a "user" role by default. If the role needs to be updated to "admin", it needs to be changes manually in the database. 
Every field is mandatory, except for the number of purchases.
Inside of address and data anyhting can be stored, amount doesn't matter. 
- Details like gender and taste preferences can be stored in **data**.
- Details like street name nad zipcode can be stores in **address**.

```
table USER
  id        Int     @id @default(autoincrement())
  name      String  
  password  String   
  email     String   @unique
  role      String   @default("user")
  phone     String   @unique 
  dob       DateTime
  address   Json     @default("{}")  // Default JSONB
  data      Json     @default("{}")  // Default JSONB
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
```

## JWT example
```
{
    "sub": "1234567890", - user id

    "name": "John Doe", - name of user

    "email": "john.doe@example.com", - email of user

    "role": "user", - role of user (user or admin)

    "exp": 1739659869 - token expiry time (utc, since unix epoch)
}
```

### OBS Swagger UI updates automatically and works as our documentation, so the endpoint can be tested there as well. 
