#airplane problem
filled = 0
number = int(raw_input().strip())
row = 0
tempFilled = -1


def construct(seatsGrid):
    seats = []
    for i in seatsGrid:
        rows = i[1]
        cols = i[0]
        mat = []
        for i in range(rows):
            mat.append([-1]*cols)
        seats.append(mat)
    return seats
    
def printSeats(seats):
    blksize = len(str(number))
    rows = [x[1] for x in seatsGrid]
    cols = [x[0] for x in seatsGrid]
    maximum = max(rows)
    for i in range(maximum):
        rowlist = []
        for j in range(length):
            #print cols[j]
            row = ' '
            if len(seats[j]) <= i:
                for k in range(cols[j]):
                    row += '---'+(' '*(blksize - len(str(k))))
                    row += ' '
            else:
                for k in seats[j][i]:
                    if k == -1:
                                row += '-X-'+(' '*(blksize - len(str(k))))
                                row += ' '
                    else:
                        row += str(k).zfill(3)+(' '*(blksize - len(str(k))))
                        row += ' '
                    #break
            #print row
            rowlist.append(' '.join(row.strip().split()))
        print(' | '.join(rowlist))



def fill_aisle_seats():
    # filled = 0
    global filled
    row = 0
    tempFilled = -1
    while filled < number and filled != tempFilled:
        tempFilled = filled
        for i in range(length):
            if seatsGrid[i][1] > row:
                if i == 0 and seatsGrid[i][0] > 1:
                    filled += 1
                    aisleCol = seatsGrid[i][0] - 1
                    seats[i][row][aisleCol] = filled
                    if filled >= number:
                        break
                elif i == length - 1 and seatsGrid[i][0] > 1:
                    filled += 1
                    aisleCol = 0
                    seats[i][row][aisleCol] = filled
                    if filled >= number:
                        break
                else:
                    filled += 1
                    aisleCol = 0
                    seats[i][row][aisleCol] = filled
                    if filled >= number:
                        break
                    if seatsGrid[i][0] > 1:
                        filled += 1
                        aisleCol = seatsGrid[i][0] - 1
                        seats[i][row][aisleCol] = filled
                        if filled >= number:
                            break
        row += 1

def fill_window_seats():
    row = 0
    global filled
    global number
    tempFilled = 0
    while filled < number and filled != tempFilled:
        tempFilled = filled
        if seatsGrid[0][1] > row:
            filled += 1
            window = 0
            seats[0][row][window] = filled
            if filled >= number:
                break
        if seatsGrid[length-1][1] > row:
            filled += 1
            window = seatsGrid[length-1][0] - 1
            seats[length-1][row][window] = filled
            if filled >= number:
                break
        row += 1

def fill_middle_seats():
    row = 0
    tempFilled = 0
    global filled
    while filled < number and filled != tempFilled:
        tempFilled = filled
        for i in range(length):
            if seatsGrid[i][1] > row:
                if seatsGrid[i][0] > 2 and filled < number:
                    for col in range(1, seatsGrid[i][0] - 1):
                        filled += 1
                        seats[i][row][col] = filled
                        if filled >= number:
                            break
        row += 1




seatsGrid=[]
while True:
    try:
        seats = list(map(int, raw_input().strip().split()))
        seatsGrid.append(seats)
    except EOFError:
        break
#print seatsGrid
#seatsGrid = [[3,2], [4,3], [2,3], [3,4]]

seats = construct(seatsGrid)

length = len(seatsGrid)

# Aisle
fill_aisle_seats()

# Window
fill_window_seats()

# Center
fill_middle_seats()


printSeats(seats)

##input1:
#30
#3 2
#4 3
#2 3
#3 4

##input2:
#0
#1 5
#3 6
#2 4
#3 2
