KEY, IDX = 'func2', 16
META = dict(tag='Functions II · Second floor', title='Functions II: settings and scope', topic='functions',
            lastBtn='Fit the oven', doneTitle='The oven is in!',
            doneText='You learned default values, keyword arguments, returning two things, *args, **kwargs, scope and a function that calls itself. The kitchen has an oven with dials. Your toaster is in the kitchen: turn its dial with level=.')
QUIZ = [
 ('What does this show?', 'def toast(n, level=3):\n    print(n, level)\ntoast(2)', ['2 3', '2', '2 None', 'An error'], 0,
  ['level was left out, so it uses its default, 3.', 'print shows both n and level.', 'level has a default, so it is 3, not None.', 'Leaving out a parameter with a default is allowed.']),
 ('What does this show?', 'def toast(n, level=3):\n    print(n, level)\ntoast(level=5, n=1)', ['1 5', '5 1', '1 3', 'An error'], 0,
  ['With names, order does not matter: n is 1, level is 5.', 'print shows n first, then level.', 'level=5 replaces the default 3.', 'Keyword arguments can come in any order.']),
 ('What does this show?', 'def size():\n    return 3, 4\nw, h = size()\nprint(h)', ['4', '3', '(3, 4)', 'An error'], 0,
  ['size returns the tuple (3, 4), unpacked into w and h: h is 4.', '3 went into w.', 'The tuple was unpacked into two boxes.', 'Returning two values is allowed.']),
 ('What does this show?', 'def total(*nums):\n    return sum(nums)\nprint(total(1, 2, 3, 4))', ['10', '4', '1', 'An error'], 0,
  ['*nums collects every value, and sum adds them: 10.', '4 is how many values there are.', 'nums holds all the values, not just the first.', '*args lets the function take any number of values.']),
 ('What does this show?', 'x = 1\ndef f():\n    x = 5\nf()\nprint(x)', ['1', '5', 'None', 'An error'], 0,
  ['The x inside f is a new local box. The outside x is still 1.', 'f made its own x. It did not change the outside one.', 'x is 1, set on the first line.', 'This code runs without errors.']),
 ('What happens?', 'def toast(n, level=3):\n    pass\ntoast(level=5, 2)', ['A SyntaxError', 'It works', 'level is 2', 'n is 5'], 0,
  ['A plain argument cannot come after a named one: SyntaxError.', 'Plain arguments must come first.', 'Python never gets that far: it is a SyntaxError.', 'Python stops before running anything.']),
 ('What does this show?', 'def count(n):\n    if n == 0:\n        return\n    print(n)\n    count(n - 1)\ncount(2)', ['2, then 1', '2', '2, then 1, then 0', 'Nothing'], 0,
  ['It prints 2, calls count(1) which prints 1, then count(0) stops.', 'count calls itself, so 1 is printed too.', 'When n is 0 it returns before printing.', 'count(2) prints before calling itself again.']),
]
CARDS = [
 ('f5', 'recipes', 16, 'What does `level=3` in `def toast(n, level=3):` mean?', 'A default: if you leave level out, it is 3.'),
 ('f6', 'recipes', 16, 'What are keyword arguments?', 'Arguments with names, like `toast(level=5, n=2)`. Order does not matter.'),
 ('f7', 'recipes', 16, 'What does `*nums` collect? And `**items`?', '`*nums`: any number of values, as a tuple. `**items`: named values, as a dictionary.'),
 ('f8', 'bugs', 16, 'Does `x = 5` inside a function change an `x` outside it?', 'No. It makes a new local x (unless you write `global x`).'),
]
GEN_JS = r'''
      function () { var d = ri(2, 6), n = ri(1, 4), give = pickOne([true, false]), l = ri(7, 9);
        return mk('What does this show?', 'def toast(n, level=' + d + '):\n    print(n, level)\ntoast(' + n + (give ? ', level=' + l : '') + ')', [[n + ' ' + (give ? l : d), give ? 'level=' + l + ' replaces the default.' : 'level was left out, so it uses its default, ' + d + '.'], [n + ' ' + (give ? d : l), give ? 'The default is only used when level is left out.' : 'Check the default in the def line: ' + d + '.'], [String(n), 'print shows both n and level.'], [n + ' None', 'level always has a value here.']]); },
      function () { var vals = [ri(1, 9), ri(1, 9), ri(1, 9), ri(1, 9), ri(1, 9)].slice(0, ri(2, 5)), s = vals.reduce(function (p, q) { return p + q; }, 0);
        return mk('What does this show?', 'def total(*nums):\n    return sum(nums)\nprint(total(' + vals.join(', ') + '))', [[s, '*nums collects every value, and sum adds them: ' + s + '.'], [vals.length, 'That is how many values there are.'], [vals[0], 'nums holds all the values, not just the first.'], [vals.join(''), 'sum adds the numbers, it does not join them.']]); },
      function () { var a = ri(1, 9), b = ri(10, 19);
        return mk('What does this show?', 'x = ' + a + '\ndef f():\n    x = ' + b + '\nf()\nprint(x)', [[a, 'The x inside f is a new local box. The outside x is still ' + a + '.'], [b, 'f made its own x. It did not change the outside one.'], ['None', 'x is ' + a + ', set on the first line.'], ['An error', 'This code runs without errors.']]); },
      function () { var a = ri(1, 9), b = ri(10, 19), w = pickOne(['w', 'h']);
        return mk('What does this show?', 'def size():\n    return ' + a + ', ' + b + '\nw, h = size()\nprint(' + w + ')', [[w === 'w' ? a : b, 'size returns (' + a + ', ' + b + '), unpacked into w and h.'], [w === 'w' ? b : a, 'That went into the other box.'], ['(' + a + ', ' + b + ')', 'The tuple was unpacked into two boxes.'], ['An error', 'Returning two values is allowed.']]); },
      function () { var n = ri(2, 4), seq = []; for (var i = n; i >= 1; i--) seq.push(i);
        return mk('What does this show?', 'def count(n):\n    if n == 0:\n        return\n    print(n)\n    count(n - 1)\ncount(' + n + ')', [[seq.join(' '), 'It prints ' + n + ', then calls itself with ' + (n - 1) + ', and so on until 0 stops it.'], [String(n), 'count calls itself, so the smaller numbers print too.'], [seq.concat([0]).join(' '), 'When n is 0 it returns before printing.'], [seq.slice().reverse().join(' '), 'It prints n first, then counts down.']]); }
'''
