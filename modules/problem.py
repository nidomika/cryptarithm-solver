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
        return set(letter for letter in self.equation if letter.isalpha())

    def get_first_letters(self):
        # Zwraca pierwsze litery każdego słowa (które nie mogą być 0)
        words = self.equation.split('=')[0].split('+')
        return {word.strip()[0] for word in words}

    def parse_equation(self):
        # Parsowanie równania na słowa wejściowe i wynikowe
        input_part, result_part = self.equation.split('=')
        input_words = [word.strip() for word in input_part.split('+')]
        result_word = result_part.strip()
        print(input_words, result_word)
        return input_words, result_word

    def get_domains(self):
        # Domeny wartości dla zmiennych (dla kryptoarytmetycznego to cyfry 0-9)
        return {var: set(range(10)) for var in self.variables}

    def constraints(self, assignments):
        # Sprawdź, czy wszystkie przypisane wartości są unikalne
        if len(set(assignments.values())) != len(assignments):
            return False

        # Sprawdź, czy pierwsze litery słów nie są przypisane do 0
        for first_letter in self.first_letters:
            if assignments.get(first_letter) == 0:
                return False

        # Suma słów wejściowych jest równa słowu wynikowemu, jeśli wszystkie zmienne w słowie wynikowym mają przypisania
        if all(var in assignments for var in self.result_word):
            sum_input = sum(word_to_number(word, assignments) for word in self.words)
            sum_result = word_to_number(self.result_word, assignments)
            if sum_input != sum_result:
                return False

        # Jeśli dotąd nie stwierdzono żadnych naruszeń, wszystkie ograniczenia są spełnione
        return True
