from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
import random
import pandas as pd
import re
import gspread
import math
from oauth2client.service_account import ServiceAccountCredentials

Builder.load_file('Buttons.kv')

class Data_operations():
    def __init__(self):
        pass

    def answer_data(self):
        # Update the label
        name = self.ids.name_input.text
        if name == '':
            self.ids.answer_label.text = 'Your answer'

        elif name.lower() == self.right_word:
            self.ids.answer_label.text = 'Correct'
            Data_operations.add_value_to_cell(self, self.num_row, len(self.col))
            self.next_word()
        else:
            self.ids.answer_label.text = 'Wrong'
            Data_operations.add_value_to_cell(self, self.num_row, len(self.col), sign='-')

        # Clear input box
        self.ids.name_input.text = ''

    def next_word_data(self):
        self.ids.hint_label.text = ''
        self.hinter = ''
        self.hint_count = 0
        self.df['Prob_for_chose'] = Data_operations.calc_prob(self)
        self.num_row = random.choices(range(0, len(self.df)), weights=self.df['Prob_for_chose'], k=1)[0]
        self.foreign_word = self.df.loc[self.num_row, self.df.columns[0]]
        self.ids.name_label.text = self.foreign_word[::-1]
        self.right_word = self.df.loc[self.num_row, self.df.columns[1]].lower()
        self.ids.name_input.text = ''
        Data_operations.add_value_to_cell(self, self.num_row, len(self.col) - 1)

    def hint_data(self):
        if self.hint_count < len(self.right_word):
            self.hinter = self.hinter + self.right_word[self.hint_count]
            self.ids.hint_label.text = self.hinter
            self.hint_count += 1

    def create_and_fill_col(self):
        self.col = self.df.columns
        if 'Count_of_appearance' not in self.col:
            Data_operations.add_value_to_cell(self, 1, len(self.col) + 1, None, 'Count_of_appearance')
            Data_operations.add_value_to_cell(self, 1, len(self.col) + 2, None, 'Count_of_Right_answers')
        else:
            pass
        self.df = pd.DataFrame(self.spreadsheet.get_all_records())
        self.col = self.df.columns
        return self.df

    def add_value_to_cell(self, num_row, num_col, sign=None, value=None):
        if value == None:
            num_row = num_row + 2
            val = self.spreadsheet.cell(num_row, num_col).value
            val = int(0 if val is None else val)
            if sign == None:
                return self.spreadsheet.update_cell(num_row, num_col, val + 1)
            else:
                if val > 0:
                    return self.spreadsheet.update_cell(num_row, num_col, val - 1)
                else:
                    pass
        else:
            return self.spreadsheet.update_cell(num_row, num_col, value)

    def calc_prob(self):
        self.df['Count_of_appearance'] = pd.to_numeric(self.df['Count_of_appearance'])
        self.df['Count_of_Right_answers'] = pd.to_numeric(self.df['Count_of_Right_answers'])
        self.df['Count_of_each'] = 1
        self.df['prob_of_three'] = (self.df['Count_of_each'] + self.df['Count_of_Right_answers'].fillna(0) + self.df[
            'Count_of_appearance'].fillna(0))
        self.df['prob_of_three^(-1)'] = self.df['prob_of_three']**(-1)
        return self.df['prob_of_three^(-1)']

class MyLayout(Widget):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            r'credential.json', self.scope)
        self.client = gspread.authorize(self.credentials)
        self.Sheet_ID = "1bKL7pCOHBFQTwfaL2Lr9mBMPCNagV16F7VjihIp-tYg"
        self.spreadsheet = self.client.open_by_key(self.Sheet_ID).get_worksheet(0)
        self.df = pd.DataFrame(self.spreadsheet.get_all_records())
        self.df = Data_operations.create_and_fill_col(self)
        self.df = pd.DataFrame(self.spreadsheet.get_all_records())
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