from kivy.uix.settings import text_type
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

# this is the popup class for settings
class SettingsPopup(Popup):
    def send_info(self, caller):
        self.caller = caller
        self.ids.gridSize.text = str(caller.grid_size)
        self.ids.winCount.text = str(caller.win_count)
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
            self.caller.check_winner(self, False, self.caller.grid)
            if self.caller.ai_player == 'AI' and self.text == 'X':
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
        best_move = self.ai_choice(1)
        print(best_move)
        # making the move
        #self.caller.grid[best_move[0]][best_move[1]].text = 'O'
        #self.caller.check_winner(self.caller.grid[best_move[0]][best_move[1]], True, copy_grid)
        #self.caller.current_player = 'X'
    def ai_choice(self, depth):
        index_depth = 0
        moves = []
        i = 0
        while i < len(self.caller.grid):
            j = 0
            while j < len(self.caller.grid[i]):
                if self.caller.grid[i][j].text == '':
                    moves.append([i, j])
                j += 1
            i += 1
        #print(moves)
        while index_depth < depth:
            print('depth:', index_depth)
            for move in moves:
                copy_grid = self.caller.grid.copy()
                copy_grid[move[0]][move[1]].text = 'O'
                #print(self.caller.check_winner(copy_grid[move[0]][move[1]], True, copy_grid))
                if self.caller.check_winner(copy_grid[move[0]][move[1]], True, copy_grid):
                    print('winning move at move:', move)
                    return move

            index_depth += 1

# this is the main grid class of the app
class MainGrid(GridLayout):
    def settings(self):
        popup = SettingsPopup()
        popup.send_info(self)
        popup.open()
    def reset(self):
        self.current_player = 'X'
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
    def check_winner(self, button_clicked, called_by_ai, grid):
        #print(called_by_ai, button_clicked.text)
        buttons_of_player = 0
        winner_buttons = []
        # checking both horizontal options
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if grid[button_clicked.row][button_clicked.col + checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row][button_clicked.col + checked])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if grid[button_clicked.row][button_clicked.col - checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row][button_clicked.col - checked])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1: # the plus one is there because the button that was clicked last is counted twice
            self.winner(button_clicked.text, winner_buttons, called_by_ai)
        # checking both vertical options
        buttons_of_player = 0
        checked = 0
        winner_buttons = []
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if grid[button_clicked.row + checked][button_clicked.col].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row + checked][button_clicked.col])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if grid[button_clicked.row - checked][button_clicked.col].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row - checked][button_clicked.col])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1:
            self.winner(button_clicked.text, winner_buttons, called_by_ai)
        # checking the first pair of diagonal options
        buttons_of_player = 0
        checked = 0
        winner_buttons = []
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if grid[button_clicked.row + checked][button_clicked.col + checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row + checked][button_clicked.col + checked])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if grid[button_clicked.row - checked][button_clicked.col - checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row - checked][button_clicked.col - checked])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1:
            self.winner(button_clicked.text, winner_buttons, called_by_ai)
        # checking the second pair of diagonal options
        buttons_of_player = 0
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if grid[button_clicked.row - checked][button_clicked.col + checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row - checked][button_clicked.col + checked])
            except:
                break
            checked += 1
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if grid[button_clicked.row + checked][button_clicked.col - checked].text == button_clicked.text:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row + checked][button_clicked.col - checked])
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1:
            self.winner(button_clicked.text, winner_buttons, called_by_ai)
    def winner(self, winner, winner_buttons, called_by_ai):
        if not called_by_ai: 
            self.ids.currentPlayer.text = 'Winner is: ' + winner
            for button in self.ids.gameGrid.children:
                button.disabled = True
            for button in winner_buttons:
                button.background_color = (0, 1, 0, 1)
        else:
            print("somewhere is an ai winner move")
            return True

# app class
class TicTacToeApp(App):
    def build(self):
        return MainGrid()

# running the app
if __name__ == '__main__':
    TicTacToeApp().run()