from flask import Flask, request, Response
import os

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

from controller.ApartmentsController import ApartmentController
from controller.UsersController import UsersController
from controller.ReservationsController import ReservationsController

@app.post('/v1/login/')
def login():
    return UsersController(app).login(request)

@app.post('/v1/register')
def register():
    return UsersController(app).register(request)

@app.get('/v1/users')
def get_users():
    return UsersController(app).get_users(request)

@app.delete('/v1/users/<int:user_id>')
def del_user(user_id):
    return UsersController(app).del_user(request, user_id)

@app.delete('/v1/users/')
def del_user_error():
    return Response("{\"error\":\"You have not entered the ID of the user you wish to delete.\"}")

@app.patch('/v1/users/<int:user_id>')
def modify_user(user_id):
    return UsersController(app).modify_user(request, user_id)

@app.patch('/v1/users/')
def modify_user_error():
    return Response("{\"error\":\"You have not entered the ID of the user you wish to modify.\"}")

@app.get('/v1/apartments/')
def get_aps():
    return ApartmentController(app).get_apartments(request)

@app.post('/v1/apartments/')
def add_ap():
    return ApartmentController(app).add_apartment(request)

@app.delete('/v1/apartments/<int:ap_id>')
def del_ap(ap_id):
    return ApartmentController(app).del_apartment(request, ap_id)

@app.delete('/v1/apartments/')
def del_ap_error():
    return Response("{\"error\":\"You have not entered the ID of the apartment you wish to delete.\"}")

@app.patch('/v1/apartments/<int:ap_id>')
def update_ap(ap_id):
    return ApartmentController(app).modify_apartment(request, ap_id)

@app.patch('/v1/apartments/')
def update_ap_error():
    return Response("{\"error\":\"You have not entered the ID of the apartment you wish to modify.\"}")

@app.get('/v1/my_aps/')
def get_my_aps():
    return ApartmentController(app).get_my_apartments(request)

@app.patch('/v1/availability_change/<int:ap_id>')
def change_availability(ap_id):
    return ApartmentController(app).change_availability(request, ap_id)

@app.patch('/v1/availability_change/')
def change_availability_error():
    return Response("{\"error\":\"You have not entered the ID of the apartment you wish to modify.\"}")

@app.post('/v1/reservations/')
def add_reservation():
    return ReservationsController(app).add_reservation(request)

@app.get('/v1/reservations/')
def get_reservations():
    return ReservationsController(app).get_reservation(request)

@app.delete('/v1/reservations/<int:reserv_id>')
def del_reservation(reserv_id):
    return ReservationsController(app).del_reservation(request, reserv_id)

@app.delete('/v1/reservations/')
def del_reservation_error():
    return Response("{\"error\":\"You have not entered the ID of the reservation you wish to delete.\"}")

@app.patch('/v1/reservations/<int:reserv_id>')
def update_reservation(reserv_id):
    return ReservationsController(app).modify_reservation(request, reserv_id)

@app.patch('/v1/reservations/')
def update_reservation_error():
    return Response("{\"error\":\"You have not entered the ID of the reservation you wish to modify.\"}")

if __name__ == "__main__":
    app.run()
