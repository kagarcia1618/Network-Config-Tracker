from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException

def napalm_ssh(driver,node_ip,cli_cmd,username,password):
    net_driver = get_network_driver(driver)
    device = net_driver(node_ip, username, password, optional_args={'global_delay_factor': 2})
    try:
        device.open()
        output = device.cli(cli_cmd)
        device.close()
        return output[cli_cmd[0]]
    except (ConnectionException):
        return False
