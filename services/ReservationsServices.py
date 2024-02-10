from repository.ReservationsRepository import ReservationsRepository
from repository.ApartmentsRepository import ApartmentsRepository
import exceptions.exceptions as exce
from datetime import datetime

class ReservationsService:
    def __init__(self):
        self.reserv_repo = ReservationsRepository()

    def del_reservation(self, reserv_id):
        return self.reserv_repo.del_reservation(reserv_id)

    def check_reservation_body_obligatory(self, body):
        obligatory_data = self.reserv_repo.get_reservation_columns()
        print(obligatory_data)
        if len(body.keys()) != len(obligatory_data.keys()):
            raise exce.NoMandatoryFields()
        for k, v in body.items():
            if k not in obligatory_data.keys() or type(v) != obligatory_data[k]:
                raise exce.IncorrectFields()
        return True

    def get_reservations(self, filters):
        available_filters = self.reserv_repo.get_reservations_filters()
        filters = {}
        for arg in filters:        
            if arg in available_filters:
                filters[arg] = filters[arg]
        return self.reserv_repo.get_reservations(filters)

    def add_reservation(self, body, user_id):
        try:
            body['starting_date'] = datetime.strptime(body['starting_date'], "%Y-%m-%d")
            body['ending_date'] = datetime.strptime(body['ending_date'], "%Y-%m-%d")
        except ValueError:
            raise exce.WrongDates()
        if self.reserv_repo.check_disponibility(body['apartment'], body['starting_date'], body['ending_date']):
            try:
                body['price'] = ApartmentsRepository().get_ap_price(body['apartment']) * (body['ending_date'] - body['starting_date']).days
            except:
                raise exce.ObjectDoesntExist()
            body['customer'] = user_id
            return self.reserv_repo.create_reservation(body)
        raise exce.ReservationNotPossible()
        