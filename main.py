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
        self.rowconfigure((1, 2, 3, 4, 5,
                           6, 7, 8, 9, 10, 11, 12), weight=1)

        # Create entry
        entry_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, placeholder_text="Kelimeyi giriniz", textvariable=entry_var)
        self.entry.grid(row=0, column=1, ipadx=330, pady=5, columnspan=2)
        self.entry.focus_set()
        entry_var.trace("w", self.search_word)

    def search_word(self, *args):
        word = self.entry.get()

        # Connect to database
        conn = sqlite3.connect("imlakilavuzu3.db")
        cursor = conn.cursor()

        # Execute a query to search for the intended word in database
        try:
            cursor.execute("SELECT Osmanlica FROM Kelime WHERE latince = ?", (word,))
            result = cursor.fetchall()
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

                # print(str(corresponding_word)[8:-3])
                self.text = ctk.CTkLabel(self, width=150, text=corresponding_word, font=("Arial", 16), bg_color="green")
                self.text.grid(row=i, column=1, pady=0)
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
