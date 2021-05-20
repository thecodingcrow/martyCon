# Marty the connector

Marty is a professional software tool originally developed for
JK-Regeltechnik to improve the performance of certain tasks

**Table of Contents**

- What is Marty here for
- How does Marty even work
- How to use Marty

### What is Marty here for

The goal of Marty is to filter a file for certain data points, process and connect them
and finally write the connection string into another file.

### How does Marty even work

Marty uses simple python string techniques to achieve glamorous results.

### How to use Marty

#### Prerequesites

You have to have **Python 3** installed, min version 3.6
https://www.python.org/downloads/

How to set up python on Windows \
https://www.pytorials.com/python-download-install-windows/

How to run python scripts under windows \
https://realpython.com/run-python-scripts/#how-to-run-python-scripts-using-the-command-line

#### General setup and usage

Navigate to the [dist](https://github.com/thecodingcrow/martyCon/tree/master/dist) folder and download the current version

The file structure should look like following:

- res
- out
- datapoint.py
- main.py
- utils.py

##### **Running the script**

- Change directory to martyCon_release_x
- The file you want to analyze has to be placed in res
- Open main.py in your favorite editor and change the dp_csv_filename variable to your actual filename
- start the main.py script via cmd \
  `python main.py` \
  or \
  `python3 main.py`

##### **Usage**

In the main window you have to load the file via the respective button \
The search will not work until the file is loaded

After that you can enter the desired abbreviations to look for the data points to be connected \

**Marty** will automatically adapt the resulting files name to include the desired data points abbreviations. This is done to get handier file names

Last thing to do is to click the write button. The file will then be placed inside the out folder

### Relase notes

20.04.2021 Initial Release

20.5.2021 Fixed some bugs and beautified logging, initated github repo
