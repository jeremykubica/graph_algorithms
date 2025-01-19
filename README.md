
# graph_algorithms

[![Template](https://img.shields.io/badge/Template-LINCC%20Frameworks%20Python%20Project%20Template-brightgreen)](https://lincc-ppt.readthedocs.io/en/latest/)

[![PyPI](https://img.shields.io/pypi/v/graph_algorithms?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/graph_algorithms/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/jeremykubica/graph_algorithms/smoke-test.yml)](https://github.com/jeremykubica/graph_algorithms/actions/workflows/smoke-test.yml)
[![Codecov](https://codecov.io/gh/jeremykubica/graph_algorithms/branch/main/graph/badge.svg)](https://codecov.io/gh/jeremykubica/graph_algorithms)

Code from Graph Algorithms the Fun Way by Jeremy Kubica (No Starch Press 2024).

This code is provided for illustration purposes only. The code written to match the explanations in the book
and is NOT fully optimized and does not include all the validity checks that I would normally recommend
in production code.

This project was automatically generated using the LINCC-Frameworks 
[python-project-template](https://github.com/lincc-frameworks/python-project-template).

For more information about the project template see the 
[documentation](https://lincc-ppt.readthedocs.io/en/latest/).

## Dev Guide - Getting Started

Before installing any dependencies or writing code, it's a great idea to create a
virtual environment.

```
python3 -m venv ~/envs/graph_book
source ~/envs/graph_book/bin/activate
```

Once you have created a new environment, you can install this project for local
development using the following commands:

```
>> ./.setup_dev.sh
>> pip install -e .
```

Notes:
1. `./.setup_dev.sh` will initialize pre-commit for this local repository, so
   that a set of tests will be run prior to completing a local commit. For more
   information, see the Python Project Template documentation on 
   [pre-commit](https://lincc-ppt.readthedocs.io/en/latest/practices/precommit.html)
