# Python curriculum: the house

Checked on 2026-11-15 against the official pages:

- PCEP-30-03 (entry), Python Institute, revised 2026-11-02: https://pythoninstitute.org/pcep-exam-syllabus
- PCAP-31-04 (associate), Python Institute, revised 2026-11-02: https://pythoninstitute.org/pcap-exam-syllabus
- The Python Tutorial, chapters 1–16: https://docs.python.org/3/tutorial/index.html

Beginner + Intermediate cover PCEP. Advanced covers PCAP. Expert goes beyond both exams.

## Ground floor: Beginner (PCEP sections 1–2)

| # | Topic | House part |
|---|---|---|
| B1 | How code runs: interpreter vs compiler, lexical/syntax/semantic errors, keywords, statements vs expressions, indentation, comments, `print()` | Front door + doorbell |
| B2 | Values and variables: int/float/str/bool literals, naming rules and PEP 8, variables reference values | Foundation + labelled boxes |
| B3 | Numbers and operators: `** * / // % + -`, unary vs binary, precedence and associativity, augmented assignment, floating-point limits | Brick walls |
| B4 | Strings basics: quotes, `+` and `*` with strings, `len()`, escapes | Study bookshelf |
| B5 | Input and conversion: `input()` returns a string, `int()` `float()` `str()`, input → process → output | Mailbox |
| B6 | True/False and logic: relational operators, `not` `and` `or` | Light switches |
| B7 | Decisions: `if`, `if-else`, `if-elif-else`, nesting, unreachable branches | Hallway doors |
| B8 | Loops: `while`, sentinels, infinite loops, walrus `:=`, `for…in`, `range(start, stop, step)`, nested loops, `break` `continue` `pass` | Staircase |
| Boss | Mixed | Porch light |

## Second floor: Intermediate (PCEP sections 3–5, tutorial ch. 5–8)

| # | Topic | House part |
|---|---|---|
| I1 | Lists: build, index, slice, modify, search, sort, iterate, copy vs reference, 2D lists, stacks/queues, `del` | Wardrobe |
| I2 | Tuples and unpacking | Glass cabinet |
| I3 | Sets | Toy box |
| I4 | Dictionaries | Key rack |
| I5 | String tools: methods, search, slicing, f-strings and `format()`, immutability | Writing desk |
| I6 | Functions: `def`, `return`, parameters, default/keyword args, `*args`/`**kwargs`, scope, docstrings | Kitchen |
| I7 | Errors basics: common exceptions, `try`/`except` | Smoke alarm |
| I8 | Files: text files, `with`, CSV | Attic filing cabinet |
| I9 | Modules: `import`, `math`, `random` | Toolbox |
| Boss | Mixed | Balcony |

## Third floor and roof: Advanced (PCAP sections 1–6)

| # | Topic | House part |
|---|---|---|
| A1 | Own modules and packages: `from`/`as`, `import *` risks, `dir()`, `sys.path`, `__name__ == "__main__"`, `__pycache__`, `__init__.py`, pip, `requirements.txt`, virtual environments | Workshop + delivery van |
| A2 | Exceptions in depth: ordering, tuples, `as`, `else`/`finally`, hierarchy, raise/re-raise, propagation, custom exception families, chaining | Fire-safety system |
| A3 | Text and Unicode: ASCII, Unicode, UTF-8, `str` vs `bytes`, `ord`/`chr`, `is...()` checks, comparison and ordering | Translator / mail sorter |
| A4 | OOP foundations: classes, objects, instance vs class variables, methods, `__init__`, safe initialisation | Blueprints → furniture |
| A5 | Namespaces and introspection: name mangling, `__dict__`, `isinstance`/`hasattr`, class metadata | X-ray scanner |
| A6 | Inheritance and polymorphism: single, multiple, diamond and MRO, `super()`, type and identity checks | Family portrait wall |
| A7 | Comprehensions (incl. nested), `match-case`, loop `else` | Sorting conveyor |
| A8 | `lambda`, `map()`/`filter()`, closures | Kitchen robot helpers |
| A9 | Files pro: I/O modes, text vs binary, safe handling, `pathlib` | Basement with a map |
| A10 | Testing and debugging: unit tests, assertions, finding causes of defects | Home inspector |
| A11 | Team coding: Git, shared repositories, code review | Shared blueprint table |
| A12 | Coding with AI responsibly: generate, improve, validate AI-written code | Nibb's control room |
| Boss | Mixed | Smart roof |

## Rooftop and garden: Expert (beyond the exams; tutorial ch. 9–12)

| # | Topic | House part |
|---|---|---|
| E1 | Iterators and generators | Water tap |
| E2 | Decorators | String lights |
| E3 | Context managers | Self-closing door |
| E4 | Type hints, annotations, dataclasses | Label printer |
| E5 | Logging and performance (`timeit`) | Smart meter |
| E6 | Threads, multiprocessing, `async` | Smart hub |
| E7 | Internet and APIs, JSON | Rooftop antenna |
| E8 | Standard library tour: `os`, `glob`, `sys.argv`, `re`, `datetime`, `decimal`, `zlib` | Hardware store |

Each floor also has a garage mini-project: number-guessing game (Beginner), to-do list saved to a file (Intermediate), weather app using an API (Advanced).

## Interconnections (wires appear when both ends are built)

| Link | Python fact shown |
|---|---|
| Mailbox ↔ Bookshelf | `input()` always gives a string |
| Light switches ↔ Hallway doors | `if` checks a True/False value |
| Foundation ↔ Walls | operators work on values stored in variables (`total = price * 2`) |
| Staircase ↔ Wardrobe | loops walk through a list one item at a time |
| Kitchen ↔ Toolbox | modules are full of ready-made functions |
| Key rack ↔ Antenna | JSON from the internet arrives as dictionaries |
| Attic ↔ Smoke alarm | opening a file can fail, so use try/except |
| Blueprints ↔ Kitchen | methods are functions inside a class |
| Water tap ↔ Staircase | a for loop asks a generator for one item at a time |

## Coverage check

| Source | Section | Covered in |
|---|---|---|
| PCEP 1 | Fundamentals, literals, variables, operators, console I/O | B1–B6 |
| PCEP 2 | Conditionals and loops | B6–B8 |
| PCEP 3 | Lists, tuples, sets, dictionaries, strings | I1–I5 |
| PCEP 4 | Functions and exceptions | I6–I7 |
| PCEP 5 | Text/CSV files, imports, `math`, `random` | I8–I9 |
| PCAP 1 | Modules and packages | A1 |
| PCAP 2 | Exceptions | A2 |
| PCAP 3 | Strings | A3 |
| PCAP 4 | Object-oriented programming | A4–A6 |
| PCAP 5 | Advanced constructs and I/O | A7–A9 |
| PCAP 6 | Testing, debugging, collaboration, AI assistance | A10–A12 |
