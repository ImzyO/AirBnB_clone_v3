#!/usr/bin/python3
"""test for file storage"""
import unittest
import pep8
import json
import os
from os import getenv
from models.amenity import Amenity
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,\
        "Place": Place, "Review": Review, "State": State, "User": User}

class TestFileStorage(unittest.TestCase):
    '''this will test the FileStorage'''

    @classmethod
    def setUpClass(cls):
        """set up for test"""
        cls.user = User()
        cls.user.first_name = "Kev"
        cls.user.last_name = "Yo"
        cls.user.email = "1234@yahoo.com"
        cls.storage = FileStorage()

    @classmethod
    def teardown(cls):
        """at the end of the test this will tear it down"""
        del cls.user

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_FileStorage(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_all(self):
        """tests if all works in File Storage"""
        storage = FileStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._FileStorage__objects)

    def test_all_v2(self):
        """Tests the new all() method in the v2"""
        storage = FileStorage()
        users = storage.all(User)
        self.assertIsNotNone(users)
        self.assertEqual(type(users), dict)

    def test_new(self):
        """test when new is created"""
        storage = FileStorage()
        obj = storage.all()
        user = User()
        user.id = 123455
        user.name = "Kevin"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_reload_filestorage(self):
        """Tests reload"""
        self.storage.save()
        Root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(Root, "file.json")
        with open(path, 'r') as f:
            lines = f.readlines()
        try:
            os.remove(path)
        except:
            pass
        self.storage.save()
        with open(path, 'r') as f:
            lines2 = f.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except:
            pass
        with open(path, "w") as f:
            f.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)

    def test_delete(self):
        """Tests the delete v2 method"""
        storage = FileStorage()
        new_state = State()
        new_state.name = "California"
        storage.new(new_state)
        storage.save()
        states = storage.all(State)
        self.assertIsNotNone(states)
        self.assertEqual(type(states), dict)
        storage.delete(new_state)
        states = storage.all(State)
        self.assertEqual(states, {})

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db', "not testing file storage")
    def test_get(self):
        """ Tests method for obtaining an instance file storage"""
        storage = FileStorage()
        dic = {"name": "Colorado"}
        instance = State(**dic)
        self.new(instance)
        self.save()
        storage = FileStorage()
        get_instance = storage.get(State, instance.id)
        self.assertEqual(get_instance, instance)

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db', "not testing file storage")
    def test_count(self):
        """ Tests count method file storage """
        storage = FileStorage()
        dic = {"name": "Arizona"}
        state = State(**dic)
        storage.new(state)
        dic = {"name": "Mexico"}
        city = City(**dic)
        storage.new(city)
        storage.save()
        c = storage.count()
        self.assertEqual(len(storage.all()), c)

if __name__ == "__main__":
    unittest.main()
