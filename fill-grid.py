from collections import defaultdict
import random

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
print(letter_data[0]["A"].intersection(letter_data[1]["H"]))

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
        print_grid(grid)
        print(counter)
        return True
    for iteration in range(100):
        random_word = random.choice(all_words)
        # random_word = "HELP"
        valid = True
        for i in range(word_length):
            grid[row][i] = random_word[i]
            if(len(get_intersection([row[i] for row in grid], letter_data, row+1)) == 0):
                valid = False
        if valid:
            # print_grid(grid)s
            backtrack(grid, letter_data, word_length, row + 1, iteration)
        for i in range(word_length):
            grid[row][i] = ""

def get_intersection(letters, letter_data, length):
    intersect = set(letter_data[0][letters[0]])
    for i in range(length):
        intersect = intersect.intersection(letter_data[i][letters[i]])
    # print("intersection" + str(list(intersect)) + "for letters" + str(lettesrs))
    return list(intersect)

for word in all_words[:3]:
    grid = [[" " for _ in range(4)] for _ in range(4)]
    for i in range(4):
        grid[0][i] = word[i]
    print_grid(grid)
    backtrack(grid, letter_data, 4, 1, 0)
    # print_grid(grid)
# backtrack(grid, letter_data, 4, 0)
# print_grid(grid)

