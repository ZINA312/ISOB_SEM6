import json
import time
import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key_from_password(password):
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

class AuthenticationServer:
    def __init__(self, tgs_secret_key):
        self.clients = {}
        self.tgs_secret_key = tgs_secret_key

    def register_client(self, client_id, password):
        key = generate_key_from_password(password)
        self.clients[client_id] = key

    def request_tgt(self, client_id, tgs_id):
        if client_id not in self.clients:
            raise Exception("Client not registered")
        
        client_key = self.clients[client_id]
        session_key = Fernet.generate_key()
        timestamp = int(time.time())
        
        tgt_data = {
            'client_id': client_id,
            'session_key': session_key.decode(),  
            'timestamp': timestamp,
            'lifetime': 3600
        }
        
        fernet_tgs = Fernet(self.tgs_secret_key)
        tgt = fernet_tgs.encrypt(json.dumps(tgt_data).encode())
        
        response_data = {
            'session_key': session_key.decode(),  
            'tgt': tgt.decode(),  
            'timestamp': timestamp,
            'lifetime': 3600
        }
        
        fernet_client = Fernet(client_key)
        return fernet_client.encrypt(json.dumps(response_data).encode())

class TicketGrantingServer:
    def __init__(self, tgs_secret_key):
        self.tgs_secret_key = tgs_secret_key
        self.services = {}

    def register_service(self, service_id, service_key):
        self.services[service_id] = service_key

    def request_service_ticket(self, tgt, authenticator, service_id):
        fernet_tgs = Fernet(self.tgs_secret_key)
        decrypted_tgt = json.loads(fernet_tgs.decrypt(tgt).decode())
        
        session_key = decrypted_tgt['session_key'].encode()  
        client_id = decrypted_tgt['client_id']
        
        fernet_session = Fernet(session_key)
        decrypted_auth = json.loads(fernet_session.decrypt(authenticator).decode())
        
        if decrypted_auth['client_id'] != client_id:
            raise Exception("Client ID mismatch")
        
        if time.time() - decrypted_auth['timestamp'] > 30:
            raise Exception("Authenticator expired")
        
        if service_id not in self.services:
            raise Exception("Service not registered")
        
        service_key = self.services[service_id]
        service_session_key = Fernet.generate_key()
        
        ticket_data = {
            'client_id': client_id,
            'service_session_key': service_session_key.decode(),  
            'timestamp': int(time.time()),
            'lifetime': 3600
        }
        
        fernet_service = Fernet(service_key)
        service_ticket = fernet_service.encrypt(json.dumps(ticket_data).encode())
        
        response_data = {
            'service_session_key': service_session_key.decode(),  
            'service_ticket': service_ticket.decode()  
        }
        
        return fernet_session.encrypt(json.dumps(response_data).encode())

class ApplicationServer:
    def __init__(self, service_key):
        self.service_key = service_key

    def verify_ticket(self, service_ticket, authenticator):
        fernet_service = Fernet(self.service_key)
        ticket_data = json.loads(fernet_service.decrypt(service_ticket).decode())
        
        session_key = ticket_data['service_session_key'].encode()  
        client_id = ticket_data['client_id']
        
        fernet_session = Fernet(session_key)
        auth_data = json.loads(fernet_session.decrypt(authenticator).decode())
        
        if auth_data['client_id'] != client_id:
            raise Exception("Client ID mismatch")
        
        if time.time() - auth_data['timestamp'] > 30:
            raise Exception("Authenticator expired")
        
        return True

if __name__ == "__main__":
    # Генерация ключей
    tgs_key = Fernet.generate_key()
    ap_key = Fernet.generate_key()

    # Инициализация серверов
    as_server = AuthenticationServer(tgs_key)
    tgs_server = TicketGrantingServer(tgs_key)
    ap_server = ApplicationServer(ap_key)

    # Регистрация клиента и сервиса
    as_server.register_client("alice", "password1234")
    tgs_server.register_service("file_server", ap_key)

    # Клиентская часть
    client = type('', (), {})()
    client.id = "alice"
    client.password = "password1234"

    # Аутентификация в AS
    client_key = generate_key_from_password(client.password)
    tgt_response = as_server.request_tgt(client.id, "tgs")
    response = Fernet(client_key).decrypt(tgt_response)
    tgt_data = json.loads(response.decode())
    client.session_key = tgt_data['session_key'].encode()  
    client.tgt = tgt_data['tgt'].encode()  

    # Получение сервисного билета
    authenticator = Fernet(client.session_key).encrypt(
        json.dumps({'client_id': client.id, 'timestamp': int(time.time())}).encode()
    )

    service_ticket_response = tgs_server.request_service_ticket(
        client.tgt, authenticator, "file_server"
    )

    service_data = json.loads(Fernet(client.session_key).decrypt(service_ticket_response).decode())
    client.service_session_key = service_data['service_session_key'].encode()  
    client.service_ticket = service_data['service_ticket'].encode()  

    # Доступ к сервису
    auth = Fernet(client.service_session_key).encrypt(
        json.dumps({'client_id': client.id, 'timestamp': int(time.time())}).encode()
    )

    print("Authentication successful:", ap_server.verify_ticket(client.service_ticket, auth))