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
            self.caller.check_winner(self, self.caller.grid)
            if self.caller.ai_player == 'AI' and self.text == 'X' and not self.caller.game_over:
                self.ai_move()
    def ai_move(self):
        # getting the best move
        best_move = self.ai_choice()
        print(str(best_move) + ' is the chosen move')
        # making the move
        self.caller.grid[best_move[0]][best_move[1]].click()
    def ai_choice(self):
        moves = []
        for i in range(self.caller.grid_size):
            for j in range(self.caller.grid_size):
                if self.caller.grid[i][j].text == '':
                    moves.append((i,j))
        for i in range(self.caller.grid_size):
            for j in range(self.caller.grid_size):
                if self.caller.grid[i][j].text != '':
                    if (i,j) in moves:
                        moves.remove((i,j))
        chosen = random.choice(moves)
        grid_copy = []
        for i in range(self.caller.grid_size):
            grid_copy.append([])
            for j in range(self.caller.grid_size):
                grid_copy[i].append(self.caller.grid[i][j].text)
        #print(grid_copy)
        for move in moves:
            grid_copy[move[0]][move[1]] = 'O'
            if self.caller.check_winner([move[0],move[1]], grid_copy):
                chosen = move
                print('winning move at ' + str(chosen))
                break
            grid_copy[move[0]][move[1]] = ''
        return chosen

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
    def check_winner(self, button_clicked, grid):
        buttons_of_player = 0
        winner_buttons = []
        called_by_ai = False
        #print(type(grid[0][0]), "type")
        if type(grid[0][0]) == text_type:
            called_by_ai = True
            #print('called by ai')
            #print(button_clicked[0], button_clicked[1], "button clicked")
        else:
            #print("not ai")
            pass
        #print(called_by_ai)
        # checking both horizontal options
        checked = 0
        #if called_by_ai:
        #    print(button_clicked)
        #    print(grid[button_clicked[0] + checked][button_clicked[1]])
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if not called_by_ai and grid[button_clicked.row][button_clicked.col + checked].text == button_clicked.text and button_clicked.col + checked < self.grid_size:
                    buttons_of_player += 1
                    #print(button_clicked.row, button_clicked.col + checked, "button clicked not ai")
                    winner_buttons.append(grid[button_clicked.row][button_clicked.col + checked])
                elif called_by_ai and grid[button_clicked[0]][button_clicked[1] + checked] == "O" and button_clicked[1] + checked < self.grid_size:
                    buttons_of_player += 1
                    #print(button_clicked[0], button_clicked[1] + checked, "button clicked ai")
                    winner_buttons.append((button_clicked[0], button_clicked[1] + checked))
                else:
                    break
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if not called_by_ai and grid[button_clicked.row][button_clicked.col - checked].text == button_clicked.text and button_clicked.col - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row][button_clicked.col - checked])
                elif called_by_ai and grid[button_clicked[0]][button_clicked[1] - checked] == "O" and button_clicked[1] - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append((button_clicked[0], button_clicked[1] - checked))
                else:
                    break
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1 and self.current_player != 'O': # the plus one is there because the button that was clicked last is counted twice
            #print(winner_buttons)
            self.winner(button_clicked.text, winner_buttons)
        elif buttons_of_player >= self.win_count + 1:
            print("horizontal")
            return True
        # checking both vertical options
        buttons_of_player = 0
        checked = 0
        winner_buttons = []
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if not called_by_ai and grid[button_clicked.row + checked][button_clicked.col].text == button_clicked.text and button_clicked.row + checked < self.grid_size:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row + checked][button_clicked.col])
                elif called_by_ai and grid[button_clicked[0] + checked][button_clicked[1]] == "O" and button_clicked[0] + checked < self.grid_size:
                    buttons_of_player += 1
                    winner_buttons.append((button_clicked[0] + checked, button_clicked[1]))
                else:
                    break
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if not called_by_ai and grid[button_clicked.row - checked][button_clicked.col].text == button_clicked.text and button_clicked.row - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row - checked][button_clicked.col])
                elif called_by_ai and grid[button_clicked[0] - checked][button_clicked[1]] == "O" and button_clicked[0] - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append((button_clicked[0] - checked, button_clicked[1]))
                else:
                    break
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1 and self.current_player != 'O':
            self.winner(button_clicked.text, winner_buttons)
        elif buttons_of_player >= self.win_count + 1:
            print("vertical")
            return True
        # checking the first pair of diagonal options
        buttons_of_player = 0
        checked = 0
        winner_buttons = []
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if not called_by_ai and grid[button_clicked.row + checked][button_clicked.col + checked].text == button_clicked.text and button_clicked.row + checked < self.grid_size and button_clicked.col + checked < self.grid_size:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row + checked][button_clicked.col + checked])
                elif called_by_ai and grid[button_clicked[0] + checked][button_clicked[1] + checked] == "O" and button_clicked[0] + checked < self.grid_size and button_clicked[1] + checked < self.grid_size:
                    buttons_of_player += 1
                    winner_buttons.append((button_clicked[0] + checked, button_clicked[1] + checked))
                else:
                    break
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if not called_by_ai and grid[button_clicked.row - checked][button_clicked.col - checked].text == button_clicked.text and button_clicked.row - checked >= 0 and button_clicked.col - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row - checked][button_clicked.col - checked])
                elif called_by_ai and grid[button_clicked[0] - checked][button_clicked[1] - checked] == "O" and button_clicked[0] - checked >= 0 and button_clicked[1] - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append((button_clicked[0] - checked, button_clicked[1] - checked))
                else:
                    break
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1 and self.current_player != 'O':
            self.winner(button_clicked.text, winner_buttons)
        elif buttons_of_player >= self.win_count + 1:
            print("first diagonal")
            return True
        # checking the second pair of diagonal options
        buttons_of_player = 0
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if not called_by_ai and grid[button_clicked.row - checked][button_clicked.col + checked].text == button_clicked.text and button_clicked.row - checked >= 0 and button_clicked.col + checked < self.grid_size:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row - checked][button_clicked.col + checked])
                elif called_by_ai and grid[button_clicked[0] - checked][button_clicked[1] + checked] == "O" and button_clicked[0] - checked >= 0 and button_clicked[1] + checked < self.grid_size:
                    buttons_of_player += 1
                    winner_buttons.append((button_clicked[0] - checked, button_clicked[1] + checked))
                else:
                    break
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if not called_by_ai and grid[button_clicked.row + checked][button_clicked.col - checked].text == button_clicked.text and button_clicked.row + checked < self.grid_size and button_clicked.col - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row + checked][button_clicked.col - checked])
                elif called_by_ai and grid[button_clicked[0] + checked][button_clicked[1] - checked] == "O" and button_clicked[0] + checked < self.grid_size and button_clicked[1] - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append((button_clicked[0] + checked, button_clicked[1] - checked))
                else:
                    break
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1 and self.current_player != 'O':
            self.winner(button_clicked.text, winner_buttons)
        elif buttons_of_player >= self.win_count + 1:
            print("second diagonal")
            return True
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