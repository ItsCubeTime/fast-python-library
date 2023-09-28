# fast-python-library

Contains a broad set of helper functions and classes designed to complement or replace parts of Python STD. The main purpose of the library is to speed up software development by reducing the amount of code necessary to achieve various common problems faced when writing software.

Some of the more notable features currently present:
* An experimental, lightweight, filesystem based database that lets you store and read data from disk with syntax identical to setting class instance variables. Designed to make storing data on disk as simple as absolutely possible, handles pickling & depickling of data and stores basic python types in a readable format on disk, while compressing & decompressing larger data sets automatically. Theoretically the database should scale very well if the OS filesystem is good at handling large sets of files as all data lookups are direct filepath requests (it never has to iterate through data to find what its looking for nor use any kind of lookuptable - theoretically making the performance of the database (almost) solely limited by the speed of which the file system can operate).
* Running python & console commands in an elevated instance with ease (Windows only).
* Simplified socketing.
* A pathlib & os wrapper API for handling file manipulation (because I find pathlib's & os module's file system APIs somewhat unintuitive)
* Various other small & useful functions & classes :)


Planned:
* A fast webserver with built in tools to make JS frontend communication a brease.
* A lightweight UI library
* Tools for deploying Python apps with a webview based UI on popular platforms. Windows will get first hand priority, but I also have interest in supporting other desktop platforms as well as mobile.
## Thank you for checking out my repo!  💝
![image](https://media.tenor.com/KmUN-K6LjVkAAAAC/lion-king-simba.gif)
