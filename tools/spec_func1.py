KEY, IDX = 'func1', 15
META = dict(tag='Functions I · Second floor', title='Functions I: recipes you can reuse', topic='functions',
            lastBtn='Fit the kitchen', doneTitle='The kitchen is in!',
            doneText='You learned functions: def, parameters and return. A recipe written once and cooked many times. The upstairs kitchen has a sink and a stove. Your kettle is in the kitchen: call make_tea() to make it whistle.')
QUIZ = [
 ('What does this show?', 'def hello():\n    print("Hi")\nhello()\nhello()', ['Hi, then Hi', 'Hi', 'Nothing', 'An error'], 0,
  ['The function is called twice, so Hi shows twice.', 'hello() is called two times.', 'Calling hello() runs it, so something shows.', 'Defining and calling a function is allowed.']),
 ('What does this show?', 'def hello():\n    print("Hi")', ['Nothing', 'Hi', 'hello', 'An error'], 0,
  ['def only writes the recipe. Nothing runs until you call hello().', 'Hi only shows when hello() is called.', 'def never prints the name.', 'This is a correct function. It just is not called.']),
 ('What does this show?', 'def double(n):\n    return n * 2\nprint(double(4))', ['8', '4', '42', 'None'], 0,
  ['double(4) returns 4 * 2 = 8.', 'return gives back n * 2, not n.', 'n * 2 multiplies, it does not join digits.', 'The function returns a value, so it is not None.']),
 ('What is x?', 'def shout(w):\n    print(w)\nx = shout("hi")', ['None', 'hi', '"hi"', 'An error'], 0,
  ['shout prints, but never returns anything, so x is None.', 'hi is shown on screen, but it is not returned.', 'print does not give the value back.', 'The code works, x is just None.']),
 ('What does this show?', 'def area(w, h):\n    return w * h\nprint(area(2, 5))', ['10', '7', '25', '2 5'], 0,
  ['w is 2 and h is 5, so 2 * 5 = 10.', 'That would be w + h.', 'That would be 5 * 5.', 'The function returns one number.']),
 ('What does this show?', 'def add(a, b):\n    return a + b\nprint(add("1", "2"))', ['12', '3', '"12"', 'An error'], 0,
  ['These are strings, so + glues them: 12.', 'Quotes make them text, and text is glued, not added.', 'print shows the text without quotes.', 'Functions work with any values.']),
 ('What happens?', 'def hi(name):\n    print("Hi", name)\nhi()', ['A TypeError', 'Hi', 'Hi None', 'Nothing'], 0,
  ['hi needs one argument, name, but got none: TypeError.', 'Without a name, Python stops with an error.', 'Python does not fill in None by itself.', 'Python stops with an error.']),
]
CARDS = [
 ('f1', 'recipes', 15, 'How do you make a function called `hello`?', '`def hello():` then the indented steps. Call it with `hello()`.'),
 ('f2', 'recipes', 15, 'What does `return` do?', 'Hands a value back to whoever called the function.'),
 ('f3', 'bugs', 15, 'A function only prints. What does it return?', 'None.'),
 ('f4', 'recipes', 15, 'What are parameters?', 'The names in the brackets of `def`: the ingredients you hand in.'),
]
GEN_JS = r'''
      function () { var k = ri(2, 5), n = ri(2, 9);
        return mk('What does this show?', 'def times(n):\n    return n * ' + k + '\nprint(times(' + n + '))', [[n * k, 'times(' + n + ') returns ' + n + ' * ' + k + ' = ' + (n * k) + '.'], [n, 'return gives back n * ' + k + ', not n.'], ['' + n + k, 'n * ' + k + ' multiplies, it does not join digits.'], ['None', 'The function returns a value.']]); },
      function () { var w = ri(2, 6), h = ri(2, 6);
        return mk('What does this show?', 'def area(w, h):\n    return w * h\nprint(area(' + w + ', ' + h + '))', [[w * h, 'w is ' + w + ' and h is ' + h + ': ' + w + ' * ' + h + ' = ' + (w * h) + '.'], [w + h, 'That would be w + h.'], [w === h ? w * h + 1 : w * w, 'Check the order: w is ' + w + ', h is ' + h + '.'], [w + ' ' + h, 'The function returns one number.']]); },
      function () { var c = ri(2, 3), word = pickOne(['Hi', 'Yo', 'Hey']);
        var calls = new Array(c + 1).join('greet()\n');
        return mk('What does this show?', 'def greet():\n    print("' + word + '")\n' + calls.trim(), [[new Array(c + 1).join(word + ' ').trim(), 'greet() is called ' + c + ' times, so ' + word + ' shows ' + c + ' times.'], [word, 'Count the calls: there are ' + c + '.'], ['Nothing', 'Calling greet() runs it.'], ['An error', 'Defining and calling a function is allowed.']]); },
      function () { var a = ri(1, 9), b = ri(1, 9), txt = pickOne([true, false]);
        var arg = txt ? '"' + a + '", "' + b + '"' : a + ', ' + b;
        return mk('What does this show?', 'def add(a, b):\n    return a + b\nprint(add(' + arg + '))', [[txt ? '' + a + b : a + b, txt ? 'They are text, so + glues them.' : 'They are numbers, so + adds them.'], [txt ? a + b : '' + a + b, txt ? 'Quotes make them text, and text is glued.' : 'No quotes, so these are numbers and + adds them.'], ['None', 'The function returns a + b.'], ['An error', 'Functions work with any values that + can handle.']]); }
'''
