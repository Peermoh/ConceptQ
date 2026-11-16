KEY, IDX = 'sets', 12
META = dict(tag='Sets · Second floor', title='Sets: no repeats allowed', topic='sets',
            lastBtn='Raise the walls', doneTitle='Floor 2 has walls and a roof!',
            doneText='You learned sets: collections with no repeats, that can be joined and compared. One wall per side, never two norths. The walls are up, the crane lowered the roof, and you can go upstairs. Your toy box is in the house.')
QUIZ = [
 ('What does this show?', 'nums = {1, 1, 2, 2, 3}\nprint(len(nums))', ['3', '5', '2', '1'], 0,
  ['Repeats vanish, so the set is {1, 2, 3}: 3 items.', 'A set drops the repeated 1 and 2.', 'Count again: 1, 2 and 3 are left.', 'Only the repeats vanish, not every number.']),
 ('What happens?', 'walls = {"north", "south"}\nprint(walls[0])', ['A TypeError', 'north', 'south', 'None'], 0,
  ['A set has no positions, so [0] is a TypeError.', 'A set has no first item: it has no order.', 'A set has no order at all.', 'Python stops with an error instead.']),
 ('What does this show?', 'toys = {"car", "ball"}\ntoys.add("car")\nprint(len(toys))', ['2', '3', '1', 'An error'], 0,
  ['car is already in the set, so add does nothing: still 2.', 'Adding something that is already there does not repeat it.', 'add never removes anything.', 'Adding a repeat is allowed: it is just ignored.']),
 ('What does this show?', 'a = {1, 2, 3}\nb = {2, 3, 4}\nprint(sorted(a & b))', ['[2, 3]', '[1, 2, 3, 4]', '[1]', '[4]'], 0,
  ['& keeps only what is in both: 2 and 3.', 'That is a | b, everything joined.', 'That is a - b.', 'That is b - a.']),
 ('What does this show?', 'a = {1, 2, 3}\nb = {2, 3, 4}\nprint(sorted(a - b))', ['[1]', '[4]', '[2, 3]', '[]'], 0,
  ['a - b keeps what is in a but not in b: just 1.', 'That is b - a. The order matters.', 'That is the overlap, a & b.', '1 is in a and not in b, so it stays.']),
 ('What is an empty set?', '# pick one', ['set()', '{}', '[]', '()'], 0,
  ['set() makes an empty set.', 'Empty curly brackets make an empty dictionary.', 'Square brackets make a list.', 'Round brackets make a tuple.']),
 ('What does this show?', 'print("cat" in {"cat", "dog"})', ['True', 'False', 'cat', 'An error'], 0,
  ['in checks if it is in the set, and cat is.', 'cat is right there in the set.', 'in gives True or False.', 'in works on sets.']),
]
CARDS = [
 ('s11', 'coll', 12, 'What happens to repeats in a set?', 'They vanish: `{1, 1, 2}` is `{1, 2}`.'),
 ('s12', 'coll', 12, 'What do `a | b`, `a & b` and `a - b` give?', 'Join (everything), overlap (in both), and what is in a but not b.'),
 ('s13', 'bugs', 12, 'How do you make an empty set?', '`set()`. `{}` is an empty dictionary.'),
 ('s14', 'coll', 12, 'How do you remove the repeats from a list?', '`set(my_list)`'),
]
GEN_JS = r'''
      function () { var base = [ri(1, 5), ri(6, 9)], x = shuffled(base.concat([base[0], base[1], ri(1, 9)])), u = x.filter(function (v, i) { return x.indexOf(v) === i; }).length;
        return mk('What does this show?', 'print(len({' + x.join(', ') + '}))', [[u, 'Repeats vanish. ' + u + ' different numbers are left.'], [x.length, 'That counts the repeats too. A set keeps each number once.'], [u === 1 ? 2 : u - 1, 'Count the different numbers again.'], [x.join('').length + 10, 'len counts the items in the set.']]); },
      function () { var a = shuffled([1, 2, 3, 4, 5, 6]).slice(0, 3).sort(), b = shuffled([1, 2, 3, 4, 5, 6]).slice(0, 3).sort(), op = pickOne(['|', '&', '-']);
        function srt(z) { return z.slice().sort(function (p, q) { return p - q; }); }
        var U = srt(a.concat(b.filter(function (v) { return a.indexOf(v) < 0; }))), I = srt(a.filter(function (v) { return b.indexOf(v) >= 0; })), D = srt(a.filter(function (v) { return b.indexOf(v) < 0; })), D2 = srt(b.filter(function (v) { return a.indexOf(v) < 0; }));
        var R = { '|': U, '&': I, '-': D }[op], name = { '|': 'joins everything', '&': 'keeps only what is in both', '-': 'keeps what is in a but not in b' }[op];
        var others = [[U, 'That is a | b, everything joined.'], [I, 'That is a & b, the overlap.'], [D, 'That is a - b.'], [D2, 'That is b - a. The order matters.']].filter(function (o) { return pyList(o[0]) !== pyList(R); }).slice(0, 3);
        if (others.length < 3) return null; // two results came out equal: try new values
        return mk('What does this show?', 'a = {' + a.join(', ') + '}\nb = {' + b.join(', ') + '}\nprint(sorted(a ' + op + ' b))', [[pyList(R), op + ' ' + name + '.']].concat(others.map(function (o) { return [pyList(o[0]), o[1]]; }))); },
      function () { var t = shuffled(['car', 'ball', 'kite', 'drum']).slice(0, 2), add = pickOne([t[0], 'yoyo']), n = t.indexOf(add) >= 0 ? 2 : 3;
        return mk('What does this show?', 'toys = {"' + t[0] + '", "' + t[1] + '"}\ntoys.add("' + add + '")\nprint(len(toys))', [[n, n === 2 ? add + ' is already there, so nothing changes.' : add + ' is new, so the set grows to 3.'], [n === 2 ? 3 : 2, n === 2 ? 'A set never holds a repeat.' : 'add puts the new toy in.'], [1, 'add never removes anything.'], ['An error', 'Adding to a set is allowed.']]); },
      function () { var w = pickOne(['cat', 'dog', 'fox']), s = shuffled(['cat', 'dog', 'owl', 'bee']).slice(0, 2), r = s.indexOf(w) >= 0;
        return mk('What does this show?', 'print("' + w + '" in {"' + s[0] + '", "' + s[1] + '"})', [[r ? 'True' : 'False', r ? w + ' is in the set.' : w + ' is not in the set.'], [r ? 'False' : 'True', 'Look at the set again.'], [w, 'in gives True or False.'], ['An error', 'in works on sets.']]); }
'''
