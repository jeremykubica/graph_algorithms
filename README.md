
# graph_algorithms

[![Template](https://img.shields.io/badge/Template-LINCC%20Frameworks%20Python%20Project%20Template-brightgreen)](https://lincc-ppt.readthedocs.io/en/latest/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/jeremykubica/graph_algorithms/smoke-test.yml)](https://github.com/jeremykubica/graph_algorithms/actions/workflows/smoke-test.yml)

Code from Graph Algorithms the Fun Way by Jeremy Kubica (No Starch Press 2024).

This code is provided for illustration purposes only. The code written to match the explanations in the book
and is NOT fully optimized and does not include all the validity checks that I would normally recommend
in production code. It is posted here so readers can explore the algorithms and teachers can use the code in their classes.

This project was automatically generated using the LINCC-Frameworks 
[python-project-template](https://github.com/lincc-frameworks/python-project-template). For more information about the project template see the 
[documentation](https://lincc-ppt.readthedocs.io/en/latest/).

## Dev Guide - Getting Started

Before installing any dependencies or writing code, it's a great idea to create a
virtual environment.

```
python3 -m venv ~/envs/graph_book
source ~/envs/graph_book/bin/activate
```

Next you need to clone this repository. I recommend the github desktop client, but you can
also use the command line tools.

```
git clone https://github.com/jeremykubica/graph_algorithms
cd graph_algorithms
```

Once you have created a new environment and downloaded the code, you can install this
project for local testing using the following commands:

```
>> pip install -e .
```

and you can run the unittests from the tests directory

```
>> cd tests/graph_algorithms_the_fun_way
>> python -m unittest
```