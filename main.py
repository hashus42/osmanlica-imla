import sqlite3


def search_word_in_database(word):
    # Connect to the database
    conn = sqlite3.connect('imlakilavuzu3.db')
    cursor = conn.cursor()

    # Execute a query to search for the input word in the 'Kelime' table
    cursor.execute("SELECT Osmanlica FROM Kelime WHERE latince = ?", (word,))
    result = cursor.fetchone()

    # Check if the word was found
    if result:
        corresponding_word = result[0]
        print(f"The corresponding word for '{word}' in Osmanlica is '{corresponding_word}'.")
    else:
        print(f"No corresponding word found for '{word}'.")

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    # Ask user to input a word to search
    search_word = input("Enter the word to search: ")

    # Call the function to search for the word in the database
    search_word_in_database(search_word)
