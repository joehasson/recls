A command line utility for recursively displaying the contents of a directory. Uses
the `rich` library's `Tree` class.

<img width="365" alt="Screenshot 2022-10-21 at 01 06 13" src="https://user-images.githubusercontent.com/104148871/197081775-618902b8-23ec-4248-bb2e-e4a5fc6aa809.png">

 The currently supported optional arguments are:

 - `-a --all` : display directories and files  which start with `.` if passed
 - `-d --depth` : The height of the tree displayed (default is 2)
 - `-q --quiet` : Display only directories, no files

Planned features:
 - Searching with regular expressions
