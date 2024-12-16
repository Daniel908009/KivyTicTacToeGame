from kivy.uix.settings import text_type
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import random

# this array will be used to store the results of the recursive algorithm, it is a global variable, because passing it between the functions would make it more complicated
ai_results = []

# this is the popup class for settings
class SettingsPopup(Popup):
    # method for sending the info to the popup
    def send_info(self, caller):
        self.caller = caller
        self.ids.gridSize.text = str(caller.grid_size)
        self.ids.winCount.text = str(caller.win_count)
        self.ids.aiPlayer.text = caller.ai_player
        self.ids.aiDifficulty.text = caller.ai_difficulty
    # method for applying the settings
    def apply_settings(self):
        if self.ids.gridSize.text != '' and int(self.ids.gridSize.text) > 0 and self.ids.winCount.text != '' and int(self.ids.winCount.text) > 0 and int(self.ids.winCount.text) <= int(self.ids.gridSize.text):
            self.caller.grid_size = int(self.ids.gridSize.text)
            self.caller.fill_grid()
            self.caller.win_count = int(self.ids.winCount.text)
            self.caller.ai_player = self.ids.aiPlayer.text
            self.caller.ai_difficulty = self.ids.aiDifficulty.text
            self.dismiss()

# this is the grid button class used in the main grid
class GridButton(Button):
    # method for sending the info to the button, maybe could be done differently, however this is simple and it works
    def send_info(self, caller, row, col):
        self.caller = caller
        self.row = row
        self.col = col
    # method for clicking the button, is called by both the player and the ai
    def click(self):
        if self.text == '':
            self.text = self.caller.current_player
            self.caller.current_player = 'X' if self.caller.current_player == 'O' else 'O'
            self.caller.check_winner(self, self.caller.grid, self.text, True)
            #print(self.caller.ai_player)
            if self.caller.ai_player == 'AI' and self.text == 'X' and not self.caller.game_over:
                self.ai_move()
    # method for the ai to make a move
    def ai_move(self):
        # getting the best move
        best_move = self.ai_choice()
        print(str(best_move) + ' is the chosen move')
        # making the move
        self.caller.grid[best_move[0]][best_move[1]].click()
    # the choice works like this: first the ai will check if it can win in one move, if not then it will check if the player can win in one move, if not then it will use algorithm to choose the best move
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
        chosen = [random.choice(moves), 0]
        grid_copy = []
        for i in range(self.caller.grid_size):
            grid_copy.append([])
            for j in range(self.caller.grid_size):
                grid_copy[i].append(self.caller.grid[i][j].text)
        # checking if the ai can win in one move
        for move in moves:
            grid_copy[move[0]][move[1]] = 'O'
            if self.caller.check_winner([move[0],move[1]], grid_copy, 'O', False):
                chosen = [move, 1]
                print('winning move at ' + str(chosen))
                break
            grid_copy[move[0]][move[1]] = ''
        # checking if the player can win in one move, if so, blocking it
        if chosen[1] == 0:
            for move in moves:
                grid_copy[move[0]][move[1]] = 'X'
                if self.caller.check_winner([move[0],move[1]], grid_copy, 'X', False):
                    chosen = [move, 1]
                    print('blocking move at ' + str(chosen))
                    break
                grid_copy[move[0]][move[1]] = ''

        # calling the algorithm to choose the best move, this will take like a thousand years to finish
        if chosen[1] == 0 and self.caller.ai_difficulty == 'Hard':
            chosen[0] = self.algorithm(grid_copy)
        
        return chosen[0]
    # the algorithm to choose the best ai move
    def algorithm(self, grid):
        global ai_results
        move = [0,0]
        base_empty_tiles = []
        # getting all the empty tiles
        for i in range(self.caller.grid_size):
            ai_results.append([])
            for j in range(self.caller.grid_size):
                ai_results[i].append(0)
                if grid[i][j] == '':
                    base_empty_tiles.append([i,j])
                
        # original texts of the grid
        original_texts = []
        for i in range(self.caller.grid_size):
            original_texts.append([])
            for j in range(self.caller.grid_size):
                original_texts[i].append(self.caller.grid[i][j].text)
        #print(original_texts)
        # doing recursive algorithm things
        all_possibilities = []
        #print('base empty tiles: ' + str(base_empty_tiles))
        for possibility in base_empty_tiles:
            all_possibilities.append(possibility)
            #print('possibility jfkalsdfjklas;dfjaskldfjl;asdjfklasjfdlk;: ' + str(possibility))
            #print(ai_results[possibility[0]][possibility[1]])
            self.recursion('O',grid, possibility, 0)         #############################################important
            #print('ai results: ' + str(ai_results))
            #print('recursion started')
            # resetting the grid texts, because the recursion changes them since there is no way to make a copy of the buttons grid, so the function work with the original
            for i in range(self.caller.grid_size):
                for j in range(self.caller.grid_size):
                    self.caller.grid[i][j].text = original_texts[i][j]
            #print('resetting')
        #print('all possibilities: ' + str(all_possibilities))
        #self.recursion('O',grid, all_possibilities[0], 0)
        print('ai results: ' + str(ai_results))
        # calling a function to get the best move based on the result values inside the all_possibilities list
        #move = self.get_best_move_from_possibilities()
        return move
    # recursive method to get all the possibilities of how the game can end, it is so complicated that I have no clue if there is something not neccessary in it and its so complicated, that I have a paper with a lot of drawings and notes about it
    def recursion(self,player,text_grid,answer_pos, depth):
        #print(depth)
        global ai_results
        empty_tiles = []
        #print("/////////////////////////////////////////////////////////////////////")
        #for i in range(self.caller.grid_size):
            #print(text_grid[i])
        for i in range(self.caller.grid_size):
            for j in range(self.caller.grid_size):
                if text_grid[i][j] == '':
                    empty_tiles.append((i,j))
        #print('empty tiles: ' + str(len(empty_tiles)))
        if len(empty_tiles) > 0:
            for place in empty_tiles:
                copy_text_grid = []
                for i in range(self.caller.grid_size):
                    copy_text_grid.append([])
                    for j in range(self.caller.grid_size):
                        copy_text_grid[i].append(text_grid[i][j])
                copy_text_grid[place[0]][place[1]] = player
                if self.caller.check_winner([place[0],place[1]], copy_text_grid, player, False):
                    #print(answer_pos)
                    if player == 'O':
                        ai_results[answer_pos[0]][answer_pos[1]] += (10 - depth)
                        #print(str(copy_text_grid) + 'added 1 to ' + str(answer_pos))
                        #print('added 1 to ' + str(answer_pos))
                        #print(ai_results)
                    elif player == 'X':
                        ai_results[answer_pos[0]][answer_pos[1]] -= (depth - 10)
                        #print(str(copy_text_grid) + 'subtracted 1 from ' + str(answer_pos))
                        #print('addedfromX 1 from ' + str(answer_pos))
                        #print(ai_results)
                    else:
                        print("something terrible happened")
                else:
                    if player == 'O':
                        self.recursion('X',copy_text_grid,answer_pos, depth+1)
                    elif player == 'X':
                        self.recursion('O',copy_text_grid,answer_pos, depth+1)
                    else:
                        print("all hope is lost")
        else:
            pass
            #print("this should be printed when the recursion ends, grid = " + str(text_grid))

    # method to get the best move from the possibilities list, will need a lot of work
    def get_best_move_from_possibilities(self):
        global ai_results
        highest = 0
        for i in ai_results:
            if i > highest:
                highest = i
        best_move = self.caller.grid[ai_results.index(highest)]
        print('best move is ' + str(best_move))
        return best_move

