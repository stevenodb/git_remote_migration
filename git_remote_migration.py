#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import re
from git import Repo, InvalidGitRepositoryError, GitCommandError
from termcolor import colored
from texttable import Texttable
from argparse import ArgumentParser, Namespace
from os import DirEntry
from typing import AnyStr, List, Dict

WHITE = 'white'
RED = 'red'
YELLOW = 'yellow'
GREEN = 'green'
BLUE = 'blue'
COLOR_ATTRS = ['bold']

COL_TRUNC = 40


def is_git_repo(r: DirEntry) -> bool:
    dot_git_path = os.path.join(r.path, '.git')
    return os.path.isdir(dot_git_path)


def scan_repositories(directory: AnyStr) -> List[DirEntry]:
    with os.scandir(directory) as it:
        return [r for r in it if r.is_dir() and is_git_repo(r)]


def evaluate_arguments() -> Namespace:
    parser = ArgumentParser(description="Bulk migrate git remotes.")
    parser.add_argument("directory",
                        type=str,
                        nargs='?',
                        default=os.getcwd(),
                        help="directory to scan for repositories, default's to the current directory")
    required = parser.add_argument_group("mandatory arguments")
    required.add_argument('-p', '--pattern',
                          required=True,
                          dest='pattern',
                          metavar='REGEXP',
                          help="replacement pattern, supports regular expressions")
    required.add_argument('-r', '--replace',
                          required=True,
                          dest='replacement',
                          help="value to replace the matched pattern with")
    return parser.parse_args()


class GitRemoteTransform:
    def __init__(self, repo_path, replace_pattern, replace_value) -> None:
        super().__init__()
        self.repo = Repo(path=repo_path)
        self.pattern = re.compile(replace_pattern, re.IGNORECASE)
        self.replace_value = replace_value

    def get_new_remotes(self) -> Dict[str, str]:
        remotes = dict()
        try:
            for remote_url in self.repo.remote().urls:
                new_remote_url = self.pattern.sub(self.replace_value, remote_url)
                remotes[remote_url] = new_remote_url
        except InvalidGitRepositoryError:
            pass
        return remotes

    def add_as_row(self, table: Texttable) -> None:
        for (old, new) in self.get_new_remotes().items():
            key = truncate(os.path.basename(self.repo.working_dir), COL_TRUNC)
            value = new + " " + colored("(unchanged)", color=YELLOW, attrs=COLOR_ATTRS) \
                if old == new \
                else colored(new, color=GREEN, attrs=COLOR_ATTRS)
            table.add_row([key, value])

    def transform(self):
        for (old, new) in self.get_new_remotes().items():
            print(f"- \"{os.path.basename(self.repo.working_dir)}\"... ", end='')
            if old == new:
                print(colored("Skipped", color=YELLOW, attrs=COLOR_ATTRS))
            else:
                try:
                    self.repo.remote('origin').set_url(old_url=old, new_url=new)
                    print(colored("Done", color=GREEN, attrs=COLOR_ATTRS))
                except (ValueError, GitCommandError) as e:
                    print(colored(f"Failed ({e})", color=RED, attrs=COLOR_ATTRS))


def truncate(string: str, length: int) -> str:
    dots = ".."
    return string[:length - len(dots)] + dots if len(string) > length - len(dots) else string


def prepare_transformations(repo_dirs: List[DirEntry], pattern: str, replacement: str) -> List[GitRemoteTransform]:
    return [GitRemoteTransform(repo.path, pattern, replacement) for repo in repo_dirs]


def print_table(transformations: List[GitRemoteTransform]) -> None:
    tbl = Texttable()
    tbl.set_cols_width([COL_TRUNC, 120])
    tbl.header(['REPOSITORY', 'NEW REMOTE'])
    tbl.set_cols_align(['r', 'l'])
    tbl.set_header_align(['r', 'l'])
    tbl.set_deco(Texttable.HEADER | Texttable.VLINES)
    for t in transformations:
        t.add_as_row(tbl)
    print(tbl.draw())


def main():
    options = evaluate_arguments()

    print(
        r"""
 __  __ _                 _          ____ _ _     ____                      _
|  \/  (_) __ _ _ __ __ _| |_ ___   / ___(_) |_  |  _ \ ___ _ __ ___   ___ | |_ ___  ___
| |\/| | |/ _` | '__/ _` | __/ _ \ | |  _| | __| | |_) / _ \ '_ ` _ \ / _ \| __/ _ \/ __|
| |  | | | (_| | | | (_| | ||  __/ | |_| | | |_  |  _ <  __/ | | | | | (_) | ||  __/\__ \
|_|  |_|_|\__, |_|  \__,_|\__\___|  \____|_|\__| |_| \_\___|_| |_| |_|\___/ \__\___||___/
          |___/                                                       Migrate Git Remotes
---          
        """
    )

    print("The following git repositories have been found:\n")

    repos = scan_repositories(options.directory)
    transformations = prepare_transformations(repos, options.pattern, options.replacement)
    print_table(transformations)

    print("")
    if not input("Migrate repositories? (type 'yes' to continue)\n[yes/NO]: ").lower().strip() == "yes":
        print("Aborted.")
        sys.exit(1)

    for t in transformations:
        t.transform()

    print("Bye.")


if __name__ == '__main__':
    main()
