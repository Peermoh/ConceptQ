KEY, IDX = 'comp', 28
META = dict(tag='Comprehensions · Third floor', title='Comprehensions: build and sort in one line', topic='comprehensions',
            lastBtn='Build the lift', doneTitle='The lift is running!',
            doneText='You learned list, dict and set comprehensions, grids, match and case, and loop else. A lift now runs through all three floors, sorting boxes on the way. The sorting conveyor is in the house: put a box on the belt and match sends it to the right floor.')
QUIZ = [
 ('What does this show?', 'print([n * 2 for n in range(4)])', ['[0, 2, 4, 6]', '[2, 4, 6, 8]', '[0, 1, 2, 3]', '[0, 2, 4, 6, 8]'], 0,
  ['range(4) gives 0 to 3, and each one is doubled.', 'range starts at 0, so the first is 0 * 2.', 'Each n is multiplied by 2.', 'range(4) stops before 4.'], 0),
 ('What does this show?', 'print([n for n in [3, -1, 4, -5] if n > 0])', ['[3, 4]', '[-1, -5]', '[3, -1, 4, -5]', '[True, False, True, False]'], 0,
  ['Only the numbers greater than 0 are kept.', 'Those are the ones that fail n > 0.', 'The if removes some numbers.', 'It keeps the numbers themselves, not True/False.'], 1),
 ('What does this show?', 'print({w: len(w) for w in ["hi", "sun"]})', ["{'hi': 2, 'sun': 3}", "['hi', 'sun']", '{2, 3}', "{'hi': 'sun'}"], 0,
  ['Each word becomes a key, with its length as the value.', 'Curly brackets with a colon make a dictionary.', 'The keys are the words, the values the lengths.', 'Each value is a length.'], 3),
 ('What does this show?', 'print(len({c for c in "hello"}))', ['4', '5', '3', 'An error'], 0,
  ['A set keeps each letter once: h, e, l, o.', 'The two l letters become one.', 'Count again: h, e, l, o.', 'Set comprehensions are allowed.'], 4),
 ('What does this show?', 'floor = 3\nmatch floor:\n    case 1:\n        print("ground")\n    case 2:\n        print("upstairs")\n    case _:\n        print("loft")', ['loft', 'ground', 'upstairs', 'Nothing'], 0,
  ['3 matches neither 1 nor 2, so case _ runs.', 'That is case 1.', 'That is case 2.', 'case _ catches everything else.'], 6),
 ('What does this show?', 'for n in [1, 2, 3]:\n    if n == 7:\n        print("found")\n        break\nelse:\n    print("no 7")', ['no 7', 'found', 'Nothing', 'found, then no 7'], 0,
  ['No 7, so the loop never breaks and else runs.', 'There is no 7 in the list.', 'The else runs because there was no break.', 'found is never printed.'], 8),
 ('What does this show?', 'print([[0] * 2 for _ in range(3)])', ['[[0, 0], [0, 0], [0, 0]]', '[[0, 0, 0], [0, 0, 0]]', '[0, 0, 0, 0, 0, 0]', '[[0], [0], [0]]'], 0,
  ['3 rows, each with 2 zeros.', 'That is 2 rows of 3. Here range(3) makes the rows.', 'It is a list of lists, not one long list.', 'Each row is [0] * 2.'], 5),
 ('What does this show?', 'print([w.upper() for w in ["a", "b"]])', ["['A', 'B']", "['a', 'b']", 'AB', "['A', 'b']"], 0,
  ['Each word is changed with upper().', 'upper() changes each one.', 'A comprehension makes a list.', 'Every item is changed.'], 2),
]
CARDS = [
 ('p1', 'power', 28, 'Write the squares of 0 to 4 in one line.', '`[n * n for n in range(5)]`'),
 ('p2', 'power', 28, 'How do you keep only some items in a comprehension?', 'Add an if: `[n for n in nums if n > 0]`'),
 ('p3', 'power', 28, 'What does `case _:` do in match?', 'Catches anything the other cases did not.'),
 ('p4', 'power', 28, 'When does a loop\'s else run?', 'When the loop finishes without a break.'),
]
GEN_STEPS = [0, 1, 6, 8]
GEN_JS = r'''
      function () { var k = ri(2, 5), m = ri(3, 5), r = []; for (var n = 0; n < m; n++) r.push(n * k);
        var off = r.map(function (x) { return x + k; }), plain = r.map(function (x, i) { return i; });
        return mk('What does this show?', 'print([n * ' + k + ' for n in range(' + m + ')])', [[pyList(r), 'range(' + m + ') gives 0 to ' + (m - 1) + ', and each is multiplied by ' + k + '.'], [pyList(off), 'range starts at 0, so the first is 0 * ' + k + '.'], [pyList(plain), 'Each n is multiplied by ' + k + '.'], [pyList(r.concat([m * k])), 'range(' + m + ') stops before ' + m + '.']]); },
      function () { var xs = shuffled([ri(-9, -1), ri(1, 9), ri(-9, -1), ri(10, 20), 0]).slice(0, 5), t = pickOne([0, 5]), keep = xs.filter(function (x) { return x > t; }), drop = xs.filter(function (x) { return x <= t; });
        return mk('What does this show?', 'print([n for n in ' + pyList(xs) + ' if n > ' + t + '])', [[pyList(keep), 'Only the numbers greater than ' + t + ' are kept.'], [pyList(drop), 'Those are the ones that fail n > ' + t + '.'], [pyList(xs), 'The if removes some numbers.'], [pyList(xs.map(function (x) { return x > t ? 'True' : 'False'; })).replace(/'/g, ''), 'It keeps the numbers, not True/False.']]); },
      function () { var v = ri(1, 5), r = v === 1 ? 'ground' : (v === 2 || v === 3) ? 'upstairs' : 'loft';
        var others = ['ground', 'upstairs', 'loft'].filter(function (x) { return x !== r; });
        var why = { ground: 'case 1 matches only 1.', upstairs: 'case 2 | 3 matches 2 or 3.', loft: 'case _ only runs when nothing above matched.' };
        return mk('What does this show?', 'floor = ' + v + '\nmatch floor:\n    case 1:\n        print("ground")\n    case 2 | 3:\n        print("upstairs")\n    case _:\n        print("loft")', [[r, v + ' matches: ' + why[r]]].concat(others.map(function (o) { return [o, why[o]]; })).concat([['Nothing', 'case _ catches everything else, so something always prints.']])); },
      function () { var xs = shuffled([1, 2, 3, 4, 5, 6, 8, 9]).slice(0, 4), t = pickOne([7, xs[2]]), has = xs.indexOf(t) >= 0;
        return mk('What does this show?', 'for n in ' + pyList(xs) + ':\n    if n == ' + t + ':\n        print("found")\n        break\nelse:\n    print("no ' + t + '")', [[has ? 'found' : 'no ' + t, has ? t + ' is there, so the loop breaks and else is skipped.' : 'No ' + t + ', so the loop never breaks and else runs.'], [has ? 'no ' + t : 'found', has ? 'else is skipped after a break.' : 'There is no ' + t + ' in the list.'], ['found no ' + t, 'Only one of them prints.'], ['Nothing', 'One of the two prints always runs here.']]); }
'''
