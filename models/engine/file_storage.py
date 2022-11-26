#!/usr/bin/python3
"""This is the file storage module
It facilitates the storage of class instances"""
import json
import os.path


class FileStorage:
    """File storage class"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns a dictionary of models currently in storage"""
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj.to_dict()

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__filepath, 'w', encoding="utf-8") as f:
            json.dump(self.__objects, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            t = {}
            with open(FileStorage.__file_path, 'r') as f:
                t = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
