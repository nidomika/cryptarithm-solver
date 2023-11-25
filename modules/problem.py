def word_to_number(word, assignments):
    # Przekształca słowo w liczbę na podstawie obecnych przypisań
    number = 0
    for letter in word:
        number = number * 10 + assignments.get(letter, 0)
    return number


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

    def is_constraining(self, var, other_var):
        # W problemach kryptoarytmetycznych każda litera ogranicza każdą inną
        return var != other_var

    def get_domains(self):
        # Domeny wartości dla zmiennych (dla kryptoarytmetycznego to cyfry 0-9)
        domains = {var: set(range(10)) for var in self.variables}
        return domains

    def constraints(self, assignments):
        # Wszystkie różne
        if len(set(assignments.values())) != len(assignments):
            return False

        # Domena: pierwsze litery nie mogą być zero
        for first_letter in self.first_letters:
            if assignments.get(first_letter) == 0:
                return False

        # Kolumny arytmetyczne
        if all(var in assignments for var in self.variables):
            carry = 0
            max_length = max(len(word) for word in self.words + [self.result_word])

            for i in range(1, max_length + 1):
                column_sum = sum(assignments.get(word[-i], 0) for word in self.words if len(word) >= i) + carry
                result_digit = assignments.get(self.result_word[-i], 0) if len(self.result_word) >= i else 0
                if column_sum % 10 != result_digit:
                    return False
                carry = column_sum // 10

            # Sprawdź, czy ostatnie przeniesienie pasuje do najwyższej cyfry w słowie wynikowym
            if carry != (assignments.get(self.result_word[-max_length], 0) if len(self.result_word) > max_length else 0):
                return False


        return True

