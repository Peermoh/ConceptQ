KEY, IDX = 'lambda', 29
META = dict(tag='Lambda and closures · Third floor', title='Lambda and closures: functions as values', topic='lambda and closures',
            lastBtn='Fit the smart switches', doneTitle='Smart switches everywhere!',
            doneText='You learned lambda, sorting with a key, map and filter, functions as values, functions that make functions, closures and nonlocal. Every room has a smart switch now. Your robot vacuum is in the house: filter the dirty rooms and it cleans them.')
QUIZ = [
 ('What does this show?', 'f = lambda x: x + 3\nprint(f(4))', ['7', '4', '3', 'An error'], 0,
  ['f adds 3 to whatever it gets: 4 + 3.', 'f(4) runs the lambda.', 'f adds 3 to 4.', 'A lambda can be called like any function.'], 0),
 ('What does this show?', 'print(sorted(["kiwi", "fig", "banana"], key=len))', ["['fig', 'kiwi', 'banana']", "['banana', 'fig', 'kiwi']", "['kiwi', 'fig', 'banana']", "['banana', 'kiwi', 'fig']"], 0,
  ['key=len sorts by length: 3, 4, 6 letters.', 'That is alphabet order. key=len sorts by length.', 'sorted changes the order.', 'Shortest comes first, not longest.'], 1),
 ('What does this show?', 'print(list(map(lambda n: n * 10, [1, 2])))', ['[10, 20]', '[1, 2]', '[11, 12]', '30'], 0,
  ['map uses the lambda on every item.', 'map changes every item.', 'The lambda multiplies by 10.', 'map gives a list, not a total.'], 3),
 ('What does this show?', 'print(list(filter(lambda n: n % 2 == 0, [1, 2, 3, 4])))', ['[2, 4]', '[1, 3]', '[1, 2, 3, 4]', '[False, True, False, True]'], 0,
  ['filter keeps the even numbers.', 'Those are the odd ones, which fail the test.', 'filter removes some items.', 'filter keeps items, not True/False.'], 4),
 ('What does this show?', 'def make_adder(a):\n    def add(b):\n        return a + b\n    return add\nadd5 = make_adder(5)\nprint(add5(2))', ['7', '5', '2', 'An error'], 0,
  ['add5 remembers a = 5, so add5(2) is 5 + 2.', 'add5 also adds the 2.', 'add5 remembers the 5 too.', 'Returning a function is allowed.'], 7),
 ('What does this show?', 'shout = str.upper\nprint(shout("hi"))', ['HI', 'hi', 'shout', 'An error'], 0,
  ['shout is another name for str.upper.', 'shout runs upper().', 'shout is called, so its result is shown.', 'Functions can be stored in names.'], 5),
 ('What does this show?', 'def counter():\n    n = 0\n    def add():\n        nonlocal n\n        n += 1\n        return n\n    return add\nc = counter()\nc()\nprint(c())', ['2', '1', '0', 'An error'], 0,
  ['nonlocal lets add() change the remembered n: 1, then 2.', 'c() was already called once before.', 'Each call adds 1.', 'nonlocal makes this work.'], 8),
]
CARDS = [
 ('p5', 'power', 29, 'What is a lambda?', 'A tiny one-line function: `lambda n: n * 2`'),
 ('p6', 'power', 29, 'What do `map` and `filter` do?', 'map changes every item; filter keeps the items that pass a test.'),
 ('p7', 'power', 29, 'How do you sort words by length?', '`sorted(words, key=len)`'),
 ('p8', 'power', 29, 'What is a closure?', 'An inner function that remembers values from the function that made it.'),
]
GEN_STEPS = [0, 1, 3, 4, 7]
GEN_JS = r'''
      function () { var k = ri(2, 5), c = ri(1, 9), n = ri(1, 6);
        return mk('What does this show?', 'f = lambda x: x * ' + k + ' + ' + c + '\nprint(f(' + n + '))', [[n * k + c, n + ' * ' + k + ' + ' + c + ' = ' + (n * k + c) + '.'], [n * (k + c), 'Times happens before plus.'], [n * k, 'Do not forget the + ' + c + '.'], [n + k + c, '* means times.']]); },
      function () { var ws = shuffled(['ox', 'cat', 'bird', 'zebra', 'turtle']).slice(0, 3), byLen = ws.slice().sort(function (a, b) { return a.length - b.length; }), byAbc = ws.slice().sort();
        if (pyList(byLen) === pyList(byAbc)) return null; // make sure length order and alphabet order differ
        return mk('What does this show?', 'print(sorted(' + pyList(ws).replace(/'/g, '"') + ', key=len))', [[pyList(byLen), 'key=len sorts by length, shortest first.'], [pyList(byAbc), 'That is alphabet order. key=len sorts by length.'], [pyList(byLen.slice().reverse()), 'Shortest comes first, not longest.'], [pyList(ws), 'sorted changes the order.']]); },
      function () { var k = ri(2, 10), xs = [ri(1, 5), ri(6, 9), ri(10, 12)].slice(0, ri(2, 3)), r = xs.map(function (x) { return x * k; });
        return mk('What does this show?', 'print(list(map(lambda n: n * ' + k + ', ' + pyList(xs) + ')))', [[pyList(r), 'map uses the lambda on every item.'], [pyList(xs), 'map changes every item.'], [pyList(xs.map(function (x) { return x + k; })), 'The lambda multiplies by ' + k + '.'], [r.reduce(function (a, b) { return a + b; }, 0), 'map gives a list, not a total.']]); },
      function () { var xs = shuffled([ri(1, 3), ri(4, 6), ri(7, 9), ri(10, 12), ri(13, 15)]), t = ri(4, 10), keep = xs.filter(function (x) { return x > t; }), drop = xs.filter(function (x) { return x <= t; });
        if (!keep.length || !drop.length) return null;
        return mk('What does this show?', 'print(list(filter(lambda n: n > ' + t + ', ' + pyList(xs) + ')))', [[pyList(keep), 'filter keeps the numbers greater than ' + t + '.'], [pyList(drop), 'Those are the ones that fail the test.'], [pyList(xs), 'filter removes some items.'], [keep.length, 'filter gives a list of items, not how many.']]); },
      function () { var a = ri(2, 9), b = ri(1, 9), nm = 'add' + a;
        return mk('What does this show?', 'def make_adder(a):\n    def add(b):\n        return a + b\n    return add\n' + nm + ' = make_adder(' + a + ')\nprint(' + nm + '(' + b + '))', [[a + b, nm + ' remembers a = ' + a + ', so it gives ' + a + ' + ' + b + '.'], [a, nm + ' also adds the ' + b + '.'], [b, nm + ' remembers the ' + a + ' too.'], ['An error', 'Returning a function is allowed.']]); }
'''
