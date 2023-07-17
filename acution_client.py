import json
import socket
import encry_decrypt


class Auction_client():

    def __init__(self):
        self.target_ip = "localhost"
        self.target_port = 9190
        self.userKey = self.getting_key()
        self.client_menu()
        global user_info, info_datas

    def getting_key(self):
        userKey: str = input("Enter your encryption key for the whole process:")
        return userKey

    def client_runner(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.target_ip, self.target_port))
        return client  # to send and received data

    def client_menu(self):

        print("------------This is client menu:----------")
        client = self.client_runner()

        try:
            user_data = input("get:Get_all_information\nlogin:to login\nreg:to register"
                              "\nPress 1 to get auction info:\nPress 2 To Exit:")
            if user_data == 'info':
                # user_data = 'info'
                self.getDataClient(client)

            elif user_data == '2':
                print("Bye Bye .....")
                exit(-1)

            elif user_data == 'login':
                # user_data = 'login'
                self.login_client(client, user_data)

            elif user_data == 'reg':
                # user_data = 'reg'
                # self.register(client, user_data)
                self.register2(client, user_data)

            elif user_data == 'get':
                # user_data = 'get'
                self.getUserData(client)
                # self.getUserData2(client)

            else:
                print("Invalid option")
                self.client_menu()

            # self.client_menu()

        except Exception as cE:
            print("Client menu error: ", cE)
            self.client_menu()

    def getUserData(self, client):
        data_form = "get"
        self.sending_encrypted(client, data_form)
        # self.client_menu()
        exit(-1)

    def register2(self, client, user_data):
        print("-------------------register------------------")
        r_name = input("Enter your name: ")
        r_email = input("Enter your email: ")
        flag = self.email_checking(r_email)
        if flag == 1:
            print("Email pass ....")
            r_password = input("Enter your password: ")
            c_password = input("Confirm your password: ")
            if r_password == c_password:
                data_form = user_data+' '+str(r_name)+' '+str(r_email)+' '+str(c_password)
                self.sending_encrypted(client,data_form)
                exit(-1)
            else:
                print("Password does not match ....")
                self.register2(client, user_data)
        else:
            print("Email does not pass ....")
            self.register2(client, user_data)

    def email_checking(self, r_email):
        name_counter = 0
        for i in range(len(r_email)):
            if r_email[i] == '@':
                # print("Name End Here")
                break
            name_counter += 1

        print("Name counter: ", name_counter)

        email_name = r_email[0:name_counter]
        email_form = r_email[name_counter:]

        # print(email_name)
        print(email_form)

        # checking for name
        name_flag = 0
        email_flag = 0
        for i in range(len(email_name)):
            aChar = email_name[i]
            if (ord(aChar) > 31 and ord(aChar) < 48) or (ord(aChar) > 57 and ord(aChar) < 65) or (
                    ord(aChar) > 90 and ord(aChar) < 97) or (ord(aChar) > 122 and ord(aChar) < 128):
                name_flag = -1
                break

        domain_form = ["@facebook.com", "@ncc.com", "@mail.ru", "@yahoo.com", "@outlook.com", "@apple.com", "@zoho.com",
                       "@gmail.com"]

        for i in range(len(domain_form)):

            if domain_form[i] == email_form:
                email_flag = 1
                break

        if name_flag == -1 or email_flag == 0:
            return -1

        else:
            return 1

    def login_client(self, client, user_data):
        print("user data", user_data)
        print("--------------Login--------------")
        l_email = input("Enter your email... ")
        l_password = input("Enter your password... ")
        data_form = user_data + ' ' + l_email + ' ' + l_password
        user_data = data_form
        self.sending_encrypted(client, user_data)
        # self.client_menu()
        exit(-1)

    def getDataClient(self, client):
        data_form = 'info'
        self.sending_encrypted(client, data_form)
        # self.client_menu()
        exit(-1)

    def sending_encrypted(self, client, raw_data):
        global info_datas
        se_flag = -1
        print("Raw data Client : ", raw_data)
        encry = encry_decrypt.A3Encryption()
        decry = encry_decrypt.A3Decryption()
        encrypted_data = encry.start_encryption(raw_data, self.userKey)
        client.send(bytes(encrypted_data, "utf-8"))

        recv_info = client.recv(4096)
        recv_encrypted = recv_info.decode("utf-8")
        print("Received Encrypted Data : ", recv_encrypted)

        recv_decrypted = decry.startDecryption(recv_encrypted)
        datas = json.loads(recv_decrypted)
        # print("$:", type(datas), datas)
        info_datas = datas
        self.autions_item(info_datas)

    def autions_item(self, datas):
        for i in datas:
            print(info_datas[i])


if __name__ == "__main__":
    auction_client: Auction_client = Auction_client()
    while True:
        auction_client.client_menu()
