class CryptoarithmeticProblem:
    def __init__(self, equation):
        self.equation = equation
        self.variables = self._extract_variables()
        self.first_letters = self._get_first_letters()
        self.words, self.result_word = self._parse_equation()
        self.domains = {var: list(range(10)) for var in self.variables}
        # Ustawienie ograniczeń
        self.constraints = self._setup_constraints()

    def _extract_variables(self):
        # Ekstrakcja zmiennych z równania
        return sorted(set(letter for letter in self.equation if letter.isalpha()))

    def _get_first_letters(self):
        # Zwraca pierwsze litery każdego słowa (które nie mogą być 0)
        words = self.equation.split('=')[0].split('+')
        return sorted(set(word.strip()[0] for word in words))

    def _parse_equation(self):
        # Parsowanie równania na słowa wejściowe i wynikowe
        input_part, result_part = self.equation.split('=')
        input_words = [word.strip() for word in input_part.split('+')]
        result_word = result_part.strip()
        return input_words, result_word

    def _setup_constraints(self):
        # Przypisanie listy funkcji ograniczeń do każdej zmiennej
        constraints = {var: [self.all_different_constraint,
                             self.first_letter_not_zero_constraint,
                             self.columns_sum_with_carry_constraint] for var in self.variables}
        return constraints

    def all_different_constraint(self, assignment):
        # Wszystkie wartości przypisane muszą być różne
        return len(set(assignment.values())) == len(assignment.values())

    def first_letter_not_zero_constraint(self, assignment):
        # Pierwsze litery każdego słowa nie mogą być 0
        return all(assignment[letter] != 0 for letter in self.first_letters if letter in assignment)

    def columns_sum_with_carry_constraint(self, assignment):
        if len(assignment) < len(self.variables):
            return False  # Nie wszystkie zmienne są jeszcze przypisane

        # Obliczanie sumy dla każdej kolumny
        carry = 0
        for i in range(1, len(self.result_word) + 1):
            sum_column = carry
            for word in self.words:
                if len(word) >= i:
                    sum_column += assignment.get(word[-i], 0)
            if len(self.result_word) >= i:
                sum_column -= assignment.get(self.result_word[-i], 0)
            if sum_column % 10 != 0 or (sum_column // 10 != carry and i != len(self.result_word)):
                return False
            carry = sum_column // 10

        # Sprawdzenie, czy ostatnie przeniesienie jest równe 0
        return carry == 0

    def word_to_number(self, word, assignment):
        # Konwersja słowa na liczbę na podstawie przypisania
        return int(''.join(str(assignment[letter]) for letter in word if letter in assignment))

    def columns_sum_with_carry(self, assignments):
        # Sprawdź, czy suma kolumn jest poprawna (z przeniesieniami)
        # np. SEND + MORE = MONEY
        #   S E N D
        # + M O R E
        # ----------
        # M O N E Y
        #
        # D+E=Y+10*(wartość kol)//10 (D - ostatnia cyfra pierwszego słowa, E - ostatnia cyfra drugiego słowa, Y - ostatnia cyfra wyniku)
        # N+R+przeniesienie = E+10*(wartość kol)//10
        # E+O+przeniesienie = N+10*(wartość kol)//10
        # S+M+przeniesienie = O+10*(wartość kol)//10
        # przeniesienie = M

        words_inverted = [word[::-1] for word in self.words]
        result_word_inverted = self.result_word[::-1]
        carry = 0
        for i in range(len(result_word_inverted)):
            print(assignments, result_word_inverted[i], words_inverted, carry, i)
            column_values = [assignments[word[i]] if i < len(word) else 0 for word in words_inverted]
            column_sum = sum(column_values) + carry
            carry = column_sum // 10
            if column_sum != assignments[result_word_inverted[i]] + 10 * carry:
                return False
        return True
