# If you are to contribute, then you are to READ THIS IN ITS ENTIRETY

## BEFORE STARTING

- Review over the project documentation, remember the required and recommended practices while you work, **IF YOU DON'T FOLLOW THE PRACTICE GUIDELINES, OR DON'T UNDERSTAND THE DOCUMENTATION, YOUR PULL REQUEST WILL NOT BE APPROVED**

## Workspace setup

- Clone the branch you desire to work off of, or create your own branch off an existing one. Where you clone this'll be your workspace.

- Run the command, where **path**'s the fully qualified path to the desired workspace folder: *python -m venv **path***

- With PyCharm the venv activation is done automatically, unless the setting "Tools/Terminal/Activate virtualenv" is disabled. Thus the manual steps can be skipped.

- Activate your venv, Unix(included Mac), execute the command: *source **path**/bin/activate*

- Activate your venv, Windows, execute the command: ***path**\Scripts\activate*

- Run the command: *pip install flask requests pytest*
- Run the command: *pip install --upgrade robotframework-seleniumlibrary*
- Run the command: *pip install selenium* and then *pip install unittest (or pytest)*

**For Selenium, make sure to download browser-specific webdriver:**

- For Chrome, the webdriver is called ChromeDriver. You can download it from the [ChromeDriver download page](https://sites.google.com/a/chromium.org/chromedriver/downloads). Make sure to download the version that corresponds to the version of Chrome installed on your machine.

- For Edge, the webdriver is called Microsoft Edge Driver. You can download it from the [Microsoft Edge Driver download page](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/). Again, make sure to download the version that corresponds to the version of Edge installed on your machine.

- For Firefox, the webdriver is called GeckoDriver. You can download it from the [GeckoDriver download page](https://github.com/mozilla/geckodriver/releases). As with the other drivers, make sure to download the version that corresponds to the version of Firefox installed on your machine.

After downloading the webdriver, you need to add it to your system's PATH. This process varies depending on your operating system:

- On Windows, you can add it to the PATH by going to Control Panel > System > Advanced system settings > Environment Variables, then under System variables select Path and click Edit. In the Edit Environment Variable window, click New and add the path to the directory where you saved the webdriver.

- On Unix-based systems like Linux or macOS, you can add it to the PATH by adding `export PATH=$PATH:/path/to/directory/containing/webdriver` to your shell profile file (like `~/.bashrc` or `~/.bash_profile`), then running `source ~/.bashrc` or `source ~/.bash_profile` to reload the profile. Replace `/path/to/directory/containing/webdriver` with the actual path to the directory where you saved the webdriver.

## Running tests

- To run pytests run the following command from your workspace environment: *python -m pytest src/test/*
- To run Robot Framework tests run the following command from your workspace environment: *python -m robot --pythonpath . src test/*
- To run Selenium tests, run the following command from your workspace environment:
    For unit tests: *python -m unittest test_file_name.py*
    For pytest: *python -m pytest test_file_name.py* or for verbose output: *python -v pytest test_file_name.py*
- To run all automated test at once on windows run the following command from your workspace environment: *src/test/test_all*

## Running app

- To run the server simply run the python file src/tms_server.py
- For some environments, you may need to begin with running the terminal command: *$env:PYTHONPATH = "${PWD}"*, then *cd src/server*, and finally *python tms_server.py* (ignore asterisk in command.)
