from Tenant import Qlik 

Q = Qlik(api_key='eyJhbGciOiJFUzM4NCIsImtpZCI6IjZlYWEzNjdiLWM2MTUtNDhlNi1iNGQ1LWRmNTgwNDVkOWE3ZiIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiMU5JR2F6aUZsRzY3dHhQSU1udHlWUTZzX2R5WVJDUzkiLCJqdGkiOiI2ZWFhMzY3Yi1jNjE1LTQ4ZTYtYjRkNS1kZjU4MDQ1ZDlhN2YiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNjRiYWVjZDVkYjk0NTE2NzI4ZDdlZmFiIn0.6Eb7GaZhh2-eU0enRMODJMxKsN0R7u4sSaNm-YC2I_gdC_c4oC83QgWkTftkqL5HPOVHvzFxk1M4TSQ-QSKI_qG8n3U8g1CYAN9mePtk3D5mR6n3WXMWDM2wmkyInDjF',
         tenant='cy9q7hypi26aug7.us.qlikcloud.com',
         tenant_id='1NIGaziFlG67txPIMntyVQ6s_dyYRCS9')

Q.reload_App(Q.app_info('Posicionamiento de Unidades', '65ea3cf62538edf0f16c7b28'))
input('Presiona enter para cerrar')