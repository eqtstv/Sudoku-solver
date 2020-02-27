def import_grid():
    grid = []
    print("Input line by line:")
    i = 0
    while i<9:
        print("Enter line: {}".format(i+1))
        line = input()
        if len(line) != 9:
            print("Line must have 9 numbers. This has: {}".format(len(line)))
        elif not line.isdigit():
            print("You have to enter only digits")
        else:
            grid.append([int(x) for x in list(line)])
            i += 1
    return grid


if __name__ == "__main__":
    print(import_grid())