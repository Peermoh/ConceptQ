KEY, IDX = 'modules', 19
META = dict(tag='Modules · Second floor', title='Modules: ready-made tools', topic='modules',
            lastBtn='Fill the toolbox', doneTitle='The toolbox is full!',
            doneText='You learned to import modules and use math and random: square roots, rounding up and down, dice rolls, picks and shuffles. Your toolbox is in the house: tap the tools inside.')
QUIZ = [
 ('What does this show?', 'import math\nprint(math.sqrt(9))', ['3.0', '81', '4.5', '9'], 0,
  ['sqrt gives the square root: 3 * 3 = 9, so 3.0.', 'That is 9 * 9. sqrt goes the other way.', 'That is 9 / 2. A square root is different.', 'sqrt changes the number.']),
 ('What does dir(math) give you?', 'import math\nprint(dir(math))', ['A list of the tools inside math', 'The square root of math', 'The folder math is saved in', 'An error'], 0,
  ['dir lists every name inside a module, like sqrt, pi and ceil.', 'dir looks inside the module. It does not do maths.', 'dir lists what is inside, not where it is.', 'dir works on any module.']),
 ('Which number can random.randint(1, 6) NOT give?', 'import random\nrandom.randint(1, 6)', ['0', '1', '6', '3'], 0,
  ['randint(1, 6) gives 1 to 6, so 0 is impossible.', '1 is the lowest it can give.', 'randint includes the top number, 6.', '3 is between 1 and 6.']),
 ('What is wrong here?', 'print(math.pi)', ['math was never imported', 'pi needs brackets', 'Nothing', 'pi is not in math'], 0,
  ['Without import math, Python does not know math: NameError.', 'math.pi is a value, not a function, so no brackets.', 'It needs import math first.', 'math.pi is right there in math.']),
 ('What does this show?', 'from math import floor\nprint(floor(7.9))', ['7', '8', '7.9', 'An error'], 0,
  ['floor always rounds down: 7.', 'That is ceil, or round. floor goes down.', 'floor gives a whole number.', 'from math import floor lets you write floor() on its own.']),
 ('What does random.shuffle(cards) do?', 'import random\ncards = [1, 2, 3]\nrandom.shuffle(cards)', ['Mixes cards in place', 'Gives back one card', 'Sorts the cards', 'Makes a copy'], 0,
  ['shuffle mixes the list itself, like shuffling a deck.', 'That is random.choice.', 'Sorting puts things in order. shuffle mixes.', 'shuffle changes the list itself.']),
 ('What is r here?', 'import random as r', ['A nickname for random', 'A random number', 'A new module', 'An error'], 0,
  ['as gives the module a shorter name: r.randint(1, 6).', 'r is the module, not a number.', 'It is the same random module.', 'import ... as ... is allowed.']),
]
CARDS = [
 ('m1', 'talk', 19, 'What is a module?', 'A box of ready-made tools. Open one with `import math`.'),
 ('m2', 'maths', 19, 'What do `math.ceil(2.1)` and `math.floor(2.9)` give?', '3 and 2: ceil rounds up, floor rounds down.'),
 ('m3', 'talk', 19, 'Can `random.randint(1, 6)` give 6?', 'Yes: randint includes both ends.'),
 ('m4', 'talk', 19, 'What does `import random as r` do?', 'Gives random a nickname, so you write `r.randint(1, 6)`.'),
]
GEN_JS = r'''
      function () { var n = ri(2, 12);
        return mk('What does this show?', 'import math\nprint(math.sqrt(' + (n * n) + '))', [[n + '.0', n + ' * ' + n + ' = ' + (n * n) + ', so the square root is ' + n + '.0.'], [String(n * n * n * n), 'That is ' + (n * n) + ' * ' + (n * n) + '. sqrt goes the other way.'], [String(n * n / 2), 'That is half. A square root is different.'], [String(n * n), 'sqrt changes the number.']]); },
      function () { var a = ri(1, 9), f = ri(1, 8), fn = pickOne(['ceil', 'floor']), x = a + f / 10;
        var r = fn === 'ceil' ? a + 1 : a;
        return mk('What does this show?', 'import math\nprint(math.' + fn + '(' + x.toFixed(1) + '))', [[r, fn + ' always rounds ' + (fn === 'ceil' ? 'up' : 'down') + ': ' + r + '.'], [fn === 'ceil' ? a : a + 1, 'That is ' + (fn === 'ceil' ? 'floor' : 'ceil') + '. Check which one the code uses.'], [x.toFixed(1), fn + ' gives a whole number.'], [r + '.0', 'math.' + fn + ' gives a whole number, with no .0.']]); },
      function () { var a = ri(1, 9), f = ri(1, 8), x = a + f / 10, fn = pickOne(['floor', 'ceil']);
        return mk('What does this show?', 'from math import ' + fn + '\nprint(' + fn + '(' + x.toFixed(1) + '))', [[fn === 'ceil' ? a + 1 : a, 'from math import ' + fn + ' lets you write ' + fn + '() on its own.'], [fn === 'ceil' ? a : a + 1, fn + ' rounds ' + (fn === 'ceil' ? 'up' : 'down') + '.'], [x.toFixed(1), fn + ' gives a whole number.'], ['An error', 'The import brings ' + fn + ' in, so this works.']]); }
'''
