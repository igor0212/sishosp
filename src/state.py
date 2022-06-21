import random

class State:

    def get():
        #Sorteando número aleatório entre 0 e 1
        number = random.random()

        #Pacientes em estado leve representam 25%
        if number <= .25: 
            return 1, 4, False
        #Pacientes em estado moderado representam 25%
        elif number <= .50: 
            return 2, 3, False
        #Pacientes em estado grave representam 25%
        elif number <= .75: 
            return 3, 2, False
        #Pacientes em estado gravíssimo representam 25%
        return 4, 1, True