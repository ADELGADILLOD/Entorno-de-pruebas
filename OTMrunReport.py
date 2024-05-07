import requests
import base64
import re
import gc
import xml.etree.ElementTree as ET

def __decode_base64__(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.
    """
    # Convertimos la cadena de texto a bytes
    data_bytes = data.encode('utf-8')

    data_bytes = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data_bytes)
    missing_padding = len(data_bytes) % 4
    if missing_padding:
        data_bytes += b'=' * (4 - missing_padding)
    return base64.b64decode(data_bytes, altchars)

def getFolderContents(patern_path,
                      headers,
                      server):
    SoapPathResponse = r'.//{http://xmlns.oracle.com/oxp/service/PublicReportService}'
    url = f"https://{server}.oraclecloud.com:443/xmlpserver/services/ExternalReportWSSService?WSDL"
    soapQueryRequestPath = f""" 
        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" 
                    xmlns:pub="http://xmlns.oracle.com/oxp/service/PublicReportService">
        <soap:Header/>
        <soap:Body>
            <pub:getFolderContents>
                <pub:folderAbsolutePath>
                    {patern_path}
                </pub:folderAbsolutePath>
            </pub:getFolderContents>
        </soap:Body>
        </soap:Envelope>"""
    try:
        response = requests.post(url, data=soapQueryRequestPath.encode('utf-8'), headers=headers)
        absp = ET.fromstring(response.content)
        paths, names = [path.text for path in absp.findall(f'{SoapPathResponse}absolutePath')], [name.text for name in absp.findall(f'{SoapPathResponse}displayName')]
        response.close()
        return paths, names
    except Exception as e: return e
def runReport(absolutepath,
              server,
              headers,
              sizeOfDataChunkDownload = -1):
    url = f"https://{server}.oraclecloud.com:443/xmlpserver/services/ExternalReportWSSService?WSDL"

    soapQueryRequest = f"""
        <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" 
                        xmlns:pub="http://xmlns.oracle.com/oxp/service/PublicReportService">
            <soap:Header/>
            <soap:Body>
                <pub:runReport>
                    <pub:reportRequest>
                        <pub:attributeFormat></pub:attributeFormat>
                        <pub:parameterNameValues>
                        <pub:item>
                            <pub:name></pub:name>
                            <pub:values>
                                <pub:item></pub:item>
                            </pub:values>
                        </pub:item>
                        </pub:parameterNameValues>
                        <pub:reportAbsolutePath>{absolutepath}</pub:reportAbsolutePath>
                        <pub:sizeOfDataChunkDownload>{sizeOfDataChunkDownload}</pub:sizeOfDataChunkDownload>
                    </pub:reportRequest>
                </pub:runReport>
            </soap:Body>
        </soap:Envelope>"""
    try:
        response = requests.post(url, data=soapQueryRequest.encode('utf-8'), headers=headers)
        root = ET.fromstring(response.content)
        try:
            report_bytes = root.find('.//{http://xmlns.oracle.com/oxp/service/PublicReportService}reportBytes').text
            response.close()
            return __decode_base64__(report_bytes).decode('utf-8')
        except:
            content = response.content
            response.close()
            return content
    except Exception as e:
        print(f'Ha ocurrido el error {e}')
        return e

def headers(user: str, pas: str):
    return {
            'Content-Type': 'application/soap+xml;charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Apache-HttpClient/4.5.5 (Java/16.0.2)',
            'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pas}'.encode()).decode()
            }
gc.collect()

