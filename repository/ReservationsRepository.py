from database.crud import CrudManager
from database.models import Reservations
import exceptions.exceptions as exce

class ReservationsRepository:
    def __init__(self):
        self.crud = CrudManager(Reservations)

    def del_reservation(self, reserv_id):
        if self.crud.delete(reserv_id):
            return True
        raise exce.ObjectDoesntExist()

    def del_ap_reserv(self, ap_id):
        for reserv in self.crud.find_by_kargs(apartment=ap_id):
            self.crud.delete(reserv.id)
        return True
        
    def del_user_reserv(self, user_id):
        for reserv in self.crud.find_by_kargs(customer=user_id):
            self.crud.delete(reserv.id)
        return True

    def get_reservation_columns(self, creating = True):
        default_column = {'starting_date':str, 'ending_date':str, 'apartment':int}
        reserv = self.crud.find_all()
        if reserv:
            reserv_data = dict(reserv[0].__dict__)
            reserv_data.pop('_sa_instance_state')
            reserv_data.pop('id')
            if creating:
                reserv_data.pop('price')
                reserv_data.pop('customer')
            reserv_data['starting_date'] = ""
            reserv_data['ending_date'] = ""
            return {k:type(v) for k, v in reserv_data.items()}
        return default_column
    
    def check_disponibility(self, reservation_id, starting, ending):
        reservations = self.crud.find_by_kargs(apartment = reservation_id)
        for reservation in reservations:
            if (reservation.starting_date >= starting and reservation.starting_date <= ending) \
                or (reservation.ending_date >= starting and reservation.ending_date <= ending) \
                or (reservation.starting_date <= starting and reservation.ending_date >= ending):
                return False
        return True
    
    def get_reservations_filters(self):
        default_filters = ['starting_date', 'ending_date', 'apartment', 'customer', 'price', 'id']
        reservations = self.crud.find_all()
        if reservations:
            reservations_data = dict(reservations[0].__dict__)
            reservations_data.pop('_sa_instance_state')
            return list(reservations_data.keys())
        return default_filters

    def create_reservation(self, body):
        created_object_id = self.crud.insert(body)
        if created_object_id:
            created_object_data = self.crud.find_by_id(created_object_id).__dict__
            created_object_data.pop('_sa_instance_state')
            return created_object_data
        return exce.ObjectNotCreated()
    
    def get_reservations(self, filters):
        reservations_data = {}
        for reservation in self.crud.find_by_kargs(**filters):
            reservation_data = dict(reservation.__dict__)
            reservation_data.pop('_sa_instance_state')
            reservations_data[reservation.id] = reservation_data
        return reservations_data
    
    def modify_reserv(self, reserv_id, body):
        updated_obj_id = self.crud.update(reserv_id, **body)
        if updated_obj_id:
            updated_obj_data = self.crud.find_by_id(updated_obj_id).__dict__
            updated_obj_data.pop('_sa_instance_state')
            return updated_obj_data
        raise exce.ObjectDoesntExist()