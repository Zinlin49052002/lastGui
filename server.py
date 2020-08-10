import base64
import hashlib
import os
import json
import mysql.connector as mc
from socket import AF_INET, socket, SOCK_STREAM,gethostbyname,gethostname
from threading import Thread
from Cryptodome.Cipher import AES
from Cryptodome import Random

# For AES Encryptiion
BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
unpad = lambda s: s[0:-ord(s[-1:])]
# We use the symmetric Encryption So this password have to be the same in both client and server
password = "852020"

def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))
 
def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))
#bytes.decode(decrypt(s.recv(1024),password))
    
def acceptIncomingConnection():
    while True:
        client , clientAddr = server.accept()
        print("%s : %s has connected."% clientAddr)
        addresses[client] = clientAddr
        # print(client) # the whole data of connection
        # print(addresses[client]) # client IP addr
        Thread(target=handleClient,args=(client,)).start() # Create a thread for each client
def handleClient(client):
    while True:
        connetionStart = bytes.decode(decrypt(client.recv(bufsiz),password))
        data = json.loads(connetionStart)
        # to signup
        if data["to"] == "signup":
            cur.execute(dbQuery["checkUsername"].format(data["username"]))
            checkUsername = cur.fetchall()
            #check wherethere username is avaliable 
            if checkUsername:
                validReply = {"to":"valid","msg":"Username already exists!"}
                validReply = json.dumps(validReply)
                client.send(encrypt(validReply,password))
            #if it is avaliable insert it into database
            else :
                cur.execute(dbQuery["signup"].format(data["username"],data["email"],data["ps"]))
                con.commit()
        # to login
        elif data["to"] == "login":
            cur.execute(dbQuery["login"].format(data["username"],data["ps"]))
            login = cur.fetchall()
            # check wherethere username or password is correct
            if not login:
                loginReply = {"to":"loginReply","msg":"Wrong Username or Password!"}
                loginReply = json.dumps(loginReply)
                client.send(encrypt(loginReply,password))
            # if correct, we put them in a dict to kepp track of who is online
            else :
                clients[client] = [login[0][0],data["username"]]

clients = {}
addresses = {}
# Database Query 
dbQuery = {"userinfo":"""create table userinfo (id int primary key not null AUTO_INCREMENT, username varchar(100) not null, email varchar(100) not null, password varchar(50) not null);""",
           "signup" : """insert into userinfo (username,email,password) values ("{}","{}","{}");""","checkUsername":"""select username from userinfo where username="{}";""",
           "login" : """select id from userinfo where username="{}" and password="{}";""" }

# Server Info
host = ""
port = 33000
bufsiz = 1024
addr = (host,port)
# Create socket and bind IP and port
server = socket(AF_INET,SOCK_STREAM)
server.bind(addr)

# Start *
# Note -- We use MySQL
# Creating a connection with db
while True:
    user = input("Enter Database username : ")
    dbpassword = input("Enter Password : ")
    try : 
        con = mc.connect(host="localhost",user=user,password=dbpassword)
        os.system('cls')
        break
    except :
        os.system('cls')
        print("Wrong Username or Password!")
# Create a Cursor 
cur = con.cursor()
cur.execute("show databases")
alldb = cur.fetchall()
# Checking wherethere needed database exist if not we will create 
if ("livechat",) not in alldb:
    cur.execute("create database livechat")
    cur.execute("use livechat")
    cur.execute(dbQuery["userinfo"])
cur.execute("use livechat")

# Get Server IP
print("Server IP : "+gethostbyname(gethostname()))

if __name__ == "__main__":
    server.listen(5)
    acceptThread = Thread(target=acceptIncomingConnection)
    acceptThread.start()
    acceptThread.join()
    server.close()
    