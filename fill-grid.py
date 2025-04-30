from collections import defaultdict
import random
import csv

def preprocess_words(filepath, word_length):

    letter_data = [defaultdict(set) for _ in range(word_length)]
    all_words = []
    with open(filepath, "r") as f:
        for line in f:
            word = line.strip()
            for i in range(word_length):
                letter_data[i][word[i]].add(word)
            all_words.append(word)
    return letter_data, all_words

letter_data, all_words = preprocess_words("four_letter_words.csv", 4)
# print(letter_data[0]["A"].intersection(letter_data[1]["H"]))

def print_grid(grid):
    if not grid or not grid[0]:
        return
        
    rows = len(grid)
    cols = len(grid[0])
    
    # Print horizontal line
    def print_horizontal_line():
        print("+" + ("-" * 3 + "+") * cols)
    
    # Print each row
    for row in grid:
        print_horizontal_line()
        # Print cell contents
        print("|", end="")
        for cell in row:
            # Center the content in a 3-character wide cell
            content = str(cell).center(3)
            print(f"{content}|", end="")
        print()
    print_horizontal_line()

def backtrack(grid, letter_data, word_length, row, counter):
    if row >= word_length:
        # print_grid(grid)
        # print(counter)
        # Write to CSV
        with open('solutions.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            # Combine grid rows into single strings
            grid_strings = [''.join(row) for row in grid]
            # Write grid strings and counter in one row
            writer.writerow([*grid_strings, sum(counter), *counter])
        return True  # Return True to indicate solution found
    for iteration in range(1, 100):
        random_word = random.choice(all_words)
        valid = True
        for i in range(word_length):
            grid[row][i] = random_word[i]
            if(len(get_intersection([row[i] for row in grid], letter_data, row+1)) == 0):
                valid = False
        if valid:
            new_counter = counter.copy()
            new_counter.append(iteration)
            # If solution found in recursive call, return True to stop further exploration
            if backtrack(grid, letter_data, word_length, row + 1, new_counter):
                return True
        for i in range(word_length):
            grid[row][i] = ""
    return False  # Return False if no solution found in this branch

def get_intersection(letters, letter_data, length):
    intersect = set(letter_data[0][letters[0]])
    for i in range(length):
        intersect = intersect.intersection(letter_data[i][letters[i]])
    # print("intersection" + str(list(intersect)) + "for letters" + str(lettesrs))
    return list(intersect)

# Clear the solutions file before starting
with open('solutions.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Grid Row 1', 'Grid Row 2', 'Grid Row 3', 'Grid Row 4', 'Counter Values'])

for word in all_words:
    grid = [[" " for _ in range(4)] for _ in range(4)]
    for i in range(4):
        grid[0][i] = word[i]
    # print_grid(grid)
    backtrack(grid, letter_data, 4, 1, [])
    # print_grid(grid)
# backtrack(grid, letter_data, 4, 0)
# print_grid(grid)

