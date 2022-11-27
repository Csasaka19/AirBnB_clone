#!/usr/bin/python3
"""This file enables the directory to be a package
which in turn enables inheritance to occur
instantiates an object of classes of Storage"""
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from os import getenv
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()

class Classes(dict):
    """ classes """
    def __getitem__(self, key):
        """get item"""
        try:
            return super(Classes, self).__getitem__(key)
        except Exception as e:
            raise Exception("** class doesn't exist **")


classes = {'User': User, 'BaseModel': BaseModel,
           'Amenity': Amenity, 'State': State,
           'City': City, 'Place': Place, 'Review': Review}
