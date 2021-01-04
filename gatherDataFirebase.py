import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from Crypto.Cipher import AES
import base64
import json



def get_common_cipher():
    # AES key must be either 16, 24, or 32 bytes long
    COMMON_ENCRYPTION_KEY = 'asdjk@15r32r1234asdsaeqwe314SEFT'
    # Make sure the initialization vector is 16 bytes
    COMMON_16_BYTE_IV_FOR_AES = 'Land0f5n0wns0roW'
    return AES.new(str.encode(COMMON_ENCRYPTION_KEY),
                   AES.MODE_CBC,
                   str.encode(COMMON_16_BYTE_IV_FOR_AES))


def decrypt_with_common_cipher(ciphertext):
    common_cipher = get_common_cipher()
    raw_ciphertext = base64.b64decode(ciphertext)
    decrypted_message_with_padding = common_cipher.decrypt(raw_ciphertext)
    return decrypted_message_with_padding.decode('utf-8').strip()


def decrypt_json_with_common_cipher(json_ciphertext):
    json_string = decrypt_with_common_cipher(json_ciphertext)
    return json.loads(json_string)



def gatherData():
    #Decript the data from ligma.txt
    f = open("ligma.txt", 'r')
    text = f.read()
    f.close()

    x = decrypt_json_with_common_cipher(text)

    # Fetch the service account key JSON file contents
    #cred = credentials.Certificate('firebase-service-account.json')
    cred = credentials.Certificate(x)

    # Initialize the app with a custom auth variable, limiting the server's access
    try:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://merqueo-pro.firebaseio.com'
        })

        # The app only has access as defined in the Security Rules
        ref = db.reference('/vehicles')
        dataShoppers = ref.get()
    except:
        ref = db.reference('/vehicles')
        dataShoppers = ref.get()
    dataShoppers = json.dumps(dataShoppers)
    return(dataShoppers)

