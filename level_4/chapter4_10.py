"""
Compare Python Implementations (e.g., CPythom Pypy) / Exploring Python Engines

Cpython
 - Default and most common implementatio
 - Written in C
 - Know for stability, ecosystem compptability, and wide support

Pypy
 - Uses Just-In-Time (JIT) compilation to speed up code execution
 - Can run many programs much faster than CPython
 - Not always 100% compatible with C extensión (like Numpy)

Jython
 - Written in Java, runs Python Code on the Java
 Virtual Machine (JVM)
 - Great for Java Interoperability
 - Limited support for Pythons 3 Features

IronPython
 - Designed to run Microsoft's .NET platform
 - Ideal for integrating with .NE libraries and tools
 - Like Jython, often lags behind the latest Python Features

 """

import platform
import sys

print("Python Implementatation : ", platform.python_implementation())
print("Python Version: ",sys.version)

"""
Step 2: Try Cooking in Pypy
Download from pypy.org or use brew install pypy3 on macOs.
Now, test performance with a benchmark script stored in timing_test.py

Step 3 : Jython

A . Install Java if not already installed
B . Download from jython.org
C . Launch with:

Step 4 : Cooking in IronPython
 - What is is: Python rebuilt for the .NET world.
 - Best fit: Works smoothly on Windows and within Microsoft's NET ecosystem
 - Strength:
    * Directly calls -net Libraries
    * Useful for enterprise system that mix Python with Microsoft Technologies
 - Limitations
    * Lag behind the latest Python 3 features
    * Less Ideal if youn want cutting -edge Python compatiblity

A .NET microwave - convenient in Microsoft kitchend, but not always up to date with the latest recipes


"""