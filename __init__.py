import os
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.engine import db_storage, file_storage

"""CNC - dictionary = { Class Name (string) : Class Type }"""

if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
    CNC = db_storage.DBStorage.CNC
    storage = db_storage.DBStorage()
else:
    CNC = file_storage.FileStorage.CNC
    storage = file_storage.FileStorage()

storage.reload()
