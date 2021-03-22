import numpy as np

grid = []
static_pieces = set()
letters = 'ISZLJOT'
keywords = ['right', 'left', 'down', 'break', 'rotate']
flag = 1


def output(row_, col_):
    f = 0
    t = row_

    for j in range(col_):
        print(*grid[f:t])
        f = t
        t += row_

    print()


def update_grid(r, c, *pieces):
    for p in pieces:
        for el in p:
            grid[el] = '0'
    output(r, c)


def check_border(piece1, row1, side_):
    for ind, c in enumerate(piece1):
        if c % row1 == 0 and side_ == 'left' or (c + 1) % row1 == 0 and side_ == 'right':
            return False
    return True


def update_coord(letter):
    i_piece = np.array([[4, 14, 24, 34], [3, 4, 5, 6], [4, 14, 24, 34], [3, 4, 5, 6], [4, 14, 24, 34]])
    s_piece = np.array([[5, 4, 14, 13], [4, 14, 15, 25], [5, 4, 14, 13], [4, 14, 15, 25], [5, 4, 14, 13]])
    z_piece = np.array([[4, 5, 15, 16], [5, 15, 14, 24], [4, 5, 15, 16], [5, 15, 14, 24], [4, 5, 15, 16]])
    l_piece = np.array([[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14], [4, 14, 24, 25]])
    j_piece = np.array([[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16], [5, 15, 25, 24]])
    o_piece = np.array([[4, 14, 15, 5], [4, 14, 15, 5], [4, 14, 15, 5], [4, 14, 15, 5], [4, 14, 15, 5]])
    t_piece = np.array([[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15], [4, 14, 24, 15]])

    pieces = {'I': i_piece, 'S': s_piece, 'Z': z_piece, 'L': l_piece, 'J': j_piece, 'O': o_piece, 'T': t_piece}

    return pieces[letter]


while True:
    user_input = input().split()

    try:
        if len(user_input) == 2:
            static_pieces = set()
            row = int(user_input[0])
            col = int(user_input[1])
            dim = row * col
            grid = ['-' for i in range(dim)]
            piece_state = 0
            output(row, col)

        elif len(user_input) == 1:
            if user_input[0] == 'exit':
                break

            if user_input[0] in letters:
                if flag == 1:
                    piece = update_coord(user_input[0])
                    piece_state = 0
                    check_static = [i + row in static_pieces for i in piece[piece_state]]
                    grid = ['-' for i in range(dim)]
                    update_grid(row, col, piece[piece_state], static_pieces)
                    flag = 0

                continue

            elif user_input[0] in keywords:
                if max(piece[piece_state]) < (dim - row) and not any(check_static):
                    piece += row

                elif min(piece[piece_state]) < row:
                    output(row, col)
                    print('Game Over!')
                    break

                grid = ['-' for i in range(dim)]

                if user_input[0] == 'rotate':
                    if piece_state < len(piece):
                        piece_state += 1
                    else:
                        piece_state = 0

                elif user_input[0] == 'right':
                    side = 'right'
                    check = check_border(piece[piece_state], row, side)

                    if check:
                        piece += 1

                elif user_input[0] == 'left':
                    side = 'left'
                    check = check_border(piece[piece_state], row, side)

                    if check:
                        piece -= 1

                elif user_input[0] == 'break':
                    while True:
                        indexes = []
                        if all((i in static_pieces for i in range(dim - row, dim))):
                            indexes = [i + row for i in static_pieces if i < (dim - row)]
                            static_pieces.clear()
                            for i in indexes:
                                static_pieces.add(i)
                        else:
                            break

                    update_grid(row, col, static_pieces)
                    continue

                check_static = [i + row in static_pieces for i in piece[piece_state]]

                if max(piece[piece_state]) >= (dim - row) or any(check_static):
                    flag = 1

                    for i in piece[piece_state]:
                        static_pieces.add(i)

                update_grid(row, col, piece[piece_state], static_pieces)

    except (ValueError, NameError):
        continue
