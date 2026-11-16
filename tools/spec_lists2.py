KEY, IDX = 'lists2', 10
META = dict(tag='Lists II · Second floor', title='Lists II: working with lists', topic='lists',
            lastBtn='Lay the floorboards', doneTitle='The floorboards are down!',
            doneText='You learned to loop through lists, sort them, copy them, and put lists inside lists. The floorboards are laid in rows and columns, like floor[row][col]. Your shoe rack is in the house.')
QUIZ = [
 ('What does this show?', 'for p in ["a", "b", "c"]:\n    print(p)', ['a, then b, then c', 'abc', '["a", "b", "c"]', 'a'], 0,
  ['The loop takes one item each turn and prints it: a, then b, then c.', 'Each print is a new line, so they are not stuck together.', 'p is one item at a time, never the whole list.', 'The loop keeps going until every item has had a turn.']),
 ('What does this show?', 'x = [5, 2, 8]\nprint(max(x) - min(x))', ['6', '8', '2', '3'], 0,
  ['max is 8, min is 2, and 8 - 2 = 6.', '8 is max(x). We take min(x) away from it.', '2 is min(x). We take it away from max(x).', '3 is how many items there are, from len(x).']),
 ('What does this show?', 'x = [3, 1, 2]\nx.sort()\nprint(x)', ['[1, 2, 3]', '[3, 1, 2]', '[3, 2, 1]', 'None'], 0,
  ['sort() puts the list in order, smallest first.', 'sort() changes the list itself, so it is now in order.', 'That is reverse order. Plain sort() puts the smallest first.', 'We print x, the list. It is sort() itself that gives back None.']),
 ('What does this show?', 'a = [1, 2]\nb = a\nb.append(9)\nprint(a)', ['[1, 2, 9]', '[1, 2]', '[9, 1, 2]', 'An error'], 0,
  ['b = a gives the same list a second name, so a changes too.', 'b = a does not copy. a and b are one list.', 'append adds to the end, not the start.', 'Giving a list two names is allowed.']),
 ('What does this show?', 'a = [1, 2]\nb = a[:]\nb.append(9)\nprint(a)', ['[1, 2]', '[1, 2, 9]', '[9]', 'An error'], 0,
  ['a[:] made a real copy, so changing b leaves a alone.', 'That would happen with b = a. a[:] is a separate copy.', 'a still holds 1 and 2.', 'a[:] is a normal way to copy a list.']),
 ('What does this give?', 'grid = [[1, 2], [3, 4]]\nprint(grid[0][1])', ['2', '1', '3', '[1, 2]'], 0,
  ['Row 0 is [1, 2], and position 1 in it is 2.', '1 is grid[0][0], the first item of row 0.', '3 is in row 1. [0] picks row 0.', 'That is grid[0], the whole row. [1] then picks one item.']),
 ('What does this show?', 'q = [1, 2, 3]\nq.pop(0)\nprint(q)', ['[2, 3]', '[1, 2]', '[1, 2, 3]', '1'], 0,
  ['pop(0) takes the first item, like serving the front of a queue.', 'pop() with nothing would take the last. pop(0) takes the first.', 'pop changes the list, so the 1 is gone.', 'pop(0) gives back 1, but we print the list.']),
 ('What does this show?', 'x = [3, 1, 2]\ny = sorted(x)\nprint(x)', ['[3, 1, 2]', '[1, 2, 3]', 'None', '[3, 2, 1]'], 0,
  ['sorted() gives back a new list. x itself is not changed.', 'That is y. sorted() leaves x as it was.', 'sorted() gives back a list, not None.', 'Nothing was reversed here.']),
]
CARDS = [
 ('l6', 'coll', 10, 'What do `sum`, `min` and `max` do to `[7, 3, 9]`?', 'sum → 19, min → 3, max → 9'),
 ('l7', 'coll', 10, 'What is the difference between `x.sort()` and `sorted(x)`?', '`x.sort()` changes x. `sorted(x)` gives a new sorted list and leaves x alone.'),
 ('l8', 'bugs', 10, 'After `b = a`, does `b.append(1)` change a?', 'Yes! b and a are the same list. Copy with `b = a[:]`.'),
 ('l9', 'coll', 10, 'In `grid = [[1, 2], [3, 4]]`, what is `grid[1][0]`?', '3. Row 1, then column 0.'),
 ('l10', 'coll', 10, 'Stack or queue: which takes from the front?', 'A queue: `queue.pop(0)`. A stack takes from the top: `stack.pop()`.'),
]
GEN_JS = r'''
      function () { var x = [ri(1, 9), ri(1, 9), ri(1, 9), ri(1, 9)].slice(0, ri(3, 4)), s = x.reduce(function (a, b) { return a + b; }, 0);
        return mk('What does this give?', 'print(sum(' + pyList(x) + '))', [[s, 'sum adds every item: ' + x.join(' + ') + ' = ' + s + '.'], [x.length, 'That is len, how many items. sum adds them up.'], [Math.max.apply(null, x), 'That is max, the biggest. sum adds them all.'], [x.join(''), 'sum adds numbers, it does not join digits.']]); },
      function () { var x = [ri(1, 30), ri(1, 30), ri(1, 30), ri(1, 30)], f = pickOne(['max', 'min']), r = Math[f].apply(null, x), o = Math[f === 'max' ? 'min' : 'max'].apply(null, x);
        return mk('What does this give?', 'print(' + f + '(' + pyList(x) + '))', [[r, f + ' gives the ' + (f === 'max' ? 'biggest' : 'smallest') + ' item: ' + r + '.'], [o, 'That is ' + (f === 'max' ? 'min' : 'max') + '. Check which one the code uses.'], [x[0], 'That is just the first item.'], [x[x.length - 1], 'That is just the last item.']]); },
      function () { var x = shuffled([ri(1, 5), ri(6, 10), ri(11, 15), ri(16, 20)]).slice(0, 3), up = x.slice().sort(function (a, b) { return a - b; }), rev = pickOne([false, true]);
        var want = rev ? up.slice().reverse() : up;
        return mk('What does this show?', 'x = ' + pyList(x) + '\nx.sort(' + (rev ? 'reverse=True' : '') + ')\nprint(x)', [[pyList(want), rev ? 'reverse=True puts the biggest first.' : 'sort() puts the list in order, smallest first.'], [pyList(rev ? up : up.slice().reverse()), rev ? 'reverse=True flips the order: biggest first.' : 'Plain sort() puts the smallest first.'], [pyList(x), 'sort() changes the list itself, so x is now in order.'], ['None', 'We print x, the list. Only sort() itself gives back None.']]); },
      function () { var g = [[ri(1, 9), ri(1, 9)], [ri(10, 19), ri(10, 19)], [ri(20, 29), ri(20, 29)]].slice(0, ri(2, 3)), r = ri(0, g.length - 1), c = ri(0, 1);
        return mk('What does this give?', 'grid = ' + '[' + g.map(pyList).join(', ') + ']' + '\nprint(grid[' + r + '][' + c + '])', [[g[r][c], 'Row ' + r + ' is ' + pyList(g[r]) + ', and position ' + c + ' in it is ' + g[r][c] + '.'], [g[c] && g[c][r] !== undefined && (c !== r) ? g[c][r] : g[r][1 - c], c !== r && g[c] ? 'That is grid[' + c + '][' + r + ']. The row comes first.' : 'That is the other item in row ' + r + '.'], [pyList(g[r]), 'That is the whole row. The second [' + c + '] picks one item.'], [g[(r + 1) % g.length][c], 'That is in row ' + ((r + 1) % g.length) + '. The first number picks the row.']]); },
      function () { var w = pickOne(['a', 'b']), x = shuffled(['a', 'a', 'b', 'c', w]).slice(0, ri(4, 5)), n = x.filter(function (q) { return q === w; }).length;
        return mk('What does this give?', 'print(' + pyList(x).replace(/'/g, '"') + '.count("' + w + '"))', [[n, w + ' appears ' + n + ' time' + (n === 1 ? '' : 's') + '.'], [x.length, 'That is len, all the items. count only counts "' + w + '".'], [x.indexOf(w) >= 0 ? (x.indexOf(w) === n ? n + 1 : x.indexOf(w)) : n + 1, x.indexOf(w) >= 0 && x.indexOf(w) !== n ? 'That is where the first "' + w + '" is, from index().' : 'Count again, one by one.'], [n + (n > 1 ? -1 : 2), 'Count again, one by one.']]); },
      function () { var p = ri(1, 9), q = ri(1, 9), v = ri(10, 20), copy = pickOne([true, false]);
        return mk('What does this show?', 'a = [' + p + ', ' + q + ']\nb = a' + (copy ? '[:]' : '') + '\nb.append(' + v + ')\nprint(a)', [[copy ? pyList([p, q]) : pyList([p, q, v]), copy ? 'a[:] made a real copy, so a is not changed.' : 'b = a gives the same list a second name, so a changes too.'], [copy ? pyList([p, q, v]) : pyList([p, q]), copy ? 'That would happen with b = a. a[:] is a copy.' : 'b = a does not copy: a and b are one list.'], [pyList([v, p, q]), 'append adds to the end, not the start.'], ['An error', 'This is all allowed.']]); }
'''
