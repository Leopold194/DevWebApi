from database.crud import CrudManager
from database.models import Apartments
import exceptions.exceptions as exce

class ApartmentsRepository:
    def __init__(self):
        self.crud = CrudManager(Apartments)

    def get_apartments_filters(self):
        default_filters = ['area', 'capacity', 'address', 'availability', 'night_price', 'proprio', 'id']
        ap = self.crud.find_all()
        if ap:
            ap_data = dict(ap[0].__dict__)
            ap_data.pop('_sa_instance_state')
            return list(ap_data.keys())
        return default_filters

    def get_apartments(self, filters):
        aps_data = {}
        for ap in self.crud.find_by_kargs(**filters):
            ap_data = dict(ap.__dict__)
            ap_data.pop('_sa_instance_state')
            aps_data[ap.id] = ap_data
        return aps_data
    
    def get_apartments_columns(self):
        default_column = {'area':float, 'capacity':int, 'address':str, 'availability':bool, 'night_price':float, 'proprio':int}
        ap = self.crud.find_all()
        if ap:
            ap_data = dict(ap[0].__dict__)
            ap_data.pop('_sa_instance_state')
            ap_data.pop('id')
            return {k:type(v) for k, v in ap_data.items()}
        return default_column

    def add_apartments(self, body):
        created_object_id = self.crud.insert(body)
        if created_object_id:
            created_object_data = self.crud.find_by_id(created_object_id).__dict__
            created_object_data.pop('_sa_instance_state')
            return created_object_data
        return exce.ObjectNotCreated()
    
    def modify_apartment(self, ap_id, body):
        updated_obj_id = self.crud.update(ap_id, **body)
        if updated_obj_id:
            updated_obj_data = self.crud.find_by_id(updated_obj_id).__dict__
            updated_obj_data.pop('_sa_instance_state')
            return updated_obj_data
        raise exce.ObjectDoesntExist()

    def update_availability(self, ap_id):
        updated_obj_data = self.crud.find_by_id(ap_id).__dict__
        self.crud.update(ap_id, availability=(not updated_obj_data["availability"]))
        updated_obj_data.pop('_sa_instance_state')
        updated_obj_data['availability'] = (not updated_obj_data["availability"])
        return updated_obj_data

    def check_is_proprio(self, ap_id, user_id):
        current_obj = self.crud.find_by_id(ap_id)
        if current_obj and current_obj.proprio == user_id:
            return True
        return False

    def del_apartment(self, ap_id):
        if self.crud.delete(ap_id):
            return True
        raise exce.ObjectDoesntExist()
    
    def get_ap_price(self, ap_id):
        ap = self.crud.find_by_id(ap_id)
        if ap:
            return ap.night_price
        raise exce.ObjectDoesntExist()