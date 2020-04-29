# vim:ts=4:sts=4:sw=4:expandtab


from kolejka.judge import config
from kolejka.judge.args import *
from kolejka.judge.checking import *
from kolejka.judge.limits import *
from kolejka.judge.parse import *
from kolejka.judge.paths import *
from kolejka.judge.result import *

from kolejka.judge.commands import *
from kolejka.judge.tasks import *

from kolejka.judge.judge import judge_parser

def main():
    import argparse
    import logging
    import setproctitle

    setproctitle.setproctitle('kolejka-client')
    parser = argparse.ArgumentParser(description='KOLEJKA judge')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='show more info')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='show debug info')
    judge_parser(parser)
    args = parser.parse_args()
    level=logging.WARNING
    if args.verbose:
        level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(level = level)
    args.execute(args)

if __name__ == '__main__':
    main()
