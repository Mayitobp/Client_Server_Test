
import argparse
import threading
from client import Client
from server import Server
import logging


# Configure logging to record client-server interactions
logging.basicConfig(filename= 'client-server.log', level=logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")

def start_comm(host, port):
    # starts the server in a background thread to avoid blocking the client
    server = Server(host, port)
    server_thread = threading.Thread(target=server.start_server, daemon=True)
    server_thread.start()
    return server_thread

def main():
    # main function:  sets up and runs client-server communication
    
    # commands to set up port , host and number of chains parameters of client and server direct from command line
    parser = argparse.ArgumentParser(description="Cliente-Servidor para envío y recepción de cadenas.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Dirección IP del servidor.")
    parser.add_argument("--port", type=int, default=65432, help="Puerto de comunicación.")
    parser.add_argument("--num-chains", type=int, required=True, help="Número de cadenas a enviar.")

    args = parser.parse_args()


    server_thread = start_comm(args.host, args.port) # start server in background

    client = Client(args.host, args.port, args.num_chains)
    client.generate_file()
    client.send_file()

    server_thread.join() # wait for server thread to terminate

if __name__ == "__main__":
    main()