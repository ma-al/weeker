Description
===========
Converts a tabbed CSV file into list of lists chunked by weeks.

Eventually, this will be installable via `python setup.py install` and
`pip install ...`

Code Quality
============
[![Build Status](https://travis-ci.org/ma-al/weeker.svg?branch=master)](https://travis-ci.org/ma-al/weeker)

This repo uses Travis for code quality checks.
- `pylint`
- `flake8`
- `py.test` and `coverage` checks coming soon

Use the included `local-cqa.sh` script to run the above checks locally on your
machine before code-pushes.

Setup
=====
First create an isolated environment, using either of:
- [virtualenv](https://virtualenv.pypa.io/en/stable/), or
- [miniconda](https://conda.io/miniconda.html).

I like `conda` as sometimes it has packages missing in PyPI (e.g., `OpenCV`).
Plus `pip` works just fine inside a `conda` environment.

Note that the instructions here work on Mac and Linux. If you're on Windows,
seek help.

```bash
# create a new environment with latest pip and go into it
conda create -n week pip
source activate week
cd $CONDA_PREFIX

# should be something like: /Users/<username>/miniconda2/envs/week/
pwd

# now clone this repo
git clone https://github.com/ma-al/weeker.git
```

If developing, you'll need to install packages that allow you to do the tests
above.
```bash
cd weeker
pip install -r reqs/dev.txt
```

Testing
=======
*Work In Progress*

Run the code with:
```bash
python weeker/Weeker.py
```
