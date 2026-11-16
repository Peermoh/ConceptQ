KEY, IDX = 'strtools', 14
META = dict(tag='String tools · Second floor', title='String tools: shaping text', topic='string tools',
            lastBtn='Hang the wallpaper', doneTitle='The wallpaper is up!',
            doneText='You learned string tools: replace, split, join, strip, find, step slices and neat f-strings. The upstairs walls have patterned wallpaper, stripes repeated like "|" * 20. Your notice board is in the house.')
QUIZ = [
 ('What does this show?', 'print("cat".replace("c", "h"))', ['hat', 'cat', 'hcat', 'An error'], 0,
  ['replace swaps c for h: hat.', 'replace gives a new string with the change in it.', 'replace swaps, it does not add.', 'replace is a normal string method.']),
 ('What does this give?', 'print("a b c".split())', ["['a', 'b', 'c']", 'abc', "['a b c']", 'a b c'], 0,
  ['split cuts at the spaces and gives a list.', 'split gives a list, not glued text.', 'split cuts at every space, so there are three parts.', 'split gives a list of words.']),
 ('What does this give?', 'print("-".join(["x", "y"]))', ['x-y', '-xy', 'xy-', "['x', 'y']"], 0,
  ['join puts the dash between the items: x-y.', 'The dash goes between the items, not in front.', 'The dash goes between, not at the end.', 'join gives one string, not a list.']),
 ('What does this give?', 'print(len("  hi  ".strip()))', ['2', '6', '4', '0'], 0,
  ['strip removes the spaces at both ends, leaving hi: 2 letters.', 'That counts the spaces too. strip removed them.', 'strip removes the spaces on both sides, not one side.', 'The letters h and i are still there.']),
 ('What does this give?', 'print("banana".count("a"))', ['3', '1', '6', '2'], 0,
  ['banana has three a letters.', 'That would be find, not count. Count them all.', 'That is len, every letter.', 'Count again: b-a-n-a-n-a.']),
 ('What does this give?', 'print("stop"[::-1])', ['pots', 'stop', 's', 'An error'], 0,
  ['[::-1] walks backwards, so it reverses the word: pots.', 'The -1 step goes backwards.', 'That would be [0]. [::-1] takes every letter, backwards.', 'Step slices are allowed.']),
 ('What happens?', 'word = "Jam"\nword[0] = "H"', ['A TypeError', 'word is Ham', 'word is HJam', 'Nothing'], 0,
  ['Strings can never change, so this is a TypeError.', 'To get Ham, build a new string: "H" + word[1:].', 'Assigning to [0] does not add a letter.', 'Python stops with an error.']),
 ('What does this show?', 'price = 2.5\nprint(f"{price:.2f}")', ['2.50', '2.5', '2', '2.500'], 0,
  [':.2f shows exactly two decimal places: 2.50.', 'The .2f adds a second decimal place.', '.2f keeps decimals, it does not drop them.', '.2f means two decimal places, not three.']),
]
CARDS = [
 ('st1', 'types', 14, 'What does `"cat".replace("c", "h")` give?', '"hat". replace gives a new string.'),
 ('st2', 'types', 14, 'What do `split()` and `join()` do?', '`"a b".split()` → `["a", "b"]`; `"-".join(["a", "b"])` → `"a-b"`'),
 ('st3', 'types', 14, 'How do you reverse a string?', '`s[::-1]`'),
 ('st4', 'types', 14, 'How do you show 3.5 as 3.50?', '`f"{3.5:.2f}"`'),
 ('st5', 'bugs', 14, 'Why does `word[0] = "H"` fail?', 'Strings cannot change. Build a new one: `"H" + word[1:]`'),
]
GEN_JS = r'''
      function () { var w = pickOne(['cat', 'cot', 'cup', 'cap']), to = pickOne(['b', 'h', 'm']);
        return mk('What does this show?', 'print("' + w + '".replace("c", "' + to + '"))', [[to + w.slice(1), 'replace swaps c for ' + to + ': ' + to + w.slice(1) + '.'], [w, 'replace gives a new string with the swap in it.'], [to + w, 'replace swaps, it does not add.'], ['An error', 'replace is a normal string method.']]); },
      function () { var ws = shuffled(['red', 'blue', 'green', 'pink', 'gold']).slice(0, ri(2, 4)), sep = pickOne(['-', '+', '/']);
        return mk('What does this give?', 'print("' + sep + '".join(' + pyList(ws).replace(/'/g, '"') + '))', [[ws.join(sep), 'join puts "' + sep + '" between the items.'], [sep + ws.join(sep), 'The "' + sep + '" goes between the items, not in front.'], [ws.join(''), 'join puts the "' + sep + '" between them.'], [pyList(ws), 'join gives one string, not a list.']]); },
      function () { var w = pickOne(['banana', 'pepper', 'cocoa', 'letter', 'kitten']), ch = pickOne(w.split('')), n = w.split(ch).length - 1;
        return mk('What does this give?', 'print("' + w + '".count("' + ch + '"))', [[n, w + ' has ' + n + ' "' + ch + '".'], [w.length, 'That is len, every letter.'], [w.indexOf(ch) !== n ? w.indexOf(ch) : n + 1, w.indexOf(ch) !== n ? 'That is find: where the first "' + ch + '" is.' : 'Count them again.'], [n === 1 ? 2 : n - 1, 'Count them again, one by one.']]); },
      function () { var w = pickOne(['stop', 'live', 'star', 'drawer', 'parts']), r = w.split('').reverse().join('');
        return mk('What does this give?', 'print("' + w + '"[::-1])', [[r, '[::-1] walks backwards: ' + r + '.'], [w, 'The -1 step goes backwards.'], [w[0], 'That is [0]. [::-1] takes every letter, backwards.'], [w[w.length - 1], 'That is [-1], just the last letter.']]); },
      function () { var w = pickOne(['python', 'rocket', 'planet', 'kitten']), st = pickOne([2, 3]), r = w.split('').filter(function (c, i) { return i % st === 0; }).join('');
        return mk('What does this give?', 'print("' + w + '"[::' + st + '])', [[r, '[::' + st + '] takes every ' + (st === 2 ? 'second' : 'third') + ' letter, starting with the first.'], [w.slice(0, st), 'That is [:' + st + '], the first ' + st + ' letters.'], [w.split('').filter(function (c, i) { return i % st === 1; }).join(''), 'The step starts at the first letter, position 0.'], [w[st], 'That is [' + st + '], one letter.']]); },
      function () { var p = pickOne([1.5, 2.25, 3.1, 4.75, 0.5]), d = (String(p).split('.')[1] || '').length > 1 ? 2 : pickOne([1, 2]); // never ask for a rounding Python and JS might disagree on
        var r = p.toFixed(d), wrong = d === 1 ? p.toFixed(2) : String(p);
        return mk('What does this show?', 'price = ' + p + '\nprint(f"{price:.' + d + 'f}")', [[r, ':.' + d + 'f shows exactly ' + d + ' decimal place' + (d > 1 ? 's' : '') + ': ' + r + '.'], [wrong === r ? p.toFixed(3) : wrong, 'Check the number after the dot: .' + d + 'f.'], [Math.floor(p), '.' + d + 'f keeps decimals.'], ['An error', 'Formatting a number like this is allowed.']]); }
'''
