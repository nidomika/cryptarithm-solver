class CryptoarithmeticProblem:
    def __init__(self, equation):
        self.equation = equation
        self.variables = self.extract_variables()
        self.first_letters = self.get_first_letters()
        self.words, self.result_word = self.parse_equation()

    def extract_variables(self):
        # Ekstrakcja zmiennych z równania
        return sorted(set(letter for letter in self.equation if letter.isalpha()))

    def get_first_letters(self):
        # Zwraca pierwsze litery każdego słowa (które nie mogą być 0)
        words = self.equation.split('=')[0].split('+')
        return {word.strip()[0] for word in words}

    def parse_equation(self):
        # Parsowanie równania na słowa wejściowe i wynikowe
        input_part, result_part = self.equation.split('=')
        input_words = [word.strip() for word in input_part.split('+')]
        result_word = result_part.strip()
        return input_words, result_word

    def get_constraints(self):
        # Ograniczenie AllDifferent dla wszystkich zmiennych
        constraints = [(self.variables, self.all_different)]

        # Ograniczenie, że pierwsze litery nie mogą być zerem
        first_letters = [word[0] for word in self.words + [self.result_word]]
        constraints.append((first_letters, self.first_letters_not_zero))

        # Ograniczenia dla sumy kolumn z przeniesieniami
        max_length = max(len(word) for word in self.words + [self.result_word])
        for i in range(max_length):
            # Zbierz zmienne reprezentujące cyfry w i-tej kolumnie
            column_vars = [word[::-1][i] for word in self.words + [self.result_word] if i < len(word)]
            constraints.append((column_vars, self.columns_sum_with_carry))
        print(constraints)
        return constraints

    def all_different(self, assignments):
        # Sprawdź, czy wszystkie zmienne mają różne wartości
        return len(set(assignments.values())) == len(assignments)

    def first_letters_not_zero(self, assignments):
        # Sprawdź, czy pierwsze litery słów wejściowych nie są 0
        for word in self.words:
            if assignments.get(word[0]) == 0:
                return False
        return True

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

        # words_inverted = [word[::-1] for word in self.words]
        # result_word_inverted = self.result_word[::-1]
        # carry = 0
        # for i in range(len(result_word_inverted)):
        #     print(assignments, result_word_inverted[i], words_inverted, carry, i)
        #     column_values = [assignments[word[i]] if i < len(word) else 0 for word in words_inverted]
        #     column_sum = sum(column_values) + carry
        #     carry = column_sum // 10
        #     if column_sum != assignments[result_word_inverted[i]] + 10 * carry:
        #         return False
        # return True
        pass

    def check_constraints(self, assignments):
        # Sprawdź, czy wszystkie ograniczenia są spełnione
        if self.all_different(assignments):
            if self.first_letters_not_zero(assignments):
                if not self.columns_sum_with_carry(assignments):
                    return True
        return False

    def get_domains(self):
        # Domeny wartości dla zmiennych (dla kryptoarytmetycznego to cyfry 0-9)
        domains = {var: set(range(10)) for var in self.variables}
        return domains

    def get_variables(self):
        return self.variables
