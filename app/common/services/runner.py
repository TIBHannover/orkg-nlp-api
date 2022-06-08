import subprocess


def run(args, shell=False):
    return subprocess.call(args, shell=shell)
