def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    # Intentional bug 1: Unused variable
    temp_val = a + b 
    
    # Intentional bug 2: Divide by zero error
    return a / 0