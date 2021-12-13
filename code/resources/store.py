from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"msg": "Store Not Found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"msg": f"Store with name '{name}' already made: BAD REQUEST"}, 400
        
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"msg": "Error in SAVE TO DATABASE: SQLITE3 (Flask-SQLAlchemy, SQLAlchemy)"}, 500
        
        return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"msg": "Store deleted from Database (STORENAME can be INVALID STORENAME)"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}