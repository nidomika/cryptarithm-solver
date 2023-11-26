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

    def get_domains(self):
        # Domeny wartości dla zmiennych (dla kryptoarytmetycznego to cyfry 0-9)
        domains = {var: set(range(10)) for var in self.variables}
        return domains

    def constraints(self, assignments):
        # Sprawdź, czy wszystkie przypisane wartości są unikalne
        assigned_values = list(assignments.values())
        if len(assigned_values) != len(set(assigned_values)):
            return False

        if all(var in assignments for var in self.variables):
            carry = 0
            words = self.words  # Lista słów po lewej stronie równania
            result_word = self.result_word  # Słowo po prawej stronie równania
            max_length = max(len(word) for word in words + [result_word])

            for i in range(1, max_length + 1):
                column_sum = sum(assignments.get(word[-i], 0) for word in words if len(word) >= i) + carry
                result_digit = assignments.get(result_word[-i], 0) if len(result_word) >= i else 0

                if column_sum % 10 != result_digit:
                    return False
                carry = column_sum // 10

            # Sprawdź ostatnie przeniesienie dla najwyższej cyfry w słowie wynikowym
            if carry != (assignments.get(result_word[-max_length], 0) if len(result_word) > max_length else 0):
                return False

        # Sprawdź, czy pierwsze litery słów wejściowych nie są 0
        for word in self.words:
            if assignments.get(word[0]) == 0:
                return False

        return True

