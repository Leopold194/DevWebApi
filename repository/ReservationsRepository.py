from database.crud import CrudManager
from database.models import Reservations
import exceptions.exceptions as exce

class ReservationsRepository:
    def __init__(self):
        self.crud = CrudManager(Reservations)

    def get_reservation_columns(self):
        default_column = {'starting_date':str, 'ending_date':str, 'apartment':int}
        reserv = self.crud.find_all()
        if reserv:
            reserv_data = dict(reserv[0].__dict__)
            reserv_data.pop('_sa_instance_state')
            reserv_data.pop('id')
            reserv_data.pop('price')
            reserv_data.pop('customer')
            reserv_data['starting_date'] = ""
            reserv_data['ending_date'] = ""
            return {k:type(v) for k, v in reserv_data.items()}
        return default_column
    
    def check_disponibility(self, ap_id, starting, ending):
        reservations = self.crud.find_by_kargs(apartment = ap_id)
        for reservation in reservations:
            if (reservation.starting_date >= starting and reservation.starting_date <= ending) \
                or (reservation.ending_date >= starting and reservation.ending_date <= ending) \
                or (reservation.starting_date <= starting and reservation.ending_date >= ending):
                return False
        return True
    
    def create_reservation(self, body):
        created_object_id = self.crud.insert(body)
        if created_object_id:
            created_object_data = self.crud.find_by_id(created_object_id).__dict__
            created_object_data.pop('_sa_instance_state')
            return created_object_data
        return exce.ObjectNotCreated()