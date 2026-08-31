import os  # Intentional mistake 1: Unused import

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    # Intentional mistake 2: Returns sum instead of product
    result = a + b 
    return result