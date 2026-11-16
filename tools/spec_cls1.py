KEY, IDX = 'cls1', 24
META = dict(tag='Classes I · Third floor', title='Classes I: blueprints and objects', topic='classes',
            lastBtn='Open the dormers', doneTitle='Three dormer windows!',
            doneText='You learned classes: a blueprint, objects made from it, __init__, self, attributes and methods. Three dormer windows open up the roof space, all made from one blueprint. Your blueprint printer is in the house: print a new window object.')
QUIZ = [
 ('What does this show?', 'class Dog:\n    def __init__(self, name):\n        self.name = name\nd = Dog("Rex")\nprint(d.name)', ['Rex', 'name', 'Dog', 'An error'], 0,
  ['__init__ stored "Rex" in self.name, and self was d.', 'd.name gives the value stored, not the word name.', 'Dog is the class. d.name is the dog\'s name.', 'This is a correct class.'], 3),
 ('How many objects are made?', 'class Cup:\n    pass\na = Cup()\nb = Cup()\nc = a', ['2', '3', '1', '0'], 0,
  ['Cup() is called twice. c = a gives the first cup a second name.', 'c = a does not make a new cup.', 'Cup() is called two times.', 'Each Cup() makes an object.'], 6),
 ('What does this show?', 'class Lamp:\n    def __init__(self):\n        self.on = False\n    def switch(self):\n        self.on = not self.on\nl = Lamp()\nl.switch()\nprint(l.on)', ['True', 'False', 'None', 'An error'], 0,
  ['It starts False, and switch() flips it to True.', 'switch() changed it.', 'on was set in __init__.', 'This is a correct class.'], 5),
 ('What does this show?', 'class Box:\n    def __init__(self, n):\n        self.n = n\na = Box(1)\nb = Box(2)\na.n = 9\nprint(b.n)', ['2', '9', '1', 'An error'], 0,
  ['Each object keeps its own n. Changing a does not change b.', '9 went into a, not b.', '1 is a\'s first value.', 'This works.'], 7),
 ('What is self?', '# def open(self): …', ['The object the method is working on', 'The class itself', 'A keyword that must be in capitals', 'A copy of the object'], 0,
  ['self is this one object, the one the method was called on.', 'self is one object, not the blueprint.', 'self is just a name, in small letters by habit.', 'It is the real object, not a copy.'], 3),
 ('What happens?', 'class Dormer:\n    def __init__(self, width):\n        if width <= 0:\n            raise ValueError("too thin")\nd = Dormer(0)', ['A ValueError', 'd is made with width 0', 'Nothing', 'A SyntaxError'], 0,
  ['The check in __init__ stops a broken window being made.', '__init__ raises before d is made.', 'The raise stops the program.', 'The code is written correctly.'], 8),
 ('What does this show?', 'class Pet:\n    def speak(self):\n        return "hi"\nprint(Pet().speak())', ['hi', 'speak', 'Pet', 'None'], 0,
  ['Pet() makes an object, and speak() returns "hi".', 'speak() is called, so its result is shown.', 'Pet() is the object; speak() gives "hi".', 'speak returns "hi", not None.'], 5),
 ('What is a class?', '# class Dormer: …', ['A blueprint for making objects', 'One real object', 'A kind of loop', 'A list of functions'], 0,
  ['A class is the plan; objects are made from it.', 'An object is made from a class.', 'Loops repeat; classes describe things.', 'A class can hold functions, but it is a blueprint.'], 0),
]
CARDS = [
 ('c1', 'blue', 24, 'What is the difference between a class and an object?', 'A class is the blueprint; an object is one thing made from it: `d = Dormer()`.'),
 ('c2', 'blue', 24, 'What does `__init__` do?', 'It sets up each new object, for example `self.colour = colour`.'),
 ('c3', 'blue', 24, 'What is `self`?', 'The object the method is working on.'),
 ('c4', 'blue', 24, 'Does changing `a.colour` change `b.colour`?', 'No. Each object keeps its own attributes.'),
]
GEN_STEPS = [3, 5, 7]
GEN_JS = r'''
      function () { var cls = pickOne(['Dog', 'Cat', 'Robot', 'Kite']), nm = pickOne(['Rex', 'Pip', 'Zed', 'Lulu']), o = pickOne(['d', 'x', 'pet']);
        return mk('What does this show?', 'class ' + cls + ':\n    def __init__(self, name):\n        self.name = name\n' + o + ' = ' + cls + '("' + nm + '")\nprint(' + o + '.name)', [[nm, '__init__ stored "' + nm + '" in self.name, and self was ' + o + '.'], ['name', o + '.name gives the value, not the word name.'], [cls, cls + ' is the class; ' + o + '.name is the name.'], ['An error', 'This is a correct class.']]); },
      function () { var a = ri(0, 5), k = ri(1, 4), m = ri(2, 3), calls = new Array(m + 1).join('c.add()\n');
        return mk('What does this show?', 'class Counter:\n    def __init__(self):\n        self.n = ' + a + '\n    def add(self):\n        self.n += ' + k + '\nc = Counter()\n' + calls + 'print(c.n)', [[a + m * k, 'It starts at ' + a + ', and add() puts on ' + k + ', ' + m + ' times.'], [a, 'add() changes self.n each time it is called.'], [a + k, 'add() is called ' + m + ' times, not once.'], [a + (m + 1) * k, 'Count the add() calls again: ' + m + '.']]); },
      function () { var x = ri(1, 5), y = ri(6, 9), z = ri(10, 20), w = pickOne(['a', 'b']);
        return mk('What does this show?', 'class Box:\n    def __init__(self, n):\n        self.n = n\na = Box(' + x + ')\nb = Box(' + y + ')\na.n = ' + z + '\nprint(' + w + '.n)', [[w === 'a' ? z : y, w === 'a' ? 'a.n was changed to ' + z + '.' : 'Each object keeps its own n, so b is still ' + y + '.'], [w === 'a' ? x : z, w === 'a' ? 'a started at ' + x + ', then a.n = ' + z + ' changed it.' : z + ' went into a, not b.'], [w === 'a' ? y : x, 'That belongs to the other box.'], ['An error', 'This works.']]); }
'''
