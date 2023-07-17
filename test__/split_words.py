import json
from mongodb_insert import  *

# data = ['asdf',"thu thu","thu0@gmail.com"]
# # dd = data[3]
# # print(dd)
#
# if len(data) > 1 and len(data) == 3:
#     print(data)

# print(len(data))
# for i in data:
#     print(i)

# data_form = {0: {'name': 'Thu Thu0', 'email': 'thu0@gmail.com', 'password': 'pass', 'phone': '94537',
#                  'info': 'User data is myat0id : 7609', 'point': 100, 'money': 0},
#              1: {'name': 'Thu Thu1', 'email': 'thu1@gmail.com', 'password': 'pass', 'phone': '94537',
#                  'info': 'User data is myat1id : 4297', 'point': 100, 'money': 0},
#              2: {'name': 'Thu Thu2', 'email': 'thu2@gmail.com', 'password': 'pass', 'phone': '94537',
#                  'info': 'User data is myat2id : 7433', 'point': 100, 'money': 0},
#              3: {'name': 'Thu Thu3', 'email': 'thu3@gmail.com', 'password': 'pass', 'phone': '94537',
#                  'info': 'User data is myat3id : 3928', 'point': 100, 'money': 0},
#              4: {'name': 'Thu Thu4', 'email': 'thu4@gmail.com', 'password': 'pass', 'phone': '94537',
#                  'info': 'User data is myat4id : 8371', 'point': 100, 'money': 0}
#              }

connection_string = 'mongodb://localhost:27017/'
client = connect_to_mongodb(connection_string)
db_name = 'ncc_dip22'
collection_products_auction = 'products_auction'
collection_observer_info = 'observer_info'
collection_user_info = 'user_info'
#
# data_form = read_documents(client, db_name, collection_products_auction, {"_id": 0})
#
# data = json.dumps(data_form)
# print("Type ",type(data), data)
#
# e_data = json.loads(data)
# print("Type ",type(e_data), e_data)

# json_string = '{"name": "John", "age": 30, "city": "New York"}'
#
# try:
#     data = json.loads(json_string)
#     print(data)
# except json.JSONDecodeError as e:
#     print(f"JSON decoding error: {e}")


user_datas = read_documents(client, db_name, collection_user_info,{"_id":0,"email":1})
for i in user_datas:
    print(user_datas[i])
    if user_datas[i]['email'] == decrypted_list[2]:
        print("Account is already taken: ")
    else:
        print("Register successfully:")
        document = {"name":decrypted_list[1],"password":decrypted_list[2]}
        create_document(client,db_name,collection_user_info,document)
