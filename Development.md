# Developer Guide

## Install development tools

Install the `flake8` linter:
```bash
python -m pip install flake8
```

## Static code analysis

```bash
flake8 simulation-system/python/
```

## Lines of code

The project consists of aorund 120k lines of Python, 30k lines of JavaScript, 2.5k lines of Dockerfiles, 
1.4k lines of Makefile, and 1.6k lines of bash. 
The lines of code can be counted by executing the following commands from the project root:
``` bash
find . -name '*.py' | xargs wc -l
find . -name '*.js' | xargs wc -l
find . -name 'Dockerfile' | xargs wc -l
find . -name 'Makefile' | xargs wc -l
find . -name '*.sh' | xargs wc -l
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2020-2022, Kim Hammar