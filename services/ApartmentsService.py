from repository.ApartmentsRepository import ApartmentsRepository
from repository.ReservationsRepository import ReservationsRepository
import exceptions.exceptions as exce

class ApartmentService:
    def __init__(self):
        self.aps_repo = ApartmentsRepository()
    
    def get_apartments(self, request_filters):
        available_filters = self.aps_repo.get_apartments_filters()
        filters = {}
        for arg in request_filters:        
            if arg in available_filters:
                filters[arg] = request_filters[arg]
        return self.aps_repo.get_apartments(filters)

    def check_body(self, body, data):
        for k, v in body.items():
            if k not in data.keys() or type(v) != data[k]:
                raise exce.IncorrectFields()
        return True
    
    def check_apartment_body_obligatory(self, body):
        obligatory_data = self.aps_repo.get_apartments_columns()
        if len(body.keys()) != len(obligatory_data.keys()):
            raise exce.NoMandatoryFields()
        return self.check_body(body, obligatory_data)
    
    def check_apartment_body(self, body):
        possible_data = self.aps_repo.get_apartments_columns()
        return self.check_body(body, possible_data)

    def add_apartments(self, body):
        return self.aps_repo.add_apartments(body)

    def modify_apartment(self, ap_id, body):
        return self.aps_repo.modify_apartment(ap_id, body)

    def modify_availability_apartment(self, ap_id, user_id):
        if self.aps_repo.check_is_proprio(ap_id, user_id):
            return self.aps_repo.update_availability(ap_id)
        raise exce.ObjectDoesntExist()

    def del_apartments(self, ap_id):
        ReservationsRepository().del_ap_reserv(ap_id)
        return self.aps_repo.del_apartment(ap_id)
    
