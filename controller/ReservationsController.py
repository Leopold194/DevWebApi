from database.models import Reservations
from database.crud import CrudManager
from flask import Response
from services.ReservationsServices import ReservationsService
from controller.UsersController import UsersController
import exceptions.exceptions as exce
import json

class ReservationsController:
    def __init__(self, app):
        self.crud = CrudManager(Reservations)
        self.reserv_serv = ReservationsService()
        self.app = app

    def get_reservation(self, request):
        is_admin = UsersController(self.app).is_admin(request)
        if is_admin == True:
            filters = request.args
            reservations = json.dumps(self.reserv_serv.get_reservations(filters))
            return Response(reservations, status=200, mimetype='application/json')
        return is_admin

    def del_reservation(self, request, reserv_id):
        is_admin = UsersController(self.app).is_admin(request)
        if is_admin == True:
            try:
                self.reserv_serv.del_reservation(reserv_id)
                return Response("{\"success\":\"This reservation is deleted from our database.\"}", status=200, mimetype='application/json')
            except exce.ObjectDoesntExist:
                return Response("{\"error\":\"This reservation does not exist.\"}", status=400, mimetype='application/json')
        return is_admin

    def add_reservation(self, request):
        this_user = UsersController(self.app).get_connected_user(request)
        if type(this_user) == int:
            try:
                body = request.json
            except:
                return Response("{\"error\":\"You have not provided a body in your request.\"}", status=400, mimetype='application/json')
            try:
                self.reserv_serv.check_reservation_body_obligatory(body)
                new_obj = json.dumps(self.reserv_serv.add_reservation(body, this_user))
                return Response(new_obj, status=200, mimetype='application/json')
            except exce.ObjectDoesntExist:
                return Response("{\"error\":\"This apartment does not exist.\"}", status=400, mimetype='application/json')
            except exce.IncorrectFields:
                return Response("{\"error\":\"You have entered incorrect fields in your body.\"}", status=400, mimetype='application/json')
            except exce.ObjectNotCreated:
                return Response("{\"error\":\"Your object could not be created.\"}", status=404, mimetype='application/json')
            except exce.NoMandatoryFields:
                return Response("{\"error\":\"You have not completed all the required fields.\"}", status=400, mimetype='application/json')
            except exce.ReservationNotPossible:
                return Response("{\"error\":\"This apartment is not available on these dates.\"}", status=400, mimetype='application/json')
            except exce.WrongDates:
                return Response("{\"error\":\"Please enter correct dates (YYYY-MM-DD).\"}", status=400, mimetype='application/json')
            except AttributeError:
                return Response("{\"error\":\"Please enter a body in dictionary form.\"}", status=400, mimetype='application/json')
        return this_user
    
    def modify_reservation(self, request, reserv_id):
        is_admin = UsersController(self.app).is_admin(request)
        if is_admin == True:
            try:
                body = request.json
            except:
                return Response("{\"error\":\"You have not provided a body in your request.\"}", status=400, mimetype='application/json')
            try:
                self.reserv_serv.check_reserv_body(body)
                updated_obj = json.dumps(self.reserv_serv.modify_reserv(reserv_id, body))
                return Response(updated_obj, status=200, mimetype='application/json')
            except exce.IncorrectFields:
                return Response("{\"error\":\"You have entered incorrect fields in your body.\"}", status=400, mimetype='application/json')
            except exce.ObjectDoesntExist:
                return Response("{\"error\":\"This reservation does not exist.\"}", status=400, mimetype='application/json')
            except AttributeError:
                return Response("{\"error\":\"Please enter a body in dictionary form.\"}", status=400, mimetype='application/json')
        return is_admin