from database.models import db

def check_table_defined(func):
    def wrapper(self, *args, **kwargs):
        if self.table is None:
            raise ValueError("You have not defined a queried table.")
        return func(self, *args, **kwargs)
    return wrapper

class CrudManager():

    def __init__(self, table = None):
        self.table = table
        
    @check_table_defined
    def find_all(self):
        return self.table.query.all() 

    @check_table_defined
    def find_by_id(self, id):
        return self.table.query.filter_by(id=id).first()

    @check_table_defined
    def find_by_kargs(self, **kargs):
        query_ = self.table.query
        for key, value in kargs.items():
            query_ = query_.filter(getattr(self.table, key) == value)
        return query_.all()

    @check_table_defined
    def insert(self, object):
        obj = self.table(**object)
        db.session.add(obj)
        db.session.commit()
        return obj.id

    @check_table_defined
    def update(self, id, **kargs):
        obj = self.find_by_id(id)
        if obj:
            for key, value in kargs.items():
                setattr(obj, key, value)
            db.session.commit()
            return obj.id
        return False
    
    @check_table_defined
    def delete(self, id):
        obj = self.find_by_id(id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False