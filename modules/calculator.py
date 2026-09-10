import ast
import math
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv
}


FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,
    "ln": math.log,
    "abs": abs
}


def calculate(expression):
    try:
        expression = expression.replace("^", "**")
        tree = ast.parse(expression, mode="eval")

        result = evaluate(tree.body)

        if isinstance(result, float):
            result = round(result, 6)

        return result

    except Exception:
        return None


def evaluate(node):

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

    if isinstance(node, ast.UnaryOp):
        value = evaluate(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        if isinstance(node.op, ast.UAdd):
            return value

    if isinstance(node, ast.BinOp):
        left = evaluate(node.left)
        right = evaluate(node.right)

        operation = OPERATORS.get(type(node.op))

        if operation:
            return operation(left, right)

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function")

        function_name = node.func.id

        if function_name not in FUNCTIONS:
            raise ValueError("Function not allowed")

        arguments = [
            evaluate(argument)
            for argument in node.args
        ]

        return FUNCTIONS[function_name](*arguments)

    raise ValueError("Unsupported expression")