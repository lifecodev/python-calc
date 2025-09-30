# Простое консольное приложение с защитой на ввод (защита от инъекций кода в строку)
import ast
import math

class MathExpressionValidator(ast.NodeVisitor):

    def __init__(self):

        self.is_safe = True

        self.safe_operations = {
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
            ast.UAdd, ast.USub,
            ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        }

        self.safe_functions = {
            'abs', 'round', 'max', 'min', 'pow', 'sum',
            # Математические функции
            'sqrt', 'sin', 'cos', 'tan', 'log', 'log10', 'exp',
            'ceil', 'floor', 'factorial'
        }

        self.safe_constants = {
            'pi', 'e', 'inf', 'nan'
        }

    def visit_Call(self, node):
        """Проверка вызова функций"""
        if isinstance(node.func, ast.Name):
            if node.func.id not in self.safe_functions:
                self.is_safe = False
                return
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr not in self.safe_functions:
                self.is_safe = False
                return
        self.generic_visit(node)

    def visit_BinOp(self, node):
        """Проверка операций"""
        if type(node.op) not in self.safe_operations:
            self.is_safe = False
            return
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        if type(node.op) not in self.safe_operations:
            self.is_safe = False
            return
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == 'math':
            if node.attr not in self.safe_constants and node.attr not in self.safe_functions:
                self.is_safe = False
        else:
            self.is_safe = False

def expression_validate(expression):
    try:
        tree = ast.parse(expression, mode='eval')
        validator = MathExpressionValidator()
        validator.visit(tree)
        return validator.is_safe
    except SyntaxError:
        return False

def safe_execute(expression, variables=None):
    """
    Безопасное выполнение выражения
    """
    if not expression_validate(expression):
        raise ValueError('Выражение не безопасно!')

    safe_globals = {
        'abs': abs, 'round': round, 'max': max, 'min': min, 'pow': pow, 'sum': sum,
        'math': math, '__builtins__': {}
    }

    local_vars = variables or {}

    try:
        code = compile(expression, '<string>', 'eval')
        result = eval(code, safe_globals, local_vars)
        return result
    except Exception as e:
        raise ValueError(f"Ошибка выполнения выражения: {e}")

def main():
    while True:
        try:
            expression = input("Enter expression: ")
            result = safe_execute(expression)
            print(f"Результат: {result}")
        except ValueError as e:
            print(f"Ошибка: {e}")


# конструктор: запуск скрипта напрямую
if __name__ == '__main__':
    main()