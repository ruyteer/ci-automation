import imaplib
import email
from email.header import decode_header
from datetime import datetime

# Configurações de login e servidor
IMAP_SERVER = 'outlook.office365.com'
EMAIL_ACCOUNT = 'ruarocha@universal.org'
PASSWORD = 'yamahaS900'

def ler_emails():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, PASSWORD)
        print("Login bem-sucedido!")
        
        # Seleciona a caixa de entrada
        mail.select('inbox')
        
        # Procura por todos os emails
        result, data = mail.search(None, 'ALL')
        email_ids = data[0].split()
        print(result, data, email_ids)

        emails = []
        
        for email_id in email_ids:
            result, data = mail.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]
            
            # Decodifica o email
            msg = email.message_from_bytes(raw_email)

            # Decodifica o assunto
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')
            
            # Pega o remetente
            from_ = msg['From']
            
            # Pega a data e converte para um formato legível
            date_ = msg['Date']
            date_ = datetime.strptime(date_, '%a, %d %b %Y %H:%M:%S %z')
            date_ = date_.strftime('%Y-%m-%d %H:%M')

            # Armazena informações em um dicionário
            emails.append({
                'subject': subject,
                'from': from_,
                'date': date_,
            })
        
        mail.logout()  # Mova o logout aqui para garantir que todos os emails sejam lidos
        return emails
    except imaplib.IMAP4.error as e:
        print(f"Falha no login: {e}")

# Para testar a função
if __name__ == "__main__":
    emails = ler_emails()
    for email in emails:
        print(email)
