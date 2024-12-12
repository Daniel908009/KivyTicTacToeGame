from kivy.uix.settings import text_type
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import random

# this is the popup class for settings
class SettingsPopup(Popup):
    def send_info(self, caller):
        self.caller = caller
        self.ids.gridSize.text = str(caller.grid_size)
        self.ids.winCount.text = str(caller.win_count)
        self.ids.aiPlayer.text = caller.ai_player
        self.ids.aiDifficulty.text = caller.ai_difficulty
    def apply_settings(self):
        if self.ids.gridSize.text != '' and int(self.ids.gridSize.text) > 0 and self.ids.winCount.text != '' and int(self.ids.winCount.text) > 0 and int(self.ids.winCount.text) <= int(self.ids.gridSize.text):
            self.caller.grid_size = int(self.ids.gridSize.text)
            self.caller.fill_grid()
            self.caller.win_count = int(self.ids.winCount.text)
            self.caller.ai_player = self.ids.aiPlayer.text
            self.caller.ai_difficulty = self.ids.aiDifficulty.text
            print(self.caller.ai_player, self.caller.ai_difficulty)
            self.dismiss()

# this is the grid button class used in the main grid
class GridButton(Button):
    def send_info(self, caller, row, col):
        self.caller = caller
        self.row = row
        self.col = col
    def click(self):
        if self.text == '':
            self.text = self.caller.current_player
            self.caller.current_player = 'X' if self.caller.current_player == 'O' else 'O'
            self.caller.check_winner(self)
            if self.caller.ai_player == 'AI' and self.text == 'X' and not self.caller.game_over:
                self.ai_move()
    def ai_move(self):
        # getting the dificulty, this is used to get the depth of the minimax algorithm
        if self.caller.ai_difficulty == 'Easy':
            depth = 2
        elif self.caller.ai_difficulty == 'Medium':
            depth = 4
        elif self.caller.ai_difficulty == 'Hard':
            depth = 6
        # getting the best move
        best_move = self.ai_choice(depth)
        print(str(best_move) + ' is the best move')
        # making the move
        self.caller.grid[best_move[0]][best_move[1]].click()
    def ai_choice(self, depth):
        index_depth = 0
        moves = []
        #moves = [(0,0),(0,1), (0,4), (0,2)]
        #moves_to_remove = []
        #for move in moves:
        #    print(move)
        #    if self.caller.grid[move[0]][move[1]].text == 'O':
        #        moves_to_remove.append(move)
        #for move in moves_to_remove:
        #    moves.remove(move)
        # getting all the possible moves
        for i in range(self.caller.grid_size):
            for j in range(self.caller.grid_size):
                if self.caller.grid[i][j].text == '':
                    moves.append([i, j])
        # if there is a winning move, return it
        #print(moves)
        for move in moves:
            if self.check_if_winner(move):
                print('winning move')
                return move
        return moves[random.randint(0, len(moves)-1)]
        
    def check_if_winner(self, move):
        copy_grid = []
        #print(move)
        for i in range(self.caller.grid_size):
            copy_grid.append([])
            for j in range(self.caller.grid_size):
                copy_grid[i].append(self.caller.grid[i][j].text)
        #print(move)
        copy_grid[move[0]][move[1]] = 'O'
        for i in range(self.caller.grid_size):
            print(copy_grid[i])
        # checking both horizontal options
        checked = 0
        buttons_of_player = 0
        while buttons_of_player < self.caller.win_count+1 and checked < self.caller.win_count:
            try:
                if copy_grid[move[0]][move[1] + checked] == 'O':
                    buttons_of_player += 1
                    print('button of player at ' + str(move[0]) + ' ' + str(move[1] + checked))
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.caller.win_count+1 and checked < self.caller.win_count:
            try:
                if copy_grid[move[0]][move[1] - checked] == 'O':
                    buttons_of_player += 1
            except:
                break
            checked += 1
        print(buttons_of_player)
        if buttons_of_player >= self.caller.win_count + 1:
            print("decided by horizontal")
            print(move)
            checked = 0
            return True
        # checking both vertical options
        #checked = 0
        #buttons_of_player = 0
        #while buttons_of_player < self.caller.win_count+1 and checked < self.caller.win_count:
        #    try:
        #        if copy_grid[move[0] + checked][move[1]] == 'O':
        #            buttons_of_player += 1
        #    except:
        #        break
        #    checked += 1
        #checked = 0
        #while buttons_of_player < self.caller.win_count+1 and checked < self.caller.win_count:
        #    try:
        #        if copy_grid[move[0] - checked][move[1]] == 'O':
        #            buttons_of_player += 1
        #    except:
        #        break
        #    checked += 1
        #if buttons_of_player >= self.caller.win_count + 1:
        #    print("decided by vertical")
        #    print(move)
        #    return True
        return False

# this is the main grid class of the app
class MainGrid(GridLayout):
    def settings(self):
        popup = SettingsPopup()
        popup.send_info(self)
        popup.open()
    def reset(self):
        self.current_player = 'X'
        self.ids.currentPlayer.text = 'Current player: ' + self.current_player
        self.game_over = False
        self.fill_grid()
    def fill_grid(self):
        self.current_player = 'X'
        game_grid = self.ids.gameGrid
        game_grid.clear_widgets()
        self.grid = []
        for i in range(self.grid_size):
            self.grid.append([])
            for j in range(self.grid_size):
                grid_button = GridButton()
                grid_button.send_info(self, i, j)
                game_grid.add_widget(grid_button)
                self.grid[i].append(grid_button)
        # its a bit weird to set the cols, and then return it as well, but it is necessary and it works
        game_grid.cols = self.grid_size
        return self.grid_size
    def check_winner(self, button_clicked):
        buttons_of_player = 0
        winner_buttons = []
        # checking both horizontal options
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row][button_clicked.col + checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row][button_clicked.col + checked])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row][button_clicked.col - checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row][button_clicked.col - checked])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1: # the plus one is there because the button that was clicked last is counted twice
            self.winner(button_clicked.text, winner_buttons)
        # checking both vertical options
        buttons_of_player = 0
        checked = 0
        winner_buttons = []
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row + checked][button_clicked.col].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row + checked][button_clicked.col])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row - checked][button_clicked.col].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row - checked][button_clicked.col])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1:
            self.winner(button_clicked.text, winner_buttons)
        # checking the first pair of diagonal options
        buttons_of_player = 0
        checked = 0
        winner_buttons = []
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row + checked][button_clicked.col + checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row + checked][button_clicked.col + checked])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row - checked][button_clicked.col - checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row - checked][button_clicked.col - checked])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1:
            self.winner(button_clicked.text, winner_buttons)
        # checking the second pair of diagonal options
        buttons_of_player = 0
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row - checked][button_clicked.col + checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row - checked][button_clicked.col + checked])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if self.grid[button_clicked.row + checked][button_clicked.col - checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(self.grid[button_clicked.row + checked][button_clicked.col - checked])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1:
            self.winner(button_clicked.text, winner_buttons)
    def winner(self, winner, winner_buttons): 
        self.ids.currentPlayer.text = 'Winner is: ' + winner
        self.game_over = True
        for button in self.ids.gameGrid.children:
            button.disabled = True
        for button in winner_buttons:
            button.background_color = (0, 1, 0, 1)

# app class
class TicTacToeApp(App):
    def build(self):
        return MainGrid()

# running the app
if __name__ == '__main__':
    TicTacToeApp().run()