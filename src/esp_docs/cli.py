#!/usr/bin/env python3
#
# Copyright 2026 Espressif Systems (Shanghai) CO LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence


GUIDES = {
    'update-docs': 'update_docs.md',
}


def load_agent_guide(name: str) -> str:
    """Load an agent guide bundled with esp-docs."""
    guide_file = GUIDES.get(name)
    if guide_file is None:
        raise ValueError('Unknown agent guide: {}'.format(name))

    guide_path = Path(__file__).resolve().parent / 'agent_guides' / guide_file
    return guide_path.read_text(encoding='utf-8')


def _print_agent_guide(args: argparse.Namespace) -> int:
    try:
        guide = load_agent_guide(args.guide)
    except (OSError, ValueError) as error:
        print('esp-docs: {}'.format(error), file=sys.stderr)
        return 1

    sys.stdout.write(guide)
    if not guide.endswith('\n'):
        sys.stdout.write('\n')
    return 0


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='esp-docs',
        description='Utilities provided by the ESP-Docs package',
    )
    commands = parser.add_subparsers(dest='command', required=True)

    agent_guide_parser = commands.add_parser(
        'agent-guide',
        help='Print instructions for an AI coding agent',
    )
    agent_guides = agent_guide_parser.add_subparsers(dest='guide', required=True)
    update_docs_parser = agent_guides.add_parser(
        'update-docs',
        help='Print the ESP-IDF target documentation update guide',
    )
    update_docs_parser.set_defaults(handler=_print_agent_guide)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = create_parser().parse_args(argv)
    return args.handler(args)


if __name__ == '__main__':
    sys.exit(main())
