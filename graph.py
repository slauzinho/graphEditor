import sys


def valid_coordinates(coordinates, board):
    """
    Validates if the given pixel coordinates are valid for the size of the given image

    :param coordinates: pixel coordinates
    :param board: List of pixels that forms the main image.
    :return (bool): True if it's valid otherwise False
    """
    return 0 <= coordinates[0] < len(board[0]) and 0 <= coordinates[1] < len(board)


def create_board(column, row):
    """
    Create a board with x columns and y rows.

    :param column: Number of rows to be draw.
    :param row: Number of rows to be draw.
    :return: initial image.
    """
    return [["O" for x in range(column)] for y in range(row)]


def draw_board(board):
    """
    Draws the image on the terminal.

    :param board: List of pixels for main image
    """
    for row in board:
        print(''.join(row))


def draw_pixel(board, values):
    """
    Draws a pixel into the image

    :param board: List of pixels that forms the main image.
    :param values: Arguments for the command, X Y C.
    """
    [column, row, color] = values
    board[int(row) - 1][int(column) - 1] = color


def draw_vertical_line(board, values):
    """
    Draws a vertical line into the image.

    :param board: List of pixels that forms the main image.
    :param values: Arguments for the command, X Y1 Y2 C.
    """
    [column, row1, row2, color] = values
    for index, value in enumerate(board):
        if int(row1) - 1 <= index <= int(row2) - 1:
            board[index][int(column) - 1] = color


def draw_horizontal_line(board, values):
    """
    Draws an horizontal line into the image

    :param board: List of pixels that forms the main image.
    :param values: Arguments for the command, X1 X2 Y C.
    """
    [column1, column2, row, color] = values
    for index, value in enumerate(board[int(row) - 1]):
        if int(column1) - 1 <= index <= int(column2) - 1:
            board[int(row) - 1][index] = color


def check_pixel_recursive(checked, coordinates_in_r, color_to_match, coordinates, board):
    """
    Recursive function that checks if the pixel and the neighbors belong to R.
    Function breaks with default setrecursionlimit, if you want to use this function you
    should uncomment line 235.
    :param checked: List of checked pixels.
    :param coordinates_in_r: list of pixels to be changed.
    :param color_to_match: color to be matched.
    :param coordinates: pixel coordinates.
    :param board: List of pixels that forms the main image.
    """
    # check if we already checked the coordinate and it's valid.
    if coordinates not in checked and valid_coordinates(coordinates, board):
        if board[coordinates[1]][coordinates[0]] == color_to_match:
            coordinates_in_r.append(coordinates)

            checked.append(coordinates)
            # check top neighbour
            check_pixel_recursive(
                checked, coordinates_in_r, color_to_match, (coordinates[0], coordinates[1]-1), board)

            # check bottom neighbour
            check_pixel_recursive(
                checked, coordinates_in_r, color_to_match, (coordinates[0], coordinates[1]+1), board)

            # check left neighbour
            check_pixel_recursive(
                checked, coordinates_in_r, color_to_match, (coordinates[0]-1, coordinates[1]), board)

            # check right neighbour
            check_pixel_recursive(
                checked, coordinates_in_r, color_to_match, (coordinates[0]+1, coordinates[1]), board)


def check_pixel_imperative(color_to_match, board, coordinates):
    """
    Checks if a pixel and it's neighbors belongs to R.
    :param color_to_match: initial color of (X,Y)
    :param board: List of pixels that forms the main image.
    :param coordinates: Initial coordinates (X,Y)
    :return: List of all coordinates that belong to R
    """
    NUMBER_OF_ROWS = len(board)
    NUMBER_OF_COLS = len(board[0])
    coordinates_in_r = [coordinates]  # coordinates to be drawn
    should_be_checked = {coordinates: True}
    already_checked = {}

    while len(should_be_checked) > 0:
        current_coordinates = list(should_be_checked.keys())[0]

        if current_coordinates not in already_checked:
            already_checked[current_coordinates] = True

            neighbor_top = (current_coordinates[0], current_coordinates[1] - 1)
            neighbor_btn = (current_coordinates[0], current_coordinates[1] + 1)
            neighbor_left = (
                current_coordinates[0] - 1, current_coordinates[1])
            neighbor_right = (
                current_coordinates[0] + 1, current_coordinates[1])

            # check top neighbour
            if 0 <= neighbor_top[0] < NUMBER_OF_COLS and 0 <= neighbor_top[1] < NUMBER_OF_ROWS \
                    and board[neighbor_top[1]][neighbor_top[0]] == color_to_match:
                coordinates_in_r.append(neighbor_top)
                if neighbor_top not in already_checked:
                    should_be_checked[neighbor_top] = True

            # check bottom neighbour
            if 0 <= neighbor_btn[0] < NUMBER_OF_COLS and 0 <= neighbor_btn[1] < NUMBER_OF_ROWS \
                    and board[neighbor_btn[1]][neighbor_btn[0]] == color_to_match:
                coordinates_in_r.append(neighbor_btn)
                if neighbor_btn not in already_checked:
                    should_be_checked[neighbor_btn] = True

            # check left neighbour
            if 0 <= neighbor_left[0] < NUMBER_OF_COLS and 0 <= neighbor_left[1] < NUMBER_OF_ROWS \
                    and board[neighbor_left[1]][neighbor_left[0]] == color_to_match:
                coordinates_in_r.append(neighbor_left)
                if neighbor_left not in already_checked:
                    should_be_checked[neighbor_left] = True

            # check right neighbour
            if 0 <= neighbor_right[0] < NUMBER_OF_COLS and 0 <= neighbor_right[1] < NUMBER_OF_ROWS \
                    and board[neighbor_right[1]][neighbor_right[0]] == color_to_match:
                coordinates_in_r.append(neighbor_right)
                if neighbor_right not in already_checked:
                    should_be_checked[neighbor_right] = True

            del should_be_checked[current_coordinates]

    return coordinates_in_r


