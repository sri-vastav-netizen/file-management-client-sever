"""
This file is the server program using async I/O
--------
"""
import asyncio
import signal
from commandhandler import CommandHandler

signal.signal(signal.SIGINT, signal.SIG_DFL)

def request(commandhandler, message):
    """[summary]

    Parameters
    ----------
    commandhandler : Object
        Create a commandhandler object specific to a client and hand it over to 
        request module.
    message : str
        Message Received from the client and handled by the server.
    """
    command = message.rstrip("\n").lstrip(" ").rstrip(" ").split(" ")[0]
    if command == "commands":
        return commandhandler.commands()

    if command == "register":
        if len(message.split(" ")) == 3:
            return commandhandler.register(message.split(" ")[1], message.split(" ")[2])
        return "Enter correct command"

async def handle_client(reader, writer):
    """
    This funtion handles the connection from the client,
    acknowledges the messages from the client

    Parameters
    ----------
    reader : Object
        Reads the data from the client socket
    writer : Object
        Writes the data to the client socket.
    """

    client_address = writer.get_extra_info("peername")
    server_log = f"{client_address} is connected !!!"
    print(server_log)
    commandhandler = CommandHandler()
    while True:
        data = await reader.read(4096)
        message = data.decode().strip()
        if message == "exit":
            break
        print(f"Received {message} from {client_address}")
        writer.write(str(request(commandhandler, message).encode()))
        await writer.drain()

    print("Closing the connection !!!")
    writer.close()

async def main():
    """
    Initiates the connection between the server and client.
    """

    server = await asyncio.start_server(request, "127.0.0.1", 8088)
    server_listening_ip = server.sockets[0].getsockname()
    print(f"Serving on {server_listening_ip}")
    async with server:
        await server.serve_forever()

asyncio.run(main())
