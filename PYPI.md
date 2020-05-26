
Improvising developer's effort
==============================
Dated: 10/02/2019


Overview
--------

When comes to SDLC, time is very efficient. This "Dev-work-tracker" is the efficient way to reduce time specially on testing phase. 

In many scenarios, same bug caught at different releases by the tester. Which means developers can make same mistakes gain and gain. The frequency of the developer tent to concentrate lesser on not interesting stuff.Example many developers excited about writing codes, but same excitement will be lacking when comes to writing unit test code. This leads to cause more bugs in the testing cycle.

In this case, "Dev-work-tracker" will help to track assignee's bug history and compare them (using natural language processing - NLP)  with his current task, then it will create a sub-task in this current task stating - "You have more than one bug history related to the current task, please make sure this won't render in current task".

Example:

Current Task - UI Development - positioning img.

If Assignee's Bug History - 10

		* Out of 10, 4 is related to UI Development
		* Out of 4, 2 is related to positioning.

So this 2 positioning bugs will send it to Assignee's eye, so that he can avoid this mistake again in his current work.


Dependencies
------------


Install the package by running:


pip install dev-work-tracker

OR

shell sudo python3 setup.py install


Install the dependencies:
------------------------------------


pip install jira
pip install spacy
python -m spacy download en_core_web_sm

Python standard dependencies:
------------------------------------

* .. image:: https://img.shields.io/badge/Python%20Package-jira-blue
		  :target: https://pypi.org/project/jira/

* .. image:: https://img.shields.io/badge/Python%20Package-spacy-blue
		  :target: https://pypi.org/project/spacy/

devtracker
--------------
.. image:: https://img.shields.io/badge/Dev-Github-green
        :target: https://github.com/jagadeesh-l/dev-work-tracker

.. image:: https://img.shields.io/pypi/v/dev-work-tracker.svg
        :target: https://pypi.python.org/pypi/dev-work-tracker

.. image:: https://img.shields.io/pypi/wheel/wheel
		:target: https://pypi.python.org/pypi/dev-work-tracker

.. image:: https://img.shields.io/badge/python-3.0%20%7C%203.1%20%7C%203.2%20%7C%203.3%20%7C%203.4%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue
		:target: https://www.python.org/downloads/release/python-380/
		
.. image:: https://img.shields.io/apm/l/vim-mode
		:target: https://pypi.python.org/pypi/dev-work-tracker

This package is to track developers work rate

* Free software: MIT license
* Documentation: (COMING SOON!) https://dev-work-tracker.readthedocs.org.

Maintainers
-----------

* Jagadeesh Lakshminarasimhan - jagadeeshlaks@gmail.com


USAGE
------


from devtracker.devtracker import Trigger

jira_server = "https://example.atlassian.net/"

jira_user = "example@gm.com"

jira_password = "examplePassW@rd"

Issue_ID = "EXAM-1234" #Jira Issue ID

description = 'This is sample description about the issue'

session = Trigger().jira_login(jira_server, jira_user, jira_password)

out = Trigger().windfall(Issue_ID, session, description)

print(out)

	


.. image:: https://img.shields.io/badge/LINK-GitHub-orange
		:target: https://github.com/jagadeesh-l/dev-work-tracker




