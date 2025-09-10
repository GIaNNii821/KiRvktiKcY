# 代码生成时间: 2025-09-11 05:00:46
from bottle import route, run, request, response
import math

# Dictionary to map function names to actual math functions
math_functions = {
    "add": lambda x, y: x + y,
    "subtract": lambda x, y: x - y,
    "multiply": lambda x, y: x * y,
    "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero",
    "sqrt": lambda x: math.sqrt(x) if x >= 0 else "Error: Negative number for square root"
}


@route("/calculate", method="POST")
def calculate():
    # Retrieve the JSON request data
    try:
        data = request.json
    except Exception as e:
        response.status = 400
        return {"error": "Invalid JSON data"}

    # Check if necessary data is present
    if not all(k in data for k in ["function", "x", "y\]):
        response.status = 400
        return {"error": "Missing parameters"}

    # Execute the math function
    func_name = data["function"]
    x = data["x"]
    y = data.get("y")  # 'y' is optional for square root
    if func_name not in math_functions:
        response.status = 400
        return {"error": "Function not supported"}

    try:
        result = math_functions[func_name](x, y) if y is not None else math_functions[func_name](x)
    except Exception as e:
        response.status = 500
        return {"error": "Internal server error"}

    # Return the result
    return {"result": result}


if __name__ == "__main__":
    # Run the application on port 8080
    run(host="localhost", port=8080, debug=True)
