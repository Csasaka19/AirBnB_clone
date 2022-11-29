#!/usr/bin/python3
"""This is the file storage module
It facilitates the storage of class instances"""
import json
from os import path


class FileStorage:
    """
    File storage class, stores info about an object in a json file

    Attributes:
        __file_path (str): contains the path to the file
        __objects (obj): the dictionary that stores all objects
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary, __objects"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """ serializes __objects to JSON file(path:__file_path) """
        
        my_dict = {}
        instance = FileStorage.__objects
        my_dict = {key: value.to_dict() for key, value in instance.items()}

        with open(self.__file_path, 'w') as f:
            json.dump(my_dict, f)

    def reload(self):
        """ Loads storage dictionary from file """
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        if path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path) as f:
                my_dict = json.load(f)
                for key, val in my_dict.items():
                    FileStorage.__objects[key] = eval(val['__class__'])(**val)
