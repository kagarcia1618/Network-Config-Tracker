import json
import requests
from requests.exceptions import ConnectionError, Timeout, ConnectTimeout
import urllib3
from library.napalm_ssh import napalm_ssh

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def nxapi_cli(node_ip, cli_cmd, cli_type, username, password):
    '''
    node_ip - ip address of the device to be accessed
    cli_cmd - cli command to be executed to the device
    cli_type - nxapi cli access type
    '''
    url = 'https://{}/ins'.format(node_ip)
    payload = {
        "ins_api":{
            "version": "1.0",
            "type": cli_type,
            "chunk": "0",
            "sid": "1",
            "input": cli_cmd,
            "output_format": "json"
        }
    }
    header = {'content-type':'application/json'}
    try:      
        response = requests.post(
            url,
            verify=False,
            timeout=10,
            data=json.dumps(payload),
            headers=header,
            auth=(username,password)
        ).json()
        output = response['ins_api']['outputs']['output']
        return output['body']
    
    except (ConnectionError, Timeout, ConnectTimeout):
        return napalm_ssh('nxos_ssh',node_ip,[cli_cmd],username,password)