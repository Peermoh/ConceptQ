KEY, IDX = 'dicts', 13
META = dict(tag='Dictionaries · Second floor', title='Dictionaries: look things up by name', topic='dictionaries',
            lastBtn='Hang the doors', doneTitle='The upstairs doors are in!',
            doneText='You learned dictionaries: values stored under names, looked up by their key. Every upstairs door now has a name plate. Your key rack is in the house: every hook has a label.')
QUIZ = [
 ('What does this show?', 'pets = {"cat": 2, "dog": 1}\nprint(pets["cat"])', ['2', '1', 'cat', 'An error'], 0,
  ['The key "cat" holds the value 2.', '1 is stored under "dog".', 'The key finds the value. It does not show the key.', '"cat" is a key in the dictionary.']),
 ('What happens?', 'pets = {"cat": 2}\nprint(pets["owl"])', ['A KeyError', '0', 'None', 'owl'], 0,
  ['"owl" is not a key, so Python stops with a KeyError.', 'Python does not make up a 0 for a missing key.', 'Square brackets do not give None. .get() would.', 'A missing key is an error, not the name.']),
 ('What does this show?', 'pets = {"cat": 2}\nprint(pets.get("owl", 0))', ['0', 'A KeyError', 'None', 'owl'], 0,
  ['get gives the default, 0, when the key is missing.', 'get is the safe way: it never gives a KeyError.', 'We gave a default of 0, so that is what comes back.', 'get gives a value, not the key.']),
 ('What does this show?', 'pets = {"cat": 2}\npets["cat"] = 5\nprint(pets)', ["{'cat': 5}", "{'cat': 2}", "{'cat': 2, 'cat': 5}", 'An error'], 0,
  ['cat was already a key, so its value is changed to 5.', 'The new value replaced the old one.', 'A dictionary never has the same key twice.', 'Changing a value is allowed.']),
 ('What does this show?', 'd = {"a": 1, "b": 2}\nprint("b" in d, 2 in d)', ['True False', 'True True', 'False True', 'False False'], 0,
  ['in checks the keys: "b" is a key, 2 is only a value.', '2 is a value, and in only looks at keys.', '"b" is a key, so that part is True.', '"b" is a key, so the first part is True.']),
 ('What does this show?', 'rooms = {"bed": ["bunk", "lamp"]}\nprint(rooms["bed"][0])', ['bunk', 'lamp', "['bunk', 'lamp']", 'An error'], 0,
  ['rooms["bed"] is the list, and [0] is its first item: bunk.', 'lamp is at position 1.', 'The [0] picks one item from the list.', 'This is allowed: a value can be a list.']),
 ('What does this show?', 'd = {"a": 1, "b": 2, "c": 3}\nprint(len(d))', ['3', '6', '2', '9'], 0,
  ['len counts the keys: a, b and c.', 'len counts keys, not keys and values together.', 'Count the keys again: a, b, c.', 'len does not add up the values.']),
]
CARDS = [
 ('d1', 'coll', 13, 'What is a dictionary?', 'Values stored under keys: `{"cat": 2}`. Look one up with `pets["cat"]`.'),
 ('d2', 'bugs', 13, 'What happens with a key that is not there, like `pets["owl"]`?', 'A KeyError. Use `pets.get("owl", 0)` to be safe.'),
 ('d3', 'coll', 13, 'Does `in` check the keys or the values of a dictionary?', 'The keys.'),
 ('d4', 'coll', 13, 'How do you loop through every key and value?', '`for key, value in d.items():`'),
]
GEN_JS = r'''
      function () { var ks = shuffled(['cat', 'dog', 'owl', 'fox', 'bee']).slice(0, 3), vs = [ri(1, 5), ri(6, 9), ri(10, 15)], i = ri(0, 2);
        var code = 'pets = {' + ks.map(function (k, j) { return '"' + k + '": ' + vs[j]; }).join(', ') + '}\nprint(pets["' + ks[i] + '"])';
        return mk('What does this show?', code, [[vs[i], 'The key "' + ks[i] + '" holds ' + vs[i] + '.'], [vs[(i + 1) % 3], 'That is stored under "' + ks[(i + 1) % 3] + '".'], [ks[i], 'The key finds the value. It does not show the key.'], ['An error', '"' + ks[i] + '" is a key in the dictionary.']]); },
      function () { var k = pickOne(['cat', 'dog']), miss = pickOne(['owl', 'fox']), d = ri(0, 9), v = ri(10, 20);
        return mk('What does this show?', 'pets = {"' + k + '": ' + v + '}\nprint(pets.get("' + miss + '", ' + d + '))', [[d, '"' + miss + '" is missing, so get gives the default, ' + d + '.'], [v, 'That is the value of "' + k + '", a different key.'], ['A KeyError', 'get never gives a KeyError. Square brackets would.'], ['None', 'We gave a default of ' + d + ', so that comes back.']]); },
      function () { var k = pickOne(['cat', 'dog']), a = ri(1, 9), b = ri(10, 20);
        return mk('What does this show?', 'pets = {"' + k + '": ' + a + '}\npets["' + k + '"] = ' + b + '\nprint(pets["' + k + '"])', [[b, '"' + k + '" was already a key, so its value changed to ' + b + '.'], [a, 'The new value replaced ' + a + '.'], [a + b, 'The value is replaced, not added to.'], ['An error', 'Changing a value is allowed.']]); },
      function () { var ks = shuffled(['a', 'b', 'c', 'd']).slice(0, ri(2, 4)), vs = ks.map(function () { return ri(1, 9); }), s = vs.reduce(function (p, q) { return p + q; }, 0);
        var code = 'd = {' + ks.map(function (k, j) { return '"' + k + '": ' + vs[j]; }).join(', ') + '}\nprint(len(d))';
        return mk('What does this show?', code, [[ks.length, 'len counts the keys: ' + ks.join(', ') + '.'], [ks.length * 2, 'len counts keys, not keys and values together.'], [s, 'len does not add up the values.'], [ks.length - 1, 'Count the keys again.']]); },
      function () { var ks = shuffled(['x', 'y', 'z']).slice(0, 2), vs = [ri(1, 9), ri(10, 19)], probe = pickOne([ks[1], String(vs[1])]), isKey = probe === ks[1];
        var code = 'd = {"' + ks[0] + '": ' + vs[0] + ', "' + ks[1] + '": ' + vs[1] + '}\nprint(' + (isKey ? '"' + probe + '"' : probe) + ' in d)';
        return mk('What does this show?', code, [[isKey ? 'True' : 'False', isKey ? '"' + probe + '" is a key.' : probe + ' is a value, and in only checks keys.'], [isKey ? 'False' : 'True', 'in checks the keys of a dictionary, not the values.'], [isKey ? vs[1] : ks[1], 'in gives True or False.'], ['An error', 'in works on dictionaries.']]); }
'''
