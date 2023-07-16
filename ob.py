# This is ob program for servertcp and client actions
# from mongodb_insert import *

class Ob:
    def __init__(self):
        print("Starting OB Program!")
        # db server
        # self.connection_string = 'mongodb://localhost:27017/'
        # self.client = connect_to_mongodb(self.connection_string)
        # self.db_name = 'ncc_dip22'
        # self.collection_observer_info = 'observer_info'

    def get_received(self,data):
        print("Received",data)
        return data


    def send_data(self,data):
        print("Sent:",data)
        return data

    # def recordData(self):
    #     data = {"username":"Thu Thu","email":"thu1@gmail.com","client_request":str()}
    #     create_document(self.client, self.db_name, self.collection_observer_info, data)
