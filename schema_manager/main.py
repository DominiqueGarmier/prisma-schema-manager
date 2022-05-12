from __future__ import annotations

from argparse import ArgumentParser
from argparse import Namespace
from typing import Callable
from typing import cast

from config import Config
from config import get_config

from schema_manager.commands.codegen import codegen
from schema_manager.commands.init_project import init
from schema_manager.commands.switch import switch
from schema_manager.exceptions import ConfigNotFound
from schema_manager.exceptions import InvalidConfig


def main() -> int:

    parser = ArgumentParser('prisma schema manager')
    subparsers = parser.add_subparsers(title='commands')
    init_parser = subparsers.add_parser(
        'init',
        help='initialize a new project',
    )
    init_parser.add_argument('root', help='root directory', type=str, default='.')
    init_parser.set_defaults(func=init)

    condgen_parser = subparsers.add_parser('codegen', help='generate prisma client')
    condgen_parser.add_argument('client', help='client to generate', type=str)
    condgen_parser.set_defaults(func=codegen)

    switch_parser = subparsers.add_parser('switch', help='switch client')
    switch_parser.add_argument('client', help='client to generate', type=str)
    switch_parser.set_defaults(func=switch)

    parser.add_argument(
        '--debug', help='enable debug mode', action='store_true', dest='debug'
    )

    parser.add_argument(
        '--config',
        dest='config_path',
        type=str,
        help='path to config file',
        required=False,
    )

    args = parser.parse_args()
    args.func = cast(Callable[..., int], args.func)

    try:
        config = get_config(args, args.config_path)
    except InvalidConfig:
        print('invalid config')
    except ConfigNotFound:
        if args.func is init:
            return cast(Callable[[Namespace], int], args.func)(args)
        print('config not found')

    return cast(Callable[[Config, Namespace], int], args.func)(config, args)


if __name__ == '__main__':
    raise SystemExit(main())
