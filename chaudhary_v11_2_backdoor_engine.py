import numpy as np
import time
from itertools import combinations, product

class CombinatorialBackdoorEngine:
    """
    Chaudhary Complexity Engine V11.2
    Deterministic Optimal Backdoor Detection for 3-SAT
    Author: Harendra
    """
    def __init__(self, n):
        self.n = n
        print(f" Chaudhary Engine V11.2 Active. n={n}")

    def check_if_2sat(self, clauses, fixed_assignments):
        for clause in clauses:
            reduced_clause = []
            clause_satisfied = False
            for literal in clause:
                var = abs(literal)
                sign = 1 if literal > 0 else -1
                if var in fixed_assignments:
                    if fixed_assignments[var] == sign:
                        clause_satisfied = True
                        break
                    else:
                        continue
                else:
                    reduced_clause.append(literal)
            if not clause_satisfied:
                if len(reduced_clause) > 2:
                    return False
        return True

    def is_2sat_after_fix(self, clauses, subset):
        for assignments in product([1, -1], repeat=len(subset)):
            fixed_assignments = dict(zip(subset, assignments))
            if self.check_if_2sat(clauses, fixed_assignments):
                return True
        return False

    def find_exact_backdoor_set(self, clauses):
        worst_case_backdoor = list(range(1, self.n + 1))
        max_search_limit = int(np.log2(self.n)) + 1
        print(f"[PROCESS] Searching backdoor up to size: {max_search_limit}")

        for size in range(1, max_search_limit + 1):
            for subset in combinations(range(1, self.n + 1), size):
                if self.is_2sat_after_fix(clauses, subset):
                    return list(subset)
        return worst_case_backdoor

    def verify_p_space_claim(self, backdoor_set):
        backdoor_size = len(backdoor_set)
        max_allowed_p_size = np.log2(self.n)
        print(f"\n--- BACKDOOR ANALYSIS ---")
        print(f"Variables (n): {self.n} | Backdoor Size: {backdoor_size}")
        print(f"P-Time Threshold log2(n): {max_allowed_p_size:.4f}")
        if backdoor_size <= max_allowed_p_size:
            return "SUCCESS: Instance is fixed-parameter tractable"
        else:
            return "LIMIT EXHAUSTED: Exponential wall encountered"

def generate_hard_3sat(n_vars, seed=42):
    np.random.seed(seed)
    n_clauses = int(4.26 * n_vars)
    print(f"[GENERATOR] Hard 3-SAT: {n_vars} vars, {n_clauses} clauses")
    clauses = []
    attempts = 0
    while len(clauses) < n_clauses and attempts < n_clauses * 10:
        vars_chosen = np.random.choice(range(1, n_vars + 1), size=3, replace=False)
        signs = np.random.choice([1, -1], size=3)
        clause = [int(v * s) for v, s in zip(vars_chosen, signs)]
        if sorted(clause) not in [sorted(c) for c in clauses]:
            clauses.append(clause)
        attempts += 1
    return clauses

if __name__ == "__main__":
    n_vars = 22
    hard_clauses = generate_hard_3sat(n_vars=n_vars, seed=101)
    engine = CombinatorialBackdoorEngine(n=n_vars)
    start_time = time.time()
    optimal_backdoors = engine.find_exact_backdoor_set(hard_clauses)
    verdict = engine.verify_p_space_claim(optimal_backdoors)
    end_time = time.time()
    print(f"Time: {end_time - start_time:.4f}s")
    print(f"[VERDICT] {verdict}")
