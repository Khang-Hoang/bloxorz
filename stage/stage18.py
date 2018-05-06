start = (3, 2)

board = [
    [0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0,  0,  0],
    [1, 1, 10, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0,  0,  0],
    [1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0,  0,  0],
    [1, 10, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0,  0,  1],
    [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1,  0,  0],
    [1, 1, 10, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1,  0,  0],
    [1, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 1, 1,  1,  0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 100, 1,  0],
    [1, 0, 0, 20, 0, 0, 0, 0, 0, 0, 1, 1, 1,  1,  0]
]

buttons = {
    (0, 7): [[1, (3, 8)], [1, (3, 9)]],
    (1, 2): [[0, (3, 12)], [0, (3, 13)], [0, (8, 1)], [0, (8, 2)]],
    (3, 1): [[0, (3, 8)], [0, (3, 9)]],
    (5, 2): [[0, (3, 12)], [0, (3, 13)], [0, (8, 1)], [0, (8, 2)]],
    (6, 8): [[1, (3, 12)], [1, (3, 13)], [1, (8, 1)], [1, (8, 2)]],
    (8, 3): [[2, (4, 5)]]
}
