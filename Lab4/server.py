import socket
import threading

HOST = '0.0.0.0'  # Слушать все интерфейсы
PORT = 12345       # Порт сервера
MAX_CONNECTIONS = 5  # Максимальное количество одновременных соединений

active_connections = []

def handle_client(client_socket, client_address):
    """
    Обработка подключения клиента.
    """
    print(f"[INFO] Подключен клиент: {client_address}")
    try:
        client_socket.settimeout(10)

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"[{client_address}] Получено: {data.decode('utf-8')}")
            
            response = f"Echo: {data.decode('utf-8')}"
            client_socket.sendall(response.encode('utf-8'))

    except socket.timeout:
        print(f"[WARNING] Таймаут соединения с {client_address}")
    except Exception as e:
        print(f"[ERROR] Ошибка при обработке клиента {client_address}: {e}")
    finally:
        print(f"[INFO] Соединение с {client_address} закрыто")
        active_connections.remove(client_socket)
        client_socket.close()

def start_server():
    """
    Запуск TCP-сервера.
    """
    global active_connections

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)

    print(f"[INFO] Сервер запущен на {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            if len(active_connections) >= MAX_CONNECTIONS:
                print(f"[WARNING] Превышено максимальное количество соединений: {MAX_CONNECTIONS}")
                client_socket.close()
                continue

            active_connections.append(client_socket)

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True  
            client_thread.start()

    except KeyboardInterrupt:
        print("[INFO] Сервер остановлен пользователем")
    finally:
        server_socket.close()

if __name__ == "main":
    start_server()