import re
from itertools import product

class TruthTable:
    def __init__(self, expression):
        self.original_expression = expression
        self.expression = self._normalize(expression)
        self.variables = sorted(list(self._extract_variables()))
        self.validate()
        self.parsed = self._parse(self.expression)
        self.rows = []

    def _normalize(self, expr):
        return expr.replace(" ", "").replace("&&", "&").replace("||", "|")

    def _extract_variables(self):
        """Извлекает все уникальные переменные из выражения, игнорируя операторы"""
        variables = set()
        i = 0
        while i < len(self.expression):
            c = self.expression[i]
            if c.isalpha():
                # Проверяем, не является ли это частью операторов and/or/not
                if (c == 'a' and i + 2 < len(self.expression)
                        and self.expression[i + 1:i + 3] == "nd"):
                    i += 3
                elif (c == 'o' and i + 1 < len(self.expression)
                      and self.expression[i + 1] == "r"):
                    i += 2
                elif (c == 'n' and i + 2 < len(self.expression)
                      and self.expression[i + 1:i + 3] == "ot"):
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
                if c == '-' and i+1 < len(expr) and expr[i+1] == '>':
                    return ('->', self._parse(expr[:i]), self._parse(expr[i+2:]))
                elif c == '~':
                    return ('~', self._parse(expr[:i]), self._parse(expr[i+1:]))
                elif c == '|':
                    return ('|', self._parse(expr[:i]), self._parse(expr[i+1:]))
                elif c == '&':
                    return ('&', self._parse(expr[:i]), self._parse(expr[i+1:]))

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
            # Исправленная версия дизъюнкции
            left = self._evaluate(parsed[1], values)
            right = self._evaluate(parsed[2], values)
            return left or right
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
        header = self.variables + [self.original_expression]
        print(" | ".join(f"{var:^5}" for var in header))
        print("-" * (6 * len(header) - 2))

        self.rows = []
        for values in product([False, True], repeat=len(self.variables)):
            value_dict = dict(zip(self.variables, values))
            result = self._evaluate(self.parsed, value_dict)
            row = list(values) + [result]
            self.rows.append(row)
            print(" | ".join(f"{str(int(val)):^5}" for val in row))

    def build_sdnf_sknf(self):
        sdnf_terms = []
        sknf_terms = []
        sdnf_nums = []
        sknf_nums = []
        index_form = []

        for i, row in enumerate(self.rows):
            values, result = row[:-1], row[-1]
            value_dict = dict(zip(self.variables, values))
            index_form.append('1' if result else '0')

            if result:
                term = []
                for var in self.variables:
                    term.append(f"{var if value_dict[var] else '!'+var}")
                sdnf_terms.append("(" + "&".join(term) + ")")
                sdnf_nums.append(i)
            else:
                term = []
                for var in self.variables:
                    term.append(f"{var if not value_dict[var] else '!'+var}")
                sknf_terms.append("(" + "|".join(term) + ")")
                sknf_nums.append(i)

        sdnf = " | ".join(sdnf_terms) if sdnf_terms else "0"
        sknf = " & ".join(sknf_terms) if sknf_terms else "1"

        print("\nСовершенная дизъюнктивная нормальная форма (СДНФ):")
        print(sdnf)
        print("Числовая форма СДНФ:", sdnf_nums)

        print("\nСовершенная конъюнктивная нормальная форма (СКНФ):")
        print(sknf)
        print("Числовая форма СКНФ:", sknf_nums)

        print("\nИндексная форма:")
        print("Битовая строка:", "".join(index_form))
        print("Десятичное число:", int("".join(index_form), 2))
        #((((a & b)~c)->(!d)) | c)
