from qsaas.qsaas import Tenant
import json
import os
import time
from colorama import Fore, Style, init

init()

class Qlik():
    def __init__(self, api_key = None, tenant = None, tenant_id = None, config = None):
        self.api_key = api_key
        self.tenant = tenant
        self.tenant_id = tenant_id
        self.config = config
        self.tenant_c = Tenant(api_key=api_key, tenant = tenant, tenant_id=tenant_id, config=config)
    
    def Qlik_close(self):
        try: self.tenant_c.close()
        except: return BaseException
        
    def Qlik_users(self):
        users = self.tenant_c.get('users')
        for user in users: print(user['id'])
        
    def Qlik_spaces(self):
        spaces = self.tenant_c.get('spaces')
        for space in spaces: print(f"{space['name']} | {space['id']} | {space['type']}")
        
    def Qlik_Apps(self):
        apps = self.tenant_c.get('items', params={"resourceType":"app"})
        for app in apps: print(f"{app}")
    
    def app_info(self, app_name, space_id):
        apps = self.tenant_c.get('items', params={"resourceType":"app"})
        for app in apps: 
            if app_name == app['name'] and app['spaceId'] == space_id: return app
        return False
    
    def file_info(self, file_name):
        files = self.tenant_c.get('qix-datafiles')
        for file in files: 
            if file_name == file['name']: return file
        return False
    
    def space_info(self, space_name):
        spaces = self.tenant_c.get('spaces')
        for space in spaces: 
            if space_name == space['name']: return space
        return False
        
    def Upload_File(self, file_path: str = False, 
                    file_name: str = False, 
                    file_extension: str = False):
        try: 
            if file_extension: file_name = file_name + file_extension
            if file_path: 
                with open(os.path.join(file_path, file_name), 'rb') as f: file_content = f.read()
            else: 
                with open(file_name, 'rb') as f: file_content = f.read()
            self.tenant_c.post('qix-datafiles', file_content, 
                           params={"name": file_name})
        except Exception as e: return BaseException 
        return True
    
    def Delete_File(self, file_id):
        try: self.tenant_c.delete(f'qix-datafiles/{file_id}')
        except: return BaseException
        return True

    def reload_App(self, app_info: dict):
        reload_app =self.tenant_c.post('reloads', json.dumps({"appId": app_info['resourceId']}))
        reload_id = reload_app['id']
        status = None
        i = 1
        while status not in ['SUCCEEDED', 'FAILED']:
            time.sleep(1)
            status = self.tenant_c.get('reloads/' + reload_id)['status']
            if status not in ['SUCCEEDED', 'FAILED']:
                print(f"The Status of {Fore.YELLOW + app_info['name'] + Style.RESET_ALL} is {Fore.LIGHTCYAN_EX + status + Style.RESET_ALL}, Elapsed Time (Sec): {i}")
            i += 1
        print(self.tenant_c.get('reloads/' + reload_id)['log'])
        if status == 'SUCCEEDED': status = Fore.GREEN + status
        else: status = Fore.RED + status
        return status + Style.RESET_ALL, self.tenant_c.get('reloads/' + reload_id)['log']