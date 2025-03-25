import socket
import random
import string
import logging
import time


class Client:
    # Class to handle client-side communication with the server
    def  __init__(self, host: str, port: int, num_chains: int):
        # Initialize client with server address, port, and chain configuration
        self._host = host
        self._port = port
        self.file_name = 'chains.txt'        # File to store generated chains  
        self.result_file = 'server_responses.txt'  # File to save server responses  
        self.num_chains = num_chains         # Number of chains to generate  
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket  

    def generate_random_string(self):
        
        # Generates a random string with letters, digits, and strategic spaces  
        length = random.randint(50, 100)      # Random length between 50-100 characters  
        chars = string.ascii_letters + string.digits  
        base_string = ''.join(random.choices(chars, k=length - 5))  # Base string without spaces  
        
        # Insert 3-5 spaces at random positions (excluding start/end)  
        space_positions = sorted(random.sample(range(1, length - 1), random.randint(3, 5)))  
        result = list(base_string)  
        for space_pos in space_positions:  
            result.insert(space_pos, ' ')  
        
        return ''.join(result) 

    def generate_file(self):
        
        # Generates a file containing all random chains  
        logging.info(f"Generating {self.num_chains} chains in {self.file_name}...")  
        chains = [self.generate_random_string() + "\n" for _ in range(self.num_chains)]  
        with open(self.file_name, "w", encoding="utf-8") as f:  
            f.writelines(chains)  
        logging.info("File generation completed.") 


    def send_file(self):
        
        # sends chains to the server and saves responses
        start_time = time.time()
        
        with open(self.file_name, "r", encoding="utf-8") as f, \
            open(self.result_file, "w", encoding="utf-8") as rf:
            
            self._sock.connect((self._host,self._port)) # establish connection
            logging.info("Connected to server.")
        
            for line in f:
                self._sock.sendall(line.strip().encode() + b"\n")  
                response = self._sock.recv(1024).decode().strip()  
                rf.write(response + "\n") # write responses to file
                
            self._sock.send(b"End") # send termination signal
            
            self._sock.recv(1024).decode().strip() #confirm closure

            logging.info("File processing completed.")
            logging.info(f"Server responses saved in {self.result_file}")

        total_time = time.time() - start_time
        logging.info(f"Process completed in {total_time:.2f} seconds.")
        