# this is the main grid class of the app
class MainGrid(GridLayout):
    # method for opening the settings popup
    def settings(self):
        popup = SettingsPopup()
        popup.send_info(self) # maybe can be done differently, however this works and its simple
        popup.open()
    # method for resetting the game
    def reset(self):
        self.current_player = 'X'
        self.ids.currentPlayer.text = 'Current player: ' + self.current_player
        self.game_over = False
        self.fill_grid()
    # method for filling up the grid with the grid buttons
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
    # method for checking if someone won the game in the inputted grid, its really big and maybe could be better, however it works
    def check_winner(self, button_clicked, grid, text_of_clicked, is_real):
        buttons_of_player = 0
        winner_buttons = []
        called_by_ai = False
        if type(grid[0][0]) == text_type:
            called_by_ai = True
        # checking both horizontal options
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if not called_by_ai and grid[button_clicked.row][button_clicked.col + checked].text == button_clicked.text and button_clicked.col + checked < self.grid_size:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row][button_clicked.col + checked])
                elif called_by_ai and grid[button_clicked[0]][button_clicked[1] + checked] == text_of_clicked and button_clicked[1] + checked < self.grid_size:
                    buttons_of_player += 1
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
                elif called_by_ai and grid[button_clicked[0]][button_clicked[1] - checked] == text_of_clicked and button_clicked[1] - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append((button_clicked[0], button_clicked[1] - checked))
                else:
                    break
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1 and self.current_player != 'O' and is_real: # the plus one is there because the button that was clicked last is counted twice
            self.winner(button_clicked.text, winner_buttons)
        elif buttons_of_player >= self.win_count + 1:
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
                elif called_by_ai and grid[button_clicked[0] + checked][button_clicked[1]] == text_of_clicked and button_clicked[0] + checked < self.grid_size:
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
                elif called_by_ai and grid[button_clicked[0] - checked][button_clicked[1]] == text_of_clicked and button_clicked[0] - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append((button_clicked[0] - checked, button_clicked[1]))
                else:
                    break
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1 and self.current_player != text_of_clicked and is_real:
            self.winner(button_clicked.text, winner_buttons)
        elif buttons_of_player >= self.win_count + 1:
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
                elif called_by_ai and grid[button_clicked[0] + checked][button_clicked[1] + checked] == text_of_clicked and button_clicked[0] + checked < self.grid_size and button_clicked[1] + checked < self.grid_size:
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
                elif called_by_ai and grid[button_clicked[0] - checked][button_clicked[1] - checked] == text_of_clicked and button_clicked[0] - checked >= 0 and button_clicked[1] - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append((button_clicked[0] - checked, button_clicked[1] - checked))
                else:
                    break
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1 and self.current_player != 'O' and is_real:
            self.winner(button_clicked.text, winner_buttons)
        elif buttons_of_player >= self.win_count + 1:
            return True
        # checking the second pair of diagonal options
        buttons_of_player = 0
        checked = 0
        while buttons_of_player < self.win_count+1 and checked < self.win_count:
            try:
                if not called_by_ai and grid[button_clicked.row - checked][button_clicked.col + checked].text == button_clicked.text and button_clicked.row - checked >= 0 and button_clicked.col + checked < self.grid_size:
                    buttons_of_player += 1
                    winner_buttons.append(grid[button_clicked.row - checked][button_clicked.col + checked])
                elif called_by_ai and grid[button_clicked[0] - checked][button_clicked[1] + checked] == text_of_clicked and button_clicked[0] - checked >= 0 and button_clicked[1] + checked < self.grid_size:
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
                elif called_by_ai and grid[button_clicked[0] + checked][button_clicked[1] - checked] == text_of_clicked and button_clicked[0] + checked < self.grid_size and button_clicked[1] - checked >= 0:
                    buttons_of_player += 1
                    winner_buttons.append((button_clicked[0] + checked, button_clicked[1] - checked))
                else:
                    break
            except:
                break
            checked += 1
        if buttons_of_player >= self.win_count + 1 and self.current_player != 'O' and is_real:
            self.winner(button_clicked.text, winner_buttons)
        elif buttons_of_player >= self.win_count + 1:
            return True
        elif self.no_empty_tiles() and is_real:
            #print("everything is either broken or full")
            #print("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
            self.ids.currentPlayer.text = 'No winner'
            self.game_over = True
            for button in self.ids.gameGrid.children:
                button.disabled = True
    # method to show the winner of the game         
    def winner(self, winner, winner_buttons): 
        #print("How did we get here?")
        self.ids.currentPlayer.text = 'Winner is: ' + winner
        self.game_over = True
        for button in self.ids.gameGrid.children:
            button.disabled = True
        for button in winner_buttons:
            button.background_color = (0, 1, 0, 1)
    # method to check if there are any empty tiles left
    def no_empty_tiles(self):
        for button in self.ids.gameGrid.children:
            if button.text == '':
                return False
        return True

# app class
class TicTacToeApp(App):
    def build(self):
        return MainGrid()

# running the app
if __name__ == '__main__':
    TicTacToeApp().run()