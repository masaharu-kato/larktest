"""

"""

CH_LF = ord('\n')
CH_BB = ord('(')
CH_BB = ord(')')

def parse_pdf(text:str):
    in_comment = False
    str_level = 0

    for ch in text:

        if in_comment:
            if ch == '\n':
                in_comment = False
            continue

        if ch == '(':
            str_level += 1
        elif ch == ')':
            if str_level:
                str_level -= 1
        if str_level:
            continue

        if ch == '%':
            in_comment = True

        
