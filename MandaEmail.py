import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

with open('config.json', 'r') as file:
    dados = json.load(file)

url = dados["Url"]

#User = dados["User"]
User = "rpa"

Environment = dados["Environment"]
Environment = "protheus"

#destinatarios = ["WILSON.PALHARES@bomfuturo.com.br", "hianny.urt@bomfuturo.com.br"]
destinatarios = ["hianny.urt@bomfuturo.com.br"]

def enviar_warning(DESC):

    try:
        server_smtp = os.getenv('server_smtp')
        port = os.getenv('port')    
        sender_mail = os.getenv('sender_mail')
        password = os.getenv('password')

        subject = "WARNING NO ´Protheus_tir"
        body = f"""\
        <p>O LOG DEU UM WARNING</p>
        <p>WARNING : {DESC}</p>
        <p>O CONTAINER DOCKER hiannyurt/protheus_tir_bf:latest</p>
        <p>O USUARIO {User} ACESSOU A ACESSAR A BASE {url}</p>
        <p>VERIFIQUE SE O AMBIENTE {Environment} ESTA ATIVO</p>
        <p>OU A SENHA ATUAL EXPIROU. </p>"""

        message = MIMEMultipart()
        message["From"] = sender_mail
        message["To"] = ", ".join(destinatarios)  # Concatena os destinatários em uma string separada por vírgulas
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_mail, password)
        server.sendmail(sender_mail, destinatarios, message.as_string())  # Passa a lista de destinatários
        print('--------------------------------')
        print('Email warning enviado com sucesso')
        print('--------------------------------')

        server.quit()
    except Exception as e:
        print(f'Ocorreu um erro: {e}')

    return


def enviar_erro():
    try:
        server_smtp = os.getenv('server_smtp')
        port = os.getenv('port')    
        sender_mail = os.getenv('sender_mail')
        password = os.getenv('password')

        subject = "ERRO NO DOCKER_TIR"
        body = f"""\
        <p>NO MEIO DO PROCESSO OUVE UM ERRO</p>
        <p>O ERRO NAO AFETA DIRETAMENTE O FUNCIONAMENTE DO RPA</p>
        <p>VERIFIQUE SE O ROBO CONCLUIU A EXECUÇÃO NO BANCO</p>
        <p>A BASE USADO FOI: {url}</p>"""


        message = MIMEMultipart()
        message["From"] = sender_mail
        message["To"] = ", ".join(destinatarios)  # Concatena os destinatários em uma string separada por vírgulas
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_mail, password)
        server.sendmail(sender_mail, destinatarios, message.as_string())  # Passa a lista de destinatários
        print('--------------------------------')
        print('Email error enviado com sucesso')
        print('--------------------------------')

        server.quit()
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
    return

def enviar_temp_exc():
    try:
        server_smtp = os.getenv('server_smtp')
        port = os.getenv('port')    
        sender_mail = os.getenv('sender_mail')
        password = os.getenv('password')

        subject = "TEMPO EXECUÇÃO ELEVADO"
        body = f"""\
        <p>O TEMPO DE EXECUCAO DO ROBO EXCEDEU 40% DO TEMPO DA ULTIMA ROTINA </p>
        <p>A BASE USADO FOI: {url}</p>"""


        message = MIMEMultipart()
        message["From"] = sender_mail
        message["To"] = ", ".join(destinatarios)  # Concatena os destinatários em uma string separada por vírgulas
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        server = smtplib.SMTP(server_smtp, port)
        server.starttls()
        server.login(sender_mail, password)
        server.sendmail(sender_mail, destinatarios, message.as_string())  # Passa a lista de destinatários
        print('--------------------------------')
        print('Email tempo enviado com sucesso')
        print('--------------------------------')

        server.quit()
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
    return


if __name__ == "__main__":
    enviar_warning()
    enviar_erro()