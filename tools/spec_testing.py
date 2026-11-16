KEY, IDX = 'testing', 31
META = dict(tag='Testing · Third floor', title='Testing: the inspector visits', topic='testing',
            lastBtn='Call the inspector', doneTitle='Inspection passed!',
            doneText='You learned assert, test functions, unittest, edge cases, finding the cause of a bug, and writing the test first. The inspector checked every switch and pipe, the house passed, and the scaffolding has come down. The inspector\'s clipboard is in the house: run the checklist.')
QUIZ = [
 ('What happens?', 'assert 3 * 3 == 9\nprint("ok")', ['ok', 'An AssertionError', 'True', '9'], 0,
  ['The check is true, so assert does nothing and the print runs.', 'assert only stops the program when the check is False.', 'assert prints nothing itself.', 'assert does not show the answer.'], 0),
 ('What happens?', 'assert len("hi") == 3\nprint("ok")', ['An AssertionError', 'ok', '2', 'A SyntaxError'], 0,
  ['len("hi") is 2, so the check is False and assert stops the program.', 'The check is False, so the print is never reached.', 'assert does not print the length.', 'The code is written correctly.'], 0),
 ('Which method will unittest run as a test?', 'class LampTest(unittest.TestCase):', ['test_lamp_on', 'lamp_test_on', 'check_lamp', 'lampOn'], 0,
  ['unittest runs methods whose names start with test.', 'The name must start with test.', 'check_ is not picked up.', 'It must start with test.'], 2),
 ('What does this do?', 'self.assertEqual(2 + 2, 5)', ['Fails, saying 4 != 5', 'Passes', 'Prints 5', 'Changes the answer to 5'], 0,
  ['2 + 2 is 4, not 5, so the test fails and says so.', '4 is not equal to 5.', 'It checks, it does not print.', 'Tests never change your code.'], 3),
 ('Brightness can be 0 to 100. Which is an edge case?', '# test these', ['0', '50', '42', '70'], 0,
  ['0 is at the very edge of what is allowed.', '50 is right in the middle.', '42 is a normal value.', '70 is a normal value.'], 5),
 ('A test fails. What do you read first?', 'Traceback (most recent call last): …', ['The last line of the error', 'The first line of your file', 'The test names', 'Nothing: just run it again'], 0,
  ['The last line says what went wrong.', 'The error message points you to the right line.', 'Names do not explain the failure.', 'It will fail the same way again.'], 6),
 ('What does "test first" mean?', '# 1. write the check  2. watch it fail  3. write the code', ['Write the check before the code', 'Only run tests at the end', 'Test only the first function', 'Delete the failing tests'], 0,
  ['You write what should be true, then make it true.', 'Testing first means before writing the code.', 'It is about when, not which.', 'Failing tests show what to fix.'], 8),
]
CARDS = [
 ('tm1', 'team', 31, 'What does `assert x == 4` do?', 'Nothing if it is true; stops with an AssertionError if it is false.'),
 ('tm2', 'team', 31, 'How does unittest find your tests?', 'Methods whose names start with `test` in a `unittest.TestCase` class.'),
 ('tm3', 'team', 31, 'What is an edge case?', 'A value at the very edge, like 0 or 100 for brightness 0 to 100.'),
 ('tm4', 'team', 31, 'A test fails. What do you read first?', 'The last line of the error message.'),
]
GEN_STEPS = [0, 1]
GEN_JS = r'''
      function () { var a = ri(2, 9), b = ri(2, 9), ok = pickOne([true, false]), claim = ok ? a * b : a * b + pickOne([-1, 1, 2]);
        return mk('What happens?', 'assert ' + a + ' * ' + b + ' == ' + claim + '\nprint("ok")', [[ok ? 'ok' : 'An AssertionError', ok ? a + ' * ' + b + ' is ' + (a * b) + ', so the check is true and the print runs.' : a + ' * ' + b + ' is ' + (a * b) + ', not ' + claim + ', so assert stops the program.'], [ok ? 'An AssertionError' : 'ok', ok ? 'assert only stops when the check is False.' : 'The check is False, so the print is never reached.'], ['True', 'assert prints nothing itself.'], [String(a * b), 'assert does not show the answer.']]); },
      function () { var k = pickOne([3, 4, 5, 6, 7]), buggy = pickOne([true, false]), body = buggy ? 'n * n' : 'n + n';
        return mk('What happens?', 'def double(n):\n    return ' + body + '\nassert double(' + k + ') == ' + (2 * k) + '\nprint("pass")', [[buggy ? 'An AssertionError' : 'pass', buggy ? 'double(' + k + ') gives ' + (k * k) + ' because of the bug n * n, not ' + (2 * k) + '.' : 'n + n is ' + (2 * k) + ', so the test passes.'], [buggy ? 'pass' : 'An AssertionError', buggy ? 'Look at the body: n * n is not doubling.' : 'n + n really doubles.'], [String(buggy ? k * k : 2 * k), 'The test does not print the value.'], ['A SyntaxError', 'The code is written correctly.']]); }
'''
