# 代码生成时间: 2025-09-19 02:59:24
# math_calculator_app.py
# Bottle web application to perform mathematical calculations

from bottle import route, run, request, response

# Define a namespace for our math operations
MATH_OPERATIONS = {
    'add': lambda x, y: x + y,
    'subtract': lambda x, y: x - y,
    'multiply': lambda x, y: x * y,
    'divide': lambda x, y: x / y if y != 0 else 'Error: Division by zero',
    'power': lambda x, y: x ** y
}

# Define route for the math calculator
@route('/calculate/<operation>/<x:re:-?\d+\.?\d*>/<y:re:-?\d+\.?\d*>')
def calculate(operation, x, y):
    # Attempt to parse the inputs as floats
    try:
        x = float(x)
        y = float(y)
    except ValueError:
        return response.json({'error': 'Invalid input'}, status=400)

    # Execute the mathematical operation
    result = None
    if operation in MATH_OPERATIONS:
        result = MATH_OPERATIONS[operation](x, y)
    else:
        return response.json({'error': 'Invalid operation'}, status=400)

    # Return the result as JSON
    return response.json({'result': result})

# Run the Bottle application on port 8080
run(host='localhost', port=8080)
