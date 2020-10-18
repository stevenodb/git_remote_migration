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
usage: git_remote_migration.py [-h] -p REGEXP -r REPLACEMENT [directory]

Bulk migrate git remotes.

positional arguments:
  directory             directory to scan for repositories, default's to the current directory

optional arguments:
  -h, --help            show this help message and exit

mandatory arguments:
  -p REGEXP, --pattern REGEXP
                        replacement pattern, supports regular expressions
  -r REPLACEMENT, --replace REPLACEMENT
                        value to replace the matched pattern with
```

## Example
```
# cd path/with/repositories
# path/to/git_remote_migration.py . --pattern git@bitbucket.org --replace git@github.com:
```

Follow instructions.