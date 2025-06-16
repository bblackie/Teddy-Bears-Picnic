
# Website Setup

Open Terminal and run the following:


### If you get a script error, allow scripts to run:
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Create a virtual environment

### To install a virtual environment called "dev"

*REM: Remember that a virtual environment creates a small project-specific set of code libraries, which makes them easier to delete and avoids versioning hell,
encountered when running multiple projects on one machine.*

```
python -m venv .venv
```

### To activate virtual environment:

```
.venv\scripts\activate
```

## Install dependencies

### To install Flask, if not already installed

```
pip install flask
```

### To run:
```
python app.py
```



