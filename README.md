
Improvising developer's effort
==============================
Dated: 10/02/2019


Overview
--------

* Create an issue under task(input) which contains history of developer's bug for current module.


Dependencies
------------

Install the package by running:

* ```pip install dev-work-tracker```
* ```shell sudo python3 setup.py install```

Python standard dependencies:

[![Jira](https://img.shields.io/badge/Python%20Package-jira-blue)](https://pypi.org/project/jira/)

[![spacy](https://img.shields.io/badge/Python%20Package-spacy-blue)](https://pypi.org/project/spacy/)


devtracker
--------------

[![Github](https://img.shields.io/badge/Dev-Github-green)](https://github.com/jagadeesh-l/dev-work-tracker)

[![Pypi](https://img.shields.io/pypi/v/dev-work-tracker.svg)](https://pypi.python.org/pypi/dev-work-tracker)

[![Wheel](https://img.shields.io/pypi/wheel/wheel)](https://pypi.python.org/pypi/dev-work-tracker)

[![Python version](https://img.shields.io/pypi/pyversions/jira-client)](https://www.python.org/downloads/release/python-370/)

[![Licence](https://img.shields.io/apm/l/vim-mode)](https://pypi.python.org/pypi/dev-work-tracker)


This package is to track developers work rate

* Free software: MIT license
* Documentation: (COMING SOON!) https://dev-work-tracker.readthedocs.org.

Maintainers
------------

* Jagadeesh Lakshminarasimhan - jagadeesh_lakshminarasimhan@comcast.com

## USAGE

```python

from devtracker.devtracker import Tracker

jira_server = "https://example.atlassian.net/"
jira_user = "example@gm.com"
jira_password = "examplePassW@rd"
Issue_ID = EXA-0001 #Jira Issue ID

session = Tracker().jira_login(jira_server, jira_user, jira_password)
Tracker().windfall(Issue_ID, session)
```







