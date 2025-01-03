import pygame
import random
from words import mylist
import math

                    
def wrap_text(text, font, rect):
    words = text.split(' ')
    lines = []
    current_line = ""
    max_width = rect.w
    for word in words:
        # Check the width of the current line with the new word added
        test_line = current_line + word + " "
        width, _ = font.size(test_line)
        
        # If the line width exceeds max_width, start a new line
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "  # Start a new line with the current word

    if current_line:
        lines.append(current_line.strip())  # Add any remaining text as a final line

    return lines
    
def find_seperator(text):
    seperators = [" ", ".", "!", "?", ","]
    for sep in seperators:
        if text.rfind(sep) != -1:
            line, rem_text = text.rsplit(sep, 1) 
            return line, rem_text
    line = text[:-1] #found no seperators
    rem_text = text[-1]
    return line, text
    
def get_word():
    word = random.choice(mylist)
    return word

def find_all(original_list, value):
    # Find all indices of a specific value (e.g., 2)
    indices = [index for index, element in enumerate(original_list) if element == value]
    return indices