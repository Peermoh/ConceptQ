KEY, IDX = 'errors', 17
META = dict(tag='Errors · Second floor', title='Errors: catch problems safely', topic='errors',
            lastBtn='Fit the smoke alarm', doneTitle='The smoke alarm is up!',
            doneText='You learned the names of errors and how try and except catch them, so one problem does not stop everything. The kitchen has a smoke alarm now. Press its test button in the kitchen: it catches the burnt toast and the house carries on.')
QUIZ = [
 ('Which error is this?', 'int("hi")', ['ValueError', 'TypeError', 'NameError', 'ZeroDivisionError'], 0,
  ['"hi" is text that cannot become a number: ValueError.', 'The type is fine (text into int), but the value is not a number.', 'NameError is for a name Python does not know.', 'Nothing is divided here.']),
 ('Which error is this?', '"age" + 9', ['TypeError', 'ValueError', 'SyntaxError', 'IndexError'], 0,
  ['Text and a number are different types: TypeError.', 'ValueError is for a value that cannot be turned into a number.', 'The code is written correctly. The types just do not mix.', 'There is no list here.']),
 ('What does this show?', 'try:\n    n = int("hi")\n    print("A")\nexcept ValueError:\n    print("B")', ['B', 'A', 'A, then B', 'An error'], 0,
  ['int("hi") fails, so Python jumps straight to except: B.', 'print("A") is skipped, because the line before it failed.', 'Once the error happens, the rest of try is skipped.', 'except catches the ValueError, so there is no crash.']),
 ('What does this show?', 'try:\n    n = int("7")\n    print("A")\nexcept ValueError:\n    print("B")', ['A', 'B', 'A, then B', 'Nothing'], 0,
  ['"7" turns into 7 fine, so except never runs: A.', 'except only runs when there is an error.', 'except is skipped when nothing goes wrong.', 'print("A") runs, because nothing failed.']),
 ('What does this show?', 'try:\n    x = 5 / 0\nexcept ValueError:\n    print("V")\nexcept ZeroDivisionError:\n    print("Z")', ['Z', 'V', 'V, then Z', 'An error'], 0,
  ['Dividing by zero is a ZeroDivisionError, so the second except runs.', 'This is not a ValueError.', 'Only the except that matches runs.', 'The ZeroDivisionError is caught.']),
 ('Which line tells you what went wrong?', '# Traceback (most recent call last):\n#   File "game.py", line 3\n# IndexError: list index out of range', ['The last line', 'The first line', 'The middle line', 'None of them'], 0,
  ['The last line names the error and says what went wrong.', 'Traceback only says that an error is coming.', 'That line says where it happened, not what.', 'The last line explains it.']),
 ('Why avoid a bare except:?', 'try:\n    score = scroe + 1\nexcept:\n    pass', ['It hides your own typos too', 'It is slower', 'It is a SyntaxError', 'It catches nothing'], 0,
  ['The typo scroe is a NameError, and the bare except hides it.', 'Speed is not the problem. Hiding bugs is.', 'It is allowed, which is why it is risky.', 'It catches everything, including bugs.']),
]
CARDS = [
 ('e1', 'bugs', 17, 'What are ValueError, TypeError and ZeroDivisionError?', 'Bad value (int("hi")), wrong types ("a" + 1), dividing by zero (5 / 0).'),
 ('e2', 'bugs', 17, 'What do `try` and `except` do?', 'Run the code in try. If it fails, jump to except instead of crashing.'),
 ('e3', 'bugs', 17, 'Which line of an error message says what went wrong?', 'The last one.'),
 ('e4', 'bugs', 17, 'Why is `except ValueError:` better than `except:`?', 'It only catches the error you expect, so other bugs still show up.'),
]
GEN_JS = r'''
      function () { var good = pickOne([true, false]), v = good ? String(ri(1, 99)) : pickOne(['hi', 'ten', '7a', 'x']), a = pickOne(['Yes', 'Ok', 'Done']), b = pickOne(['Oops', 'No', 'Bad']);
        return mk('What does this show?', 'try:\n    n = int("' + v + '")\n    print("' + a + '")\nexcept ValueError:\n    print("' + b + '")', [[good ? a : b, good ? '"' + v + '" turns into a number fine, so except never runs.' : 'int("' + v + '") fails, so Python jumps straight to except.'], [good ? b : a, good ? 'except only runs when there is an error.' : 'print("' + a + '") is skipped, because the line before it failed.'], [a + ' ' + b, 'Only one of them runs.'], ['An error', good ? 'Nothing goes wrong here.' : 'except catches the ValueError.']]); },
      function () { var d = pickOne([0, ri(1, 5)]), n = ri(6, 20);
        var r = d === 0 ? 'Z' : String(Math.floor(n / d));
        return mk('What does this show?', 'try:\n    print(' + n + ' // ' + d + ')\nexcept ZeroDivisionError:\n    print("Z")', [[r, d === 0 ? 'Dividing by zero jumps to except: Z.' : n + ' // ' + d + ' is ' + r + ', and nothing goes wrong.'], [d === 0 ? '0' : 'Z', d === 0 ? 'Python cannot divide by zero, so except runs.' : 'except only runs if there is an error.'], [d === 0 ? String(n) : r + ' Z', d === 0 ? 'Dividing by zero is an error.' : 'Only one of them is printed.'], ['An error', 'The except catches the ZeroDivisionError.']]); },
      function () { var cases = [['int("hi")', 'ValueError'], ['"a" + 1', 'TypeError'], ['10 / 0', 'ZeroDivisionError'], ['[1, 2][5]', 'IndexError'], ['{"a": 1}["b"]', 'KeyError']], c = pickOne(cases);
        var others = shuffled(cases.filter(function (o) { return o[1] !== c[1]; })).slice(0, 3);
        var why = { ValueError: 'a value that cannot be turned into a number', TypeError: 'two types that do not mix', ZeroDivisionError: 'dividing by zero', IndexError: 'a position that does not exist', KeyError: 'a dictionary key that is not there' };
        function art(e) { return (/^[AEIOU]/.test(e) ? 'An ' : 'A ') + e; } // An IndexError, A TypeError
        return mk('Which error does this cause?', 'print(' + c[0] + ')', [[art(c[1]), 'This is ' + why[c[1]] + '.']].concat(others.map(function (o) { return [art(o[1]), o[1] + ' is for ' + why[o[1]] + '.']; }))); }
'''
