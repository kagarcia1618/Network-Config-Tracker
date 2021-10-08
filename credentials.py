from getpass import getpass
from library.encrypt import generate_key,encrypt_message

def extract(a):
    """
    a - exact filename of the data to be extracted
    """
    with open(a,'r') as i:
        return(i.read())

def main():
    try:
        extract('private/.secret.key')
        print('[INFO] Secret key located.')

    except (FileNotFoundError):
        print('[WARNING] Secret key not found.')
        print('[INFO] Generating secret key in private directory.')
        generate_key()
        print('[INFO] Secret key created.')

    netdev_user = encrypt_message(input('Network Device Username: ')).decode()
    netdev_pass = encrypt_message(getpass('Network Device Password: ')).decode()
    netbox_url = input('Netbox URL: ')
    netbox_token = encrypt_message(getpass('Netbox Token: ')).decode()
    gitlab_url = input('Gitlab URL: ')
    gitlab_token = encrypt_message(getpass('Gitlab Token: ')).decode()
    gitlab_project = encrypt_message(input('Gitlab Project Name (owner/project-name): ')).decode()

    credentials = f'{netdev_user},{netdev_pass},{netbox_token},{gitlab_token},{gitlab_project}'
    webportals = f'NETBOX={netbox_url}\nGITLAB={gitlab_url}'

    with open("private/credentials.txt", "w") as key_file:
        key_file.write(credentials)

    with open("private/webportals.txt", "w") as key_file:
        key_file.write(webportals)

    print('Credential and web portal details updated.')

if __name__ == '__main__':
    main()