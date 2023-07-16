import json
import socket
import encry_decrypt


class Auction_client():

    def __init__(self):
        self.target_ip = "localhost"
        self.target_port = 9190
        self.userKey = self.getting_key()
        self.client_menu()
        global user_info

    def getting_key(self):
        userKey: str = input("Enter your encryption key for the whole process:")
        return userKey

    def client_runner(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))
        return client  # to send and received data

    def client_menu(self):

        print("------------This is client menu:----------")
        user_data = input("get:Get_all_information\nlogin:to login\nreg:to register"
                          "\nPress 1 to get auction info:\nPress 2 To Exit:")
        client = self.client_runner()
        if user_data == '1':
            # user_data = 'info'
            self.getDataClient(client)

        elif user_data == 'login':
            # user_data = 'login'
            # self.login_client(client, user_data)
            self.login_client(client)

        elif user_data == 'reg':
            user_data = 'reg'
            self.register_client(client, user_data)

        elif user_data == 'get':
            pass

        elif user_data == '2':
            print("Bye Bye .....")
            exit(-1)

    def register_client(self, client, user_data):
        print("-------------Register-------------")

    def login_client(self, client, user_data):
        print("user data", user_data)
        print("--------------Login--------------")
        l_email = input("Enter your email... ")
        l_password = input("Enter your password... ")
        data_form = user_data + ' ' + l_email + ' ' + l_password
        user_data = data_form
        self.sending_encrypted(client, user_data)

    def getDataClient(self, client):
        data_form = 'info'
        self.sending_encrypted(client, data_form)

    def sending_encrypted(self, client, raw_data):
        print("Raw data Client : ", raw_data)
        encry = encry_decrypt.A3Encryption()
        decry = encry_decrypt.A3Decryption()
        encrypted_data = encry.start_encryption(raw_data, self.userKey)
        client.send(bytes(encrypted_data, "utf-8"))

        recv_info = client.recv(4096)
        recv_encrypted = recv_info.decode("utf-8")
        # print("Received Encrypted Data : ", recv_encrypted)

        recv_decrypted = decry.startDecryption(recv_encrypted)
        datas = json.loads(recv_decrypted)
        print("$:", type(datas), datas)
        # for i in datas:
        #     print(datas[i])


if __name__ == "__main__":
    auction_client: Auction_client = Auction_client()

    while True:
        auction_client.client_menu()
