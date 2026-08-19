from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,EmailStr,field_validator
from config import supabase
import re


app=FastAPI(title="Smart Ag API")

# Enable CORS for React frontend (Vite default port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Base(BaseModel):
    pass

class SignUpSchema(Base):
    email: EmailStr
    password: str
    farmer_name: str
    location: str
    soil_type: str
    area_acres: float

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return value

class LoginSchema(Base):
    email:EmailStr
    password:str

@app.post("/auth/signup")
async def signup(data:SignUpSchema):
    try:
        # Step A: Register email & password with Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })

        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Failed to register user account.")

        user_id = auth_response.user.id

        # Step B: Insert farm profile linked to the user_id
        farm_payload = {
            "user_id": user_id,
            "farmer_name": data.farmer_name,
            "location": data.location,
            "soil_type": data.soil_type,
            "area_acres": data.area_acres
        }
        
        db_response = supabase.table("farms").insert(farm_payload).execute()

        return {
            "status": "success",
            "message": "Account created successfully!",
            "user_id": user_id,
            "farm_data": db_response.data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/")
async def root():
    return {"status": "healthy", "service": "AgriSmart Backend"}

# 2. Login Endpoint: Authenticates user credentials
@app.post("/auth/login")
async def login(credentials: LoginSchema):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        
        return {
            "status": "success",
            "access_token": auth_response.session.access_token,
            "user_id": auth_response.user.id
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")



