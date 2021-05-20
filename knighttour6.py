import sys

def get_yn(msg, errmsg):
    while True:
        yn = input(msg)
        if yn == "y" or yn == "n":
            return yn  
        print(errmsg)

def get_xy(msg, errmsg, maxx, maxy):
    while True:
        line = input(msg)
        items = line.split()
        if len(items) != 2:
            print(errmsg)
            continue
        x, y = items
        if not str.isdigit(x) or not str.isdigit(y):
            print(errmsg)
            continue
        x = int(x)
        y = int(y)
        if 1 <= x <= maxx and 1 <= y <= maxy:
            return x, y
        print(errmsg)
        
def get_move(msg, retrymsg, possible_move):
    while True:
        line = input(msg)
        items = line.split()
        if len(items) != 2:
            msg = retrymsg
            continue
        x, y = items
        if not str.isdigit(x) or not str.isdigit(y):
            msg = retrymsg
            continue
        x = int(x)
        y = int(y)
        if (x, y) in possible_move:
            return x, y
        msg = retrymsg

def editnumrow(num, maxrow):
    num = str(num)
    if maxrow >= 100:
        return f"{num:>3s}"
    elif maxrow >= 10:
        return f"{num:>2s}"
    else:
        return f"{num}"

def editnumcol(num, maxcol, maxrow):
    num = str(num)
    if maxcol * maxrow >= 100:
        return f"{num:>4s}"
    elif maxcol * maxrow >= 10:
        return f"{num:>3s}"
    else:
        return f"{num:>2s}"

def editprerow(maxrow):
    if maxrow >= 100:
        return "   "
    elif maxrow >= 10:
        return "   "
    else:
        return "  "

def editborder(maxcol, maxrow):
    if maxcol * maxrow >= 100:
        if maxrow >= 10:
            return "  -" + "----" * maxcol + "--"
        else:    
            return " -" + "----" * maxcol + "--"
    elif maxcol * maxrow >= 10:
        return " -" + "---" * maxcol + "--"
    else:
        return " -" + "--" * maxcol + "--"

def countmoves(x, y, maxcol, maxrow, originx, originy, history):
    possible_move = get_possible_move(x, y, maxcol, maxrow, history)
    count = len(possible_move)
    if (originx, originy) in possible_move:
        count -= 1
    return count
    
def show(x, y, maxcol, maxrow, possible_move, history):
    if maxcol * maxrow >= 100:
        emptypos  = " ___"
        knightpos = "   X"
        footprint = "   *"
    elif maxcol * maxrow >= 10:
        emptypos  = " __"
        knightpos = "  X"
        footprint = "  *"
    else:
        emptypos  = " _"
        knightpos = " X"
        footprint = " *"

    print(editborder(maxcol, maxrow))
    for i in range(maxrow):
        print(editnumrow(maxrow - i, maxrow), end="")
        print("|", end="")
        for j in range(maxcol):
            move = (j + 1, maxrow - i)
            if move == (x, y):
                print(knightpos, end="")
            elif move in history:
                print(footprint, end="")
            elif move in possible_move:
                count = countmoves(j + 1, maxrow - i, maxcol, maxrow, x, y, history)
                print(editnumcol(count, maxcol, maxrow), end="")
            else:
                print(emptypos, end="")
        print(" |")
    print(editborder(maxcol, maxrow))
    print(editprerow(maxrow), end="")
    for j in range(maxcol):
        print(editnumcol(j + 1, maxcol, maxrow), end="")
    print("  ")

def get_possible_move(x, y, maxcol, maxrow, history):
    temp_list = []
    up2 = y + 2
    dn2 = y - 2
    left  = x - 1
    right = x + 1
    up = y + 1
    dn = y - 1
    left2  = x - 2
    right2 = x + 2
    temp_list.append((left, up2))
    temp_list.append((right, up2))
    temp_list.append((left, dn2))
    temp_list.append((right, dn2))
    temp_list.append((left2, up))
    temp_list.append((right2, up))
    temp_list.append((left2, dn))
    temp_list.append((right2, dn))
    possible_move = []
    for move in temp_list: 
        x, y = move
        if 1 <= x <= maxcol and 1 <= y <= maxrow:
            if move not in history:
                possible_move.append(move) 

    return possible_move

def game(x, y, maxcol, maxrow):
    history = []
    possible_move = get_possible_move(x, y, maxcol, maxrow, history)
    show(x, y, maxcol, maxrow, possible_move, history)
    history.append((x, y))
    while len(possible_move) > 0:
        x, y = get_move("Enter your next move: ", "Invalid move! Enter your next move: ", possible_move) 
        possible_move = get_possible_move(x, y, maxcol, maxrow, history)
        show(x, y, maxcol, maxrow, possible_move, history)
        history.append((x, y))
    print()
    if len(history) == maxcol * maxrow:
        print("What a great tour! Congratulations!")
    else:
        print("No more possible moves!")
        print(f"Your knight visited {len(history)} squares!")

def knightmove(x, y, maxcol, maxrow, history): 
    
    if len(history) == maxcol * maxrow:
        return True

    possible_move = get_possible_move(x, y, maxcol, maxrow, history)
    if len(possible_move) == 0:
        return False

    movelist = []
    for move in possible_move:
        move_x, move_y = move
        count = countmoves(move_x, move_y, maxcol, maxrow, x, y, history)
        movelist.append([move_x, move_y, count])
    movelist.sort(key=lambda t: -t[2])

    for movec in movelist:
        history.append((movec[0], movec[1]))
        if knightmove(movec[0], movec[1], maxcol, maxrow, history):
            return True
        history.pop(-1)

    return False

def showhistory(history, maxcol, maxrow):
    if maxcol * maxrow >= 100:
        emptypos  = " ___"
    elif maxcol * maxrow >= 10:
        emptypos  = " __"
    else:
        emptypos  = " _"

    print(editborder(maxcol, maxrow))
    for i in range(maxrow):
        print(editnumrow(maxrow - i, maxrow), end="")
        print("|", end="")
        for j in range(maxcol):
            move = (j + 1, maxrow - i)
            index = history.index(move) if move in history else -1
            if index > -1:
                print(editnumcol(index + 1, maxcol, maxrow), end="")
            else:
                print(emptypos, end="")
        print(" |")
    print(editborder(maxcol, maxrow))
    print(editprerow(maxrow), end="")
    for j in range(maxcol):
        print(editnumcol(j + 1, maxcol, maxrow), end="")
    print("  ")

def showsolution(x, y, maxcol, maxrow):
    print()
    print("Here's the solution!")
    history = [(x, y)]
    knightmove(x, y, maxcol, maxrow, history)
    showhistory(history, maxcol, maxrow)

maxcol, maxrow = get_xy("Enter your board dimensions: ", "Invalid dimensions!", sys.maxsize, sys.maxsize)
x, y = get_xy("Enter the knight's starting position: ", "Invalid position!", maxcol, maxrow)
yn = get_yn("Do you want to try the puzzle? (y/n): ", "invalid answer")
if maxcol < 5 or maxrow < 5:
    if not knightmove(x, y, maxcol, maxrow, [(x, y)]):
        print("No solution exists!")
        sys.exit()
if yn == "y":
    game(x, y, maxcol, maxrow)
else:
    showsolution(x, y, maxcol, maxrow)

