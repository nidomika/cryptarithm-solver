import itertools
import re


class CryptoarithmeticProblem:
    def __init__(self, equation):
        self.equation = equation.replace(" ", "")
        self.variables = sorted(set(re.findall(r'[A-Z]', self.equation)))
        self.domains = {var: list(range(10)) for var in self.variables}
        self.constraints = {var: [] for var in self.variables}
        self.create_constraints()

    def create_constraints(self):
        # Dodaj ogólne ograniczenie unikalności wartości.
        self.add_all_different_constraint()

        # Dodaj ograniczenie, że pierwsze litery nie mogą być zerami.
        first_letters = set(re.findall(r'\b[A-Z]', self.equation))
        for letter in first_letters:
            self.constraints[letter].append(lambda values, l=letter: values[l] != 0)

        # Dodaj ograniczenie arytmetyczne dla całego równania.
        self.add_non_zero_constraint()
        self.add_arithmetic_constraint()
        self.add_carry_constraints()

    def add_non_zero_constraint(self):
        first_letters = set(re.findall(r'\b[A-Z]', self.equation))
        for letter in first_letters:
            self.constraints[letter].append(lambda assignment, l=letter: assignment.get(l, 1) != 0)

    def add_all_different_constraint(self):
        def all_different(values):
            return len(values) == len(set(values))
        for pair in itertools.combinations(self.variables, 2):
            self.constraints[pair[0]].append(lambda values, p=pair: all_different([values.get(p[0]), values.get(p[1])]))

    def add_arithmetic_constraint(self):
        def check_equation(assignment):
            if len(assignment) < len(self.variables):  # Jeszcze nie wszystkie zmienne mają wartość
                return True
            #  sprawdzanie, czy równanie jest poprawne
            left_side, right_side = self.equation.split('=')
            left_side = left_side.replace('+', '')
            left_sum = sum(assignment[var] for var in left_side)
            right_sum = sum(assignment[var] for var in right_side)
            return left_sum == right_sum
        for var in self.variables:
            self.constraints[var].append(check_equation)

    def add_carry_constraints(self):
        # Podziel równanie na składniki i wynik.
        left_side, right_side = self.equation.split('=')
        addends = left_side.split('+')

        # Najdłuższy składnik określa potrzebną liczbę zmiennych przeniesienia.
        max_length = max(len(addend) for addend in addends)
        carry_vars = ['C{}'.format(i) for i in range(max_length)]
        self.variables.extend(carry_vars)

        # Każda zmienna przeniesienia może mieć wartość 0 lub 1.
        for carry_var in carry_vars:
            self.domains[carry_var] = [0, 1]
            self.constraints[carry_var] = []

        # Dla każdej kolumny tworzymy ograniczenia binarne.
        for i in range(max_length):
            # Zmienne w kolumnie i-tej i przeniesienie z poprzedniej kolumny.
            column_vars = [addend[-i - 1] for addend in addends if i < len(addend)]
            if i > 0:
                column_vars.append(carry_vars[i - 1])

            # Wynik w kolumnie i-tej.
            result_var = right_side[-i - 1] if i < len(right_side) else '0'

            # Przeniesienie do następnej kolumny.
            next_carry_var = carry_vars[i] if i < len(carry_vars) - 1 else None

            # Tworzenie ograniczenia dla bieżącej kolumny.
            self.create_column_constraint(column_vars, result_var, next_carry_var)

    def create_column_constraint(self, column_vars, result_var, next_carry_var):
        # Funkcja tworząca ograniczenie dla kolumny.
        def column_constraint(assignment):
            if any(var not in assignment for var in column_vars):
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
