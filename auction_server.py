import socket
import s_encrypt_and_decrypt
import ob
from mongodb_insert import *
import json

toReturn = None

# db server
connection_string = 'mongodb://localhost:27017/'
client = connect_to_mongodb(connection_string)
db_name = 'ncc_dip22'
collection_products_auction = 'products_auction'
collection_observer_info = 'observer_info'
collection_user_info = 'user_info'


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

    def client_control(self, client):

        with client as sock:
            from_client = sock.recv(1024)
            data_list = from_client.decode("utf-8")

            decrypted = self.decrypt.startDecryption(data_list)
            print("#:", decrypted)
            decrypted_list = decrypted.split(' ')
            ob_recv = self.ob.get_received(decrypted_list[0])
            print("Ob data:", ob_recv)

            print('Decrypted data', decrypted)
            print('Decrypted_list data', decrypted_list)

            data = ''
            if decrypted_list[0] == 'info':
                data = 'data received from client:' + decrypted_list[0]
                self.getData(sock)
                self.observerAlert(decrypted_list[0])

            elif decrypted_list[0] == 'login':
                print("server login --->", decrypted_list)
                self.login(decrypted_list, sock)

            elif decrypted_list[0] == 'reg':
                self.register(decrypted_list, sock)

            elif decrypted_list[0] == 'get':
                pass

            else:
                print("Server: Invalid Option")
                data = {"error": -1}
                data = json.dumps(data)
                encrypted = self.encrypt.start_encryption(data, 'servertcp')
                sock.send(bytes(encrypted, "utf-8"))

            # encrypted = self.encrypt.start_encryption(data, 'servertcp')
            # sock.send(bytes(encrypted, "utf-8"))

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
            data = {"error": -1}
            data = json.dumps(data)
            encrypted = self.encrypt.start_encryption(data, 'servertcp')
            sock.send(bytes(encrypted, "utf-8"))

        client.close()

    def register(self, decrypted_list, sock):
        print("-----------[Register]----------")

    def observerAlert(self, data):
        ob_send = self.ob.send_data(data)
        print("Ob send:", ob_send)
        data_form = {"username": "Thu Thu", "email": "thu1@gmail.com", "client_request": str(ob_send)}
        create_document(client, db_name, collection_observer_info, data_form)
        print("Record observer")

    def getData(self, sock):
        # json -> encrypt -> send
        print("-----------[Get Data]----------")
        data = read_documents(client, db_name, collection_products_auction, {"_id": 0})
        print('data', data)
        data = json.dumps(data)
        encrypted = self.encrypt.start_encryption(data, 'servertcp')
        sock.send(bytes(encrypted, "utf-8"))
        client.close()

    # def for_observer(self):
    #     # to_return = self.decrypted_data
    #     #
    #     # self.decrypted_data='n'
    #     return self.decrypted_data


class Data:
    def __init__(self, data):
        self.data = data


if __name__ == "__main__":
    auction: Server = Server()
    auction.main()
