import socket                          
import threading          
import paramiko                                                                                        

host_key = paramiko.RSAKey.generate(2048)                                     
port = 2222                                                                   

class SSHServer(paramiko.ServerInterface):                                    
    def __init__(self):
        self.event = threading.Event()
                                       
    def check_auth_password(self, username, password):                        
        print(username,password)                                              
        return paramiko.AUTH_FAILED                                           
                                       
    def check_auth_publickey(self, username, key):                            
        return paramiko.AUTH_FAILED    
                                       
    def get_allowed_auths(self, username):                                  
        return 'password,publickey'                                           
                                                                              
def handle_client(client):      
    transport = paramiko.Transport(client)                                    
    transport.add_server_key(host_key)                                        

    server = SSHServer()
    transport.start_server(server=server)                         
                                                                                                                                                            
    channel = transport.accept(1)
    if channel is None:                
        transport.close() 
        return    

    print(f'Authenticated: {channel.getpeername()}')                          
    channel.send('Welcome to the SSH server!\n')         
    channel.close()
    transport.close()                                                         
                                       
def start_server():                    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
        server_socket.bind(('0.0.0.0', port))                                 
        server_socket.listen(10)
                                                                              
        print(f'SSH server listening on port {port}')                         

        while True:     
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))                                                                   
            client_thread.start()
                                       
if __name__ == '__main__':
    start_server()
