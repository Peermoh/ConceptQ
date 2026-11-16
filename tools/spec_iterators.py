KEY, IDX = 'iterators', 35
META = dict(tag='Iterators · Rooftop garden', title='Iterators: one at a time', topic='iterators',
            lastBtn='Turn on the tap', doneTitle='The garden has begun!',
            doneText='You learned iter() and next(), StopIteration, what a for loop really does, your own iterator class, lazy ranges, enumerate, zip and itertools. A garden shed is built with a tap on its side. The water tap is in your garden: turn it one cup at a time.')
QUIZ = [
 ('What does this show?', 'it = iter([4, 5, 6])\nnext(it)\nprint(next(it))', ['5', '4', '6', '[5, 6]'], 0,
  ['The first next() gave 4, so this one gives 5.', 'That was used up by the first next().', 'That comes after one more next().', 'next() gives one item, not the rest.'], 1),
 ('What happens?', 'it = iter(["cup"])\nnext(it)\nnext(it)', ['A StopIteration error', 'It shows cup again', 'It shows None', 'It starts again from the start'], 0,
  ['The only item is used up, so next() raises StopIteration.', 'An iterator never goes back.', 'next() raises an error, it does not give None.', 'You need a new iter() to start again.'], 2),
 ('What does a for loop use to get each item?', 'for cup in tank:', ['next(), until StopIteration', 'An index: tank[0], tank[1]…', 'len(tank) first', 'A copy of the list'], 0,
  ['for calls iter() once, then next() until StopIteration.', 'for works on things with no index too, like files.', 'for never needs the length.', 'No copy is made.'], 3),
 ('What does this show?', 'class Countdown:\n    def __init__(self, n):\n        self.n = n\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.n == 0:\n            raise StopIteration\n        self.n -= 1\n        return self.n + 1\nprint(list(Countdown(3)))', ['[3, 2, 1]', '[2, 1, 0]', '[1, 2, 3]', 'An error'], 0,
  ['It takes one off, then returns the number before: 3, 2, 1.', 'It returns n + 1 after taking one off.', 'It counts down, not up.', 'StopIteration ends list() quietly.'], 4),
 ('Why is range(1_000_000_000) fine to use?', 'r = range(1_000_000_000)', ['It makes each number only when asked', 'Python is very fast', 'It only keeps the first million', 'It is not: it fills the memory'], 0,
  ['range is lazy: no big list is ever built.', 'Speed is not the reason: there is no list at all.', 'It can give every number, one at a time.', 'It uses almost no memory.'], 5),
 ('What does the first line show?', 'for i, bed in enumerate(["peas", "beans"]):\n    print(i, bed)', ['0 peas', '1 peas', 'peas 0', '0 beans'], 0,
  ['enumerate counts from 0 and gives (number, item).', 'Counting starts at 0.', 'The number comes first.', 'beans is on the second line.'], 6),
 ('What does this show?', 'from itertools import cycle, islice\nprint(list(islice(cycle("RG"), 3)))', ["['R', 'G', 'R']", "['R', 'G']", "['RG', 'RG', 'RG']", "['R', 'R', 'R']"], 0,
  ['cycle repeats R, G, R, G… and islice takes 3.', 'islice took 3 items, not 2.', 'cycle gives one letter at a time.', 'cycle moves on each time.'], 7),
]
CARDS = [
 ('it1', 'mach', 35, 'What do `iter()` and `next()` do?', '`iter(x)` gives an iterator; `next(it)` gives its next item.'),
 ('it2', 'mach', 35, 'What happens when an iterator runs out?', '`next()` raises `StopIteration`. A for loop stops there quietly.'),
 ('it3', 'mach', 35, 'Which two methods make a class an iterator?', '`__iter__` (return self) and `__next__` (the next item, or raise StopIteration).'),
 ('it4', 'mach', 35, 'What do `enumerate` and `zip` give?', '`enumerate`: (number, item). `zip`: items from two lists side by side.'),
]
GEN_STEPS = [1, 6, 6]
GEN_JS = r'''
      function () { var xs = shuffled([2, 3, 5, 7, 8, 9]).slice(0, 3), k = ri(1, 3), code = 'it = iter([' + xs.join(', ') + '])\n';
        for (var j = 1; j < k; j++) code += 'next(it)\n';
        return mk('What does this show?', code + 'print(next(it))', [[String(xs[k - 1]), k === 1 ? 'The first next() gives the first item.' : (k - 1) + ' next() call' + (k > 2 ? 's' : '') + ' used up the earlier items, so this gives ' + xs[k - 1] + '.'], [String(xs[(k) % 3]), 'Count how many next() calls came before.'], [String(xs[(k + 1) % 3]), 'Each next() moves on by one item.'], ['An error', 'There are still items left.']]); },
      function () { var names = shuffled(['peas', 'beans', 'kale', 'leeks', 'corn']).slice(0, ri(2, 4)), st = pickOne([0, 1, 5]), n = names.length;
        var code = 'for i, bed in enumerate(' + pyList(names).replace(/'/g, '"') + (st ? ', start=' + st : '') + '):\n    pass';
        return mk('What is i at the end?', code, [[String(st + n - 1), 'enumerate counts from ' + st + ', and the last of ' + n + ' beds gets ' + (st + n - 1) + '.'], [String(st + n), 'The count starts at ' + st + ', so the last one is ' + (st + n - 1) + '.'], [String(st ? n - 1 : n + 1), st ? 'With start=' + st + ', counting does not begin at 0.' : 'Counting starts at 0.'], ['bed', 'i holds the number, bed holds the name.']]); },
      function () { var a = ri(2, 5), b = ri(2, 5); if (a === b) b = a + 1;
        var la = shuffled(['x', 'y', 'z', 'w', 'v']).slice(0, a), lb = []; for (var j = 0; j < b; j++) lb.push(j + 1);
        return mk('What does this show?', 'beds = ' + pyList(la).replace(/'/g, '"') + '\nseeds = [' + lb.join(', ') + ']\nprint(len(list(zip(beds, seeds))))', [[String(Math.min(a, b)), 'zip stops when the shorter list runs out.'], [String(Math.max(a, b)), 'zip does not go past the end of the shorter list.'], [String(a + b), 'zip makes pairs, it does not join the lists.'], ['An error', 'zip is fine with lists of different lengths.']]); }
'''
