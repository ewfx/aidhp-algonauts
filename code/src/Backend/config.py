import os

class Config:
    SECRET_KEY = 'your-secret-key'  
    SUPABASE_PASSWORD = 'your-password'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.enmpkgkrndfztxkqzxvs:'+ SUPABASE_PASSWORD +'@aws-0-us-east-1.pooler.supabase.com:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-jwt-secret-key'
