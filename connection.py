import base64
import requests
import urllib3
import configparser
import matplotlib.pyplot as plt
import numpy as np
from Email import get_acess_token
from Email import send_email
config = configparser.ConfigParser()
config.read('C:\\codigos\\BitDefender\\config.cfg')

urllib3.disable_warnings()
apiKey = config.get('api','api_Key')
print(apiKey)
loginString = apiKey + ":"

encodedBytes = base64.b64encode(loginString.encode())
encodedUserPassSequence = str(encodedBytes,'utf-8')
authorizationHeader = "Basic " + encodedUserPassSequence

apiEndpoint_Url = "https://cloud.gravityzone.bitdefender.com/api//v1.0/jsonrpc/licensing/"
request = '{"params": {},"jsonrpc": "2.0","method": "getLicenseInfo","id": "ad12cb61-52b3-4209-a87a-93a8530d91cb"}'
result = requests.post(apiEndpoint_Url,data=request,verify=False,headers= {"Content-Type":"application/json","Authorization":authorizationHeader})

if result.status_code == 200:
    response_data = result.json()
    print(response_data)
    
    if 'result' in response_data:
        result_info = response_data['result']


        if 'usedSlots' in result_info:
            used_slots = result_info['usedSlots']
            totalSlots = result_info['totalSlots']
            expiryDate = result_info['expiryDate']
            texto_um = (f"Total de licenças = {totalSlots}")
            print(f"Licencas usadas         : {used_slots}")
            print(f"Total de Licencas       : {totalSlots}")
            print(f"Vencimento das licenças : {expiryDate}")
            y = np.array([used_slots, totalSlots])
            mylabels = [f"Licenças usadas", f"Total de licenças"]

            def func(pct, allvals):
                absolute = int(pct / 100. * np.sum(allvals))
                return f"{absolute:d}"
            
            plt.title('Relatório de Licenças Mensal Selita')
            plt.pie(y, labels=mylabels, autopct=lambda pct: func(pct, y))
            img = plt.imread('C:\\codigos\\BitDefender\\Logomarca.png')
            plt.imshow(img, extent=[0, 10, 0, 10], zorder=0, aspect='auto')
            plt.figimage(img, xo=0,yo=0)
            plt.savefig('Relatorio Mensal.png')
            send_email(get_acess_token())
            
        else:
            print("A chave 'usedSlots' não foi encontrada em 'result_info'.")
    else:
        print("A chave 'result' não foi encontrada na resposta JSON.")
else:
    print(f"Erro na solicitação: Código {result.status_code}")
    print(result.text)