from database.models import Reservations
from database.crud import CrudManager
from flask import Response
from services.ReservationsServices import ReservationsService
from controller.UsersController import UsersController
import exceptions.exceptions as exce

class ReservationsController:
    def __init__(self, app):
        self.crud = CrudManager(Reservations)
        self.reserv_serv = ReservationsService()
        self.app = app

    def add_reservation(self, request):
        this_user = UsersController(self.app).get_connected_user(request)
        if type(this_user) == int:
            try:
                body = request.json
            except:
                return Response("{\"error\":\"You have not provided a body in your request.\"}", status=400, mimetype='application/json')
            try:
                self.reserv_serv.check_reservation_body_obligatory(body)
                new_obj = self.reserv_serv.add_reservation(body, this_user)
                return Response("{\"content\":"+str(new_obj)+"}", status=200, mimetype='application/json')
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
        return this_user