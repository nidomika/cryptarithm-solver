# Plik metoda.py

class CSP:
    def __init__(self, problem, heuristic="mrv", enable_forward_checking=True):
        """Inicjalizacja problemu CSP.

        :param problem: Obiekt klasy Problem
        :param enable_forward_checking: flaga określająca, czy uruchomić forward checking
        """
        self.variables = problem.variables
        self.domains = problem.domains
        self.constraints = problem.constraints
        self.assignment = {}
        self.enable_forward_checking = enable_forward_checking
        self.heuristic = heuristic

    def backtracking_search(self):
        """Publiczna metoda rozpoczynająca przeszukiwanie w głąb."""
        return self._recursive_backtracking(self.assignment)

    def _recursive_backtracking(self, assignment):
        """Rekurencyjna funkcja implementująca algorytm przeszukiwania w głąb.

        :param assignment: Obecne przypisanie wartości
        :return: Kompletne przypisanie wartości lub porażka
        """
        # Jeżeli przypisanie jest kompletnie, zwracamy je jako rozwiązanie
        if self._is_complete(assignment):
            return assignment

        # Wybieramy nieprzypisaną zmienną
        var = self.select_unassigned_variable()
        original_domains = self.domains.copy()  # Zapisz oryginalne domeny

        # Próbujemy przypisać wartość z dziedziny zmiennej
        for value in self.domains[var]:
            print("Przypisuję {} = {}".format(var, value))
            print(self._is_consistent(var, value, assignment))
            if self._is_consistent(var, value, assignment):
                # Dodajemy wartość do przypisania i kontynuujemy rekurencyjnie
                assignment[var] = value
                if self.enable_forward_checking:
                    self._forward_check(var, value, assignment)  # Zaktualizuj domeny na podstawie nowego przypisania

                result = self._recursive_backtracking(assignment)
                if result is not None:
                    return result
                # Jeśli wartość nie prowadzi do rozwiązania, usuwamy ją
                del assignment[var]
                if self.enable_forward_checking:
                    self.domains = original_domains.copy()

        return None  # Brak rozwiązania dla obecnej ścieżki

    def _is_complete(self, assignment):
        """Sprawdza, czy przypisanie jest kompletnie (wszystkie zmienne mają wartości)."""
        return set(assignment.keys()) == set(self.variables)


    def select_unassigned_variable(self):
        unassigned_vars = [v for v in self.variables if v not in self.assignment]
        print("unassigned", unassigned_vars)
        if self.heuristic == "mrv":
            return min(unassigned_vars, key=lambda var: len(self.domains[var]))
        elif self.heuristic == "degree":
            return max(unassigned_vars, key=lambda var: self.count_constraining(var))
        elif self.heuristic == "none":
            return unassigned_vars[0]  # Po prostu wybierz pierwszą nieprzypisaną zmienną
        else:
            raise ValueError("Nieznana heurystyka")

    def is_assigned(self, var):
        return var in self.assignment

    def count_constraining(self, var):
        count = 0
        for other_var in self.variables:
            if other_var != var and not self.is_assigned(other_var):
                count += 1
        return count

    def _is_consistent(self, var, value, assignment):
        """Sprawdza, czy przypisanie jest spójne z ograniczeniami."""
        # Sprawdzamy ograniczenia dla każdej zmiennej
        # print("Sprawdzam ograniczenia dla zmiennej {} = {}".format(var, value))
        for constraint in self.constraints.get(var, []):
            if not constraint(assignment):
                return False
        return True

    def _forward_check(self, var, value, assignment):
        for other_var in self.variables:
            if other_var != var and other_var not in assignment:
                # Usuwamy wartość z domeny innych zmiennych, jeśli powoduje to konflikt
                self.domains[other_var] = [v for v in self.domains[other_var] if
                                           self._is_consistent_with_assignment(other_var, v, var, value, assignment)]

    def _is_consistent_with_assignment(self, var, value, other_var, other_value, assignment):
        # Sprawdzanie, czy przypisanie wartości 'value' do 'var' jest spójne z przypisaniem 'other_value' do 'other_var'
        temp_assignment = assignment.copy()
        temp_assignment[var] = value
        temp_assignment[other_var] = other_value
        for constraint in self.constraints.get(var, []):
            if not constraint(temp_assignment):
                return False
        return True

