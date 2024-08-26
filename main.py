import tkinter
from tkinter import filedialog
import csv
import os

def main():

    tkinter.Tk().withdraw()

    folder_path = filedialog.askopenfile()

    file = open(folder_path.name, "r")
    lines = file.readlines()
    
    starting_idx = None

    for idx, line in enumerate(lines):
        if line == 'Potential/V, Current/A\n':
            starting_idx = idx + 2
            break

    filtered_txt = lines[starting_idx:]

    potentials = [[]]
    currents = [[]]
    cycle = 0

    for line in filtered_txt:
        columns = line.split(", ")
        
        potential = float(columns[0])
        current = float(columns[1].split('\n')[0])

        if potential == 0:
            cycle += 1
            potentials.append([])
            currents.append([])

        potentials[cycle].append(potential)
        currents[cycle].append(current)

    last_x = int(input("Average the last X scans: "))

    last_5_potentials = potentials[-last_x:]
    last_5_currents = currents[-last_x:]
    average_currents = []

    for idx, current in enumerate(last_5_currents[0]):
        try:
            average_currents.append((last_5_currents[0][idx] + last_5_currents[1][idx] + last_5_currents[2][idx] + last_5_currents[3][idx] + last_5_currents[4][idx])/5)
        except:
            pass

    results_filename = os.path.join(os.path.dirname(file.name), f'{os.path.basename(file.name)}_results.csv')
    headers = ['Potential', 'Current']

    with open(results_filename, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(headers)

        for idx, item in enumerate(average_currents):
            write.writerow([last_5_potentials[0][idx], item])


if __name__ == "__main__":
    main()