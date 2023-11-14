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

    def get_domains(self):
        # Domeny wartości dla zmiennych (dla kryptoarytmetycznego to cyfry 0-9)
        domains = {var: set(range(10)) for var in self.variables}
        return domains

    def constraints(self, assignments):
        # Sprawdź, czy wszystkie przypisane wartości są unikalne
        assigned_values = list(assignments.values())
        if len(assigned_values) != len(set(assigned_values)):
            return False

        # Sprawdź, czy suma słów wejściowych jest równa słowu wynikowemu,
        # tylko jeśli wszystkie zmienne w słowie wynikowym i wejściowym mają przypisania
        if all(var in assignments for var in self.result_word):
            if all(all(var in assignments for var in word) for word in self.words):
                sum_input = sum(word_to_number(word, assignments) for word in self.words)
                sum_result = word_to_number(self.result_word, assignments)
                return sum_input == sum_result

        # Sprawdź, czy pierwsze litery słów wejściowych nie są 0
        for word in self.words:
            if assignments.get(word[0]) == 0:
                return False

        return True

