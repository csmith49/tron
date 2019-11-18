from argparse import ArgumentParser
from json import load, loads
from csv import DictWriter
from itertools import product

import subprocess

parser = ArgumentParser("T R O N")
parser.add_argument("grid")
args = parser.parse_args()

def exec(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for line in result.stdout.split("\n"):
        try:
            yield loads(line)
        except:
            pass

def get_cmds(grid):
    prod = [
        [grid["command"]]
    ]

    try: arguments = grid["arguments"]
    except: arguments = []

    for arg in arguments:
        if "flag" in arg.keys():
            flag = arg["flag"]
            prod.append(
                [f"--{flag}"]
            )

            # try and get the values
            if "values" in arg.keys():
                values = arg["values"]
                prod.append(
                    [str(v) for v in values]
                )
    
    return product(*prod)


if __name__ == "__main__":
    with open(args.grid, "r") as f:
        grid = load(f)
    
    for cmd in get_cmds(grid):
        for line in exec(cmd):
            print(line)