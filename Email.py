import requests
import json
import base64

from datetime import datetime

dt_hr = datetime.now()
dt_hr = dt_hr.strftime('%m/%Y')

name_file = "RelatorioMensal.png"
with open("C:\\codigos\\BitDefender\\Relatorio Mensal.png", "rb") as file:
    attachment_content_base64 = base64.b64encode(file.read()).decode('utf-8')

# Função para enviar e-mail
def send_email(access_token):
    graph_api_url = 'https://graph.microsoft.com/v1.0/me/sendMail'

    email_message = {
        "message": {
            "subject": "Relatório Mensal das Licenças BitDefender",
            "body": {
                "contentType": "Text",
                "content": (f"Relatório Mensal Referente ao Mês {dt_hr} ")
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": ""
                    }
                }
            ],''

            "attachments":[
                {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": name_file,
                    "contentType": "image/png",
                    "contentBytes": attachment_content_base64
                }
            ]       
        }
    }

    email_json = json.dumps(email_message)

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    response = requests.post(graph_api_url, headers=headers, data=email_json)

    if response.status_code == 202:
        pass

def get_acess_token():
    # Informe suas credenciais e configurações aqui
    client_id = ""
    client_secret = ""
    scopes = ["https://graph.microsoft.com/.default"]
    token_url = "https://login.microsoftonline.com/f11c815a-6b17-4f64-acbd-f5c8662147f4/oauth2/v2.0/token"

    token_data = {
        'grant_type': 'password',
        'scope': ' '.join(scopes),
        'client_id': client_id,
        'client_secret': client_secret,
        'username': '',
        'password': ''
    }

    token_response = requests.post(token_url, data=token_data)
    
    # Verifique se a solicitação de token foi bem-sucedida
    if token_response.status_code == 200:
        token_json = token_response.json()
        access_token = token_json.get('access_token')
        return access_token
        send_email()
    else:
        #print("Erro ao obter o access token. Código de status:", token_response.status_code)
        #print("Conteúdo da resposta:", token_response.text)
        return None