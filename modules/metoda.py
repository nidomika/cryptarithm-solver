class BacktrackingSearch:
    def __init__(self, problem):
        """
        Inicjalizacja algorytmu przeszukiwania z nawrotami.
        :param problem: problem do rozwiązania
        """
        self.variables = problem.variables
        self.domains = problem.domains
        self.constraints = problem.constraints
        self.assigment = {}

    def is_complete(self, assignment):
        """
        Sprawdza, czy przypisanie jest kompletne, tj. czy każda zmienna ma wartość.
        :param assignment: aktualne przypisanie wartości
        :return: True jeśli przypisanie jest kompletne, False w przeciwnym wypadku
        """
        return set(assignment.keys()) == set(self.variables)

    def select_unassigned_variable(self, assignment):
        """
        Wybiera zmienną, która nie ma jeszcze przypisanej wartości.
        :param assignment: aktualne przypisanie wartości
        :return: zmienna bez przypisanej wartości
        """
        for var in self.variables:
            # print(assignment)
            if var not in assignment:
                return var
        return None

    def order_domain_values(self, var, assignment):
        """
        Zwraca możliwe wartości dla zmiennej, zgodnie z jej dziedziną.
        :param var: zmienna do przypisania
        :param assignment: aktualne przypisanie wartości
        :return: lista wartości dla zmiennej
        """
        return self.domains[var]

    def is_consistent(self, var, value, assignment):
        """
        Sprawdza, czy wartość zmiennej jest zgodna z ograniczeniami.
        :param var: zmienna do przypisania
        :param value: wartość do przypisania
        :param assignment: aktualne przypisanie wartości
        :return: True, jeśli wartość jest zgodna z ograniczeniami, False w przeciwnym wypadku
        """
        assignment[var] = value
        for constraint in self.constraints[var]:
            if not constraint(assignment):
                del assignment[var]
                return False
        del assignment[var]
        return True

    def recursive_backtracking(self, assignment):
        """
        Główna funkcja rekurencyjna algorytmu.
        :param assignment: aktualne przypisanie wartości
        :return: przypisanie spełniające ograniczenia lub None, jeśli nie znaleziono rozwiązania
        """
        if self.is_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            # print(var, value)
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                del assignment[var]

        return None

    def backtrack(self):
        """
        Rozpoczyna proces przeszukiwania z nawrotami.
        :return: przypisanie spełniające ograniczenia lub None, jeśli nie znaleziono rozwiązania
        """
        return self.recursive_backtracking(self.assigment)
