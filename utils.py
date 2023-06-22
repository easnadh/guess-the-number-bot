from random import randint


def get_random_number() -> int:
    return randint(1, 5)


user: dict = {
    'secret_number': None,
    'attempts': None,
    'total_games': 0,
    'wins': 0
}
