# 代码生成时间: 2025-08-01 01:12:16
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Shopping Cart Application using Bottle framework.
This application allows users to add items to a shopping cart, view the cart,
and handle basic shopping cart functionality.
"""

from bottle import route, run, request, response, template

# Define a simple in-memory 'database' to store cart items
cart = {}

# Route to handle GET requests to the home page
@route('/')
def home():
    return template('home')  # Assuming a 'home.tpl' template exists

# Route to handle POST requests to add items to the cart
@route('/add_to_cart', method='POST')
def add_to_cart():
    """
    Adds an item to the shopping cart.
    Expects a JSON payload with item_id and quantity.
    """
    try:
        data = request.json
        item_id = data.get('item_id')
        quantity = data.get('quantity')
        
        if item_id is None or quantity is None:
            response.status = 400
            return {"error": "Missing item_id or quantity"}
        
        if item_id not in cart:
            cart[item_id] = 0
        
        cart[item_id] += quantity
        return {"message": "Item added to cart"}
    except ValueError:
        response.status = 400
        return {"error": "Invalid JSON payload"}

# Route to handle GET requests to view the cart
@route('/cart')
def view_cart():
    """
    Returns the current state of the shopping cart.
    """
    return cart

# Route to handle DELETE requests to remove items from the cart
@route('/cart/<item_id:int>', method='DELETE')
def remove_from_cart(item_id):
    """
    Removes an item from the shopping cart.
    """
    if item_id in cart:
        del cart[item_id]
        return {"message": "Item removed from cart"}
    else:
        response.status = 404
        return {"error": "Item not found in cart"}

# Route to handle GET requests to update the cart quantity
@route('/cart/<item_id:int>', method='PUT')
def update_cart(item_id):
    """
    Updates the quantity of an item in the shopping cart.
    """
    try:
        data = request.json
        quantity = data.get('quantity')
        if quantity is None:
            response.status = 400
            return {"error": "Missing quantity"}
        
        if item_id in cart:
            cart[item_id] = quantity
            return {"message": "Item quantity updated"}
        else:
            response.status = 404
            return {"error": "Item not found in cart"}
    except ValueError:
        response.status = 400
        return {"error": "Invalid JSON payload"}

# Start the Bottle server on port 8080
run(host='localhost', port=8080)