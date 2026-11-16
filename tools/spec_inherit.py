KEY, IDX = 'inherit', 27
META = dict(tag='Inheritance · Third floor', title='Inheritance: families of classes', topic='inheritance',
            lastBtn='Furnish the loft', doneTitle='The loft is furnished!',
            doneText='You learned inheritance: child classes, overriding, super(), polymorphism, isinstance in a family, two parents and the MRO, and is versus ==. The loft has its furniture, a whole family that comes from Furniture. The family portrait wall is in the house: tap a portrait to see what it inherits.')
QUIZ = [
 ('What does this show?', 'class Furniture:\n    def move(self):\n        return "slide"\nclass Bed(Furniture):\n    pass\nprint(Bed().move())', ['slide', 'Bed', 'None', 'An error'], 0,
  ['Bed inherits move() from Furniture.', 'move() returns "slide".', 'Bed got move() from its parent.', 'The child has the parent\'s methods.'], 1),
 ('What does this show?', 'class Furniture:\n    def move(self):\n        return "slide"\nclass Bed(Furniture):\n    def move(self):\n        return "roll"\nprint(Bed().move())', ['roll', 'slide', 'slide roll', 'An error'], 0,
  ['Bed overrides move(), so its own version is used.', 'The child\'s version replaces the parent\'s.', 'Only one move() runs.', 'Overriding is allowed.'], 2),
 ('What does this show?', 'class A:\n    def __init__(self):\n        self.x = 1\nclass B(A):\n    def __init__(self):\n        super().__init__()\n        self.y = 2\nb = B()\nprint(b.x + b.y)', ['3', '2', '1', 'An error'], 0,
  ['super().__init__() sets x = 1, then B sets y = 2: 1 + 2.', 'x was set too, by the parent.', 'y was set too, by B.', 'super() makes sure x exists.'], 3),
 ('What does this show?', 'class Furniture:\n    pass\nclass Bed(Furniture):\n    pass\nprint(isinstance(Bed(), Furniture))', ['True', 'False', 'Bed', 'An error'], 0,
  ['A Bed is a kind of Furniture.', 'isinstance counts the whole family.', 'isinstance gives True or False.', 'This works.'], 5),
 ('Which move() wins?', 'class Sofa:\n    def move(self):\n        return "sofa"\nclass Bed:\n    def move(self):\n        return "bed"\nclass SofaBed(Sofa, Bed):\n    pass\nprint(SofaBed().move())', ['sofa', 'bed', 'sofa bed', 'An error'], 0,
  ['Sofa is listed first, so it comes first in the MRO.', 'Bed comes second in the order.', 'Only one move() runs.', 'Two parents are allowed.'], 7),
 ('What does this show?', 'a = [1, 2]\nb = [1, 2]\nprint(a == b, a is b)', ['True False', 'True True', 'False False', 'False True'], 0,
  ['Same values, so == is True; two separate lists, so is is False.', 'They are two separate lists.', 'The values are equal.', 'If is were True, == would be too.'], 8),
 ('What is polymorphism?', 'for f in things:\n    f.move()', ['The same call works on different kinds of object', 'A class with two parents', 'Copying a class', 'A kind of loop'], 0,
  ['Each object answers move() its own way.', 'That is multiple inheritance.', 'Nothing is copied.', 'The loop is just how we try it.'], 4),
]
CARDS = [
 ('h1', 'blue', 27, 'What does `class Bed(Furniture):` mean?', 'Bed is a child of Furniture and gets all its methods.'),
 ('h2', 'blue', 27, 'What does `super().__init__()` do?', 'Runs the parent\'s setup inside the child\'s.'),
 ('h3', 'blue', 27, 'What is the MRO?', 'The order Python looks for a method: `SofaBed.__mro__`.'),
 ('h4', 'blue', 27, 'What is the difference between `==` and `is`?', '`==`: same value. `is`: the very same object.'),
]
GEN_STEPS = [2, 5, 7, 8]
GEN_JS = r'''
      function () { var pv = pickOne(['slide', 'creak', 'thud']), cv = pickOne(['roll', 'bounce', 'fold']), over = pickOne([true, false]), C = pickOne(['Bed', 'Desk', 'Chair']);
        return mk('What does this show?', 'class Furniture:\n    def move(self):\n        return "' + pv + '"\nclass ' + C + '(Furniture):\n' + (over ? '    def move(self):\n        return "' + cv + '"\n' : '    pass\n') + 'print(' + C + '().move())', [[over ? cv : pv, over ? C + ' overrides move(), so its own version is used.' : C + ' inherits move() from Furniture.'], [over ? pv : cv, over ? 'The child\'s version replaces the parent\'s.' : C + ' does not have its own move().'], [C, 'move() returns a word.'], ['An error', 'This works.']]); },
      function () { var c = pickOne([['Bed()', 'Furniture', true, 'A Bed is a kind of Furniture.'], ['Furniture()', 'Bed', false, 'Not all furniture is a bed: the parent is not the child.'], ['Lamp()', 'Furniture', false, 'Lamp is not in the Furniture family.'], ['Bed()', 'Bed', true, 'It was made from Bed.']]);
        return mk('What does this show?', 'class Furniture:\n    pass\nclass Bed(Furniture):\n    pass\nclass Lamp:\n    pass\nprint(isinstance(' + c[0] + ', ' + c[1] + '))', [[c[2] ? 'True' : 'False', c[3]], [c[2] ? 'False' : 'True', 'isinstance follows the family from child to parent only.'], [c[1], 'isinstance gives True or False.'], ['An error', 'This works.']]); },
      function () { var first = pickOne(['Sofa', 'Bed']), second = first === 'Sofa' ? 'Bed' : 'Sofa';
        return mk('Which move() wins?', 'class Sofa:\n    def move(self):\n        return "sofa"\nclass Bed:\n    def move(self):\n        return "bed"\nclass SofaBed(' + first + ', ' + second + '):\n    pass\nprint(SofaBed().move())', [[first.toLowerCase(), first + ' is listed first, so it comes first in the MRO.'], [second.toLowerCase(), second + ' comes second in the order.'], ['sofa bed', 'Only one move() runs.'], ['An error', 'Two parents are allowed.']]); },
      function () { var n = ri(1, 9), alias = pickOne([true, false]);
        return mk('What does this show?', 'a = [' + n + ']\nb = ' + (alias ? 'a' : '[' + n + ']') + '\nprint(a == b, a is b)', [[alias ? 'True True' : 'True False', alias ? 'b = a gives the same list a second name: equal, and the very same object.' : 'Same values, but two separate lists.'], [alias ? 'True False' : 'True True', alias ? 'b = a does not copy: it is the same list.' : 'Two separate [' + n + '] lists are not the same object.'], ['False False', 'The values are equal.'], ['False True', 'If is is True, == is True too.']]); }
'''
