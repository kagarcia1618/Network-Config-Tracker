import gitlab
import requests
from gitlab.exceptions import GitlabHttpError, GitlabGetError
from library.extract import extract
from library.encrypt import decrypt_message

url=extract('private/webportals.txt').splitlines()[1].split('=')[1]
token=decrypt_message(extract('private/credentials.txt').split(',')[3].encode())
project_name=decrypt_message(extract('private/credentials.txt').split(',')[4].encode())

gl = gitlab.Gitlab(url, private_token=token)
project = gl.projects.get(project_name)

def get_config(hostname):
    try:
        data = project.files.get(file_path='configs/{}.cfg'.format(hostname), ref='main')
        return data.decode().decode()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, GitlabHttpError, GitlabGetError):
        return False

def post_config(hostname,new_config):
    try:
        data = project.files.get(file_path='configs/{}.cfg'.format(hostname), ref='main')
        data.content = new_config
        data.save(branch='main', commit_message='{} configuration updated'.format(hostname))
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, ):
        return False

def create_config(hostname,new_config):
    try:
        project.files.create(
            {'file_path': 'configs/{}.cfg'.format(hostname),
            'branch': 'main',
            'content': new_config,
            'author_email': 'garciak@acrc.a-star.edu.sg',
            'author_name': 'Kenneth',
            'commit_message': 'Created new configuration for {}'.format(hostname)}
        )
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, ):
        return False