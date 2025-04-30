from collections import defaultdict
import random
import csv
from typing import List, Set, Dict, Tuple, Optional

def preprocess_words(filepath: str, word_length: int) -> Tuple[List[Dict[str, Set[str]]], List[str]]:
    letter_data = [defaultdict(set) for _ in range(word_length)]
    all_words = []
    with open(filepath, "r") as f:
        for line in f:
            word = line.strip()
            for i in range(word_length):
                letter_data[i][word[i]].add(word)
            all_words.append(word)
    return letter_data, all_words

def print_grid(grid: List[List[str]]) -> None:
    if not grid or not grid[0]:
        return
        
    rows = len(grid)
    cols = len(grid[0])
    
    # Print horizontal line
    def print_horizontal_line() -> None:
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


# backtracking that stops after first solution is found, use for step count
def backtrack(grid: List[List[str]], letter_data: List[Dict[str, Set[str]]], word_length: int, row: int, counter: List[int], filepath: str) -> bool:
    if row >= word_length:
        # Write to CSV
        with open(filepath, 'a', newline='') as f:
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
            if backtrack(grid, letter_data, word_length, row + 1, new_counter, filepath):
                return True
        for i in range(word_length):
            grid[row][i] = ""
    return False  # Return False if no solution found in this branch

# backtracking that returns all solutions
def backtrack2(grid: List[List[str]], letter_data: List[Dict[str, Set[str]]], word_length: int, row: int, solutions_count: int) -> int:
    if row >= word_length:
        solutions_count += 1
        return solutions_count
    for iteration in range(1, 100):
        random_word = random.choice(all_words)
        valid = True
        for i in range(word_length):
            grid[row][i] = random_word[i]
            if(len(get_intersection([row[i] for row in grid], letter_data, row+1)) == 0):
                valid = False
        if valid:
            # If solution found in recursive call, return True to stop further exploration
            solutions_count = backtrack2(grid, letter_data, word_length, row + 1, solutions_count)
        for i in range(word_length):
            grid[row][i] = ""
    return solutions_count

def get_intersection(letters: List[str], letter_data: List[Dict[str, Set[str]]], length: int) -> Set[str]:
    intersect = set(letter_data[0][letters[0]])
    for i in range(length):
        intersect = intersect.intersection(letter_data[i][letters[i]])
    return intersect

def write_step_counts(filepath: str) -> None:
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Grid Row 1', 'Grid Row 2', 'Grid Row 3', 'Grid Row 4', 'Counter Values'])
    for word in all_words:
        grid = [[" " for _ in range(4)] for _ in range(4)]
        for i in range(4):
            grid[0][i] = word[i]
        backtrack(grid, letter_data, 4, 1, [], filepath)

def write_solutions_count(filepath: str) -> None:
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Starting Word','Solutions Count'])
    for word in all_words:
        grid = [[" " for _ in range(4)] for _ in range(4)]
        for i in range(4):
            grid[0][i] = word[i]
        solutions = backtrack2(grid, letter_data, 4, 1, 0)
        with open(filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([word, solutions])
    

if __name__ == "__main__":
    letter_data, all_words = preprocess_words("four_letter_words.csv", 4)
    # write_step_counts("step_counts.csv")
    write_solutions_count("solutions_count.csv")


