KEY, IDX = 'cls2', 25
META = dict(tag='Classes II · Third floor', title='Classes II: shared and own', topic='classes',
            lastBtn='Build the loft rooms', doneTitle='The loft has rooms!',
            doneText='You learned class variables that every object shares, instance variables each object keeps, methods that change things, __str__, and counting objects. The loft has a floor, stairs up, and rooms. Your room badges are in the house: change the shared name and every badge changes.')
QUIZ = [
 ('What does this show?', 'class Room:\n    house = "Nova"\na = Room()\nb = Room()\nRoom.house = "Mia"\nprint(b.house)', ['Mia', 'Nova', 'house', 'An error'], 0,
  ['house is shared, so changing Room.house changes it for every room.', 'Room.house was changed to Mia.', 'b.house gives the value.', 'This works.'], 2),
 ('What does this show?', 'class Room:\n    house = "Nova"\na = Room()\nb = Room()\na.house = "Tom"\nprint(b.house)', ['Nova', 'Tom', 'house', 'An error'], 0,
  ['a.house = "Tom" made a twin just for a. b still sees the shared Nova.', 'Only a got Tom.', 'b.house gives the value.', 'This works.'], 3),
 ('What does this show?', 'class Room:\n    count = 0\n    def __init__(self):\n        Room.count += 1\nRoom()\nRoom()\nprint(Room.count)', ['2', '0', '1', 'An error'], 0,
  ['Each new Room adds 1 to the shared count: 2.', '__init__ ran twice, so count went up.', 'Two rooms were made.', 'This works.'], 7),
 ('What does this show?', 'class Room:\n    def __init__(self, size):\n        self.size = size\n    def __str__(self):\n        return "Room " + str(self.size)\nprint(Room(4))', ['Room 4', '4', '<Room object>', 'An error'], 0,
  ['print uses __str__, which returns "Room 4".', '__str__ adds the word Room.', 'Because __str__ is written, print shows its text.', 'This works.'], 5),
 ('What does one underscore mean, like self._secret?', 'self._secret = "1234"', ['Private by habit: please do not touch', 'Python blocks anyone using it', 'It is a SyntaxError', 'It makes a class variable'], 0,
  ['One underscore is a polite sign. Python still allows it.', 'Python does not block it.', 'Underscores are allowed in names.', 'It is still an instance variable.'], 6),
 ('Which one is an instance variable?', 'class Room:\n    house = "Nova"\n    def __init__(self, size):\n        self.size = size', ['size', 'house', 'Room', '__init__'], 0,
  ['self.size belongs to each object.', 'house is a class variable, shared by all.', 'Room is the class.', '__init__ is a method.'], 1),
 ('What does this show?', 'class Room:\n    def __init__(self):\n        self.colour = "white"\n    def paint(self, c):\n        self.colour = c\nr = Room()\nr.paint("blue")\nprint(r.colour)', ['blue', 'white', 'c', 'An error'], 0,
  ['paint changed self.colour to blue.', 'paint() changed it after __init__.', 'c held "blue".', 'This works.'], 4),
]
CARDS = [
 ('c5', 'blue', 25, 'Class variable or instance variable?', 'Class variable: shared by every object (`Room.house`). Instance variable: each object\'s own (`self.size`).'),
 ('c6', 'blue', 25, 'What does `__str__` do?', 'It decides what `print(obj)` shows.'),
 ('c7', 'bugs', 25, 'What does `a.house = "Tom"` do when house is a class variable?', 'It makes a twin just for a, hiding the shared one. Others still see the shared value.'),
 ('c8', 'blue', 25, 'What does one underscore mean, like `_secret`?', 'Private by habit: please do not touch.'),
]
GEN_STEPS = [2, 3, 7]
GEN_JS = r'''
      function () { var c = pickOne(['Room', 'Shelf', 'Team']), a = pickOne(['Nova', 'Ali', 'Sam']), b = pickOne(['Mia', 'Zoe', 'Kai']), w = pickOne(['x', 'y']);
        return mk('What does this show?', 'class ' + c + ':\n    tag = "' + a + '"\nx = ' + c + '()\ny = ' + c + '()\n' + c + '.tag = "' + b + '"\nprint(' + w + '.tag)', [[b, 'tag is shared, so changing ' + c + '.tag changes it for every object.'], [a, c + '.tag was changed to ' + b + '.'], ['tag', w + '.tag gives the value.'], ['An error', 'This works.']]); },
      function () { var a = pickOne(['Nova', 'Ali']), t = pickOne(['Tom', 'Bea']), w = pickOne(['x', 'y']);
        return mk('What does this show?', 'class Room:\n    tag = "' + a + '"\nx = Room()\ny = Room()\nx.tag = "' + t + '"\nprint(' + w + '.tag)', [[w === 'x' ? t : a, w === 'x' ? 'x got its own tag, ' + t + ', hiding the shared one.' : 'Only x got ' + t + '; y still sees the shared ' + a + '.'], [w === 'x' ? a : t, w === 'x' ? 'x.tag = "' + t + '" gave x its own value.' : t + ' was given to x only.'], ['tag', w + '.tag gives the value.'], ['An error', 'This works.']]); },
      function () { var n = ri(2, 5), made = new Array(n + 1).join('Room()\n');
        return mk('What does this show?', 'class Room:\n    count = 0\n    def __init__(self):\n        Room.count += 1\n' + made + 'print(Room.count)', [[n, 'Each new Room adds 1 to the shared count: ' + n + '.'], [0, '__init__ ran ' + n + ' times, so count went up.'], [1, 'Count the Room() lines: ' + n + '.'], [n + 1, 'count starts at 0, not 1.']]); }
'''
