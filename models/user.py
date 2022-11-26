#!/usr/bin/python3
"""This is the user module"""
from models.base_model import BaseModel


class User(BaseModel):
    """This is the user class"""
    email = ''
    password = ''
    first_name = ''
    last_name = ''
