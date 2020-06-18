import argparse

parser = argparse.ArgumentParser(description='Best simulator in town!')
parser.add_argument('-f', '--fake', action='store_true',
                    help='Print out the commands but does not run')

