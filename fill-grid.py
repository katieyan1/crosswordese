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

# get words that fulfill " " as first letter, " " as second letter, etc
def get_intersection(letters: List[str], letter_data: List[Dict[str, Set[str]]], length: int) -> Set[str]:
    intersect = set(letter_data[0][letters[0]])
    for i in range(length):
        intersect = intersect.intersection(letter_data[i][letters[i]])
    return intersect

# backtracking that stops after first solution is found, use for step count
def backtrack_step_count(grid: List[List[str]], letter_data: List[Dict[str, Set[str]]], word_length: int, row: int, counter: List[int], filepath: Optional[str] = None, res: Optional[Dict[str, int]] = None) -> bool:
    if row >= word_length:
        grid_strings = [''.join(row) for row in grid]
        if res is not None:
            res[grid_strings[0]] += sum(counter)
            return True
        if filepath is not None:
            with open(filepath, 'a', newline='') as f:
                writer = csv.writer(f)
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
            if backtrack_step_count(grid, letter_data, word_length, row + 1, new_counter, filepath, res):
                return True
        for i in range(word_length):
            grid[row][i] = ""
    return False  # Return False if no solution found in this branch

# backtracking that returns all solutions
def backtrack_sol_count(grid: List[List[str]], letter_data: List[Dict[str, Set[str]]], word_length: int, row: int, solutions_count: int, res: Optional[Dict[str, int]] = None) -> int:
    if row >= word_length:
        solutions_count += 1
        if res is not None:
            res[''.join(grid[0])] = solutions_count
        return solutions_count
    for _ in range(1, 100):
        random_word = random.choice(all_words)
        valid = True
        for i in range(word_length):
            grid[row][i] = random_word[i]
            if(len(get_intersection([row[i] for row in grid], letter_data, row+1)) == 0):
                valid = False
        if valid:
            solutions_count = backtrack_sol_count(grid, letter_data, word_length, row + 1, solutions_count)
        for i in range(word_length):
            grid[row][i] = ""
    return solutions_count

def write_step_counts(word_length: int, letter_data: List[Dict[str, Set[str]]], all_words: List[str], filepath: str) -> None:
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Grid Row 1', 'Grid Row 2', 'Grid Row 3', 'Grid Row 4', 'Counter Values'])
    
    for word in all_words:
        # create grid
        grid = [[" " for _ in range(word_length)] for _ in range(word_length)]
        # fill first row with starting word
        for i in range(word_length):
            grid[0][i] = word[i]
        # backtrack to find number of steps required to fill grid
        backtrack_step_count(grid, letter_data, word_length, 1, [], filepath)

def write_solutions_count(word_length: int, letter_data: List[Dict[str, Set[str]]], all_words: List[str], filepath: str) -> None:
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Starting Word','Solutions Count'])
    
    for word in all_words:
        # create grid
        grid = [[" " for _ in range(word_length)] for _ in range(word_length)]
        # fill first row with starting word
        for i in range(word_length):
            grid[0][i] = word[i]
        # backtrack to find number of solutions that fill grid
        solutions = backtrack_sol_count(grid, letter_data, word_length, 1, 0)
        with open(filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([word, solutions])

def run_step_count(word_length: int, letter_data: List[Dict[str, Set[str]]], all_words: List[str], iters: int, filepath: str) -> None:
    res = {}
    for word in all_words:
        # create grid
        res[word] = 0
        grid = [[" " for _ in range(word_length)] for _ in range(word_length)]
        # fill first row with starting word
        for i in range(word_length):
            grid[0][i] = word[i]
        for i in range(iters):
        # backtrack to find number of steps required to fill grid
            print(str(i) + " " + word)
            backtrack_step_count(grid, letter_data, word_length, 1, [], res=res)
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Starting Word','Step Count'])
        for word, count in res.items():
            writer.writerow([word, count/iters])

def backtrack_MRV(grid: List[List[str]], letter_data: List[Dict[str, Set[str]]], word_length: int, solutions_count: int, remaining_words: Dict[Tuple[int, int], Set[str]]) -> int:
    if len(remaining_words) == 0:
        solutions_count += 1
        return solutions_count
    
    # get answer with least remaining words
    answer = min(remaining_words, key=lambda x: len(remaining_words[x]))
    if len(remaining_words[answer]) == 0:
        return solutions_count  # No valid words for this position
        
    beg_remain = remaining_words[answer].copy()  # Make a copy to avoid modifying while iterating
    before = grid.copy()
    while len(beg_remain) > 0:
        chosen_word = beg_remain.pop()
        # Place word
        if answer[1] == 0:  # Across
            for i in range(word_length):
                grid[answer[0]][i] = chosen_word[i]
        else:  # Down
            for i in range(word_length):
                grid[i][answer[0]] = chosen_word[i]
                
        print_grid(grid)
        # Store current state and remove current position
        store = remaining_words[answer].copy()
        del remaining_words[answer]
        
        # Filter remaining words
        filtered = filter_words(grid, letter_data, word_length, remaining_words)
        
        solutions_count = backtrack_MRV(grid, letter_data, word_length, solutions_count, filtered)
        
        # Restore state
        remaining_words[answer] = store.copy()
        if answer[1] == 0:  # Across
            for i in range(word_length):
                grid[answer[0]][i] = before[answer[0]][i]
        else:  # Down
            for i in range(word_length):
                grid[i][answer[0]] = before[i][answer[0]]
                
    return solutions_count

def run_MRV(word_length: int, letter_data: List[Dict[str, Set[str]]], all_words: List[str], filepath: str) -> None:
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Starting Word','Solutions Count'])
        for word in all_words[4:5]:
            remaining_words = {}
            grid = [[" " for _ in range(word_length)] for _ in range(word_length)]
            for i in range(word_length):
                grid[0][i] = word[i]
            for i in range(word_length):
                for j in range(2):
                    remaining_words[(i, j)] = set(all_words)
            del remaining_words[(0, 0)] # 1A
            remaining_words = filter_words(grid, letter_data, word_length, remaining_words) 
            solutions = backtrack_MRV(grid, letter_data, word_length, 0, remaining_words)
            print(word + " " + str(solutions))
            # writer.writerow([word, solutions])

def filter_words(grid: List[List[str]], letter_data: List[Dict[str, Set[str]]], word_length: int, remaining_words: Dict[Tuple[int, int], Set[str]]) ->  Dict[Tuple[int, int], Set[str]]:
    # iterate through rows of grid
    columns = [[] for _ in range(word_length)]
    for i in range(word_length):
        for j in range(word_length):
            letter = grid[i][j]
            columns[j].append(letter)
            if letter != " " and (i, 0) in remaining_words:
                remaining_words[(i, 0)] = remaining_words[(i, 0)].intersection(letter_data[j][letter])
    # iterate through columns of grid
    for i in range(word_length):
        for j in range(word_length):
            letter = columns[i][j]
            if letter != " " and (i, 1) in remaining_words:
                remaining_words[(i, 1)] = remaining_words[(i, 1)].intersection(letter_data[j][letter])
    return remaining_words

if __name__ == "__main__":
    letter_data, all_words = preprocess_words("four_letter_words.csv", 4)
    # write_step_counts("step_counts.csv", 4, letter_data, all_words)
    # write_solutions_count("solutions_count.csv", 4, letter_data, all_words)
    # run_step_count(4, letter_data, all_words, 5, "run_step_counts.csv")
    run_MRV(4, letter_data, all_words, "run_MRV.csv")
