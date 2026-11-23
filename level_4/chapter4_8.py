"""
Use Regex in Python to Match Pattern and Extract Text

Basic Syntax Topics
1 . Basic Regular Expression - normal characters and .
2 . Beginning and ending of the line - ^ and $
3 . Regex engine basics
4 . Regular engine basics
5 . Regular Expressión Rule # 1
6 . Exercice: Basic Syntax
7 . Exercise Solution and Q & A

1 . Basic Regexes
* Most characters (alpha-numeric) match themselves:
-grep a file.txt
 match "a" anywhere in the string (line of the file

- grep abx file.txt
match "a" followed by "b" followed by "c" anywhere in the string

- grep ab12 file.txt
match "a" followed by "b" followed by "1" followed by "2" anywhere
in the string

Exception

* Many characters have special meaning
- matches any character except \n:

- grep a.b file.txt
math "a" followed by any character but \n followed by "b", anywhere
in the string

- grep a.b.c file.txt
match "a" followed by any character but \n followed by "b"
followed by any character but \n followed by "c" anywhere in the string

Begin and End of String
* We can match the beginning or end of the string:
^ - Match the beginning of the string
$ - Match the end of the string (or right before)
newline at the end of the string)

ver
regexr.com

Python Matching
* match() only matches at the beginning of the string
* search() does not default to matching at the beginning
of the string
match ('hello')
is the same as:
search('^hello')
search() is recommended over match()


For complex regexes, compile() them and use the
compile object to call search()

* Can use options such as re.X and re.I

    * Combine with the vetical bar:
    re.X | re.I

    Python Groups
* Text Matched within groupng parens are available with the following
methods in the match object m:

- m.groups() - a list of all matched groups
- m.group(0) - the part of the string that matched the regex
- m.group(1) - the 1st group
- m.group(2) - the 2nd group
- etc


"""
