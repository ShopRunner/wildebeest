.. _contrib:

Contributing
============

How to Contribute
-----------------

We welcome contributions in the form of issues or pull requests! 

We want this to be a place where all are welcome to discuss and contribute, so please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. Find the code of conduct :ref:`below <code>` or in the ``CONDUCT.md`` file on GitHub.

If you have a problem using creevey or see a possible impovement, open an issue in the GitHub issue tracker. Please be as specific as you can.

If you see an open issue you'd like to be fixed, take a stab at it and open a PR!

Steps for making a pull request:
################################
1. Fork the project from GitHub.

2. Clone the forked repo to your local disk.::

    git clone https://github.com/<your_github_user_name>/creevey.git

3. ``cd`` into the directory.

4. Create a new branch.:: 

    git checkout -b my_awesome_new_feature

5. Install the library. (We recommend using a virtual environment.)::

    pip install -e . 

6.Make your changes.

7. Update the ``unit tests``, ``_version.py``, and ``CHANGELOG``.

8. Run ``black creevey tests --skip-string-normalization`` to format code.

9. Check that unit tests pass and the linter doesn't complain.:: 

    pytest
    flake8 creevey tests

10.Submit your PR.

We prefer single quotes for strings unless using double quotes allows us to avoid escaping internal single quotes. We use numpy style for docstrings and run code using CPython 3.6+.

.. _code:

Contributor Covenant Code of Conduct
====================================

Our Pledge
----------

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

Our Standards
-----------------

**Examples of behavior that contributes to creating a positive environment include:**

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

**Examples of unacceptable behavior by participants include:**

* The use of sexualized language or imagery and unwelcome sexual attention or advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a professional setting

Our Responsibilities
--------------------

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.

Scope
------

This Code of Conduct applies both within project spaces and in public spaces when an individual is representing the project or its community. Examples of representing a project or community include using an official project e-mail address, posting via an official social media account, or acting as an appointed representative at an online or offline event. Representation of a project may be further defined and clarified by project maintainers.

Enforcement
-----------

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at gsganden@gmail.com. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident. Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good faith may face temporary or permanent repercussions as determined by other members of the project's leadership.

Attribution
-----------

This Code of Conduct is adapted from the Contributor Covenant, version 1.4, available at http://contributor-covenant.org/version/1/4.