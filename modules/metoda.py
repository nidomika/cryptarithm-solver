# metoda.py
class CSPSolver:
    def __init__(self, problem):
        self.problem = problem  # Instancja problemu CSP
        self.variables = problem.variables  # Zmienne do przypisania
        self.domains = problem.get_domains()  # Dostępne wartości dla zmiennych
        self.assignments = {}  # Słownik przechowujący obecne przypisania

    def backtrack(self):
        if len(self.assignments) == len(self.variables):
            return self.assignments.copy()  # Jeśli wszystkie zmienne są przypisane, zwróć rozwiązanie

        var = self.select_unassigned_variable()  # Wybierz zmienną do przypisania

        for value in self.order_domain_values(var):
            if self.is_consistent(var, value):
                self.assignments[var] = value  # Spróbuj przypisać wartość
                result = self.backtrack()  # Kontynuuj rekurencyjnie
                if result is not None:
                    return result  # Znaleziono rozwiązanie
                del self.assignments[var]  # Usuń przypisanie i spróbuj inną wartość (backtrack)

        return None  # Brak rozwiązania dla tej ścieżki

    def select_unassigned_variable(self):
        # Heurystyka: wybierz zmienną z najmniejszą liczbą dostępnych wartości
        # (Most Constrained Variable)
        unassigned_vars = [v for v in self.variables if v not in self.assignments]
        return min(unassigned_vars, key=lambda var: len(self.domains[var]))

    def order_domain_values(self, var):
        # Heurystyka: sortuj wartości z domeny na podstawie liczby ograniczeń nałożonych na pozostałe zmienne
        # (Least Constraining Value)
        if var not in self.assignments:
            # Sortuj wartości na podstawie liczby możliwych wartości dla pozostałych zmiennych
            return sorted(self.domains[var], key=lambda value: self.count_constraints(var, value))
        else:
            # Jeśli zmienna jest już przypisana, nie ma potrzeby sortowania
            return self.domains[var]

    def count_constraints(self, var, value):
        # Liczy ograniczenia nałożone na nieprzypisane zmienne przez wartość 'value' zmiennej 'var'
        count = 0
        # Dodaj tymczasowo wartość do zmiennej
        self.assignments[var] = value

        # Sprawdź, czy tymczasowe przypisanie nie narusza ograniczeń
        if not self.problem.constraints(self.assignments):
            # Jeśli narusza, zwiększ licznik
            count += 1
        else:
            # Sprawdź, czy przypisanie zmniejsza domeny innych zmiennych
            for other_var in set(self.variables) - set(self.assignments.keys()):
                for other_value in self.domains[other_var]:
                    # Sprawdź spójność każdej wartości w domenie other_var
                    if not self.problem.constraints(self.assignments):
                        # Jeśli dodanie tej wartości sprawi, że inne przypisania staną się niespójne, zwiększ licznik
                        count += 1
        # Usuń tymczasowe przypisanie
        del self.assignments[var]
        return count

    def is_consistent(self, var, value):
        # Sprawdź, czy przypisanie wartości nie narusza żadnych ograniczeń
        temp_assignments = self.assignments.copy()
        temp_assignments[var] = value
        if not self.problem.constraints(temp_assignments):
            return False

        # Forward checking: zaktualizuj domeny dla pozostałych zmiennych
        for other_var in self.variables:
            if other_var not in temp_assignments:
                # Sprawdź, czy istnieje jakakolwiek wartość, która jest spójna z tymczasowym przypisaniem
                if not any(self.problem.constraints({**temp_assignments, other_var: other_value})
                           for other_value in self.domains[other_var]):
                    # Jeśli nie ma żadnej spójnej wartości, to przypisanie jest niespójne
                    return False

        return True

    def solve(self):
        # Rozpocznij proces backtrackingu
        return self.backtrack()
