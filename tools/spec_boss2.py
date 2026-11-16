KEY, IDX = 'boss2', 20
META = dict(tag='Boss · Second floor', title='Boss: the garden party', topic='the floor-2 boss',
            lastBtn='Throw the party', doneTitle='Party on the balcony!',
            doneText='You beat the floor-2 boss: files, sets, dictionaries, functions, modules and try / except, all working together. The balcony is built and the party lights are on. You finished the second floor!')
QUIZ = [
 ('What does this show?', 'names = ["Mia", "Ali", "Mia"]\nprint(len(set(names)))', ['2', '3', '1', 'An error'], 0,
  ['set removes the repeated Mia: 2 guests.', 'That counts Mia twice. A set keeps her once.', 'Ali and Mia are different names.', 'set() works on any list.']),
 ('What does this show?', 'food = {"Mia": "pizza"}\nprint(food.get("Sam", "snacks"))', ['snacks', 'pizza', 'None', 'A KeyError'], 0,
  ['Sam is not a key, so get gives the default: snacks.', 'pizza belongs to Mia.', 'We gave a default, so it is not None.', 'get never gives a KeyError.']),
 ('What is chairs if someone types "lots"?', 'try:\n    chairs = int("lots")\nexcept ValueError:\n    chairs = 10', ['10', '"lots"', '0', 'An error'], 0,
  ['int("lots") fails, so except sets chairs to 10.', 'int could not turn "lots" into a number.', 'except sets it to 10, not 0.', 'except catches the ValueError.']),
 ('What does seat() give back?', 'import random\ndef seat(people):\n    people = list(people)\n    random.shuffle(people)\n    return people', ['The guests, in a random order', 'One random guest', 'The guests, sorted', 'None'], 0,
  ['shuffle mixes the list and return gives it back.', 'That would be random.choice.', 'shuffle mixes, it does not sort.', 'The function returns the list.']),
 ('What does this show?', 'guests = ["Mia", "Ali"]\nfor g in guests:\n    print("Hi", g)', ['Hi Mia, then Hi Ali', 'Hi Mia', 'Hi guests', 'Hi Mia Ali'], 0,
  ['The loop says hi to each guest in turn.', 'The loop keeps going to Ali too.', 'g is one guest at a time.', 'Each print is a new line.']),
]
CARDS = [
 ('b5', 'coll', 20, 'How do you count the different names in a list?', '`len(set(names))`'),
 ('b6', 'bugs', 20, 'How do you ask for a number safely?', 'Wrap `int(input())` in try, with `except ValueError:`'),
]
GEN_JS = r'''
      function () { var pool = shuffled(['Mia', 'Ali', 'Sam', 'Zoe']).slice(0, ri(2, 3)), names = shuffled(pool.concat([pool[0]]).concat(ri(0, 1) ? [pool[1]] : []));
        return mk('What does this show?', 'names = ' + pyList(names).replace(/'/g, '"') + '\nprint(len(set(names)))', [[pool.length, 'set removes the repeats: ' + pool.length + ' different guests.'], [names.length, 'That counts the repeats too.'], [pool.length - 1, 'Count the different names again.'], ['An error', 'set() works on any list.']]); },
      function () { var who = pickOne(['Mia', 'Ali']), other = who === 'Mia' ? 'Ali' : 'Mia', d = pickOne(['snacks', 'juice', 'fruit']), ask = pickOne([who, 'Sam']);
        return mk('What does this show?', 'food = {"' + who + '": "pizza", "' + other + '": "cake"}\nprint(food.get("' + ask + '", "' + d + '"))', [[ask === who ? 'pizza' : d, ask === who ? who + ' is a key, so get gives pizza.' : 'Sam is not a key, so get gives the default: ' + d + '.'], [ask === who ? d : 'pizza', ask === who ? 'The default is only used when the key is missing.' : 'pizza belongs to ' + who + '.'], ['cake', 'cake belongs to ' + other + '.'], ['A KeyError', 'get never gives a KeyError.']]); }
'''
