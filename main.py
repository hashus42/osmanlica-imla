#!/usr/bin/python3
import sqlite3

import customtkinter as ctk
import arabic_reshaper
from bidi.algorithm import get_display

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.text = None
        self.title("Osmanlica imla")
        self.geometry("800x600")

        # Configure window
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)

        # Create entry
        entry_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, placeholder_text="Kelimeyi giriniz", textvariable=entry_var, font=("Arial", 16))
        self.entry.grid(row=0, column=1, ipadx=330, pady=0, columnspan=2)
        self.entry.focus_set()
        entry_var.trace("w", self.search_word)

    def search_word(self, *args):
        word = self.entry.get()
        latin_letters_chars = ["a", "b", "c", "d", "e", "f", "g", "h",
                               "i", "j", "k", "l", "m", "n", "o", "p",
                               "q", "r", "s", "t", "u", "v", "w", "y",
                               "x", "y", "z", "/", "\\"]
        fake_turkish_letters = ["ç", "ğ", "ö", "ş", "ü"]
        correspond_for_fakes = ["c", "g", "o", "s", "u"]

        # If user enters an uppercase word or a word includes some fake or made-up
        # fake-turkish alphabet letter, then this code-block handle the issue
        word = word.lower()
        for j in range(len(fake_turkish_letters)):
            if fake_turkish_letters[j] in word:
                word = word.replace(fake_turkish_letters[j], correspond_for_fakes[j])

        # Connect to database
        conn = sqlite3.connect("/home/pardusumsu/code/osmanlica-imla/imlakilavuzu3.db")
        cursor = conn.cursor()

        # Execute a query to search for the intended word in database
        try:
            if word == "":
                result = []
            else:
                cursor.execute("SELECT Osmanlica FROM Kelime WHERE latince LIKE ?", (word + "%",))
                result = cursor.fetchmany(19)
                cursor.execute("SELECT Osmanlica FROM Kelime WHERE latince = ?", (word,))
                exact_result = cursor.fetchone()
                if exact_result:
                    result.insert(0, exact_result)
        except sqlite3.Error as error:
            print(error)

        if result:
            i = 0
            for label in self.grid_slaves():
                if int(label.grid_info()['row']) > 0:
                    label.grid_forget()
            for corresponding_word in result:
                i += 1

                # This code is for linux computers. Linux based systems don't have built-in
                # support for arabic fonts unlike Windows
                corresponding_word = str(corresponding_word)[8:-3]
                corresponding_word = arabic_reshaper.reshape(corresponding_word)
                corresponding_word = get_display(corresponding_word)

                # This code-blocks cleans any latin chars from ottoman turkish word
                for num in range(10):
                    if str(num) in corresponding_word:
                        corresponding_word = corresponding_word.replace(str(num), '')

                for char in latin_letters_chars:
                    if char in corresponding_word:
                        corresponding_word = corresponding_word.replace(char, '')

                # Create ottoman word's display widget
                self.text = ctk.CTkLabel(self, width=150, text=corresponding_word, font=("Arial", 16))
                self.text.grid(row=i, column=1, pady=1)
                self.text.setvar(word)
        elif word != "" and result == []:
            for label in self.grid_slaves():
                if int(label.grid_info()['row']) > 0:
                    label.grid_forget()
            alert = f"'{word}' için eşleşen bir kelime bulunamadı."
            self.text = ctk.CTkLabel(self, width=80, text=alert)
            self.text.grid(row=1, column=1)
        else:
            for label in self.grid_slaves():
                if int(label.grid_info()['row']) > 0:
                    label.grid_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()
