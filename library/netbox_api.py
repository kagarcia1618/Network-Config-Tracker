import pynetbox
import requests
import urllib3
from library.extract import extract
from library.encrypt import decrypt_message

urllib3.disable_warnings()
session = requests.Session()
session.verify = False
nb = pynetbox.api(
    url=extract('private/webportals.txt').splitlines()[0].split('=')[1],
    token=decrypt_message(extract('private/credentials.txt').split(',')[2].encode())
)
nb.http_session = session

def get_data():
    return [ i for i in nb.dcim.devices.all() ]