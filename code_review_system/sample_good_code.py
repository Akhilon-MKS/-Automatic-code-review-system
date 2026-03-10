"""
Sample good Python code for demonstration.
This file demonstrates best practices in naming, structure, and documentation.
"""

def calculate_sum(numbers):
    """
    Calculate the sum of a list of numbers.

    Args:
        numbers (list): List of numeric values.

    Returns:
        float: The sum of the numbers.
    """
    total = 0.0
    for number in numbers:
        total += number
    return total

class Calculator:
    """A simple calculator class."""

    def __init__(self):
        """Initialize the calculator."""
        self.result = 0.0

    def add(self, value):
        """
        Add a value to the current result.

        Args:
            value (float): Value to add.
        """
        self.result += value

    def get_result(self):
        """
        Get the current result.

        Returns:
            float: The current result.
        """
        return self.result
