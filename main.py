from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
#rom kivy.properties import ObjectProperty

# this is the popup class for settings
class SettingsPopup(Popup):
    def send_info(self, caller):
        self.caller = caller
        self.ids.gridSize.text = str(caller.grid_size)

    def apply_settings(self):
        if self.ids.gridSize.text != '' and int(self.ids.gridSize.text) > 0:
            self.caller.grid_size = int(self.ids.gridSize.text)
            self.caller.fill_grid()
            self.dismiss()

# this is the grid button class used in the main grid
class GridButton(Button):
    def send_info(self, caller, row, col):
        self.caller = caller
        self.row = row
        self.col = col
    def click(self):
        #print('button clicked at', self.row, self.col)
        if self.text == '':
            self.text = self.caller.current_player
            self.caller.current_player = 'X' if self.caller.current_player == 'O' else 'O'
            self.caller.check_winner(self)

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
        game_grid = self.ids.gameGrid
        game_grid.clear_widgets()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                grid_button = GridButton()
                grid_button.send_info(self, i, j)
                game_grid.add_widget(grid_button)
                self.grid.append(grid_button)
        # its a bit weird to set the cols, and then return it as well, but it is necessary and it works
        game_grid.cols = self.grid_size
        return self.grid_size
    def check_winner(self, button_clicked):
        # this is just for testing purposes
        if button_clicked.text == 'O':
            return
        #print('checking winner')
        buttons_to_check = []
        number_of_buttons_next_to = 0
        # checking both horizontal options
        for i in range(self.number_for_win):
            column_to_check = button_clicked.col + i
            row_to_check = button_clicked.row
            if column_to_check > self.grid_size - 1:
                row_to_check += 1
                column_to_check = 0
            #print(len(self.grid))
            #print('checking', row_to_check * self.grid_size + column_to_check)
            buttons_to_check.append(self.grid[row_to_check * self.grid_size + column_to_check-1])
        #print('buttons to check:', buttons_to_check)
        print("----------------------------------------------------------------------")
        for button in buttons_to_check:
            if button.text == button_clicked.text:
                number_of_buttons_next_to += 1
                print("The button at", button.row, button.col, "is next to the clicked button")
        print('number of buttons next to:', number_of_buttons_next_to)
        if number_of_buttons_next_to == self.number_for_win:
            print('winner is', button_clicked.text)
            print("the first horizontal decided this")
        buttons_to_check = []
        number_of_buttons_next_to = 0
        for i in range(self.number_for_win):
            column_to_check = button_clicked.col - i
            row_to_check = button_clicked.row
            if column_to_check < 0:
                row_to_check -= 1
                column_to_check = self.grid_size
            buttons_to_check.append(self.grid[row_to_check * self.grid_size + column_to_check-1])
        print("----------------------------------------------------------------------")
        for button in buttons_to_check:
            if button.text == button_clicked.text:
                number_of_buttons_next_to += 1
                print("The button at", button.row, button.col, "is next to the clicked button")
        print('number of buttons next to:', number_of_buttons_next_to)
        if number_of_buttons_next_to == self.number_for_win:
            print('winner is', button_clicked.text)
            print("the second horizontal decided this")
                
        
# app class
class TicTacToeApp(App):
    def build(self):
        return MainGrid()

# running the app
if __name__ == '__main__':
    TicTacToeApp().run()