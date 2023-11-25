import time


class CSP:
    def __init__(self, problem, enable_mrv=True, enable_degree_heuristic=True, enable_forward_checking=True):
        self.problem = problem
        self.variables = problem.get_variables()
        self.domains = problem.get_domains()
        self.constraints = problem.get_constraints()
        self.assignment = {}
        self.enable_mrv = enable_mrv
        self.enable_degree_heuristic = enable_degree_heuristic
        self.enable_forward_checking = enable_forward_checking
        self.nodes_expanded = 0
        self.backtracks = 0
        self.start_time = None
        self.end_time = None

    def is_consistent(self, var, value):
        self.assignment[var] = value
        # print(self.assignment)
        for constraint in self.constraints:
            print(self.constraints)
            if var in constraint[0]:  # Sprawdź, czy zmienna jest częścią ograniczenia
                # Przygotuj argumenty dla funkcji ograniczenia
                args = [self.assignment[v] if v in self.assignment else None for v in constraint[0]]
                if None not in args and not constraint[1](*args):
                    del self.assignment[var]
                    return False

        del self.assignment[var]
        return True

    def select_unassigned_variable(self):
        if self.enable_mrv:
            unassigned_vars = [v for v in self.variables if v not in self.assignment]
            return min(unassigned_vars, key=lambda var: len(self.domains[var]))
        else:
            for var in self.variables:
                if var not in self.assignment:
                    return var

    def order_domain_values(self, var):
        if self.enable_degree_heuristic:
            return sorted(self.domains[var], key=lambda val: self.count_consistent_assignments(var, val))
        else:
            return self.domains[var]

    def count_consistent_assignments(self, var, val):
        self.assignment[var] = val
        count = sum(self.is_consistent(other_var, other_val)
                    for other_var in self.variables if other_var != var
                    for other_val in self.domains[other_var])
        del self.assignment[var]
        return count

    def backtrack(self):
        self.nodes_expanded += 1

        if len(self.assignment) == len(self.variables):
            return self.assignment

        var = self.select_unassigned_variable()

        for value in self.order_domain_values(var):
            if self.is_consistent(var, value):
                self.assignment[var] = value
                result = self.backtrack()
                if result is not None:
                    return result
                del self.assignment[var]
                self.backtracks += 1

        return None

    def solve(self):
        self.start_time = time.time()
        result = self.backtrack()
        self.end_time = time.time()
        return result

    def get_stats(self):
        return {
            "solution_time": self.end_time - self.start_time,
            "nodes_expanded": self.nodes_expanded,
            "backtracks": self.backtracks
        }
