import socket      
import threading   
import logging     
import time       


class Server:
    # class to handle server-side logic
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind((self._host, self._port)) # bind socket to address
        

    def get_ponderation(self, chain: str) -> str:
        # calculates the weight of a chain based on specific rules
        # rule 1 : if 'aa' in any case combination exists, return 1000.00

        if any(pair in chain.lower() for pair in ["aa", "aA", "Aa", "AA"]):
            logging.warning(f"Double 'a' rule detected >> '{chain}'")
            return "1000.00"
        
        # normal calculation based on letters, numbers, and spaces
        letters = sum(c.isalpha() for c in chain)
        numbers = sum(c.isdigit() for c in chain)
        spaces = chain.count(" ")

        return f"{(letters * 1.5 + numbers * 2) / spaces:.2f}" if spaces > 0 else "INF"   
    
      
    def start_server(self):
        # starts the server and listens for incoming connections
        
        logging.info(f"Starting server on {self._host}:{self._port}...")
        self._sock.listen()
        
        conn, addr = self._sock.accept()
        threading.Thread(target=self.handle_client, args=(conn, addr)).start()

            
    def handle_client(self, conn, addr):
        # manages communication with a connected client
        
        logging.info(f"New connection from {addr}")
        start_time = time.time()
        
        with conn:
            while True:
                data = conn.recv(1024).decode() # real client data
                
                if not data or data == 'End': # termination signal
                    conn.close()
                    self._sock.close()
                    logging.info(f'Process completed in {time.time() - start_time:.2f} seconds.')
                    break

                logging.info(f"Received: {data}")
                response = self.get_ponderation(data) # process chain
                conn.sendall(f'Message received, compute_weight = {response}'.encode()) # send response
                logging.info(f"Sent: {response}")
        
        logging.info(f"Connection from {addr} closed")
        
        