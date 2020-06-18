import os
import sys
from .core.argparser import parser
from .core.application import Application

def report(args):
    print("Report".center(60, '-'))
    print(f" Module: {__name__}")
    print(f" Called from: {os.getcwd()}")
    print(f" {args}")
    print("".center(60, '-'))

def main():
    args = parser.parse_args()
    app = Application(args)
    app.run()
