import jwt
import passlib
import os
from dotenv import load_dotenv
from fastapi import Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')
TOKEN_EXPIRY = os.getenv('TOKEN_EXPIRY')

def authorise(request: Request):
    try:
        header = request.headers.get('Authorization') or None
        if header is None or not header.startswith("Bearer "): raise HTTPException(status_code=401)

        token = header.split(' ')[1]
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Unauthorised")
        
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Unauthorised")
        
    except HTTPException:
        raise HTTPException(status_code=401, detail="Unauthorised")
    

# Hit går apis som vi tillåter, o dom ska till cors nedan
origins = ["https://store-frontend-git-cna-25-store-frontend.2.rahtiapp.fi",
           "https://admin-frontend-git-admin-frontend.2.rahtiapp.fi/",
           "https://email-service-git-email-service-api.2.rahtiapp.fi/",
           "https://invoicing-service-git-invoicing-service.2.rahtiapp.fi/",
           "https://users-frontend-git-cloud-native-apps-users-frontend.2.rahtiapp.fi/",
           "https://wishlist-git-wishlist.2.rahtiapp.fi/wishlist",
           "https://newsletter-service-git-newsletter-service.2.rahtiapp.fi/",
           ]

def cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins, 
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "PUT","PATCH","DELETE"], 
        allow_headers=["Authorization", "Content-Type"], 
    )
