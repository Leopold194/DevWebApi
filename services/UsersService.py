from connection.functions import encode_auth_token
from repository.UsersRepository import UsersRepository
from repository.ReservationsRepository import ReservationsRepository
import exceptions.exceptions as exce
import bcrypt
import re

class UsersService:
    def __init__(self):
        self.users_repo = UsersRepository()

    def create_jwt_token(self, user_id, secret_key):
        return encode_auth_token(user_id, secret_key)
    
    def login_user(self, body, secret_key):
        if 'email' not in body.keys() or 'password' not in body.keys():
            raise exce.NoEmailOrPasswordFields()
        email = body['email']
        password = body['password']
        user = self.users_repo.check_user_password(email, password)
        if not user:
            raise exce.EmailOrPasswordIncorrect()
        token = self.create_jwt_token(user[0].id, secret_key)
        if not token:
            raise exce.TokenError()
        return token
    
    def modify_user(self, user_id, body):
        return self.users_repo.modify_user(user_id, body)

    def check_is_admin(self, user_id):
        user = self.users_repo.check_is_admin(user_id)
        if user:
            return True
        return False
    
    def check_body(self, body, data):
        for k, v in body.items():
            if k not in data.keys() or type(v) != data[k]:
                raise exce.IncorrectFields()
        return True
    
    def check_user_body_obligatory(self, body):
        obligatory_data = self.users_repo.get_users_columns()
        if len(body.keys()) != len(obligatory_data.keys()):
            raise exce.NoMandatoryFields()
        return self.check_body(body, obligatory_data)
    
    def check_user_body(self, body):
        possible_data = self.users_repo.get_users_columns(False)
        return self.check_body(body, possible_data)

    def get_users(self, filters):
        available_filters = self.users_repo.get_users_filters()
        filters = {}
        for arg in filters:        
            if arg in available_filters:
                filters[arg] = filters[arg]
        return self.users_repo.get_users(filters)

    def del_user(self, user_id):
        ReservationsRepository().del_user_reserv(user_id)
        return self.users_repo.del_user(user_id)

    def register_user(self, body):
        password_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        email_regex = "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}"
        if not self.users_repo.check_email_is_unique(body['email']):
            raise exce.NoUniqueEmail()
        if not re.match(password_regex, body['password']):
            raise exce.WrongPassword()
        if not re.fullmatch(email_regex, body['email']):
            raise exce.WrongEmail()
        if not len(body['firstname']) > 3 or not len(body['lastname']) > 3:
            raise exce.WrongNames()
        body['password'] = bcrypt.hashpw((body['password']).encode('utf-8'), bcrypt.gensalt())
        return self.users_repo.register_user(body)