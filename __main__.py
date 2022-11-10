import os
import sys
from subprocess import Popen, PIPE, STDOUT


def run(arg: str, c: int) -> tuple[Popen[str], ...]:
    return tuple(
        Popen([sys.executable, '-m', arg], stdout=PIPE, stderr=STDOUT, stdin=PIPE) for _ in range(c)
    )


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--presenter', type=int, default=0, choices=range(0, 32))
    parser.add_argument('--sum', type=int, default=0, choices=range(0, 32))
    parser.add_argument('--product', type=int, default=0, choices=range(0, 32))
    parser.add_argument('--grayscale', type=int, default=0, choices=range(0, 32))
    args = parser.parse_args()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    ps = (
        *run('presenter', args.presenter),
        *run('workers.sum', args.sum),
        *run('workers.product', args.product),
        *run('workers.grayscale', args.grayscale)
    )
    print('Running!')
    for p in ps:
        p.wait()
        print(f'[{" ".join(p.args)}] exited with code {p.returncode}')
    print('Exit.')


if __name__ == '__main__':
    main()
