from database.models import Users
from database.crud import CrudManager
from flask import Response
from services.UsersService import UsersService
import exceptions.exceptions as exce
import json
from connection.functions import decode_auth_token

class UsersController:
    def __init__(self, app):
        self.crud = CrudManager(Users)
        self.users_serv = UsersService()
        self.app = app

    def login(self, request):
        try:
            body = request.json
        except:
            return Response("{\"error\":\"You have not provided a body in your request.\"}", status=400, mimetype='application/json')
        try:
            secret_key = self.app.config.get('SECRET_KEY')
            token = json.dumps(self.users_serv.login_user(body, secret_key))
            return Response(token, status=200, mimetype='application/json')
        except exce.EmailOrPasswordIncorrect:
            return Response("{\"error\":\"Your email or your password is incorrect.\"}", status=400, mimetype='application/json')
        except exce.NoEmailOrPasswordFields:
            return Response("{\"error\":\"You have not provided an email or password.\"}", status=400, mimetype='application/json')
        except exce.TokenError:
            return Response("{\"error\":\"The token could not be created.\"}", status=404, mimetype='application/json')
        except AttributeError:
            return Response("{\"error\":\"Please enter a body in dictionary form.\"}", status=400, mimetype='application/json')
        
    def register(self, request):
        try:
            body = request.json
        except:
            return Response("{\"error\":\"You have not provided a body in your request.\"}", status=400, mimetype='application/json')
        try:
            self.users_serv.check_user_body_obligatory(body)
            new_obj = json.dumps(self.users_serv.register_user(body))
            return Response(new_obj, status=200, mimetype='application/json')
        except exce.IncorrectFields:
            return Response("{\"error\":\"You have entered incorrect fields in your body.\"}", status=400, mimetype='application/json')
        except exce.ObjectNotCreated:
            return Response("{\"error\":\"Your object could not be created.\"}", status=404, mimetype='application/json')
        except exce.NoMandatoryFields:
            return Response("{\"error\":\"You have not completed all the required fields.\"}", status=400, mimetype='application/json')
        except exce.NoUniqueEmail:
            return Response("{\"error\":\"It looks like you already have an account.\"}", status=400, mimetype='application/json')
        except exce.WrongEmail:
            return Response("{\"error\":\"Please provide a valid email address.\"}", status=400, mimetype='application/json')
        except exce.WrongPassword:
            return Response("{\"error\":\"Please provide a valid password.\"}", status=400, mimetype='application/json')
        except exce.WrongNames:
            return Response("{\"error\":\"Please provide a valid lastname and fisrtname.\"}", status=400, mimetype='application/json')
        except AttributeError:
            return Response("{\"error\":\"Please enter a body in dictionary form.\"}", status=400, mimetype='application/json')

    def modify_user(self, request, user_id):
        is_admin = UsersController(self.app).is_admin(request)
        if is_admin == True:
            try:
                body = request.json
            except:
                return Response("{\"error\":\"You have not provided a body in your request.\"}", status=400, mimetype='application/json')
            try:
                self.users_serv.check_user_body(body)
                updated_obj = json.dumps(self.users_serv.modify_user(user_id, body))
                return Response(updated_obj, status=200, mimetype='application/json')
            except exce.IncorrectFields:
                return Response("{\"error\":\"You have entered incorrect fields in your body.\"}", status=400, mimetype='application/json')
            except exce.ObjectDoesntExist:
                return Response("{\"error\":\"This user does not exist.\"}", status=400, mimetype='application/json')
            except AttributeError:
                return Response("{\"error\":\"Please enter a body in dictionary form.\"}", status=400, mimetype='application/json')
        return is_admin

    def get_users(self, request):
        is_admin = self.is_admin(request)
        if is_admin == True:
            filters = request.args
            users = json.dumps(self.users_serv.get_users(filters))
            return Response(users, status=200, mimetype='application/json')
        return is_admin

    def del_user(self, request, user_id):
        is_admin = self.is_admin(request)
        if is_admin == True:
            try:
                self.users_serv.del_user(user_id)
                return Response("{\"success\":\"This user is deleted from our database.\"}", status=200, mimetype='application/json')
            except exce.ObjectDoesntExist:
                return Response("{\"error\":\"This user does not exist.\"}", status=400, mimetype='application/json')
        return is_admin
    
    def get_connected_user(self, request):
        try:
            bearer_token = request.headers['Authorization'].split(" ")[1]
        except:
            return Response("{\"error\":\"Authentication is necessary.\"}")
        if not bearer_token:
            return Response("{\"error\":\"Authentication is necessary.\"}")
        secret_key = self.app.config.get('SECRET_KEY')
        try:
            user_id = decode_auth_token(bearer_token, secret_key)
        except exce.ExpiredToken:
            return Response("{\"error\":\"Your bearer token is expired\"}")
        except exce.InvalidToken:
            return Response("{\"error\":\"Invalid bearer token\"}")
        return user_id

    def is_admin(self, request):
        user_id = self.get_connected_user(request)
        if type(user_id) == int:
            if self.users_serv.check_is_admin(user_id):
                return True
            return Response("{\"error\":\"You do not have sufficient rights to do this.\"}")
        return user_id