import OTMrunReport
import CSV_
import os
import json
import time
from Tenant import Qlik
from colorama import Fore, Style, init
from datetime import datetime, timedelta
init()
ExceptionList = []

while True:
    configuration = json.load(open('config.json', 'r'))
    seconds = int(configuration['seconds'])
    minutes = int(configuration['minutes'])
    hours = int(configuration['hours'])
    os.system('cls')
    nQlik = Qlik(config='config.json')
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
        while True:
            print(f'Ejecutando: {Fore.GREEN + names_list[i] + Style.RESET_ALL} {datetime.now()}')
            try:
                report_resut = OTMrunReport.runReport(paths_list[i], server, header)
                CSV_.makeCSV(report_resut, names_list[i])
                break
            except Exception as e:
                ExceptionList.append(e)
                print(e)
                with open(configuration['excepcions_log'], 'w') as f:
                    for item in ExceptionList: f.write('%s\n' % item) 
        while True:
            print(f'Subiendo: {Fore.YELLOW + names_list[i] + Style.RESET_ALL} {datetime.now()}')
            try:
                if nQlik.file_info(names_list[i]+'.csv'):
                        file_id = nQlik.file_info(names_list[i]+'.csv')['id']
                        nQlik.Delete_File(file_id)
                nQlik.Upload_File(file_name=names_list[i],
                                    file_extension= '.csv')
                break 
            except Exception as e:
                ExceptionList.append(e)
                print(e)
                with open(configuration['excepcions_log'], 'w') as f:
                    for item in ExceptionList: f.write('%s\n' % item)
        if not i == reportCount: print(f'{Fore.BLUE + names_list[i] + Style.RESET_ALL} terminado | Faltan {Fore.YELLOW}{(reportCount-1 - i)}{Style.RESET_ALL} reportes por descargar {datetime.now()}')
    try:
        space_info = nQlik.space_info(configuration['Qlik_space'])
        app_info = nQlik.app_info(configuration['Qlik_app'], space_info['id'])
        nQlik.reload_App(app_info)
        nQlik.Qlik_close()
    except Exception as e:
        ExceptionList.append(e)
        with open(configuration['excepcions_log'], 'w') as f:
            for item in ExceptionList: f.write('%s\n' % item)
        print(ExceptionList)
    now = datetime.now()
    sleep_time = seconds + 60 * (minutes + 60 * hours)
    del configuration
    print(f'Actualizado: {now}')
    print(f'Proxima actualización: {now + timedelta(seconds=sleep_time)}')
    time.sleep(sleep_time)