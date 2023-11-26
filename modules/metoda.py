import time


class CSPSolver:
    def __init__(self, problem, heuristic="mrv", use_forward_checking=True):
        self.problem = problem  # Instancja problemu CSP
        self.variables = problem.variables  # Zmienne do przypisania
        self.domains = problem.get_domains()  # Dostępne wartości dla zmiennych
        self.assignments = {}  # Słownik przechowujący obecne przypisania
        self.nodes_expanded = 0  # Licznik rozwiniętych węzłów
        self.backtracks = 0  # Licznik nawrotów
        self.pruned_domains = {}  # Słownik przechowujący domeny po forward checking
        self.heuristic = heuristic  # Heurystyka wyboru zmiennej
        self.use_forward_checking = use_forward_checking  # Czy używać forward checking

    def backtrack(self):
        if len(self.assignments) == len(self.variables):
            return self.assignments.copy()  # Jeśli wszystkie zmienne są przypisane, zwróć rozwiązanie

        self.nodes_expanded += 1
        var = self.select_unassigned_variable()  # Wybierz zmienną do przypisania

        for value in self.order_domain_values(var):
            if self.is_consistent(var, value):
                self.assignments[var] = value  # Spróbuj przypisać wartość
                result = self.backtrack()  # Kontynuuj rekurencyjnie
                if result is not None:
                    return result  # Znaleziono rozwiązanie
                self.backtracks += 1
                del self.assignments[var]  # Usuń przypisanie i spróbuj inną wartość (backtrack)
                # Przywróć usunięte wartości z domen
                for other_var, other_value in self.pruned_domains[var]:
                    self.domains[other_var].add(other_value)
                self.pruned_domains[var].clear()

        return None  # Brak rozwiązania dla tej ścieżki

    def select_unassigned_variable(self):
        unassigned_vars = [v for v in self.variables if v not in self.assignments]
        if self.heuristic == "mrv":
            return min(unassigned_vars, key=lambda var: len(self.domains[var]))
        elif self.heuristic == "degree":
            return max(unassigned_vars, key=lambda var: self.count_constraining(var))
        elif self.heuristic == "none":
            return unassigned_vars[0]  # Po prostu wybierz pierwszą nieprzypisaną zmienną
        else:
            raise ValueError("Nieznana heurystyka")

    def count_constraining(self, var):
        count = 0
        for other_var in self.variables:
            if other_var != var and not self.is_assigned(other_var):
                count += 1
        return count

    def is_assigned(self, var):
        return var in self.assignments

    def order_domain_values(self, var):
        return list(self.domains[var])

    def is_consistent(self, var, value):
        # Tymczasowe przypisanie dla sprawdzenia
        self.assignments[var] = value

        # Jeśli forward checking jest wyłączone, sprawdź tylko obecne przypisanie
        if not self.use_forward_checking:
            is_consistent = self.problem.constraints(self.assignments)
        else:
            # Logika z forward checking
            self.pruned_domains[var] = set()
            for other_var in self.variables:
                if other_var not in self.assignments:
                    for other_value in self.domains[other_var].copy():
                        if not self.problem.constraints({**self.assignments, other_var: other_value}):
                            self.domains[other_var].remove(other_value)
                            self.pruned_domains[var].add((other_var, other_value))

            if any(not self.domains[other_var] for other_var in self.variables if other_var not in self.assignments):
                # Przywróć domeny przed wyjściem
                for other_var, other_value in self.pruned_domains[var]:
                    self.domains[other_var].add(other_value)
                del self.assignments[var]
                return False

        del self.assignments[var]  # Usuń tymczasowe przypisanie
        return is_consistent if not self.use_forward_checking else True

    def reset_solver(self):
        # Resetuj stan solvera
        self.assignments = {}
        self.pruned_domains = {}

    def solve(self):
        start_time = time.time()
        solution = self.backtrack()
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Możesz zwrócić te wartości, wydrukować je lub zapisać w atrybutach klasy
        print(f"Szybkość uzyskania wyniku: {elapsed_time:.4f} sekund")
        print(f"Liczba rozwijanych węzłów: {self.nodes_expanded}")
        print(f"Liczba nawrotów: {self.backtracks}")

        return solution
