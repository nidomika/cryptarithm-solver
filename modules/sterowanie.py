from metoda import CSPSolver
from problem import CryptoarithmeticProblem
import time


def main():
    # Tutaj użytkownik może wprowadzić swoje równanie lub możesz mieć zdefiniowane na stałe
    # equation = input("Proszę wprowadzić równanie kryptoarytmetyczne (np. SEND + MORE = MONEY): ")
    equation = "SEND + MORE = MONEY"

    # Stworzenie instancji problemu
    problem = CryptoarithmeticProblem(equation)

    # Stworzenie solvera z podanym problemem
    solver = CSPSolver(problem)

    start_time = time.time()
    # Rozpoczęcie procesu rozwiązywania
    solution = solver.solve()
    end_time = time.time()
    # Wyświetlenie wyniku
    if solution:
        print("Rozwiązanie zostało znalezione:")
        for var, value in solution.items():
            print(f"{var} = {value}")
    else:
        print("Nie udało się znaleźć rozwiązania.")

    print(f"Czas wykonania: {end_time - start_time}s")


if __name__ == "__main__":
    main()
