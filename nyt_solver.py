from bs4 import BeautifulSoup
import requests
import re
import json
import math
nyt = "https://www.nytimes.com/puzzles/sudoku/hard"
 
 
 
content = requests.get(nyt)
 
pattern = r'<script type="text\/javascript">window\.gameData = (.+)<\/script><\/div><div id="portal-editorial-content">'
match = re.search(pattern, content.text)
grid = [[],[],[],[],[],[],[],[],[]]
if match:
    data = json.loads(match.group(1))
    hard_puzzle = data['hard']['puzzle_data']['puzzle']
 
    row = 0
    for i in range(0, len(hard_puzzle)):
        if i % 9 == 0 and i != 0:
            row += 1
        grid[row].append(hard_puzzle[i])


def solve(grid):
    pos = find_zero(grid)
    if(pos == None):
        return True
    
    for i in range(1, 10):
        if(checkValid(pos, i, grid)):
            grid[pos[0]][pos[1]] = i
            if(solve(grid)):
                return True
            else:
                grid[pos[0]][pos[1]] = 0
    return False




def find_zero(grid):
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid)):
            if(grid[i][j] == 0):
                return i, j
    return None

def checkValid(pos, num, grid):
    if(checkRow(grid, num, pos) and checkCol(grid, num, pos) and checkBigBox(grid, num, pos)):
        return True
    return False

def checkRow(grid, num, pos):
    for row_ind in range(0,9):
        if(pos[0] == row_ind):
            continue
        if(grid[row_ind][pos[1]] == num):
            return False
    return True
 
def checkCol(grid, num, pos):
    for col_ind in range(0,9):
        if(pos[1] == col_ind):
            continue
        if(grid[pos[0]][col_ind] == num):
            return False
    return True
 
def checkBigBox(grid, num, pos):
    big_box_row = math.floor(pos[0]/3)
    big_box_col = math.floor(pos[1]/3)
    for k in range(big_box_row * 3, big_box_row*3 + 3):
        for l in range(big_box_col*3, big_box_col * 3+3):
            if(grid[k][l] == num):
                return False
    return True


solve(grid)

for row in grid:
    print(row)