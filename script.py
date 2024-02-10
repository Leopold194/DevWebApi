import getpass
import re
import bcrypt
from database.crud import CrudManager
from database.models import Users

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

crud = CrudManager(Users)

def create_adminuser():
    firstname = str(input("Firstname: "))
    lastname = str(input("Lastname: "))
    email = str(input("Email: "))

    if len(crud.find_by_kargs(email=email)) != 0:
        return("Utilisateur déjà existant")

    if not re.fullmatch(regex, email):
        return("Invalid Email")

    password = bcrypt.hashpw(getpass.getpass().encode('utf-8'), bcrypt.gensalt())

    user = crud.insert({"firstname":firstname, "lastname":lastname, "email":email, "password":password, "status":2})

    return user
    

