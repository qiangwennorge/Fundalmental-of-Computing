"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    
    length = len(line)
    result = [0] * length 
    result_index = 0
    
    for line_index in range(length):
        if line[line_index] != 0:
            result[result_index] = line[line_index]
            result_index += 1
            
    for key in range(length - 1):
        if result[key] == result[key + 1]:
            result[key] += result[key + 1]
            result.pop(key + 1)
            result.append(0)
    
    return result