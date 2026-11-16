KEY, IDX = 'typing', 39
META = dict(tag='Type hints · Rooftop garden', title='Type hints and dataclasses: label everything', topic='type hints and dataclasses',
            lastBtn='Label the beds', doneTitle='Every bed is labelled!',
            doneText='You learned type hints for variables and functions, list and dict hints, str | None, that Python does not enforce hints, @dataclass and what it gives you, frozen and field. Raised beds with printed labels now sit on the garage roof. The label printer is in your garden: print a plant.')
QUIZ = [
 ('What does this show?', 'count: int = "lots"\nprint(count)', ['lots', 'An error', '0', 'int'], 0,
  ['Python does not enforce hints: count just holds "lots".', 'Hints never stop the code running.', 'The hint does not change the value.', 'The hint is not printed.'], 4),
 ('What does -> bool tell you?', 'def water(bed: str) -> bool:', ['It gives back True or False', 'It needs a bool to run', 'bed must be True or False', 'It prints a bool'], 0,
  ['The arrow says what the function returns.', 'bed is the input, and it is a str.', 'bed: str says bed is text.', 'Hints are not about printing.'], 1),
 ('Which hint means "a list of names"?', 'beds = ["peas", "kale"]', ['list[str]', 'str[list]', 'list(str)', 'dict[str]'], 0,
  ['list[str] is a list whose items are strings.', 'It is list of str, not the other way.', 'Hints use square brackets.', 'A dict needs a key and a value type.'], 2),
 ('What does str | None mean?', 'def find(name: str) -> str | None:', ['It gives a str, or None', 'It gives a str and None', 'It cannot give None', 'name can be None'], 0,
  ['The | means "or": maybe no answer.', 'Only one value comes back.', 'None is allowed.', 'This is about what comes back, not name.'], 3),
 ('What does this show?', 'from dataclasses import dataclass\n@dataclass\nclass Plant:\n    name: str\n    height: int = 0\nprint(Plant("tomato", 3))', ["Plant(name='tomato', height=3)", '<Plant object>', 'tomato 3', 'An error'], 0,
  ['A dataclass writes a readable print for you.', 'That is a plain class without __repr__.', 'It shows the field names too.', '@dataclass writes __init__ for you.'], 6),
 ('What does this show?', 'from dataclasses import dataclass\n@dataclass\nclass Plant:\n    name: str\nprint(Plant("pea") == Plant("pea"))', ['True', 'False', 'An error', 'pea'], 0,
  ['A dataclass compares by its fields.', 'Plain objects would be False; a dataclass checks the values.', '== works fine.', '== gives True or False.'], 6),
 ('What happens?', 'from dataclasses import dataclass\n@dataclass(frozen=True)\nclass Label:\n    text: str\nlb = Label("kale")\nlb.text = "leek"', ['An error: it is frozen', 'lb.text becomes "leek"', 'A copy is made', 'Nothing'], 0,
  ['frozen=True means it cannot be changed.', 'Frozen objects cannot be changed.', 'No copy is made: it fails.', 'Python raises FrozenInstanceError.'], 7),
]
CARDS = [
 ('th1', 'mach', 39, 'What does `def water(bed: str) -> bool:` say?', 'bed should be a str, and the function gives back a bool.'),
 ('th2', 'mach', 39, 'Does Python stop you breaking a type hint?', 'No. Hints are for people and tools like mypy.'),
 ('th3', 'mach', 39, 'What does `@dataclass` give you for free?', '`__init__`, a readable print (`__repr__`) and `==` that compares fields.'),
 ('th4', 'mach', 39, 'How do you give a dataclass field a list default?', '`tags: list = field(default_factory=list)`'),
]
GEN_STEPS = [6, 6, 4]
GEN_JS = r'''
      function () { var d = ri(0, 5), h = ri(6, 12), given = pickOne([true, false]), name = pickOne(['tomato', 'kale', 'pea']);
        return mk('What does this show?', 'from dataclasses import dataclass\n@dataclass\nclass Plant:\n    name: str\n    height: int = ' + d + '\np = Plant("' + name + '"' + (given ? ', ' + h : '') + ')\nprint(p.height)', [[String(given ? h : d), given ? 'The height was given, so the default is not used.' : 'No height was given, so the default ' + d + ' is used.'], [String(given ? d : h), given ? 'The default is only used when nothing is given.' : 'Look again: only the name was given.'], [name, 'p.height is the number, not the name.'], ['An error', 'Fields with defaults can be left out.']]); },
      function () { var a = pickOne(['pea', 'kale', 'leek']), b = pickOne(['pea', 'kale', 'leek']), x = ri(1, 3), y = pickOne([x, x + 1]), same = a === b && x === y;
        return mk('What does this show?', 'from dataclasses import dataclass\n@dataclass\nclass Plant:\n    name: str\n    size: int\nprint(Plant("' + a + '", ' + x + ') == Plant("' + b + '", ' + y + '))', [[same ? 'True' : 'False', same ? 'Every field matches, so they are equal.' : 'A dataclass is equal only when every field matches.'], [same ? 'False' : 'True', same ? 'A dataclass compares the values, not which object it is.' : 'Check both fields: name and size.'], ['An error', '== works on dataclasses.'], ['None', '== gives True or False.']]); },
      function () { var s = pickOne(['ab', 'hi', 'ok']), n = ri(2, 3), useStr = pickOne([true, false]), k = ri(2, 9);
        return mk('What does this show?', 'def times(n: int) -> int:\n    return n * ' + n + '\nprint(times(' + (useStr ? '"' + s + '"' : k) + '))', [[useStr ? new Array(n + 1).join(s) : String(k * n), useStr ? 'Hints are not checked: a string times ' + n + ' repeats it.' : k + ' times ' + n + ' is ' + (k * n) + '.'], ['An error', 'Python does not check hints when the code runs.'], [useStr ? s : String(k), 'The function multiplies by ' + n + '.'], [useStr ? s + ' ' + n : String(k + n), 'It multiplies, it does not add.']]); }
'''
