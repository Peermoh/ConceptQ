KEY, IDX = 'generators', 36
META = dict(tag='Generators · Rooftop garden', title='Generators: make it when it is needed', topic='generators',
            lastBtn='Fit the rain barrel', doneTitle='Rain barrel fitted!',
            doneText='You learned yield, how a generator pauses, generator expressions, endless generators, pipelines and yield from. A rain barrel now fills from the shed roof. It is in your garden: ask it for water, one rainy day at a time.')
QUIZ = [
 ('What does this show?', 'def drops():\n    yield 1\n    yield 2\ng = drops()\nprint(next(g))', ['1', '2', '[1, 2]', 'None'], 0,
  ['next() runs up to the first yield and gives 1.', 'That comes from the second next().', 'next() gives one value at a time.', 'yield gives back a value.'], 1),
 ('What does calling drops() do?', 'def drops():\n    print("start")\n    yield 1\ng = drops()', ['Makes a generator; nothing is printed yet', 'Prints start', 'Gives back 1', 'An error'], 0,
  ['The body only runs when you call next().', 'start prints on the first next(), not now.', 'You get a generator, not the value.', 'This is fine Python.'], 1),
 ('What does this show?', 'def rain(days):\n    for litres in days:\n        if litres > 0:\n            yield litres\nprint(list(rain([3, 0, 5])))', ['[3, 5]', '[3, 0, 5]', '[0]', '8'], 0,
  ['Only the days with rain are yielded.', 'The 0 is skipped by the if.', 'The if keeps the rainy days, not the dry one.', 'list() collects the values, it does not add them.'], 2),
 ('What does this show?', 'sq = (n * n for n in range(4))\nprint(sum(sq))', ['14', '6', '16', '30'], 0,
  ['0 + 1 + 4 + 9 is 14.', 'That is 0 + 1 + 2 + 3, without squaring.', 'range(4) stops before 4.', 'That would be range(5).'], 3),
 ('Why can a generator with while True be safe?', 'def days():\n    n = 1\n    while True:\n        yield n\n        n += 1', ['It makes the next value only when asked', 'Python stops it after 1000 values', 'while True is always an error', 'It runs in the background'], 0,
  ['Each next() runs just to the next yield, then it waits.', 'There is no automatic limit.', 'It is fine inside a generator.', 'It only runs when you ask.'], 4),
 ('What does this show?', 'def a():\n    yield 1\ndef b():\n    yield from a()\n    yield 2\nprint(list(b()))', ['[1, 2]', '[2]', '[1]', '[[1], 2]'], 0,
  ['yield from passes on every value from a(), then b() yields 2.', 'yield from a() gives the 1 first.', 'b() carries on to yield 2.', 'The values are passed on one by one, not as a list.'], 6),
 ('When is a list better than a generator?', '# pick one', ['When you need to go through it twice', 'When the data is huge', 'When it never ends', 'When you only need the first item'], 0,
  ['A generator is used up after one pass.', 'Huge data is where generators shine.', 'A list cannot be endless.', 'A generator makes just the first item.'], 7),
]
CARDS = [
 ('gn1', 'mach', 36, 'What makes a function a generator?', 'It uses `yield`. Calling it gives a generator; `next()` runs it to the next yield.'),
 ('gn2', 'mach', 36, 'How is `(n*n for n in xs)` different from `[n*n for n in xs]`?', 'Round brackets make a generator: values are made one at a time, no list.'),
 ('gn3', 'mach', 36, 'What does `yield from other()` do?', 'Passes on every value from another generator.'),
 ('gn4', 'mach', 36, 'When should you use a list instead of a generator?', 'When you need all items at once, or need to go through them twice.'),
]
GEN_STEPS = [2, 3, 1]
GEN_JS = r'''
      function () { var days = []; for (var j = 0; j < 4; j++) days.push(pickOne([0, 0, 2, 3, 4, 6])); if (days.every(function (d) { return d === 0; })) days[1] = 5; if (days.every(function (d) { return d > 0; })) days[2] = 0;
        var wet = days.filter(function (d) { return d > 0; }), tot = wet.reduce(function (a, b) { return a + b; }, 0);
        return mk('What does this show?', 'def rain(days):\n    for litres in days:\n        if litres > 0:\n            yield litres\nprint(list(rain([' + days.join(', ') + '])))', [['[' + wet.join(', ') + ']', 'Only the days with rain are yielded.'], ['[' + days.join(', ') + ']', 'The dry days (0) are skipped by the if.'], [String(tot), 'list() collects the values, it does not add them up.'], ['[' + days.filter(function (d) { return d === 0; }).join(', ') + ']', 'The if keeps the rainy days, not the dry ones.']]); },
      function () { var k = ri(3, 6), even = pickOne([true, false]), xs = []; for (var j = 0; j < k; j++) if (!even || j % 2 === 0) xs.push(j);
        var tot = xs.reduce(function (a, b) { return a + b; }, 0), all = k * (k - 1) / 2;
        return mk('What does this show?', 'total = sum(n for n in range(' + k + ')' + (even ? ' if n % 2 == 0' : '') + ')\nprint(total)', [[String(tot), 'Add ' + xs.join(' + ') + ': that is ' + tot + '.'], [String(even ? all : tot + k), even ? 'The if keeps only the even numbers.' : 'range(' + k + ') stops before ' + k + '.'], [String(even ? tot + k - (k % 2 ? 0 : 0) + 1 : k), even ? 'Check which numbers are even, starting from 0.' : 'sum adds the numbers, it does not count them.'], ['An error', 'sum works on a generator.']]); },
      function () { var a = ri(1, 4), b = a + ri(1, 3), c = b + ri(1, 3), k = ri(1, 3), vals = [a, b, c], code = 'def drops():\n    yield ' + a + '\n    yield ' + b + '\n    yield ' + c + '\ng = drops()\n';
        for (var j = 1; j < k; j++) code += 'next(g)\n';
        return mk('What does this show?', code + 'print(next(g))', [[String(vals[k - 1]), 'Each next() runs to the next yield: this is yield number ' + k + '.'], [String(vals[k % 3]), 'Count the next() calls before this one.'], [String(vals[(k + 1) % 3]), 'The generator does not skip a yield.'], ['None', 'yield gives back a value.']]); }
'''
