import re
from itertools import product


class TruthTable:
    def __init__(self, expression):
        self.original_expression = expression
        self.expression = expression.replace(" ", "")
        self.variables = sorted(list(self._extract_variables()))
        self.validate_expression()
        self.parsed = self._parse_expression(self.expression)
        self.rows = []

    def _extract_variables(self):
        variables = set()
        i = 0
        n = len(self.expression)
        while i < n:
            char = self.expression[i]
            if char.isalpha():
                if (char == 'a' and i + 2 < n and self.expression[i + 1:i + 3] == "nd") or \
                        (char == 'o' and i + 1 < n and self.expression[i + 1] == "r") or \
                        (char == 'n' and i + 2 < n and self.expression[i + 1:i + 3] == "ot"):
                    i += 3 if char in ['a', 'n'] else 2
                    continue
                variables.add(char)
            i += 1
        return variables

    def validate_expression(self):
        if not self.expression:
            raise ValueError("Пустое выражение")

        if not re.fullmatch(r'[a-zA-Z&|!~()\->]+', self.expression):
            raise ValueError("Недопустимые символы в выражении")

        if len(self.variables) > 6:
            raise ValueError("Максимальное количество переменных - 6")

        stack = []
        for char in self.expression:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Несбалансированные скобки")
                stack.pop()

        if stack:
            raise ValueError("Несбалансированные скобки")

    def _parse_expression(self, expr):
        while expr.startswith('(') and expr.endswith(')'):
            if self._is_balanced(expr[1:-1]):
                expr = expr[1:-1]
            else:
                break

        if len(expr) == 1 and expr.isalpha():
            return expr

        if expr.startswith('!'):
            return ('!', self._parse_expression(expr[1:]))

        bracket_count = 0
        operator_pos = -1
        operator_char = None
        operator_priority = float('inf')

        i = 0
        while i < len(expr):
            char = expr[i]
            if char == '(':
                bracket_count += 1
                i += 1
            elif char == ')':
                bracket_count -= 1
                i += 1
            elif bracket_count == 0:
                if char == '-' and i + 1 < len(expr) and expr[i + 1] == '>':
                    priority = 1
                    if priority < operator_priority:
                        operator_priority = priority
                        operator_pos = i
                        operator_char = '->'
                    i += 2
                elif char == '~':
                    priority = 2
                    if priority < operator_priority:
                        operator_priority = priority
                        operator_pos = i
                        operator_char = '~'
                    i += 1
                elif char == '|':
                    priority = 3
                    if priority < operator_priority:
                        operator_priority = priority
                        operator_pos = i
                        operator_char = '|'
                    i += 1
                elif char == '&':
                    priority = 4
                    if priority < operator_priority:
                        operator_priority = priority
                        operator_pos = i
                        operator_char = '&'
                    i += 1
                else:
                    i += 1
            else:
                i += 1

        if operator_char:
            if operator_char == '->':
                left = expr[:operator_pos]
                right = expr[operator_pos + 2:]
            else:
                left = expr[:operator_pos]
                right = expr[operator_pos + 1:]

            if not left or not right:
                raise ValueError(f"Неверное выражение около оператора {operator_char}")

            return (operator_char, self._parse_expression(left), self._parse_expression(right))

        raise ValueError(f"Не удалось разобрать выражение: {expr}")

    def _is_balanced(self, expr):
        balance = 0
        for char in expr:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    return False
        return balance == 0

    def _evaluate(self, parsed, values):
        if isinstance(parsed, str):
            return values[parsed]
        elif parsed[0] == '!':
            return int(not self._evaluate(parsed[1], values))
        elif parsed[0] == '&':
            return self._evaluate(parsed[1], values) & self._evaluate(parsed[2], values)
        elif parsed[0] == '|':
            return self._evaluate(parsed[1], values) | self._evaluate(parsed[2], values)
        elif parsed[0] == '->':
            return (not self._evaluate(parsed[1], values)) | self._evaluate(parsed[2], values)
        elif parsed[0] == '~':
            return int(self._evaluate(parsed[1], values) == self._evaluate(parsed[2], values))
        raise ValueError(f"Неизвестный оператор: {parsed[0]}")

    def build_table(self):
        header = self.variables + [self.original_expression]
        print(" | ".join(f"{var:^5}" for var in header))
        print("-" * (6 * len(header) - 2))

        self.rows = []
        for combo in product([0, 1], repeat=len(self.variables)):
            values = dict(zip(self.variables, combo))
            try:
                result = self._evaluate(self.parsed, values)
                row = list(combo) + [result]
                self.rows.append(row)
                print(" | ".join(f"{val:^5}" for val in row))
            except Exception as e:
                print(f"Ошибка вычисления для {combo}: {e}")

    def build_sdnf_sknf(self):
        sdnf_terms = []
        sknf_terms = []
        sdnf_numeric = []  # Числовая форма СДНФ
        sknf_numeric = []  # Числовая форма СКНФ
        index_form = []  # Индексная форма функции

        for i, row in enumerate(self.rows):
            combo, result = row[:-1], row[-1]
            values = dict(zip(self.variables, combo))
            index_form.append(str(int(result)))

            if result == 1:
                # Для СДНФ
                term = []
                for var in self.variables:
                    term.append(f"{var if values[var] else '!' + var}")
                sdnf_terms.append("(" + "&".join(term) + ")")

                # Числовая форма СДНФ (номера наборов, где функция=1)
                sdnf_numeric.append(i)
            else:
                # Для СКНФ
                term = []
                for var in self.variables:
                    term.append(f"{var if not values[var] else '!' + var}")
                sknf_terms.append("(" + "|".join(term) + ")")

                # Числовая форма СКНФ (номера наборов, где функция=0)
                sknf_numeric.append(i)

        sdnf = " | ".join(sdnf_terms) if sdnf_terms else "0"
        sknf = " & ".join(sknf_terms) if sknf_terms else "1"

        print("\nСовершенная дизъюнктивная нормальная форма (СДНФ):")
        print(sdnf)
        print("Числовая форма СДНФ (номера наборов где функция=1):", sdnf_numeric)

        print("\nСовершенная конъюнктивная нормальная форма (СКНФ):")
        print(sknf)
        print("Числовая форма СКНФ (номера наборов где функция=0):", sknf_numeric)

        print("\nИндексная форма функции (битовая строка):", "".join(index_form))
        print("Индексная форма функции (десятичное число):", int("".join(index_form), 2))
