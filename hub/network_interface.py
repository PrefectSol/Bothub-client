import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import hashlib
import requests
import json

from utils.permissions import Permissions


class NetworkInterface:
    server_url = 'http://localhost'
    
    def __init__(self, id, secret):
        self._user_id = id
        self._user_secret = secret
        self._encoder = 'utf-8'
        
        hash_object = hashlib.sha256()
        hash_object.update((self._user_id + self._user_secret).encode(self._encoder))
        self._user_sign = hash_object.hexdigest()
    
    @staticmethod
    def generate_user(permissions: Permissions) -> dict:
        data = {'permissions': {'hostManagement': permissions.get_host_permission(),
                                'botManagement': permissions.get_bot_permission(),
                                'databaseView': permissions.get_database_permission()}}

        response = requests.post(url=f'{NetworkInterface.server_url}/auth', json=data)
        
        return {'code': response.status_code, 'answer': json.loads(response.text)}
    
    
    def delete_user(self):        
        data = {'user_id': self._user_id, 'user_sign': self._user_sign}
        response = requests.post(url=f'{NetworkInterface.server_url}/deauth', json=data)
        
        return {'code': response.status_code, 'answer': json.loads(response.text)}
    
    
    def create_host(self, host: dict):
        data = {'user_id': self._user_id, 'user_sign': self._user_sign, 'host': host}
        response = requests.post(url=f'{NetworkInterface.server_url}/createhost', json=data)
        
        return {'code': response.status_code, 'answer': json.loads(response.text)}
    
    
    def delete_host(self, host_id):
        data = {'user_id': self._user_id, 'user_sign': self._user_sign, 'host_id': host_id}
        response = requests.post(url=f'{NetworkInterface.server_url}/deletehost', json=data)
        
        return {'code': response.status_code, 'answer': json.loads(response.text)}
    
    
    def post_bot(self, bot_source, host_id):
        data = {'user_id': self._user_id, 'user_sign': self._user_sign, 'bot_source': bot_source, 'host_id': host_id}
        response = requests.post(url=f'{NetworkInterface.server_url}/postbot', json=data)
        
        return {'code': response.status_code, 'answer': json.loads(response.text)}
    
    
    def view(self):
        data = {'user_id': self._user_id, 'user_sign': self._user_sign}
        response = requests.post(url=f'{NetworkInterface.server_url}/view', json=data)
        
        return {'code': response.status_code, 'answer': json.loads(response.text)}