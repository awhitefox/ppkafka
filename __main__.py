import sys
from subprocess import Popen, PIPE, STDOUT


def run(arg: str, c: int) -> tuple[Popen[str], ...]:
    return tuple(
        Popen([sys.executable, '-m', arg], stdout=PIPE, stderr=STDOUT, stdin=PIPE) for _ in range(c)
    )


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--sum', type=int, default=0, choices=range(0, 32))
    parser.add_argument('--product', type=int, default=0, choices=range(0, 32))
    parser.add_argument('--grayscale', type=int, default=0, choices=range(0, 32))
    args = parser.parse_args()

    ps = (
        *run('frontend', 1),
        *run('backend.sum', args.sum),
        *run('backend.product', args.product),
        *run('backend.grayscale', args.grayscale),
    )
    print('Running!')
    for p in ps:
        p.wait()


if __name__ == '__main__':
    main()