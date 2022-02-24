from turtle import title
from venv import create
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import ForeignKey, Integer, table
from sqlalchemy.orm import relationship



db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at =  db.Column(db.DateTime, onupdate=datetime.now)
    is_superuser = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    
class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    
    def create_slug(self):
        name = self.name
        low_name = name.lower()
        slug = low_name.replace(" ", "-")
        
        return slug
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.slug = self.create_slug()
        
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    