from database.crud import CrudManager
from database.models import Users
import exceptions.exceptions as exce

class UsersRepository:
    def __init__(self) -> None:
        self.crud = CrudManager(Users)

    def check_user_password(self, email, password):
        user = self.crud.find_by_kargs(email=email)
        if user and user[0].check_password(password):
            return user
        return None
    
    def check_is_admin(self, user_id):
        user = self.crud.find_by_id(user_id)
        if user and user.is_admin:
            return user
        return None

    def modify_user(self, user_id, body):
        updated_obj_id = self.crud.update(user_id, **body)
        if updated_obj_id:
            updated_obj_data = self.crud.find_by_id(updated_obj_id).__dict__
            updated_obj_data.pop('_sa_instance_state')
            updated_obj_data.pop('password')
            return updated_obj_data
        raise exce.ObjectDoesntExist()

    def get_users_columns(self, creating = True):
        default_column = {'firstname':str, 'lastname':str, 'email':str, 'password':str}
        user = self.crud.find_all()
        if user:
            user_data = dict(user[0].__dict__)
            user_data.pop('_sa_instance_state')
            user_data.pop('id')
            if creating:
                user_data.pop('status')
            good_column = {k:type(v) for k, v in user_data.items()}
            good_column['password'] = str
            return good_column
        return default_column
    
    def register_user(self, body):
        created_object_id = self.crud.insert(body)
        if created_object_id:
            created_object_data = self.crud.find_by_id(created_object_id).__dict__
            created_object_data.pop('_sa_instance_state')
            created_object_data.pop('password')
            return created_object_data
        return exce.ObjectNotCreated()
    
    def check_email_is_unique(self, email):
        user = self.crud.find_by_kargs(email=email)
        if user:
            return False
        return True
    
    def get_users_filters(self):
        default_filters = ['email', 'firstname', 'lastname', 'status', 'id']
        user = self.crud.find_all()
        if user:
            user_data = dict(user[0].__dict__)
            user_data.pop('_sa_instance_state')
            return list(user_data.keys())
        return default_filters

    def del_user(self, user_id):
        if self.crud.delete(user_id):
            return True
        raise exce.ObjectDoesntExist()

    def get_users(self, filters):
        users_data = {}
        for user in self.crud.find_by_kargs(**filters):
            user_data = dict(user.__dict__)
            user_data.pop('_sa_instance_state')
            user_data.pop('password')
            users_data[user.id] = user_data
        return users_data
    
    def check_user_exist(self, user_id):
        return self.crud.find_by_id(user_id)
