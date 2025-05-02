from itertools import product, combinations
import re

class TruthTable:
    def __init__(self, expression):
        self.original_expression = expression
        self.expression = self._normalize(expression)
        self.variables = sorted(list(self._extract_variables()))
        self.validate()
        self.parsed = self._parse(self.expression)
        self.rows = []
        self.sdnf_nums = []
        self.sknf_nums = []

    def _normalize(self, expr):
        return expr.replace(" ", "").replace("&&", "&").replace("||", "|")

    def _extract_variables(self):
        variables = set()
        i = 0
        while i < len(self.expression):
            c = self.expression[i]
            if c.isalpha():
                if (c == 'a' and i + 2 < len(self.expression) and self.expression[i + 1:i + 3] == "nd"):
                    i += 3
                elif (c == 'o' and i + 1 < len(self.expression) and self.expression[i + 1] == "r"):
                    i += 2
                elif (c == 'n' and i + 2 < len(self.expression) and self.expression[i + 1:i + 3] == "ot"):
                    i += 3
                else:
                    variables.add(c)
                    i += 1
            else:
                i += 1
        return variables

    def validate(self):
        if not self.expression:
            raise ValueError("Пустое выражение")
        if not re.fullmatch(r'[a-zA-Z&|!~()\->]+', self.expression):
            raise ValueError("Недопустимые символы в выражении")
        if len(self.variables) > 6:
            raise ValueError("Максимальное количество переменных - 6")
        balance = 0
        for c in self.expression:
            if c == '(':
                balance += 1
            elif c == ')':
                balance -= 1
                if balance < 0:
                    raise ValueError("Несбалансированные скобки")
        if balance != 0:
            raise ValueError("Несбалансированные скобки")

    def _parse(self, expr):
        while expr.startswith('(') and expr.endswith(')'):
            if self._is_balanced(expr[1:-1]):
                expr = expr[1:-1]
            else:
                break
        if len(expr) == 1 and expr.isalpha():
            return expr
        if expr.startswith('!'):
            return ('!', self._parse(expr[1:]))
        bracket_count = 0
        for i, c in enumerate(expr):
            if c == '(':
                bracket_count += 1
            elif c == ')':
                bracket_count -= 1
            elif bracket_count == 0:
                if c == '-' and i + 1 < len(expr) and expr[i + 1] == '>':
                    return ('->', self._parse(expr[:i]), self._parse(expr[i + 2:]))
                elif c == '~':
                    return ('~', self._parse(expr[:i]), self._parse(expr[i + 1:]))
                elif c == '|':
                    return ('|', self._parse(expr[:i]), self._parse(expr[i + 1:]))
                elif c == '&':
                    return ('&', self._parse(expr[:i]), self._parse(expr[i + 1:]))
        raise ValueError(f"Не удалось разобрать выражение: {expr}")

    def _is_balanced(self, expr):
        balance = 0
        for c in expr:
            if c == '(':
                balance += 1
            elif c == ')':
                balance -= 1
                if balance < 0:
                    return False
        return balance == 0

    def _evaluate(self, parsed, values):
        if isinstance(parsed, str):
            return values[parsed]
        elif parsed[0] == '!':
            return not self._evaluate(parsed[1], values)
        elif parsed[0] == '&':
            return self._evaluate(parsed[1], values) and self._evaluate(parsed[2], values)
        elif parsed[0] == '|':
            return self._evaluate(parsed[1], values) or self._evaluate(parsed[2], values)
        elif parsed[0] == '->':
            a = self._evaluate(parsed[1], values)
            b = self._evaluate(parsed[2], values)
            return (not a) or b
        elif parsed[0] == '~':
            a = self._evaluate(parsed[1], values)
            b = self._evaluate(parsed[2], values)
            return a == b
        raise ValueError(f"Неизвестный оператор: {parsed[0]}")

    def build_table(self):
        self.rows = []
        for values in product([False, True], repeat=len(self.variables)):
            value_dict = dict(zip(self.variables, values))
            result = self._evaluate(self.parsed, value_dict)
            row = list(values) + [result]
            self.rows.append(row)

    def build_sdnf_sknf(self):
        self.build_table()
        sdnf_terms = []
        sknf_terms = []
        self.sdnf_nums = []
        self.sknf_nums = []
        for i, row in enumerate(self.rows):
            values, result = row[:-1], row[-1]
            value_dict = dict(zip(self.variables, values))
            if result:
                term = []
                for var in self.variables:
                    term.append(f"{var if value_dict[var] else '!' + var}")
                sdnf_terms.append("(" + "&".join(term) + ")")
                self.sdnf_nums.append(i)
            else:
                term = []
                for var in self.variables:
                    term.append(f"{var if not value_dict[var] else '!' + var}")
                sknf_terms.append("(" + "|".join(term) + ")")
                self.sknf_nums.append(i)
        sdnf = " | ".join(sdnf_terms) if sdnf_terms else "0"
        sknf = " & ".join(sknf_terms) if sknf_terms else "1"
        print("\nСДНФ:", sdnf)
        print("Числовая форма СДНФ:", self.sdnf_nums)
        print("\nСКНФ:", sknf)
        print("Числовая форма СКНФ:", self.sknf_nums)
        return sdnf, sknf

    def _can_glue(self, a, b):
        diff = [i for i in range(len(a)) if a[i] != b[i]]
        return len(diff) == 1, diff[0] if len(diff) == 1 else None

    def _glue(self, a, b, pos):
        return a[:pos] + 'X' + a[pos + 1:]

    def _to_term(self, imp):
        term = []
        for i, c in enumerate(imp):
            if c == '0':
                term.append(f"!{self.variables[i]}")
            elif c == '1':
                term.append(self.variables[i])
        return " & ".join(term) if term else ""

    def _to_cnf_term(self, imp):
        term = []
        for i, c in enumerate(imp):
            if c == '0':
                term.append(f"{self.variables[i]}")
            elif c == '1':
                term.append(f"!{self.variables[i]}")
        return " | ".join(term) if term else ""

    def _get_initial_terms(self, term_nums, is_dnf=True):
        terms_bin = [format(i, f'0{len(self.variables)}b') for i in term_nums]
        if not terms_bin:
            return None, "0" if is_dnf else "1"
        print(f"Исходные {'минтермы' if is_dnf else 'макстермы'}:",
              f" {' | ' if is_dnf else ' & '}".join(self._to_term(m) if is_dnf else f"({self._to_cnf_term(m)})"
                                                    for m in terms_bin))
        return terms_bin, None

    def _glue_implicants(self, implicants, is_dnf=True):
        new_implicants = set()
        used = set()
        for a, b in combinations(implicants, 2):
            can, pos = self._can_glue(a, b)
            if can:
                new_imp = self._glue(a, b, pos)
                print(f"{'V' if is_dnf else '&'} "
                      f"{' | '.join([self._to_term(a), self._to_term(b)]) if is_dnf else f'({self._to_cnf_term(a)}) & ({self._to_cnf_term(b)})'} "
                      f"=> {' | '.join([self._to_term(new_imp)]) if is_dnf else f'({self._to_cnf_term(new_imp)})'}")
                new_implicants.add(new_imp)
                used.add(a)
                used.add(b)
        return new_implicants, used

    def _find_prime_implicants(self, terms_bin, is_dnf=True):
        implicants = set(terms_bin)
        prime_implicants = set()
        stage = 1
        while implicants:
            print(f"\nЭтап склеивания {stage}:")
            new_implicants, used = self._glue_implicants(implicants, is_dnf)
            prime_implicants.update(implicants - used)
            implicants = new_implicants
            if not new_implicants:
                prime_implicants.update(implicants)
                break
            stage += 1
        return prime_implicants

    def _build_coverage(self, prime_implicants, terms_bin):
        return {imp: [m for m in terms_bin if all(imp[i] == m[i] or imp[i] == 'X' for i in range(len(imp)))]
                for imp in prime_implicants}

    def _select_essential_implicants(self, coverage, terms_bin):
        essential = []
        covered = set()
        for m in terms_bin:
            covering = [imp for imp in coverage if m in coverage[imp]]
            if len(covering) == 1 and covering[0] not in essential:
                essential.append(covering[0])
                covered.update(coverage[covering[0]])
        return essential, covered

    def _cover_remaining_terms(self, coverage, essential, covered, terms_bin):
        remaining = set(terms_bin) - covered
        if remaining:
            non_essential = [imp for imp in coverage if imp not in essential]
            while remaining:
                candidates = [(imp, len([m for m in remaining if m in coverage[imp]])) for imp in non_essential]
                if not candidates:
                    break
                best_imp = max(candidates, key=lambda x: x[1])[0]
                essential.append(best_imp)
                covered.update(coverage[best_imp])
                remaining -= covered
        return essential

    def minimize_dnf_calculation(self):
        print("\nМинимизация СДНФ расчетным методом:")
        terms_bin, result = self._get_initial_terms(self.sdnf_nums, is_dnf=True)
        if result:
            print("СДНФ = 0, минимизация невозможна")
            return result
        prime_implicants = self._find_prime_implicants(terms_bin, is_dnf=True)
        coverage = self._build_coverage(prime_implicants, terms_bin)
        essential, covered = self._select_essential_implicants(coverage, terms_bin)
        essential = self._cover_remaining_terms(coverage, essential, covered, terms_bin)
        result = " | ".join(self._to_term(imp) for imp in essential) if essential else "0"

        return result

    def minimize_cnf_calculation(self):
        print("\nМинимизация СКНФ расчетным методом:")
        terms_bin, result = self._get_initial_terms(self.sknf_nums, is_dnf=False)
        if result:
            print("СКНФ = 1, минимизация невозможна")
            return result
        prime_implicants = self._find_prime_implicants(terms_bin, is_dnf=False)
        coverage = self._build_coverage(prime_implicants, terms_bin)
        essential, covered = self._select_essential_implicants(coverage, terms_bin)
        essential = self._cover_remaining_terms(coverage, essential, covered, terms_bin)
        result = " & ".join(f"({self._to_cnf_term(imp)})" for imp in essential) if essential else "1"

        return result

    def _print_coverage_table(self, coverage, terms_bin, is_dnf=True):
        print("\nТаблица покрытия:")
        header = [""] + [self._to_term(m) if is_dnf else f"({self._to_cnf_term(m)})" for m in terms_bin]
        print(" | ".join(f"{h:^15}" for h in header))
        for imp in coverage:
            row = [self._to_term(imp) if is_dnf else f"({self._to_cnf_term(imp)})"] + \
                  ["x" if m in coverage[imp] else " " for m in terms_bin]
            print(" | ".join(f"{c:^15}" for c in row))

    def minimize_dnf_table(self):
        print("\nМинимизация СДНФ расчетно-табличным методом:")
        terms_bin, result = self._get_initial_terms(self.sdnf_nums, is_dnf=True)
        if result:
            print("СДНФ = 0, минимизация невозможна")
            return result
        prime_implicants = self._find_prime_implicants(terms_bin, is_dnf=True)
        coverage = self._build_coverage(prime_implicants, terms_bin)
        self._print_coverage_table(coverage, terms_bin, is_dnf=True)
        essential, covered = self._select_essential_implicants(coverage, terms_bin)
        essential = self._cover_remaining_terms(coverage, essential, covered, terms_bin)
        result = " | ".join(self._to_term(imp) for imp in essential) if essential else "0"

        return result

    def minimize_cnf_table(self):
        print("\nМинимизация СКНФ расчетно-табличным методом:")
        terms_bin, result = self._get_initial_terms(self.sknf_nums, is_dnf=False)
        if result:
            print("СКНФ = 1, минимизация невозможна")
            return result
        prime_implicants = self._find_prime_implicants(terms_bin, is_dnf=False)
        coverage = self._build_coverage(prime_implicants, terms_bin)
        self._print_coverage_table(coverage, terms_bin, is_dnf=False)
        essential, covered = self._select_essential_implicants(coverage, terms_bin)
        essential = self._cover_remaining_terms(coverage, essential, covered, terms_bin)
        result = " & ".join(f"({self._to_cnf_term(imp)})" for imp in essential) if essential else "1"

        return result

    def _init_karnaugh_map(self, term_nums, value='1'):
        n = len(self.variables)
        if n > 5:
            print("Карта Карно поддерживает до 5 переменных")
            return None, None, None
        size = 2 ** n
        kmap = ['0' if value == '1' else '1'] * size
        for i in term_nums:
            kmap[i] = value
        return kmap, n, size

    def _get_karnaugh_order(self, n):
        if n == 3:
            return [0, 1, 3, 2, 4, 5, 7, 6], 2, 4
        elif n == 4:
            return [0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10], 4, 4
        elif n == 5:
            return [
                0, 1, 3, 2, 6, 7, 5, 4,
                8, 9, 11, 10, 14, 15, 13, 12,
                24, 25, 27, 26, 30, 31, 29, 28,
                16, 17, 19, 18, 22, 23, 21, 20
            ], 4, 8
        return [], 0, 0

    def _display_karnaugh_map(self, kmap, n, order, rows, cols, is_dnf=True):
        kmap_ordered = [kmap[i] for i in order]
        print("Карта Карно:")
        if n == 3:
            print(f"  {self.variables[1]}{self.variables[2]} | 00 01 11 10")
            for i in range(rows):
                row = kmap_ordered[i * cols:(i + 1) * cols]
                print(f"{self.variables[0]}={i} | {' '.join(row)}")
        elif n == 4:
            print(f"  {self.variables[2]}{self.variables[3]} | 00 01 11 10")
            for i in range(rows):
                row = kmap_ordered[i * cols:(i + 1) * cols]
                print(f"{self.variables[0]}{self.variables[1]}={format(i, '02b')} | {' '.join(row)}")
        elif n == 5:
            print(f"  {self.variables[2]}{self.variables[3]}{self.variables[4]} | 000 001 011 010 110 111 101 100")
            for i in range(rows):
                row = kmap_ordered[i * cols:(i + 1) * cols]
                print(f"{self.variables[0]}{self.variables[1]}={format(i, '02b')} | {' '.join(row)}")

    def _is_valid_karnaugh_group(self, r, c, height, width, value, kmap_copy, order, rows, cols):
        indices = []
        for i in range(height):
            for j in range(width):
                row = (r + i) % rows
                col = (c + j) % cols
                idx = order[row * cols + col]
                if kmap_copy[idx] != value:
                    return False, []
                indices.append(idx)
        return True, indices

    def _find_karnaugh_groups(self, kmap, n, order, term_nums, value='1'):
        kmap_copy = kmap[:]
        rows, cols = 2 ** (n // 2), 2 ** (n - n // 2)
        sizes = [8, 4, 2, 1]
        groups = []
        for size in sizes:
            if size > 2 ** n:
                continue
            for height in [1, 2, 4]:
                for width in [1, 2, 4, 8]:
                    if height * width != size or height > rows or width > cols:
                        continue
                    for r in range(rows):
                        for c in range(cols):
                            valid, indices = self._is_valid_karnaugh_group(r, c, height, width, value, kmap_copy, order, rows, cols)
                            if valid and indices:
                                groups.append(indices)
                                for idx in indices:
                                    kmap_copy[idx] = 'X'
        return groups

    def _convert_groups_to_terms(self, groups, n, is_dnf=True):
        terms = []
        for group in groups:
            binaries = [format(idx, f'0{n}b') for idx in group]
            term = []
            for i in range(n):
                values = set(binary[i] for binary in binaries)
                if len(values) == 1:
                    bit = values.pop()
                    if is_dnf:
                        term.append(self.variables[i] if bit == '1' else f"!{self.variables[i]}")
                    else:
                        term.append(self.variables[i] if bit == '0' else f"!{self.variables[i]}")
            terms.append(" & ".join(term) if is_dnf else f"({' | '.join(term)})" if term else "")
        return terms

    def _filter_essential_terms(self, terms, groups, term_nums, is_dnf=True):
        essential_terms = []
        covered = set()
        terms_set = set(term_nums)
        for term, group in sorted([(t, g) for t, g in zip(terms, groups)], key=lambda x: len(x[1]), reverse=True):
            group_set = set(group)
            if any(m in group_set for m in terms_set - covered):
                essential_terms.append(term)
                covered.update(group_set)
            if covered == terms_set:
                break
        return essential_terms

    def minimize_dnf_karnaugh(self):
        print("\nМинимизация СДНФ методом карты Карно:")
        kmap, n, size = self._init_karnaugh_map(self.sdnf_nums, value='1')
        if kmap is None:
            return None
        order, rows, cols = self._get_karnaugh_order(n)
        self._display_karnaugh_map(kmap, n, order, rows, cols, is_dnf=True)
        groups = self._find_karnaugh_groups(kmap, n, order, self.sdnf_nums, value='1')
        terms = self._convert_groups_to_terms(groups, n, is_dnf=True)
        essential_terms = self._filter_essential_terms(terms, groups, self.sdnf_nums, is_dnf=True)
        result = " | ".join(essential_terms) if essential_terms else "0"

        return result

    def minimize_cnf_karnaugh(self):
        print("\nМинимизация СКНФ методом карты Карно:")
        kmap, n, size = self._init_karnaugh_map(self.sknf_nums, value='0')
        if kmap is None:
            return None
        order, rows, cols = self._get_karnaugh_order(n)
        self._display_karnaugh_map(kmap, n, order, rows, cols, is_dnf=False)
        groups = self._find_karnaugh_groups(kmap, n, order, self.sknf_nums, value='0')
        terms = self._convert_groups_to_terms(groups, n, is_dnf=False)
        essential_terms = self._filter_essential_terms(terms, groups, self.sknf_nums, is_dnf=False)
        result = " & ".join(essential_terms) if essential_terms else "1"

        return result
