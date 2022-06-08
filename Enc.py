from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad 
from Crypto.Random import get_random_bytes 
import base64
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

#the code that used to generate 2048 public, private key 
#key = RSA.generate(2048)
#private_key = key.export_key()
#fill_out = open("private_key.pem", "wb")
#fill_out.write(private_key)
#fill_out.close()
#public_key = key.publickey().export_key()
#fill_out = open("public_key.pem", "wb")
#fill_out.write(public_key)
#fill_out.close()


#generate 256 bits symmetric key 
sys_key = get_random_bytes(32) 


#C1=Enc(pk,k) k=sys_key
recipient_key = RSA.import_key(open("public_key.pem").read())
file_out = open("C1.bin", "wb")
cipher_rsa = PKCS1_OAEP.new(recipient_key)
C1 = cipher_rsa.encrypt(sys_key)
file_out.write(C1)
file_out.close()


#C2=Enc(k,M) k=sys_key M=jpg files
path = os.getcwd()
dirs =  os.listdir(path)

for file in dirs:
    if file.endswith('.jpg'):
        f_name, f_ext = os.path.splitext(file)   
        cipher = AES.new(sys_key, AES.MODE_CBC)
        with open(path+'/'+file,"rb") as jpg2string:
            converted_string = b64encode(jpg2string.read())    
        C2_bytes = cipher.encrypt(pad(converted_string, AES.block_size)) 
        C2= b64encode(C2_bytes).decode('utf-8')
        with open(path+'/'+f_name+'.bin',"wb") as enc_jpg:
            enc_jpg.write(C2_bytes)
        iv = b64encode(cipher.iv).decode('utf-8')
        with open(path+'/IV'+f_name+'.bin',"wb") as file:
            file.write(cipher.iv)
        os.remove(path+'/'+f_name+'.jpg')
