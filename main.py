from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

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

# this is the main grid class of the app
class MainGrid(GridLayout):
    def settings(self):
        popup = SettingsPopup()
        popup.send_info(self)
        popup.open()
    def reset(self):
        pass
    def fill_grid(self):
        game_grid = self.ids.gameGrid
        game_grid.clear_widgets()
        print(self.grid_size)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                game_grid.add_widget(Button(text='', font_size=40, size_hint=(1/self.grid_size, 1/self.grid_size)))
        # its a bit weird to set the cols, and then return it as well, but it is necessary and it works
        game_grid.cols = self.grid_size
        return self.grid_size

# app class
class TicTacToeApp(App):
    def build(self):
        return MainGrid()

# running the app
if __name__ == '__main__':
    TicTacToeApp().run()