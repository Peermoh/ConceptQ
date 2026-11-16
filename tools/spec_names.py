KEY, IDX = 'names', 26
META = dict(tag='Namespaces · Third floor', title='Namespaces: look inside', topic='namespaces',
            lastBtn='Wire the loft', doneTitle='The loft is wired!',
            doneText='You learned namespaces: where Python looks for a name, an object\'s __dict__, hasattr, getattr and setattr, isinstance, name mangling and dir(). The loft is wired, with the cables hidden inside the walls. Your X-ray scanner is in the house: point it at a wall to see its __dict__.')
QUIZ = [
 ('What does this show?', 'class Lamp:\n    pass\nl = Lamp()\nl.on = True\nprint(l.__dict__)', ["{'on': True}", '{}', 'True', 'An error'], 0,
  ['__dict__ holds the object\'s own attributes: on is True.', 'l.on = True added an attribute.', '__dict__ shows names and values together.', 'Every object has __dict__.'], 2),
 ('What does this show?', 'class Lamp:\n    pass\nprint(hasattr(Lamp(), "fly"))', ['False', 'True', 'fly', 'An error'], 0,
  ['The lamp has no attribute called fly.', 'Nothing gave the lamp a fly attribute.', 'hasattr gives True or False.', 'hasattr never raises an error for a missing name.'], 4),
 ('What does this show?', 'class Lamp:\n    pass\nprint(isinstance(Lamp(), Lamp))', ['True', 'False', 'Lamp', 'An error'], 0,
  ['A Lamp() object is an instance of Lamp.', 'It was made from Lamp.', 'isinstance gives True or False.', 'This works.'], 6),
 ('What does this show?', 'class Lamp:\n    pass\nprint(type(Lamp()).__name__)', ['Lamp', 'type', 'lamp', 'object'], 0,
  ['type() gives the class, and __name__ is its name: Lamp.', 'type() gives the class, not the word type.', 'Names keep their capital letters.', 'Its class is Lamp, more exactly than object.'], 6),
 ('Where does Python look first for a name?', '# L, E, G, B', ['Local', 'Global', 'Built-in', 'Enclosing'], 0,
  ['Local comes first: names inside the function.', 'Global comes third.', 'Built-ins come last.', 'Enclosing comes second.'], 1),
 ('What does this show?', 'class Lamp:\n    pass\nl = Lamp()\nsetattr(l, "on", True)\nprint(getattr(l, "on"))', ['True', 'on', 'None', 'An error'], 0,
  ['setattr stored True under "on", and getattr reads it back.', 'getattr gives the value, not the name.', 'setattr gave it a value.', 'This works.'], 5),
 ('What happens to self.__code inside class Lamp?', 'self.__code = 42', ['It is stored as _Lamp__code', 'It is deleted', 'It becomes public', 'It is a SyntaxError'], 0,
  ['Two leading underscores make Python mangle the name.', 'It is kept, just under a different name.', 'It becomes harder to reach, not easier.', 'Underscores are allowed.'], 7),
]
CARDS = [
 ('n1', 'blue', 26, 'What is `obj.__dict__`?', 'A dictionary of the object\'s own attributes.'),
 ('n2', 'blue', 26, 'What do `hasattr`, `getattr` and `setattr` do?', 'Check, read and set an attribute by its name in quotes.'),
 ('n3', 'blue', 26, 'In what order does Python look for a name?', 'LEGB: Local, Enclosing, Global, Built-in.'),
 ('n4', 'blue', 26, 'What happens to `self.__code`?', 'Name mangling: it is stored as `_Lamp__code`.'),
]
GEN_STEPS = [4, 5, 2]
GEN_JS = r'''
      function () { var set = pickOne(['on', 'colour', 'size']), ask = pickOne(['on', 'colour', 'size', 'fly']), r = set === ask;
        return mk('What does this show?', 'class Lamp:\n    pass\nl = Lamp()\nl.' + set + ' = 1\nprint(hasattr(l, "' + ask + '"))', [[r ? 'True' : 'False', r ? 'l.' + set + ' was set, so the lamp has it.' : 'Only ' + set + ' was set, not ' + ask + '.'], [r ? 'False' : 'True', 'Look at which attribute was set.'], [ask, 'hasattr gives True or False.'], ['An error', 'hasattr never raises an error for a missing name.']]); },
      function () { var has = pickOne([true, false]), v = pickOne(['red', 'blue', 'gold']), d = pickOne(['none', 'white']);
        return mk('What does this show?', 'class Lamp:\n    pass\nl = Lamp()\n' + (has ? 'l.colour = "' + v + '"\n' : '') + 'print(getattr(l, "colour", "' + d + '"))', [[has ? v : d, has ? 'colour is there, so getattr gives it.' : 'colour is missing, so getattr gives the default, ' + d + '.'], [has ? d : v, has ? 'The default is only used when the attribute is missing.' : 'colour was never set.'], ['colour', 'getattr gives the value, not the name.'], ['An error', 'With a default, a missing attribute is not an error.']]); },
      function () { var names = shuffled(['on', 'size', 'colour', 'room']).slice(0, ri(1, 4));
        return mk('What does this show?', 'class Lamp:\n    pass\nl = Lamp()\n' + names.map(function (n, i) { return 'l.' + n + ' = ' + i; }).join('\n') + '\nprint(len(l.__dict__))', [[names.length, names.length + ' attributes were set, and __dict__ holds them all.'], [names.length + 1, 'Count the attributes that were set.'], [0, 'Setting l.something adds it to __dict__.'], [names.length * 2, 'len counts the attributes, not names and values separately.']]); }
'''
