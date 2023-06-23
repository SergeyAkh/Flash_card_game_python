from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
import random
import pandas as pd

Builder.load_file('Buttons.kv')

class Data_operations():
    def __init__(self):
        pass

    def answer_data(self):
        # Update the label
        name = self.ids.name_input.text
        if name == '':
            self.ids.answer_label.text = 'Your answer'

        elif name.lower() in self.right_word:
            self.ids.answer_label.text = 'Correct'
            self.next_word()
        else:
            self.ids.answer_label.text = 'Wrong'

        # Clear input box
        self.ids.name_input.text = ''

    def next_word_data(self):
        self.ids.hint_label.text = ''
        self.hinter = ''
        self.hint_count = 0
        self.num_row = random.randint(0, len(self.df) - 1)
        self.foreign_word = self.df.loc[self.num_row, self.df.columns[0]]
        self.ids.name_label.text = self.foreign_word[::-1]
        self.right_word = self.df.loc[self.num_row, self.df.columns[1]].lower()
        self.ids.name_input.text = ''

    def hint_data(self):
        if self.hint_count < len(self.right_word):
            self.hinter = self.hinter + self.right_word[self.hint_count]
            self.ids.hint_label.text = self.hinter
            self.hint_count += 1


class MyLayout(Widget):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.Sheet_ID = "Your_Sheet_ID"
        self.Sheet_name = "Your_Sheet_name"
        self.df = pd.read_csv(
            f'https://docs.google.com/spreadsheets/d/{self.Sheet_ID}/gviz/tq?tqx=out:csv&sheet={self.Sheet_name}',
            header=0)
        Data_operations.next_word_data(self)

    def answer(self):
        # Create variables for our widget
        Data_operations.answer_data(self)

    def next_word(self):

        Data_operations.next_word_data(self)

    def hint(self):
        Data_operations.hint_data(self)

    def switch_on(self,instanse,value):
        assert isinstance(value, object)
        if value is True:
            self.ids.switch_label.text = self.df.columns[0]+" to "+self.df.columns[1]

        else:
            self.ids.switch_label.text = self.df.columns[1]+" to "+self.df.columns[0]



class Flash_card_App(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    Flash_card_App().run()