def draw_region(board, values):
    """
    Fill the region R with the colour C.
    :param board: List of pixels for main image,
    :param values: Arguments for the command, X Y C.
    """
    [column, row, color] = values
    # coordinates_in_r = []
    # checked = []
    color_to_match = board[int(row)-1][int(column)-1]

    # check_pixel(checked, coordinates_in_r, color_to_match, (int(column)-1, int(row)-1), board)
    coordinates_in_r = check_pixel_imperative(
        color_to_match, board, (int(column)-1, int(row)-1))

    for coordinate in coordinates_in_r:
        board[coordinate[1]][coordinate[0]] = color


def valid_column(column):
    """
    Check if a given string is a value column number.
    :param column: string representing the number.
    :return: True if it's valid, False otherwise.
    """
    try:
        return int(column) >= 1
    # If we cant convert the value to string return false
    except ValueError:
        return False


def valid_row(row):
    """
    Check if a given string is a value row number.
    :param row: string representing the number.
    :return: True if it's valid, False otherwise.
    """
    try:
        return 1 <= int(row) <= 250
    # If we cant convert the value to string return false
    except ValueError:
        return False


def valid_color(color):
    """
    Check if a given color is valid. It should be a single letter and be uppercase.
    :param color: Character
    :return: True if it's valid, False otherwise.
    """
    return len(color) == 1 and color.isupper()


def valid_arguments(operation, arguments):
    if operation == 'I':
        return valid_column(arguments[0]) and valid_row(arguments[1])

    if operation == 'L':
        return valid_column(arguments[0]) and valid_row(arguments[1]) and valid_color(arguments[2])

    if operation == 'V':
        return valid_column(arguments[0]) and valid_row(arguments[1]) and valid_row(arguments[2]) \
            and valid_color(arguments[3]) and arguments[1] <= arguments[2]

    if operation == 'H':
        return valid_column(arguments[0]) and valid_column(arguments[1]) and valid_row(arguments[2]) \
            and valid_color(arguments[3]) and arguments[0] <= arguments[1]

    if operation == 'F':
        return valid_column(arguments[0]) and valid_row(arguments[1]) and valid_color(arguments[2])


def main():
    board = []
    # sys.setrecursionlimit(10 ** 6) # Up the recursion limit otherwise python breaks
    while 1:
        print("\n")
        print("===========================")
        print("Commands:")
        print("===========================")
        print("[I M N]. Create a new M x N image with all pixels coloured white (O).")
        print("[C]. Clears the table, setting all pixels to white (O).")
        print("[L X Y C]. Colours the pixel (X,Y) with colour C.")
        print("[V X Y1 Y2 C]. Draw a vertical segment of colour C in column X between rows Y1 and Y2 (inclusive).")
        print("[H X1 X2 Y C]. Draw a horizontal segment of colour C in row Y between columns X1 and X2(inclusive).")
        print("[F X Y C]. Fill the region R with the colour C. R is defined as: Pixel (X,Y) belongs to R. Any other "
              "pixel which is the same colour as (X,Y) and shares a common side with any pixel in R also belongsto "
              "this region.")
        print("[S]. Show the contents of the current image")
        print("[X]. Terminate the session")
        print("===========================\n")
        string_command = input("Please enter your command\n")
        [operation, *values] = string_command.split(" ")

        try:
            if operation == 'I':
                if valid_arguments(operation, values):
                    board = create_board(int(values[0]), int(values[1]))
                else:
                    print("Invalid range of values, please select another range.\n"
                          "I M N where 1 <= M and 1 <= N <= 250\n")

            elif operation == 'C':
                if len(board) > 0:
                    board = create_board(len(board[0]), len(board))
                else:
                    print("You need to create a board first!")

            elif operation == 'S':
                if len(board) > 0:
                    draw_board(board)
                else:
                    print("You should create a board first.")
                    print("Try creating a board using the command I 5 6 for example...")

            elif operation == 'X':
                sys.exit()

            elif operation == 'L':
                if valid_arguments(operation, values):
                    draw_pixel(board, values)
                else:
                    print("Invalid arguments provided.\n"
                          "L X Y C. Where 1 <= X, 1 <= Y <= 250 and C is a Capital Letter")

            elif operation == 'V':
                if valid_arguments(operation, values):
                    draw_vertical_line(board, values)
                else:
                    print("Invalid arguments provided.\n"
                          "V X Y1 Y2 C. Where 1 <= X, 1 <= Y1 <= Y2 <= 250 and C is a Capital Letter")

            elif operation == 'H':
                if valid_arguments(operation, values):
                    draw_horizontal_line(board, values)
                else:
                    print("Invalid arguments provided.\n"
                          "H X1 X2 Y C. Where 1 <= X1 <= X2, 1 <= Y <= 250 and C is a Capital Letter")

            elif operation == 'F':
                if valid_arguments(operation, values):
                    draw_region(board, values)
                else:
                    print("Invalid arguments provided.\n"
                          "F X Y C. Where 1 <= X, 1 <= Y <= 250 and C is a Capital Letter")

            else:
                print("Please give a valid command\n")

        except IndexError:
            print("Incorrect number of arguments provided")


if __name__ == '__main__':
    main()
