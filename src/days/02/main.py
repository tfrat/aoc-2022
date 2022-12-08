def determine_score(one: str, two: str) -> int:
    """
    A,X - Rock, B,Y - Paper, C,Z - Scissors
    Rock = 1
    Paper = 2
    Scissors = 3

    Lose = 0
    Draw = 3
    Win = 6
    :param one:
    :param two:
    :return:
    """

    play_points = {
        "X": 1,
        "Y": 2,
        "Z": 3
    }

    win = {
        "Z": "B",
        "Y": "A",
        "X": "C"
    }

    draw = {
        "X": "A",
        "Y": "B",
        "Z": "C"
    }

    score = play_points[two]

    if one == win[two]:
        score += 6
    if one == draw[two]:
        score += 3

    return score


def determine_score_two(one: str, two: str) -> int:
    """
    A - Rock, B - Paper, C - Scissors
    X - Lose, Y - Draw, Z - Win
    Rock = 1
    Paper = 2
    Scissors = 3

    Lose = 0
    Draw = 3
    Win = 6
    :param one:
    :param two:
    :return:
    """
    win = {
        "A": 8,
        "B": 9,
        "C": 7
    }

    draw = {
        "A": 4,
        "B": 5,
        "C": 6
    }

    lose = {
        "A": 3,
        "B": 1,
        "C": 2
    }

    play_needed = {
        "X": lose,
        "Y": draw,
        "Z": win
    }

    return play_needed[two][one]


with open("input.txt", "r", encoding="utf-8") as f:
    plays = f.readlines()

total_score = 0
for play in plays:
    player_one, player_two = play[:-1].split(" ")
    total_score += determine_score_two(player_one, player_two)

print(total_score)
