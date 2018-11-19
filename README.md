author: Shubham Gupta
email: shubham180695[DOT]sg[AT]gmail[AT]com

A project which prints the graph of branches of Computer Science
The source of information is: https://en.wikipedia.org/wiki/Outline_of_computer_science
Requirements:
    - dot tool
    - yaml module for python
Steps to run:
    - python main.py
    - dot -T<extension> branches_of_CSE.dot -o branches_of_CSE.<extension>
      Here extension is any extension supported by dot, including pdf, png etc.