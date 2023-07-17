import socket
import s_encrypt_and_decrypt
import ob
from mongodb_insert import *
import json
import random

# import pymongo

toReturn = None

# db server
connection_string = 'mongodb://localhost:27017/'
client = connect_to_mongodb(connection_string)
db_name = 'ncc_dip22'
collection_products_auction = 'products_auction'
collection_observer_info = 'observer_info'
collection_user_info = 'user_info'

decrypted_list = None


class Server():

    def __init__(self):
        self.ob = ob.Ob()
        self.decrypt = s_encrypt_and_decrypt.A3Decryption()
        self.encrypt = s_encrypt_and_decrypt.A3Encryption()
        self.server_ip = "localhost"
        self.server_port = 9190

    def main(self):

        auction_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        auction_server.bind((self.server_ip, self.server_port))
        auction_server.listen()

        print("Server listen on port:{} and ip{}".format(self.server_port, self.server_ip))

        try:
            while True:
                client, address = auction_server.accept()
                print("Accepted Connection from -{} : {}".format(address[0], address[1]))

                self.client_control(client)

        except Exception as err:
            print(err)

    def custom_decode(self, from_client, sock):
        # from_client = sock.recv(1024)
        data_list = from_client.decode("utf-8")
        print("data_list", data_list)

        decrypted = self.decrypt.startDecryption(data_list)
        print("#:", decrypted)
        decrypted_list = decrypted.split(' ')

        ob_recv = self.ob.get_received(decrypted_list[0])
        print("Ob data:", ob_recv)

        print('Decrypted data', decrypted)
        print('Decrypted_list data', decrypted_list)

        return decrypted_list

    def client_control(self, client):

        with client as sock:
            from_client = sock.recv(1024)
            decrypted_list = self.custom_decode(from_client, sock)

            data = ''
            if decrypted_list[0] == 'info':
                data = 'data received from client:' + decrypted_list[0]
                self.getDataInfo(sock, decrypted_list[0])

            elif decrypted_list[0] == 'login':
                print("server login --->", decrypted_list)
                self.login(decrypted_list, sock)

            elif decrypted_list[0] == 'reg':
                self.register(decrypted_list, sock)

            elif decrypted_list[0] == 'get':
                # self.getUserData(sock)
                self.getUserData2(sock, decrypted_list[0])

            else:
                print("Server: Invalid Option")
                data = {"error": -1, "data": decrypted_list}
                data = json.dumps(data)
                encrypted = self.encrypt.start_encryption(data, 'servertcp')
                sock.send(bytes(encrypted, "utf-8"))

            # encrypted = self.encrypt.start_encryption(data, 'servertcp')
            # sock.send(bytes(encrypted, "utf-8"))

    def getUserData2(self, sock, decrypted_list):
        # json -> encrypt -> encode -> send
        # json -> decrypt -> decode -> recv
        print("-----------[Get Data]----------")
        # filter_cols = {"_id": 0, "name": 1, "email": 1, "password": 0, "phone": 0, "info": 0, "point": 0, "money": 0}
        datas = read_documents(client, db_name, collection_user_info, {"_id": 0})
        print('data', datas)

        data_form = {}
        for i in datas:
            id = len(data_form)
            data_form.update({id: datas[i]})
            print("->", datas[i])

        print("data form ", data_form)
        datas = json.dumps(data_form)
        print("json data ", datas)
        encrypted = self.encrypt.start_encryption(datas, 'servertcp')
        sock.send(bytes(encrypted, "utf-8"))
        client.close()
        # self.observerAlert(decrypted_list)

    def getDataInfo(self, sock, decrypted_list):
        # json -> encrypt -> send
        print("-----------[Get Data]----------")
        data = read_documents(client, db_name, collection_products_auction, {"_id": 0})
        print('data', data)
        for i in data:
            print(data[i])
        data = json.dumps(data)
        print("json data ", data)
        encrypted = self.encrypt.start_encryption(data, 'servertcp')
        sock.send(bytes(encrypted, "utf-8"))
        client.close()
        self.observerAlert(decrypted_list)

    def login(self, decrypted_list, sock):
        print("login server ", decrypted_list)
        print("------------[Login]------------")
        l_email = decrypted_list[1]
        l_password = decrypted_list[2]
        flag = -1
        sms = {}
        filter_cols = {"_id": 0, "name": 1, "email": 1, "password": 1, "info": 1, "point": 1, "money": 1}
        db = client[db_name]
        collection = db[collection_user_info]
        documents = collection.find({}, filter_cols)
        for i in documents:
            if i["email"] == l_email and i["password"] == l_password:
                flag = 1
                sms = {"email": i["email"], "name": i["name"], "info": i["info"], "point": i["point"],
                       "money": i["money"]}
                sms = json.dumps(sms)
                break

        if flag == 1:
            print('Login data')
            # data = json.dumps(data)
            encrypted = self.encrypt.start_encryption(sms, 'servertcp')
            sock.send(bytes(encrypted, "utf-8"))
            # client.close()
        else:
            print("Server: Invalid Login Data")
            data = {"error": -1, "data": "user not found"}
            data = json.dumps(data)
            encrypted = self.encrypt.start_encryption(data, 'servertcp')
            sock.send(bytes(encrypted, "utf-8"))

        client.close()

    def register(self, decrypted_list, sock):
        r_flag = -1
        print("-----------[Register]----------")
        print("Register data from client >>>> : ", decrypted_list)
        user_datas = read_documents(client, db_name, collection_user_info, {"_id": 0})
        for i in user_datas:
            # print("loop >> ",user_datas[i])
            if user_datas[i]['email'] == decrypted_list[2]:
                # print(user_datas[i]['email'])
                r_flag = 1
                print("same email found: ", user_datas[i]['email'])
                break

        if r_flag == 1:
            data = {"error": -1, "data": "Account is already taken: "}
            print(data)
            data = json.dumps(data)
            print("json data ", data)
            encrypted = self.encrypt.start_encryption(data, 'servertcp')
            sock.send(bytes(encrypted, "utf-8"))
            client.close()
        else:
            name = decrypted_list[1]
            email = decrypted_list[2]
            password = decrypted_list[3]
            data_form = {"name": name, "email": email, "password": password}
            print("Register successfully:", data_form)
            create_document(client, db_name, collection_user_info, data_form)
            data = {"error": 0, "data": "Account created successfully... "}
            data = json.dumps(data)
            print("json data ", data)
            encrypted = self.encrypt.start_encryption(data, 'servertcp')
            sock.send(bytes(encrypted, "utf-8"))
            client.close()

    def observerAlert(self, data):
        random_id = random.randint(100000, 9999999)
        ob_flag = -1
        ob_send = self.ob.send_data(data)
        print("Ob send:", ob_send)
        if len(data) > 1 and len(data) == 3:
            print(data)
            ob_flag = 1

        if ob_flag == 1:
            name = data[1]
            email = data[2]
            data_form = {"username": name, "email": email, "client_request": str(ob_send)}
            create_document(client, db_name, collection_observer_info, data_form)
            print("Record observer")
        else:
            name = 'Guest' + str(random_id)
            email = None
            data_form = {"username": name, "email": email, "client_request": str(ob_send)}
            create_document(client, db_name, collection_observer_info, data_form)
            print("Record observer")


class Data:
    def __init__(self, data):
        self.data = data


if __name__ == "__main__":
    auction: Server = Server()
    auction.main()
