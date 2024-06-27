from flask import Flask, request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pprint import pprint
import base64
import json
import smtplib

app = Flask(__name__)

def send_mail(mail, html):
    try:
        # Configurações do servidor SMTP
        smtp_server = 'mail.portalagendabrasil.com'  # Insira o servidor SMTP que você está usando
        smtp_port = 587  # Porta do servidor SMTP (normalmente 587 para TLS)

        # Suas credenciais de email
        sender_email = 'admin@portalagendabrasil.com'
        password = 'i23697854O!'

        # Destinatário e conteúdo do email
        recipient_email = mail
        subject = 'Protocolo Agendamento'
        html_content = html

        # Criar uma mensagem MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Anexar o conteúdo HTML ao email
        message.attach(MIMEText(html_content, 'html'))

        # Estabelecer uma conexão com o servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Inicia uma conexão segura com o servidor SMTP
        server.login(sender_email, password)  # Faça login no servidor SMTP

        # Enviar o email
        server.sendmail(sender_email, recipient_email, message.as_string())

        print("SENDER")

        # Fechar a conexão com o servidor SMTP
        server.quit()

    except Exception as e:
        print("Erro ao enviar email:", str(e))

def check_approved():
    if request.method == 'POST':
        # Obtém os dados JSON da requisição
        json_data = request.json
        
        if "action" in json_data:
            if json_data["action"] == "payment.updated":
                return True
        
        return False

@app.route('/<path:path>', methods=['POST'])
def webhook(path):
    if not check_approved():
        return "", 200

    try:
        with open(f"./save/{base64.urlsafe_b64decode(path).decode()}.json", "r") as f:
            data = json.load(f)

            if data:
                send_mail(data["email"], data["html"])

        return "", 200
    except Exception as err:
        print(err)

        return "", 500

if __name__ == '__main__':
    # send_mail("edsonrobertosou@outlook.com", "")

    ssl_context = ('cert/cert.pem', 'cert/key.pem')
    app.run(ssl_context=ssl_context, host='0.0.0.0', port=443, debug=True)
