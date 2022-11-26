#!/usr/bin/python3
"""This is the review module"""
from models.base_model import BaseModel


class Review(BaseModel):
    """This is the review class"""
    place_id = ''
    user_id = ''
    text = ''
