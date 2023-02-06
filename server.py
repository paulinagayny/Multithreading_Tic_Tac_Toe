import socket
import threading

class TicTacToe:

    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.number_of_waiting_clients = 0

        self.counter = 0

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))

        while 1:
            server.listen(10)
            client1, addr1 = server.accept()
            client2, addr2 = server.accept()
            self.number_of_waiting_clients += 2

            #2 clients
            if (self.number_of_waiting_clients == 2):
                #New match begins
                self.number_of_waiting_clients -= 2
                t = threading.Thread(target=self.handle_clients, args=(client1, client2,))
                t.start()
            else:
                print(self.number_of_waiting_clients + "clients wait for a game")

        server.close()

    def handle_clients(self, client1, client2):
        client1.send("X".encode())
        client2.send("O".encode())

        while 1:
            while 1:
                data1 = client1.recv(1024)
                if not data1:
                    break
                data1 = data1.decode('utf-8')

                if data1 == "over":
                    client1.close()
                    client2.close()
                    exit()

                if data1 != "X" and data1 != "O":
                    if self.check_valid_move(data1.split(',')):
                        client2.send(data1.encode())

                if data1 == "O":
                    client1.send("O".encode())
                    client2.send("O".encode())
                    break

            while 1:
                data2 = client2.recv(1024)
                if not data2:
                    break
            
                data2 = data2.decode('utf-8')

                if data2 == "over":
                    client1.close()
                    client2.close()
                    exit()

                if data2 != "X" and data2 != "O":
                    if self.check_valid_move(data2.split(',')):
                        client1.send(data2.encode())

                if data2 == "X":
                    client1.send("X".encode())
                    client2.send("X".encode())
                    break

    def check_valid_move(self, move):
        return self.board[int(move[0])][int(move[1])] == " "

game = TicTacToe()
game.host_game('localhost', 9999)