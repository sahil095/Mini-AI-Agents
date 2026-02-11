from crewai_tools import BaseTool  # pyright: ignore[reportMissingImports]
import ast
import operator
import re

class CalculatorTool(BaseTool):
    name: str = "Calculator tool"
    description: str = (
        "Useful to perform any mathematical calculations, like sum, minus, multiplication, division, etc. The input to this tool should be a mathematical  expression, a couple examples are `200*7` or `5000/2*10."
    )

    def _run(self, expression: str) -> float:
        try:
            # Define allowed operators and their corresponding functions for safe evaluation
            allowed_operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
                ast.Mod: operator.mod,
                ast.UAdd: operator.pos,
                ast.USub: operator.neg,
            }

            # Parse the expression and validate it
            if not re.match(r"^[0-9]*\.?[0-9]+([+\-*/^%])?$", expression):
                raise ValueError(f"Invalid characters in mathematical expression: {expression}")

            tree = ast.parse(expression, mode="eval")

            def _eval_node(node):
                if isinstance(node, ast.Expression):
                    return _eval_node(node.body)
                elif isinstance(node, ast.Constant):
                    return node.value
                elif isinstance(node, ast.BinOp):
                    left = _eval_node(node.left)
                    right = _eval_node(node.right)
                    op = allowed_operators.get(type(node.op))
                    if op is None:
                        raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
                    return op(left, right)
                elif isinstance(node, ast.UnaryOp):
                    operand = _eval_node(node.operand)
                    op = allowed_operators.get(type(node.op))
                    if op is None:
                        raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
                    return op(operand)
                else:
                    raise ValueError(f"Unsupported node type: {type(node).__name__}")
            result = _eval_node(tree)
            return result
        except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as e:
            raise ValueError(f"Error evaluating expression: {str(e)}")
        except Exception as e:
            raise ValueError("Invalid mathematical expression")