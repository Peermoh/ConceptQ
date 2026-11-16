KEY, IDX = 'ai', 33
META = dict(tag='Coding with AI · Third floor', title='Coding with AI: you are in charge', topic='coding with an AI helper',
            lastBtn='Switch on the control room', doneTitle='The control room is on!',
            doneText='You learned to ask clearly, read every line, test what AI writes, fix it, explain it back, keep secrets out, and stay in charge. Nibb\'s control room is built in the loft. The control panel is there: ask Nibb for a function, find the bug, and only then press Install.')
QUIZ = [
 ('Which is the clearest thing to ask an AI helper?', '# you want a function', ['Write is_cold(t) that returns True when t is below 18', 'Make it work', 'Fix my code', 'Do the thing'], 0,
  ['It says the name, the input and exactly what to return.', 'The helper cannot know what "it" is.', 'Which code, and what is wrong?', 'Far too vague.'], 1),
 ('An AI helper gave you this. What should you do first?', 'def is_cold(t):\n    return t > 18', ['Read it and test it', 'Use it straight away', 'Delete all your tests', 'Ask for it in capitals'], 0,
  ['Always read and test before you keep it. Here the sign is wrong!', 'The helper can be wrong.', 'Tests are how you catch its mistakes.', 'Shouting does not help the code.'], 2),
 ('What happens?', 'def is_cold(t):\n    return t > 18\nassert is_cold(10) == True', ['An AssertionError', 'Nothing: it passes', 'It prints True', 'A SyntaxError'], 0,
  ['10 > 18 is False, so the test fails: the bug is caught.', 'is_cold(10) gives False, not True.', 'assert prints nothing.', 'The code is written correctly; the logic is wrong.'], 3),
 ('How do you fix is_cold?', 'def is_cold(t):\n    return t > 18', ['return t < 18', 'return t == 18', 'return True', 'Delete the test'], 0,
  ['Cold means below 18, so the sign must be <.', 'That is only true at exactly 18.', 'Then a hot day would be cold too.', 'The test was right; the code was wrong.'], 4),
 ('Which is safe to paste into an AI tool?', '# pick one', ['A short piece of your own game code', 'Your password', 'Your home address', 'A secret API key'], 0,
  ['Code with no secrets in it is fine to share.', 'Never share passwords.', 'Never share personal details.', 'Keys are secrets too.'], 6),
 ('You keep code an AI wrote, but you cannot explain one line. What now?', '# line 3 is a mystery', ['Ask it to explain, or look it up', 'Keep it anyway', 'Ship it and hope', 'Remove all the comments'], 0,
  ['Only keep code you understand.', 'Then you could not fix it later.', 'Hope is not a test.', 'Comments help you understand it.'], 5),
 ('Who is responsible for code you keep?', '# ask → read → test → fix → keep', ['You are', 'The AI', 'Nobody', 'The computer'], 0,
  ['Once you keep it, the code is yours.', 'The helper only suggests.', 'Someone always is: you.', 'The computer only runs it.'], 7),
]
CARDS = [
 ('ai1', 'team', 33, 'What is the plan when an AI helper writes code?', 'Ask clearly → read every line → test → fix → keep.'),
 ('ai2', 'bugs', 33, 'How do you know AI code works?', 'Test it, for example with `assert`. Read it too.'),
 ('ai3', 'team', 33, 'What must you never paste into an AI tool?', 'Passwords, keys and personal details.'),
 ('ai4', 'team', 33, 'Who answers for code you keep?', 'You do. Only keep code you can explain.'),
]
GEN_STEPS = [3, 4]
GEN_JS = r'''
      function () { var lim = pickOne([15, 16, 18, 20]), t = pickOne([lim - 6, lim - 3, lim + 3, lim + 6]), buggy = pickOne([true, false]), res = buggy ? t > lim : t < lim;
        return mk('What does this show?', 'def is_cold(t):\n    return t ' + (buggy ? '>' : '<') + ' ' + lim + '\nprint(is_cold(' + t + '))', [[res ? 'True' : 'False', t + (buggy ? ' > ' : ' < ') + lim + ' is ' + (res ? 'True' : 'False') + '.' + (buggy ? ' Careful: the sign is the wrong way round for "cold".' : '')], [res ? 'False' : 'True', 'Work out ' + t + (buggy ? ' > ' : ' < ') + lim + ' exactly as written.'], [String(t), 'The function returns True or False, not the number.'], ['An error', 'The code runs fine.']]); },
      function () { var a = ri(3, 9), bug = pickOne(['a - b', 'a * b', 'a + b']), good = bug === 'a + b', b = ri(2, 6), v = bug === 'a - b' ? a - b : bug === 'a * b' ? a * b : a + b;
        return mk('An AI wrote add(a, b). What happens?', 'def add(a, b):\n    return ' + bug + '\nassert add(' + a + ', ' + b + ') == ' + (a + b) + '\nprint("ok")', [[good ? 'ok' : 'An AssertionError', good ? 'a + b is right, so the test passes.' : 'add(' + a + ', ' + b + ') gives ' + v + ', not ' + (a + b) + ': the test caught the bug.'], [good ? 'An AssertionError' : 'ok', good ? 'The code adds correctly.' : 'Look at the body: it does not add.'], [String(v), 'assert does not print the value.'], ['A SyntaxError', 'The code is written correctly.']]); }
'''
