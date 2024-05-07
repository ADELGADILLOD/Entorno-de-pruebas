import OTMrunReport
import os
import json
from Tenant import Qlik
from colorama import Fore, Style, init
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

init()
ExceptionList = []
threads = []

while True:
    configuration = json.load(open('config.json', 'r'))
    server = configuration['OTM_server']
    header = OTMrunReport.headers(configuration['OTM_user'], 
                                  configuration['OTM_password'])
    paths_list, names_list = OTMrunReport.getFolderContents(configuration['OTM_folder'],
                                header,
                                server)
    reportCount = len(paths_list)

    print(f'Reportes a Descargar:')
    for i in range(reportCount): print(f'{i+1}: {Fore.YELLOW + names_list[i] + Style.RESET_ALL}')   
    print(f'Se descargarán {Fore.MAGENTA}{reportCount}{Style.RESET_ALL} reportes')
    for i in range(reportCount):
        print(f'Ejecutando: {Fore.GREEN + names_list[i] + Style.RESET_ALL}')
        try:
            with ThreadPoolExecutor(max_workers = 4) as executor:
                threads.append(executor.submit(OTMrunReport.runReport, paths_list[i], server, header))
                if not i == reportCount: print(f'{Fore.BLUE + names_list[i] + Style.RESET_ALL} terminado | Faltan {Fore.YELLOW}{(reportCount-1 - i)}{Style.RESET_ALL} reportes por descargar') 
        except Exception as e:
            ExceptionList.append(e)

            print(e)
            with open(configuration['excepcions_log'], 'w') as f:
                for item in ExceptionList: f.write('%s\n' % item)