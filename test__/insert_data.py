import pymongo
import random

connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip22"]
collection_user_info = database["user_info"]
collection_products_auction = database["products_auction"]
collection_observer_info = database["observer_info"]


def products():
    name = "Ancient pot " + str(random.randint(10, 10000))
    price = random.randint(1000, 1000000)
    data_form = {"name": name, "price": price}
    ids = collection_products_auction.insert_one(data_form)
    print("inserted id products:", ids.inserted_id)


def observer_info(i):
    username = "Thu Thu " + str(i)
    email = "Thu" + str(i) + "@gmail.com"
    client_request = "info"
    data_form = {"username": username, "email": email, "client_request": client_request}
    ids = collection_observer_info.insert_one(data_form)
    print("inserted id observer data:", ids.inserted_id)

def user_info():
    user_id = random.randint(10, 10000)
    name = "Thu Thu"+str(i)
    email: str = "thu" + str(i) + "@gmail.com"
    password: str = "pass"
    phone: int = 94537
    point: int = 100
    info: str = "User data is myat" + str(i) + "id : " + str(user_id)
    money: int = 0
    data_form = {"_id": user_id, "name":name, "email": email, "password": password, "phone": str(phone), "info": info,
                 "point": point, "money": money}
    ids = collection_user_info.insert_one(data_form)
    print("inserted id user_data:", ids.inserted_id)


if __name__ == '__main__':

    for i in range(5):
        user_info()
        products()
        observer_info(i)

