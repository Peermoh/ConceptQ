KEY, IDX = 'exc2', 22
META = dict(tag='Exceptions in depth · Third floor', title='Exceptions in depth: safety first', topic='exceptions',
            lastBtn='Put up the scaffolding', doneTitle='The safety scaffolding is up!',
            doneText='You learned the order of excepts, catching several kinds, else, finally, the family of errors, raise, your own errors and chains. Safety scaffolding with nets is around the house, ready for work high up. Your harness hook is in the house: finally always unclips it.')
QUIZ = [
 ('What does this show?', 'try:\n    x = 1 / 0\nexcept ArithmeticError:\n    print("A")\nexcept ZeroDivisionError:\n    print("Z")', ['A', 'Z', 'A, then Z', 'An error'], 0,
  ['ArithmeticError is checked first, and it is the parent of ZeroDivisionError, so it catches it.', 'The first matching except wins, and ArithmeticError matches first.', 'Only one except runs.', 'The error is caught.'], 0),
 ('What does this show?', 'try:\n    n = int("7")\nexcept ValueError:\n    print("bad")\nelse:\n    print("ok")\nfinally:\n    print("done")', ['ok, then done', 'done', 'bad, then done', 'ok'], 0,
  ['Nothing went wrong, so else runs, and finally always runs.', 'else runs too, because there was no error.', '"7" is a fine number, so except is skipped.', 'finally always runs at the end.'], 3),
 ('What does this show?', 'try:\n    int("x")\nexcept (ValueError, TypeError):\n    print("caught")', ['caught', 'An error', 'Nothing', 'x'], 0,
  ['A tuple of errors catches either kind, and this is a ValueError.', 'The ValueError is caught.', 'except runs, so caught is shown.', 'The code prints caught.'], 1),
 ('What does this show?', 'class FallError(Exception):\n    pass\ntry:\n    raise FallError("slip")\nexcept FallError as e:\n    print(e)', ['slip', 'FallError', 'An error', 'e'], 0,
  ['print(e) shows the message the error was raised with.', 'It shows the message, not the class name.', 'The error is caught by its own except.', 'e is a name for the error; print shows its message.'], 7),
 ('Does finally run here?', 'try:\n    print("climb")\nfinally:\n    print("unclip")', ['Yes: climb, then unclip', 'No', 'Only if there is an error', 'unclip, then climb'], 0,
  ['finally always runs at the end, error or not.', 'finally always runs.', 'finally runs whether or not there was an error.', 'try runs first, finally last.'], 4),
 ('Which is a child of ArithmeticError?', '# the family of errors', ['ZeroDivisionError', 'ValueError', 'KeyError', 'NameError'], 0,
  ['Dividing by zero is an arithmetic problem.', 'ValueError is a separate branch.', 'KeyError is a LookupError.', 'NameError is its own kind.'], 5),
 ('What does raise on its own do inside except?', 'except ValueError:\n    log()\n    raise', ['Passes the same error on up', 'Stops the error', 'Makes a brand new error', 'Ignores it'], 0,
  ['raise with nothing after it sends the same error onwards.', 'It does the opposite: the error keeps going.', 'It re-raises the same one.', 'The error is passed on, not ignored.'], 6),
 ('What does from e add?', 'raise SafetyError("no rope") from e', ['It keeps the first error in the message', 'It hides the first error', 'It is a SyntaxError', 'It tries again'], 0,
  ['from e chains the errors, so you can see what started it.', 'It shows the first error, it does not hide it.', 'from is allowed after raise.', 'It does not retry anything.'], 8),
]
CARDS = [
 ('x1', 'bugs', 22, 'When do `else` and `finally` run?', '`else`: only if nothing went wrong. `finally`: always.'),
 ('x2', 'bugs', 22, 'Which except should come first?', 'The specific one (ValueError) before the general one (Exception).'),
 ('x3', 'bugs', 22, 'How do you make your own error?', '`class FallError(Exception): pass`, then `raise FallError("…")`'),
 ('x4', 'bugs', 22, 'What does `raise … from e` do?', 'Chains the errors, so the message shows what started it.'),
]
GEN_STEPS = [3, 5, 7]
GEN_JS = r'''
      function () { var good = pickOne([true, false]), v = good ? String(ri(1, 99)) : pickOne(['x', 'ten', '3a']);
        return mk('What does this show?', 'try:\n    n = int("' + v + '")\nexcept ValueError:\n    print("bad")\nelse:\n    print("ok")\nfinally:\n    print("done")', [[good ? 'ok done' : 'bad done', good ? 'No error, so else runs; finally always runs.' : 'int fails, so except runs; finally always runs.'], [good ? 'bad done' : 'ok done', good ? '"' + v + '" is a fine number.' : '"' + v + '" is not a number.'], [good ? 'ok' : 'bad', 'finally always runs at the end too.'], ['done', 'One of except or else also runs.']]); },
      function () { var c = pickOne([['1 / 0', 'A', 'ZeroDivisionError is an ArithmeticError.'], ['[1, 2][5]', 'L', 'IndexError is a LookupError.'], ['{"a": 1}["b"]', 'L', 'KeyError is a LookupError.'], ['int("x")', 'E', 'ValueError is neither, so the general Exception catches it.']]);
        var all = ['A', 'L', 'E'];
        return mk('What does this show?', 'try:\n    print(' + c[0] + ')\nexcept ArithmeticError:\n    print("A")\nexcept LookupError:\n    print("L")\nexcept Exception:\n    print("E")', [[c[1], c[2]]].concat(all.filter(function (x) { return x !== c[1]; }).map(function (x) { return [x, { A: 'ArithmeticError is for maths problems like dividing by zero.', L: 'LookupError is for missing positions and keys.', E: 'Exception only runs if nothing above matched.' }[x]]; })).concat([['An error', 'One of the excepts catches it.']])); },
      function () { var cls = pickOne(['FallError', 'RopeError', 'WindError']), msg = pickOne(['slip', 'too high', 'windy']);
        return mk('What does this show?', 'class ' + cls + '(Exception):\n    pass\ntry:\n    raise ' + cls + '("' + msg + '")\nexcept ' + cls + ' as e:\n    print(e)', [[msg, 'print(e) shows the message the error was raised with.'], [cls, 'It shows the message, not the class name.'], ['e', 'e is a name for the error; print shows its message.'], ['An error', 'The error is caught by its own except.']]); }
'''
