from metoda import CSPSolver
from problem import CryptoarithmeticProblem


def main():
    # Tutaj użytkownik może wprowadzić swoje równanie lub możesz mieć zdefiniowane na stałe
    # equation = input("Proszę wprowadzić równanie kryptoarytmetyczne (np. SEND + MORE = MONEY): ")
    # equation = "SEND + MORE = MONEY"
    # equation = "NUM + BER = PLAY"
    # equation = "TWO + TWO = FOUR"
    # equation = "WHAT + WAS + THY = CAUSE"
    equation = "CP + IS + FUN = TRUE"

    # equation = ("SO+MANY+MORE+MEN+SEEM+TO+SAY+THAT+THEY+MAY+SOON+TRY+TO+STAY+AT+HOME+SO+AS+TO+SEE+OR+HEAR+THE+SAME+ONE"
    #             "+MAN+TRY+TO+MEET+THE+TEAM+ON+THE+MOON+AS+HE+HAS+AT+THE+OTHER+TEN=TESTS")

    # equation = " ".join([
    #     "THIS + A + FIRE + THEREFORE + FOR + ALL + HISTORIES + I + TELL + A + TALE + THAT + FALSIFIES + ",
    #     "ITS + TITLE + TIS + A + LIE + THE + TALE + OF + THE + LAST + FIRE + HORSES + LATE + AFTER + ",
    #     "THE + FIRST + FATHERS + FORESEE + THE + HORRORS + THE + LAST + FREE + TROLL + TERRIFIES + THE + ",
    #     "HORSES + OF + FIRE + THE + TROLL + RESTS + AT + THE + HOLE + OF + LOSSES + IT + IS + THERE + ",
    #     "THAT + SHE + STORES + ROLES + OF + LEATHERS + AFTER + SHE + SATISFIES + HER + HATE + OFF + ",
    #     "THOSE + FEARS + A + TASTE + RISES + AS + SHE + HEARS + THE + LEAST + FAR + HORSE + THOSE + ",
    #     "FAST + HORSES + THAT + FIRST + HEAR + THE + TROLL + FLEE + OFF + TO + THE + FOREST + THE + ",
    #     "HORSES + THAT + ALERTS + RAISE + THE + STARES + OF + THE + OTHERS + AS + THE + TROLL + ASSAILS + ",
    #     "AT + THE + TOTAL + SHIFT + HER + TEETH + TEAR + HOOF + OFF + TORSO + AS + THE + LAST + HORSE + ",
    #     "FORFEITS + ITS + LIFE + THE + FIRST + FATHERS + HEAR + OF + THE + HORRORS + THEIR + FEARS + ",
    #     "THAT + THE + FIRES + FOR + THEIR + FEASTS + ARREST + AS + THE + FIRST + FATHERS + RESETTLE + ",
    #     "THE + LAST + OF + THE + FIRE + HORSES + THE + LAST + TROLL + HARASSES + THE + FOREST + HEART + ",
    #     "FREE + AT + LAST + OF + THE + LAST + TROLL + ALL + OFFER + THEIR + FIRE + HEAT + TO + THE + ",
    #     "ASSISTERS + FAR + OFF + THE + TROLL + FASTS + ITS + LIFE + SHORTER + AS + STARS + RISE + THE + ",
    #     "HORSES + REST + SAFE + AFTER + ALL + SHARE + HOT + FISH + AS + THEIR + AFFILIATES + TAILOR + ",
    #     "A + ROOFS + FOR + THEIR + SAFE = FORTRESSES"
    # ])

    # Stworzenie instancji problemu
    problem = CryptoarithmeticProblem(equation)

    # Stworzenie solvera z podanym problemem
    solver = CSPSolver(problem)
    solver.reset_solver()  # Resetuj solver przed każdym nowym wywołaniem

    # Rozpoczęcie procesu rozwiązywania
    solution = solver.solve()
    # Wyświetlenie wyniku
    if solution:
        print("Rozwiązanie zostało znalezione:")
        for var, value in solution.items():
            print(f"{var} = {value}")
    else:
        print("Nie udało się znaleźć rozwiązania. 👉👈")


if __name__ == "__main__":
    main()
