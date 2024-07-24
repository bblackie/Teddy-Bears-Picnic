
Open Terminal for the following
-------------------------------

To allow scripts to run:
=========================
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

To install a virtual environment called "dev"
REM: Remember that a virtual environment creates a small project-specific set of code libraries, which makes them easier to delete and avoids versioning hell,
encountered when running multiple projects on one machine.
=========================================================
python -m venv dev

To activate virtual environment:
================================
dev\scripts\activate

To install Flask, if not already installed
==========================================
pip install flask

To run:
=======
python app.py




