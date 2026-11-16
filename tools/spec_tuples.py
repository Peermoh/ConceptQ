KEY, IDX = 'tuples', 11
META = dict(tag='Tuples · Second floor', title='Tuples: values locked together', topic='tuples',
            lastBtn='Set the corner posts', doneTitle='The corner posts are set!',
            doneText='You learned tuples: values locked together that never change, and how to unpack them. The corner posts are set in concrete at fixed spots. Your glass cabinet is in the house: look, but you cannot change what is inside.')
QUIZ = [
 ('What does this show?', 'post = (3, 7)\nprint(post[1])', ['7', '3', '(3, 7)', 'An error'], 0,
  ['Positions start at 0, so [1] is the second value: 7.', '3 is post[0], the first value.', '[1] picks one value, not the whole tuple.', 'You can read a tuple like a list.']),
 ('What happens?', 'post = (3, 7)\npost[0] = 5', ['A TypeError', 'post becomes (5, 7)', 'post becomes (3, 5)', 'Nothing happens'], 0,
  ['A tuple can never change, so Python stops with a TypeError.', 'That would work for a list, but tuples are locked.', 'Position 0 is the first value, and anyway tuples cannot change.', 'Python does not ignore it: it stops with an error.']),
 ('What is x?', 'x, y = (4, 9)', ['4', '9', '(4, 9)', 'An error'], 0,
  ['Unpacking hands out the values in order: x gets 4.', '9 goes into y, the second box.', 'Each box gets one value, not the whole tuple.', 'Unpacking two values into two boxes is allowed.']),
 ('Which of these is a tuple?', 'a = (5)\nb = (5,)\nc = [5]', ['b', 'a', 'c', 'all three'], 0,
  ['The comma makes it a tuple: (5,).', 'Without a comma, (5) is just the number 5.', 'Square brackets make a list.', 'Only the one with the comma is a tuple.']),
 ('What does this show?', 'a, b = 1, 2\na, b = b, a\nprint(a, b)', ['2 1', '1 2', '2 2', 'An error'], 0,
  ['b, a makes the tuple (2, 1), which is unpacked into a and b.', 'The second line swaps them.', 'Both sides are worked out first, so nothing is lost.', 'Swapping like this is allowed.']),
 ('What does this show?', 'days = ("Mon", "Tue", "Wed")\nprint(len(days))', ['3', '2', '9', '"Wed"'], 0,
  ['len counts the values in the tuple: 3.', 'Count again: Mon, Tue and Wed.', 'len counts values, not letters.', 'len gives a number.']),
 ('Which is the best fit for a tuple?', '# pick one', ['the 7 days of the week', 'a shopping list', 'scores in a game', 'friends in a chat'], 0,
  ['The days never change, so a tuple fits.', 'A shopping list changes, so a list fits better.', 'Scores change during the game: use a list.', 'People join and leave: use a list.']),
]
CARDS = [
 ('t1', 'coll', 11, 'How is a tuple different from a list?', 'A tuple can never change. It uses round brackets: `(0, 4)`.'),
 ('t2', 'coll', 11, 'What is `x` after `x, y = (4, 9)`?', '4. Unpacking hands out the values in order.'),
 ('t3', 'bugs', 11, 'What happens with `post[0] = 5` when post is a tuple?', 'A TypeError. Tuples cannot be changed.'),
 ('t4', 'bugs', 11, 'Is `(5)` a tuple?', 'No, it is just 5. A one-item tuple needs a comma: `(5,)`.'),
]
GEN_JS = r'''
      function () { var t = [ri(1, 9), ri(10, 19), ri(20, 29)].slice(0, ri(2, 3)), i = ri(0, t.length - 1);
        return mk('What does this show?', 'post = (' + t.join(', ') + ')\nprint(post[' + i + '])', [[t[i], 'Positions start at 0, so [' + i + '] is ' + t[i] + '.'], [t[(i + 1) % t.length], 'That is position ' + ((i + 1) % t.length) + '. Positions start at 0.'], ['(' + t.join(', ') + ')', '[' + i + '] picks one value, not the whole tuple.'], ['An error', 'You can read a tuple like a list.']]); },
      function () { var a = ri(1, 9), b = ri(10, 20), w = pickOne(['x', 'y']);
        return mk('What does this show?', 'x, y = (' + a + ', ' + b + ')\nprint(' + w + ')', [[w === 'x' ? a : b, 'Unpacking hands out the values in order: x gets ' + a + ', y gets ' + b + '.'], [w === 'x' ? b : a, 'That went into ' + (w === 'x' ? 'y' : 'x') + '. Values are handed out in order.'], ['(' + a + ', ' + b + ')', 'Each box gets one value, not the whole tuple.'], ['An error', 'Unpacking two values into two boxes is allowed.']]); },
      function () { var t = [ri(1, 9), ri(1, 9), ri(1, 9), ri(1, 9)].slice(0, ri(2, 4)), s = t.reduce(function (p, q) { return p + q; }, 0);
        return mk('What does this show?', 'spots = (' + t.join(', ') + ')\nprint(len(spots), sum(spots))', [[t.length + ' ' + s, 'len counts the values (' + t.length + ') and sum adds them (' + s + ').'], [s + ' ' + t.length, 'len comes first in the print, then sum.'], [t.length + ' ' + t.join(''), 'sum adds the numbers, it does not join them.'], ['An error', 'len and sum both work on tuples.']]); },
      function () { var a = ri(1, 9), b = ri(10, 19);
        return mk('What does this show?', 'a, b = ' + a + ', ' + b + '\na, b = b, a\nprint(a)', [[b, 'b, a makes the tuple (' + b + ', ' + a + '), which is unpacked: a gets ' + b + '.'], [a, 'That was a before the swap.'], ['(' + b + ', ' + a + ')', 'print(a) shows just a.'], ['An error', 'Swapping in one line is allowed.']]); }
'''
