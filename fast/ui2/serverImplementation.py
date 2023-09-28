import socket

randomStr = """Based on your input, get a random alpha numeric string. The random string generator creates a series of numbers and letters that have no pattern. These can be helpful for creating security codes.With this utility you generate a 16 character output based on your input of numbers and upper and lower case letters.  Random strings can be unique. Used in computing, a random string generator can also be called a random character string generator. This is an important tool if you want to generate a unique set of strings. The utility generates a sequence that lacks a pattern and is random.Throughout time, randomness was generated through mechanical devices such as dice, coin flips, and playing cards. A mechanical method of achieving randomness can be more time and resource consuming especially when a large number of randomized strings are needed as they could be in statistical applications.  Computational random string generators replace the traditional mechanical devices. Possible applications for a random string generator could be for statistical sampling, simulations, and cryptography.  For security reasons, a random string generator can be useful. The generation of this type of random string can be a common or typical task in computer programming.  Some forms of randomness concern hash or seach algorithms.  Another task that is random concerns selecting music tracks.In statistical theory, randomization is an important principle with one possible application involving survey sampling.Many applications of randomization have caused several methods to exist for generating random data. Lottery games is one current application. Slot machine odds are another use of random number generators."""

HOST = ''
PORT = 8000

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    url = request.split()[1]
    response = f"HTTP/1.1 200 OK\nContent-type: text/html\nContent-length: {len(randomStr)}\n\n<h1>Hello, world! You requested {url}</h1><p>{randomStr}</p>".encode()

    client_socket.send(response)
    client_socket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Serving on port {PORT}")

    while True:
        client_socket, address = server_socket.accept()
        handle_request(client_socket)