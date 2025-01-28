"""
Q5.py - utilities to supply data to the templates.

This file contains a pair of functions for retrieving and manipulating data
that will be supplied to the template for generating the table.
"""
import csv


def username():
    return 'your GT username'

def data_wrangling(filter_class: str = None):
    """
    Args:
        - filter_class (str): Optional parameter that specifies the animal class
            to filter the data for.
    """
    with open('data/q5.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        table = list()
        
        # Read in the header
        for header in reader:
            break
        
        # Read in each row
        for row in reader:
            row_data = [row[0], row[1], int(row[2])]
            table.append(row_data)
        
        # [2 points] Q5.4.a - Get unique classes and sort alphabetically
        # Use a set to get unique values from the class column (index 1)
        # Convert to list and sort alphabetically
        dropdown_options = sorted(list(set(row[1] for row in table)))
        
        # [3 points] Q5.4.b
        # i. Filter by class if specified
        if filter_class:
            table = [row for row in table if row[1] == filter_class]
        
        # ii. Sort by count (index 2) in descending order
        table = sorted(table, key=lambda x: x[2], reverse=True)
        
        # iii. Limit to top 10 rows
        table = table[:10]
    
    return header, table, dropdown_options