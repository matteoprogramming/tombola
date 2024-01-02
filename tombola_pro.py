## Copyright (c) MB SOFTWARE. All rights reserved.

import random
import os
import datetime


class Tombola:

    def __init__(self):
        # Extracted and extractable numbers
        self.drawn = list()
        self.extractable = [i for i in range (1, 91)]

    def __repr__(self):
        out = str()
        for d in range(0, 9):
            for u in range(1, 11):
                pos = d*10+u
                number_str = str(d%10+u//10)+str(u%10)+" "
                if pos in self.drawn:
                    out += number_str
                else:
                    out += "-- "
            out += "\n"
        return out
    
    # Build a tombola from a matrix str
    def get_from_str(self, tomb_str):
        self.drawn = list(map(int, tomb_str.replace("-", "").replace("\n","").split()))
        self.extractable = list(set(self.extractable) - set(self.drawn))


    def print_heading_test(self):
        self.heading_title_list = [
            "██████    ████     ████ ████   █████      ████     ██      ██████    ██",
            "  ██     ██  ██    ██ ███ ██   ██  ██    ██  ██    ██      ██  ██    ██",
            "  ██    ██    ██   ██  █  ██   █████    ██    ██   ██      ██████    ██",
            "  ██     ██  ██    ██     ██   ██  ██    ██  ██    ██      ██  ██      ",
            "  ██      ████     ██     ██   █████      ████     █████   ██  ██    ██"
        ] 
        print("\n".join(self.heading_title_list))
        print("Welcome to the TOMBOLA game!")
        print("Press enter to continue...")

    # We create a file in which to write down each extraction.
    def start_backup(self):
        self.backup_file = self.date.strftime("%d-%m-%Y_%H-%M-%S") + ".txt"
        with open(self.backup_file, "w", encoding="utf-8") as f:
            print(self.date.strftime("%d/%m/%Y %H:%M:%S"), file = f)
            print("\n".join(self.heading_title_list), file = f, end="\n\n")
            return

    def save_backup(self, round_str):
        with open(self.backup_file, "a", encoding = "utf-8") as f:
            print(round_str, file = f)


    def create_cartelle(self):
        self.number_of_cart = int(input("Inserisci il numero di cartelle: ").strip())
        self.cartelle = []
        print("New cartelle\n")
        for i in range(1, self.number_of_cart+1):
            cart_p = Cartella(i)
            while cart_p in self.cartelle:
                cart_p = Cartella(i)
            self.cartelle.append(cart_p)
            print(cart_p)

    
    # Extracts a number from those available,
    # removes it from the extractable numbers
    # and inserts it among those extracted.
    # Returns the extracted number.
    def extract_number(self):
        extracted = random.choice(self.extractable)
        self.extractable.remove(extracted)
        self.drawn.append(extracted)
        return extracted
    
    def sort_cartelle_by_score(self):
        self.cartelle.sort(key = lambda x: x.get_score())
    
    def sort_cartelle_by_number(self):
        self.cartelle.sort(key = lambda x: x.number)

    def extraction(self):
        clear_terminal()
        print(f"Extraction n. {len(self.drawn)+1} ... ")
        _ = input()
        extracted_number = self.extract_number()
        print("Extracted number: ", extracted_number)
        print(self)
        for cart in self.cartelle:
            cart.remove_number(extracted_number)
            cart.get_score()
        self.sort_cartelle_by_score()
        out_string = f"Extraction n. {len(self.drawn)}\nExtracted number: {extracted_number}\n{self}\n"
        print("Results")
        for cart in self.cartelle:
            print(f"Cartella n.{cart.number}: {cart.score_str}")
            out_string += f"Cartella n.{cart.number}: {cart.score_str}\n"
        print()
        out_string+="\n"
        self.sort_cartelle_by_number()
        for cart in self.cartelle:
            print(f"{cart}")
            out_string += f"{cart}"
        out_string+="\n"
        self.save_backup(out_string)
        _ = input()


    # In order to save some notes...
    def notes(self):
        notes = multiline_input("Leave your notes here (e.g., winners, etc...):")
        if notes:
            self.save_backup(f"Notes:\n{notes}")

    # Frome this the game starts
    def play(self):
        self.date = datetime.datetime.now()
        self.print_heading_test()
        _ = input()
        self.start_backup()
        self.create_cartelle()
        _ = input()
        while self.extractable:
            self.extraction()
        self.notes()     


class Cartella:
    
    def __init__(self, number):
        self.number = number
        self.initial_numbers = random.sample([n for n in range(1, 91)], k=15)
        self.initial_rows = [self.initial_numbers[:5], self.initial_numbers[5:10], self.initial_numbers[10:]]
        self.rows = [self.initial_numbers[:5], self.initial_numbers[5:10], self.initial_numbers[10:]]
    
    def now_numbers(self):
        return self.rows[0] + self.rows[1] +self.rows[2]
    
        
    def __repr__(self):
        cart_str = f"Cartella n. {self.number}\n"
        cart_str += "—"*18
        cart_str += "\n"
        for row in self.initial_rows:
            cart_str += "| "
            for n in row:
                if n in self.now_numbers():
                    cart_str += f"{n//10}{n%10} "
                else:
                    cart_str += "   "
            cart_str += "|\n"
        cart_str += "—"*18
        return cart_str


    def remove_number(self, n):
        if n in self.initial_numbers:
            for row in self.rows:
                if n in row:
                    row.remove(n)

    def get_score(self):
        self.score = round(1 - len(self.now_numbers())/15, 2)*100
        self.score_str = f"{self.score}%"
        return self.score


# Allows you to insert multiline string input
def multiline_input(input_str):
    print(input_str)
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return '\n'.join(lines)

# Clean the terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear') 


def main():
    t = Tombola()
    t.play()



if __name__ == "__main__":
    main()