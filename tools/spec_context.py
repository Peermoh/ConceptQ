KEY, IDX = 'context', 38
META = dict(tag='Context managers · Rooftop garden', title='Context managers: always close the gate', topic='context managers',
            lastBtn='Hang the gate', doneTitle='The gate closes itself!',
            doneText='You learned with, __enter__ and __exit__, closing even after an error, @contextmanager with try and finally, several at once, and suppress. A self-closing gate now guards the garden. It is in your garden: walk through, trip over, and watch it close anyway.')
QUIZ = [
 ('What does this show?', 'class Gate:\n    def __enter__(self):\n        print("open")\n    def __exit__(self, *exc):\n        print("closed")\nwith Gate():\n    print("in")', ['open in closed', 'in', 'open closed in', 'closed in open'], 0,
  ['__enter__ runs first, then the block, then __exit__.', '__enter__ and __exit__ print too.', '__exit__ runs after the block.', '__enter__ runs at the start.'], 1),
 ('When does __exit__ run?', 'with Gate():\n    ...', ['When the block ends, even after an error', 'Only if there was no error', 'Only if you call it', 'Before the block'], 0,
  ['That is the whole point: it always runs.', 'It runs after errors too.', 'with calls it for you.', '__enter__ runs before; __exit__ after.'], 3),
 ('What happens to f after the with block?', 'with open("notes.txt") as f:\n    text = f.read()', ['It is closed', 'It stays open', 'It is deleted', 'It is emptied'], 0,
  ['with closes the file when the block ends.', 'with always closes it.', 'The file stays on disk; only the connection closes.', 'The file keeps its text.'], 0),
 ('In a @contextmanager function, when does the code before yield run?', '@contextmanager\ndef gate():\n    print("open")\n    yield\n    print("closed")', ['When the with block starts', 'When the block ends', 'Only if there is an error', 'Never'], 0,
  ['Before yield is the start; after yield is the end.', 'That is the code after yield.', 'It always runs at the start.', 'It runs every time you use with.'], 4),
 ('Why put yield inside try with finally?', '    try:\n        yield\n    finally:\n        print("closed")', ['So the closing code runs even after an error', 'To make it faster', 'Because yield needs try', 'To hide errors'], 0,
  ['finally always runs, error or not.', 'It is about safety, not speed.', 'yield works without try.', 'The error still shows; the gate just closes first.'], 5),
 ('In which order do these close?', 'with open("a.txt") as a, open("b.txt") as b:\n    ...', ['b first, then a', 'a first, then b', 'Both at exactly the same time', 'Neither closes'], 0,
  ['They close in reverse order of opening.', 'The last one opened closes first.', 'One after the other, in reverse.', 'with closes both.'], 6),
 ('What happens if old.txt does not exist?', 'from contextlib import suppress\nwith suppress(FileNotFoundError):\n    os.remove("old.txt")', ['Nothing: the error is ignored', 'A FileNotFoundError', 'The file is made', 'The program stops quietly'], 0,
  ['suppress swallows that one kind of error.', 'suppress stops that error.', 'remove never makes a file.', 'The program carries on after the with block.'], 7),
]
CARDS = [
 ('cm1', 'mach', 38, 'Which two methods make an object work with `with`?', '`__enter__` (at the start) and `__exit__` (at the end, even after an error).'),
 ('cm2', 'mach', 38, 'How do you write a context manager the easy way?', '`@contextmanager` on a generator: code before `yield` is the start, after it the end.'),
 ('cm3', 'mach', 38, 'How do you make sure the end code runs after an error?', 'Put `yield` in `try:` and the closing code in `finally:`.'),
 ('cm4', 'mach', 38, 'What does `with suppress(FileNotFoundError):` do?', 'Ignores that one kind of error inside the block.'),
]
GEN_STEPS = [2, 4, 7]
GEN_JS = r'''
      function () { var w = shuffled([['open', 'closed'], ['hello', 'bye'], ['on', 'off'], ['start', 'stop']])[0], mid = pickOne(['in', 'water', 'dig']);
        return mk('What does this show?', 'class Gate:\n    def __enter__(self):\n        print("' + w[0] + '")\n    def __exit__(self, *exc):\n        print("' + w[1] + '")\nwith Gate():\n    print("' + mid + '")', [[w[0] + ' ' + mid + ' ' + w[1], '__enter__ runs first, then the block, then __exit__.'], [mid, '__enter__ and __exit__ print as well.'], [w[0] + ' ' + w[1] + ' ' + mid, '__exit__ runs after the block, not before it.'], [mid + ' ' + w[0] + ' ' + w[1], '__enter__ runs before the block.']]); },
      function () { var a = pickOne(['open', 'unlock', 'hello']), b = pickOne(['closed', 'locked', 'bye']), m = pickOne(['dig', 'plant', 'water']), n = ri(2, 3), body = ''; for (var j = 0; j < n; j++) body += '    print("' + m + '")\n';
        var mids = []; for (j = 0; j < n; j++) mids.push(m);
        return mk('What does this show?', 'from contextlib import contextmanager\n@contextmanager\ndef gate():\n    print("' + a + '")\n    yield\n    print("' + b + '")\nwith gate():\n' + body.replace(/\n$/, ''), [[a + ' ' + mids.join(' ') + ' ' + b, 'Before yield is the start, then the block runs, then the code after yield.'], [mids.join(' '), 'The code before and after yield prints too.'], [a + ' ' + b + ' ' + mids.join(' '), 'The code after yield waits until the block is done.'], [a + ' ' + m + ' ' + b, 'The block prints ' + m + ' ' + n + ' times.']]); },
      function () { var k = pickOne(['dig', 'plant', 'seed']), err = pickOne([['ZeroDivisionError', 'x = 1 / 0'], ['KeyError', 'x = {}["a"]'], ['IndexError', 'x = [][0]']]);
        return mk('What does this show?', 'from contextlib import suppress\nwith suppress(' + err[0] + '):\n    print("' + k + '")\n    ' + err[1] + '\n    print("after")\nprint("done")', [[k + ' done', 'The error ends the block early, suppress ignores it, and the program carries on.'], [k + ' after done', 'The block stops at the error, so after never prints.'], ['done', k + ' printed before the error.'], ['An error', 'suppress(' + err[0] + ') stops that error.']]); }
'''
