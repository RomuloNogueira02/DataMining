def remove_blank_space(string):
    return string.replace(" ", "")

def diff_percent(value1, value2):
    return abs(round((1 - (value1 / value2)) * 100, 1))
