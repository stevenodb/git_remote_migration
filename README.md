# git_remote_migration
Migrate multiple git repositories to a new remote

## Setup
1. Install python (and pip) 3.7+ on your operating system of choice
2. Run: `pip install gitpython texttable termcolor`
3. Download the script (or clone this repository)
3. [Optional] make it executable: `chmod a+x git_remote_migration.py`

## Usage
```
# path/to/git_remote_migration.py --help
usage: git_remote_migration.py [-h] -p PATTERN -r REPLACEMENT [directory]

positional arguments:
  directory             Directory to scan for repositories. Default is the current directory.

optional arguments:
  -h, --help            show this help message and exit
  -p PATTERN, --pattern PATTERN
                        Replacement pattern, with support for regular expressions.
  -r REPLACEMENT, --replace REPLACEMENT
                        Value to replace the matched pattern
```

## Example
```
# cd path/with/repositories
# path/to/git_remote_migration.py . --pattern git@bitbucket.org --replace git@github.com:
```

Follow instructions.