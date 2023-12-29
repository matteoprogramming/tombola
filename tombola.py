## Copyright (c) MB SOFTWARE. All rights reserved.

import random
import os
import datetime


class Tombola:

    def __init__(self):
        # Extracted and extractable numbers
        self.drawn = list()
        self.extractable = [i for i in range (1, 100)]

    def __repr__(self):
        out = str()
        for d in range(0, 10):
            for u in range(0, 10):
                pos = d*10+u
                if pos in self.drawn:
                    out += f"{d}{u} "
                else:
                    out += "-- "
            out += "\n"
        return out


    # Extracts a number from those available,
    # removes it from the extractable numbers
    # and inserts it among those extracted.
    # Returns the extracted number.
    def extract_number(self):
        extracted = random.choice(self.extractable)
        self.extractable.remove(extracted)
        self.drawn.append(extracted)
        return extracted
    
    # We create a file in which to write down each extraction.
    def start_backup(self, heading_title_list):
        self.backup_file = self.date.strftime("%d-%m-%Y_%H-%M-%S") + ".txt"
        with open(self.backup_file, "w", encoding="utf-8") as f:
            print(self.date.strftime("%d/%m/%Y %H:%M:%S"), file = f)
            print("\n".join(heading_title_list), file = f, end="\n\n")
            return

    def save_backup(self, round_str):
        with open(self.backup_file, "a", encoding = "utf-8") as f:
            print(round_str, file = f)
    

    # In order to save some notes...
    def notes(self):
        notes = multiline_input("Leave your notes here (e.g., winners, etc...):")
        if notes:
            self.save_backup(f"Notes:\n{notes}")

    # From this the game starts
    def play(self):
        heading_title_list = [
            "██████    ████     ████ ████   █████      ████     ██      ██████    ██",
            "  ██     ██  ██    ██ ███ ██   ██  ██    ██  ██    ██      ██  ██    ██",
            "  ██    ██    ██   ██  █  ██   █████    ██    ██   ██      ██████    ██",
            "  ██     ██  ██    ██     ██   ██  ██    ██  ██    ██      ██  ██      ",
            "  ██      ████     ██     ██   █████      ████     █████   ██  ██    ██"
        ] 
        print("\n".join(heading_title_list))
        print("Welcome to the TOMBOLA game!")
        print("Press enter to continue...")
        _ = input()
        self.date = datetime.datetime.now()
        self.start_backup(heading_title_list)
        while self.extractable:
            clear_terminal()
            print(f"Extraction n. {len(self.drawn)+1} ... ")
            _ = input()
            extracted_number = self.extract_number()
            print("Extracted number: ", extracted_number)
            print(self)
            out_string = f"Extraction n. {len(self.drawn)}\nExtracted number: {extracted_number}\n{self}\n"
            self.save_backup(out_string)
            _ = input()
        self.notes()     


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
