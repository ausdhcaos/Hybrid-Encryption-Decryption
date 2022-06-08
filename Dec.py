from base64 import b64decode
from Crypto.Util.Padding import unpad 
from base64 import b64encode
import base64 
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

path = os.getcwd()

#k=Dec(sk,C1)
file_in = open("C1.bin", "rb")
private_key = RSA.import_key(open("private_key.pem").read())
C1_byte = file_in.read(private_key.size_in_bytes())
cipher_rsa = PKCS1_OAEP.new(private_key)
k = cipher_rsa.decrypt(C1_byte)
file_in.close()
os.remove("C1.bin")


#M=Dec(k,C2)
dirs =  os.listdir(path)
key = k
 
for file in dirs:
    if file.endswith('.bin') and file.startswith(('C1','IV')) is False:
        f_name, f_ext = os.path.splitext(file)
        try:
            enc_file = open(file,'rb')
            enc_jpg_byte = enc_file.read()
            enc_file.close()
            C2 = b64decode(b64encode(enc_jpg_byte).decode('utf-8'))
            iv_file = open(path+'/IV'+f_name+'.bin',"rb")
            IV_byte = iv_file.read()
            os.remove(path+'/IV'+f_name+'.bin')
            iv= b64decode(b64encode(IV_byte).decode('utf-8'))
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(C2),AES.block_size)
        except ValueError:
            print("Incorrect decryption")
        except KeyError:
            print("Incorrect Key")
            
        dec_jpg = open(f_name+'.jpg','wb')
        dec_jpg.write(base64.b64decode(pt+b'=='))
        dec_jpg.close()
        os.remove(path+'/'+f_name+'.bin')