**author** : Shubham Gupta

**email** : shubham180695[DOT]sg[AT]gmail[AT]com

A project which prints a graph of branches of Computer Science
## Web resources used:
- The source of information is: https://en.wikipedia.org/wiki/Outline_of_computer_science
- Coloring scheme was taken from: http://heyrod.com/snippets/brewer-colors-paired12.html
- http://www.graphviz.org/documentation/ was helpful in understanding Graphviz

## Requirements:
- dot tool
- yaml module for python

## Steps to run:
```shell
python main.py
dot -T<extension> branches_of_CSE.dot -o branches_of_CSE.<extension>
```

Here extension is any extension supported by dot, including pdf, png etc.
