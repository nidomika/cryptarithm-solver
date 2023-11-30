import itertools
import re


class CryptoarithmeticProblem:
    def __init__(self, equation):
        self.equation = equation.replace(" ", "")
        self.variables = sorted(set(re.findall(r'[A-Z]', self.equation)))
        self.domains = {var: list(range(10)) for var in self.variables}
        self.constraints = {var: [] for var in self.variables}
        self.carry_vars = {}
        self.create_constraints()

    def create_constraints(self):
        self.add_all_different_constraint()
        self.add_non_zero_constraint()
        self.add_carry_constraints()
        self.add_arithmetic_constraint()

    def add_non_zero_constraint(self):
        first_letters = set(re.findall(r'\b[A-Z]', self.equation))
        for letter in first_letters:
            self.constraints[letter].append(lambda assignment, l=letter: assignment.get(l, 1) != 0)

    def add_all_different_constraint(self):
        # Dodaj ograniczenie, że wszystkie zmienne muszą mieć różne wartości.
        for var1, var2 in itertools.combinations(self.variables, 2):
            self.constraints[var1].append(lambda assignment, v1=var1, v2=var2: assignment.get(v1, None) != assignment.get(v2, None))
            self.constraints[var2].append(lambda assignment, v1=var1, v2=var2: assignment.get(v1, None) != assignment.get(v2, None))

    def add_arithmetic_constraint(self):
        def check_equation(assignment):
            if len(assignment) < len(self.variables):  # Jeszcze nie wszystkie zmienne mają wartość
                return True
            # Sprawdzanie, czy równanie jest poprawne
            left_side, right_side = self.equation.split('=')
            left_words = left_side.split('+')
            left_sum = sum(int(''.join(str(assignment[letter]) for letter in word)) for word in left_words)
            right_sum = int(''.join(str(assignment[letter]) for letter in right_side))
            # print(left_sum, right_sum)
            return left_sum == right_sum

        for var in self.variables:
            self.constraints[var].append(check_equation)

    def add_carry_constraints(self):
        # Podziel równanie na składniki i wynik
        left_side, right_side = self.equation.split('=')
        addends = left_side.split('+')

        # Prawa strona równania określa potrzebną liczbę zmiennych przeniesienia
        max_length = len(right_side)
        carry_vars = ['C{}'.format(i) for i in range(max_length - 1)]
        # Dodaj zmienne przeniesienia do słownika
        self.carry_vars = {var: list(range(len(addends))) for var in carry_vars}
        # Dla każdej kolumny tworzymy ograniczenia binarne
        for i in range(max_length):
            # Zmienne w kolumnie i-tej i przeniesienie z poprzedniej kolumny
            column_vars = [addend[-i - 1] for addend in addends if i < len(addend)]
            # print(column_vars)
            if i > 0:
                column_vars.append(carry_vars[i - 1])

            # Wynik w kolumnie i-tej
            result_var = right_side[-i - 1] if i < len(right_side) else 0

            # Przeniesienie do następnej kolumny
            next_carry_var = carry_vars[i] if i < len(carry_vars) else None

            # Tworzenie ograniczenia dla bieżącej kolumny
            # print(column_vars, result_var, next_carry_var)
            self.create_column_constraint(column_vars, result_var, next_carry_var)

    def create_column_constraint(self, column_vars, result_var, next_carry_var):
        # Funkcja tworząca ograniczenie dla kolumny.
        def column_constraint(assignment):
            # jeśli nie wszystkie zmienne są przypisane lub nie wszystkie zmienne przeniesienia są przypisane, ograniczenie nie jest naruszone.
            # print(column_vars, next_carry_var)
            if any(var not in assignment for var in column_vars) or \
                    (next_carry_var not in assignment):
                # Jeśli nie wszystkie zmienne są przypisane, ograniczenie nie jest naruszone.
                return True

            # Oblicz sumę cyfr w kolumnie plus przeniesienie (jeśli istnieje).
            column_sum = sum(assignment[var] for var in column_vars)
            if next_carry_var:
                column_sum += assignment.get(next_carry_var, 0) * 10

            # Sprawdź, czy suma cyfr pasuje do wyniku (z uwzględnieniem przeniesienia).
            return column_sum % 10 == assignment.get(result_var, 0) and \
                (next_carry_var is None or column_sum // 10 == assignment.get(next_carry_var, 0))

        # Dodaj ograniczenie do wszystkich zmiennych w kolumnie.
        for var in column_vars + [result_var]:
            if var in self.constraints:  # Upewnij się, że wynik jest literą, a nie cyfrą.
                self.constraints[var].append(column_constraint)
