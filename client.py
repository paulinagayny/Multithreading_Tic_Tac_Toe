import socket
import threading
import os

class TicTacToe:

    active_game = False
    
    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = "X"
        self.player1 = "X"
        self.player2 = "0"
        self.mark = 0
        self.winner = None
        self.game_over = False
        self.not_first_turn = False
        self.other_move = -1

        self.counter = 0 #counter of turns

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        threading.Thread(target=self.handle_connection, args=(client,)).start()

    def handle_connection(self, client):

        print("Wait for a match")
        while 1:
            #waiting for a match
            data = client.recv(1024)
            if not data:
                continue

            self.mark = data.decode('utf-8')
            if self.mark == "X":
                while not self.game_over:
                    if self.not_first_turn == True:
                        data = client.recv(1024)
                        if not data:
                            break
                        data = data.decode('utf-8')
                        if data == "X" or data == "O":
                            self.turn = data

                        else:
                            self.other_move = data

                    while self.turn == "X":
                        move = input("Enter a move (row,column): ")
                        if self.check_valid_move(move.split(',')):
                            client.send(move.encode('utf-8'))
                            os.system('cls')
                            self.apply_move(client, move.split(','), "X")
                            self.not_first_turn = True
                            self.turn = "O"
                            client.send("O".encode())
                            print("Wait for your turn")
                        else:
                            print("Invalid move!")

                    if self.turn == "O":
                        if self.other_move != -1:
                            os.system('cls')
                            self.apply_move(client, self.other_move.split(','), "O")
                            self.other_move = -1

            else:
                while not self.game_over:
                    data = client.recv(1024)
                    if not data:
                        break
                    
                    data = data.decode('utf-8')

                    if data == "X" or data == "O":
                        self.turn = data

                    else:
                        self.other_move = data

                    while self.turn == "O":
                        move = input("Enter a move (row,column): ")
                        if self.check_valid_move(move.split(',')):
                            client.send(move.encode('utf-8'))
                            os.system('cls')
                            self.apply_move(client, move.split(','), "O")
                            self.turn = "X"
                            client.send("X".encode())
                            print("Wait for your turn")
                        else:
                            print("Invalid move!")

                    if self.turn == "X":
                        if self.other_move != -1:
                            os.system('cls')
                            self.apply_move(client, self.other_move.split(','), "X")
                            self.other_move = -1

    def apply_move(self, client, move, player):
        if self.game_over:
            client.send("over".encode())
            return
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()

        if self.check_if_won():
            if self.winner == self.mark:
                print("You win")
                client.send("over".encode())
                exit()
            elif self.winner != self.mark:
                print("You lose")
                client.send("over".encode())
                exit()
        else:
            if self.counter == 9:
                print("It is a tie")
                client.send("over".encode())
                exit()

    def check_valid_move(self, move):
        if len(move) <= 1 or len(move) >= 3:
            return False
        if len(move) == 2:
            check1 = int(move[0]) >= 0 and int(move[0]) <= 2 and int(move[1]) >= 0 and int(move[1]) <= 2
        if check1 == False:
            return False

        check2 = self.board[int(move[0])][int(move[1])] == " "

        return check2
            
    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
                
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.game_over = True
                return True

        #for diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]
            self.game_over = True
            return True
                
        return False

    def print_board(self):
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                #seperator for the rows
                print("--------------")

game = TicTacToe()
game.connect_to_game('localhost', 9999)
