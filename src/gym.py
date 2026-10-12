__all__ = [
    'get_gym_list',
    'gym_battle_time',
]

GYM_LIST = {'2' :  35,
            '3' :  40,
            '4' :  45,
            '5' :  50,
            '6' :  55,
            '7' :  60,
            '8' :  65,
            '9' :  70,
            'B' :  75,
            'C' :  80,
            'D' :  85,
            'E' :  90,
            'G' :  95,
            'H' : 100,
            'I' : 110,
            'J' : 120,
            'K' : 130,
            'L' : 140,
            'N' : 150,
            'O' : 155,
            'P' : 160,
            'Q' : 165,
            'S' : 170,
            'T' : 180}

def get_gym_list() -> list[str]:
    return list(GYM_LIST.keys())

def gym_battle_time(gym : str, power : float) -> float:
    gym_dificulty = GYM_LIST[gym]
    return gym_dificulty / power