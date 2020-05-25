
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

OR

* ```shell sudo python3 setup.py install```

Install the dependencies:

* ```pip install jira```
* ```pip install spacy```
* ```python -m spacy download en_core_web_sm```

Python standard dependencies:

[![Jira](https://img.shields.io/badge/Python%20Package-jira-blue)](https://pypi.org/project/jira/)

[![spacy](https://img.shields.io/badge/Python%20Package-spacy-blue)](https://pypi.org/project/spacy/)


devtracker
--------------

[![Github](https://img.shields.io/badge/Dev-Github-green)](https://github.com/jagadeesh-l/dev-work-tracker)

[![Pypi](https://img.shields.io/pypi/v/dev-work-tracker.svg)](https://pypi.python.org/pypi/dev-work-tracker)

[![Wheel](https://img.shields.io/pypi/wheel/wheel)](https://pypi.python.org/pypi/dev-work-tracker)

[![Python version](https://img.shields.io/badge/python-3.0%20%7C%203.1%20%7C%203.2%20%7C%203.3%20%7C%203.4%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue)](https://www.python.org/downloads/release/python-380/)

[![Licence](https://img.shields.io/apm/l/vim-mode)](https://pypi.python.org/pypi/dev-work-tracker)


This package is to track developers work rate

* Free software: MIT License
* Documentation: (COMING SOON!) https://dev-work-tracker.readthedocs.org.

Maintainers
------------

* Jagadeesh Lakshminarasimhan - jagadeeshlaks@gmail.com

## USAGE

```python

from devtracker.devtracker import Trigger

jira_server = "https://example.atlassian.net/"
jira_user = "example@gm.com"
jira_password = "examplePassW@rd"
Issue_ID = "EXAM-1234" #Jira Issue ID
description = 'This is sample description about the issue'

session = Trigger().jira_login(jira_server, jira_user, jira_password)
out = Trigger().windfall(Issue_ID, session, description)
print(out)
	
```








