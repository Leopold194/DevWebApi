from database.models import Apartments
from database.crud import CrudManager
from flask import Response
from services.ApartmentsService import ApartmentService
from controller.UsersController import UsersController
import exceptions.exceptions as exce


from connection.functions import decode_auth_token

class ApartmentController:
    def __init__(self, app):
        self.crud = CrudManager(Apartments)
        self.aps_serv = ApartmentService()
        self.app = app

    def get_apartments(self, request):
        filters = request.args
        aps = self.aps_serv.get_apartments(filters)
        return Response("{\"content\":"+str(aps)+"}", status=200, mimetype='application/json')

    def get_my_apartments(self, request):
        filters = dict(request.args)
        this_user = UsersController(self.app).get_connected_user(request)
        if type(this_user) == int:
            filters['proprio'] = this_user
            aps = self.aps_serv.get_apartments(filters)
            return Response("{\"content\":"+str(aps)+"}", status=200, mimetype='application/json')
        return this_user

    def change_availability(self, request, ap_id):
        this_user = UsersController(self.app).get_connected_user(request)
        if type(this_user) == int:
            try:
                updated_obj = self.aps_serv.modify_availability_apartment(ap_id, this_user)
                return Response("{\"content\":"+str(updated_obj)+"}", status=200, mimetype='application/json')
            except exce.ObjectDoesntExist:
                return Response("{\"error\":\"This apartment does not exist.\"}", status=400, mimetype='application/json')
        return this_user

    def add_apartment(self, request):
        is_admin = UsersController(self.app).is_admin(request)
        if is_admin == True:
            try:
                body = request.json
            except:
                return Response("{\"error\":\"You have not provided a body in your request.\"}", status=400, mimetype='application/json')
            try:
                self.aps_serv.check_apartment_body_obligatory(body)
                new_obj = self.aps_serv.add_apartments(body)
                return Response("{\"content\":"+str(new_obj)+"}", status=200, mimetype='application/json')
            except exce.IncorrectFields:
                return Response("{\"error\":\"You have entered incorrect fields in your body.\"}", status=400, mimetype='application/json')
            except exce.ObjectNotCreated:
                return Response("{\"error\":\"Your object could not be created.\"}", status=404, mimetype='application/json')
            except exce.NoMandatoryFields:
                return Response("{\"error\":\"You have not completed all the required fields.\"}", status=400, mimetype='application/json')
        return is_admin

    def modify_apartment(self, request, ap_id):
        is_admin = UsersController(self.app).is_admin(request)
        if is_admin == True:
            try:
                body = request.json
            except:
                return Response("{\"error\":\"You have not provided a body in your request.\"}", status=400, mimetype='application/json')
            try:
                self.aps_serv.check_apartment_body(body)
                updated_obj = self.aps_serv.modify_apartment(ap_id, body)
                return Response("{\"content\":"+str(updated_obj)+"}", status=200, mimetype='application/json')
            except exce.IncorrectFields:
                return Response("{\"error\":\"You have entered incorrect fields in your body.\"}", status=400, mimetype='application/json')
            except exce.ObjectDoesntExist:
                return Response("{\"error\":\"This apartment does not exist.\"}", status=400, mimetype='application/json')
        return is_admin

    def del_apartment(self, request, ap_id):
        is_admin = UsersController(self.app).is_admin(request)
        if is_admin == True:
            try:
                self.aps_serv.del_apartments(ap_id)
                return Response("{\"success\":\"This apartment is deleted from our database.\"}", status=200, mimetype='application/json')
            except exce.ObjectDoesntExist:
                return Response("{\"error\":\"This apartment does not exist.\"}", status=400, mimetype='application/json')
        return is_admin