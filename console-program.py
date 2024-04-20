import sqlite3

import keyboard



def search_word_in_database(word):
    # Connect to the database
    conn = sqlite3.connect('imlakilavuzu3.db')
    cursor = conn.cursor()

    # Execute a query to search for the input word in the 'Kelime' table
    cursor.execute("SELECT Osmanlica FROM Kelime WHERE latince = ?", (word,))
    result = cursor.fetchall()

    # Check if the word was found
    if result:
        for row in result:
            corresponding_word = row
            corresponding_word = str(corresponding_word)[2:-3]
            print(f"{corresponding_word}\n")
    else:
        print(f"No corresponding word found for '{word}'.")

    # Close the database connection
    conn.close()


search_word = ""

if __name__ == "__main__":

    # search_word = input("Enter the word to search: ")
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            if key == "backspace":
                search_word = search_word[:-1]
                print(f"{search_word}\n")
            elif key == "space":
                search_word = search_word + " "
                print(f"{search_word}\n")
            else:
                search_word += key
                print(f"{search_word}\n")
            if search_word != "":
                # Call the function to search for the word in the database
                search_word_in_database(search_word)

                # Ask user to input a word to search
                # search_word = input("Enter the word to search: ")

                # if user enters exit keyword break the loop
                if search_word == "exit":
                    break

