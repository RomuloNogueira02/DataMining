def remove_blank_space(string):
    return string.replace(" ", "")

def diff_percent(value1, value2):
    return round(abs((value1 - value2) / value1) * 100)