"""

"""
import sys
from pprint import pprint

from lark import Lark

import environment
import visitor

def main():
    with open("res/pdf_grammer.lark") as fr:
        parser = Lark(fr.read(), start='program', use_bytes=True)

    with open(sys.argv[1], mode='rb') as fr:
        tree = parser.parse(fr.read())

    # print(tree)

    global_env = environment.Environment(None)

    _visitor = visitor.Visitor()
    result = _visitor.visit(tree, global_env)

    pprint(result)


if __name__ == '__main__':
    main()
