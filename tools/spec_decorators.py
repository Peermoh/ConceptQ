KEY, IDX = 'decorators', 37
META = dict(tag='Decorators · Rooftop garden', title='Decorators: wrap it up', topic='decorators',
            lastBtn='Switch on the lights', doneTitle='The garden lights are on!',
            doneText='You learned functions inside functions, wrappers, the @ sign, passing arguments on, functools.wraps, decorators with settings, stacking and lru_cache. String lights now run across the garden. The light switch box is there: add @lights and watch water() change.')
QUIZ = [
 ('What does this show?', 'def lights(f):\n    def wrap():\n        print("lights on")\n        f()\n    return wrap\n@lights\ndef water():\n    print("splash")\nwater()', ['lights on, then splash', 'splash, then lights on', 'splash', 'lights on'], 0,
  ['wrap prints lights on, then calls the real water().', 'wrap prints first, then calls f().', 'The @ wrapped water, so the lights come on too.', 'wrap also calls f(), which splashes.'], 2),
 ('What does @lights above def water mean?', '@lights\ndef water(): ...', ['water = lights(water)', 'water is deleted', 'lights = water(lights)', 'water runs straight away'], 0,
  ['The @ line is a short way to write water = lights(water).', 'water still exists, wrapped.', 'It is the other way round.', 'Nothing runs until you call water().'], 2),
 ('Why does wrap take *args and **kwargs?', 'def wrap(*args, **kwargs):\n    return f(*args, **kwargs)', ['So it can pass any arguments on to f', 'To make it faster', 'Because the @ sign needs it', 'To hide the arguments'], 0,
  ['The wrapped function might take arguments; wrap passes them all on.', 'It is about arguments, not speed.', '@ works without them for functions with no arguments.', 'They are passed on, not hidden.'], 3),
 ('What does functools.wraps keep?', '@functools.wraps(f)\ndef wrap(*args, **kwargs): ...', ["The wrapped function's name and docstring", 'A copy of every call', 'The arguments', 'Nothing: it is only for speed'], 0,
  ['Without it, water.__name__ would say wrap.', 'It does not record calls.', 'Arguments are passed by *args.', 'It is about keeping the name.'], 4),
 ('How many times does this show hi?', 'def repeat(n):\n    def deco(f):\n        def wrap():\n            for _ in range(n):\n                f()\n        return wrap\n    return deco\n@repeat(3)\ndef hello():\n    print("hi")\nhello()', ['3', '1', '0', '4'], 0,
  ['repeat(3) makes a decorator that calls hello 3 times.', 'The wrapper loops n times.', 'hello() runs the wrapper, which prints.', 'range(3) runs 3 times.'], 5),
 ('Which decorator wraps water first?', '@timed\n@lights\ndef water(): ...', ['@lights: the one nearest the function', '@timed: the one on top', 'Both at the same time', 'Neither: only one is allowed'], 0,
  ['The nearest decorator wraps first; @timed wraps the result.', 'The top one wraps last.', 'They wrap one after the other.', 'You can stack as many as you like.'], 6),
 ('What does @functools.lru_cache do?', '@functools.lru_cache\ndef forecast(day): ...', ['Remembers answers, so the same call is not worked out again', 'Makes the function run in the background', 'Deletes old forecasts', 'Logs every call'], 0,
  ['A repeated call is answered from memory.', 'It does not run things in the background.', 'It keeps answers, it does not delete data.', 'It caches, it does not log.'], 7),
]
CARDS = [
 ('dc1', 'mach', 37, 'What is a decorator?', 'A function that takes a function and returns a wrapped version of it.'),
 ('dc2', 'mach', 37, 'What does `@lights` above `def water` mean?', '`water = lights(water)`'),
 ('dc3', 'mach', 37, 'Why use `@functools.wraps(f)` in a decorator?', 'So the wrapped function keeps its own name and docstring.'),
 ('dc4', 'mach', 37, 'With two decorators stacked, which wraps first?', 'The one nearest the `def`.'),
]
GEN_STEPS = [2, 5]
GEN_JS = r'''
      function () { var k = ri(1, 5), a = ri(2, 6), op = pickOne(['+', '*']), base = op === '+' ? a * 2 : a * 2;
        var res = op === '+' ? a * 2 + k : a * 2 * k;
        return mk('What does this show?', 'def boost(f):\n    def wrap(x):\n        return f(x) ' + op + ' ' + k + '\n    return wrap\n@boost\ndef double(x):\n    return x * 2\nprint(double(' + a + '))', [[String(res), 'double gives ' + (a * 2) + ', then wrap ' + (op === '+' ? 'adds ' : 'multiplies by ') + k + '.'], [String(a * 2), 'The decorator changes the answer: it is wrapped.'], [String(op === '+' ? (a + k) * 2 : (a * k) + 2), 'wrap works on what f gives back, not on x.'], [String(op === '+' ? a + k : a * k), 'double still doubles first.']]); },
      function () { var n = ri(2, 5), w = pickOne(['hi', 'splash', 'beep']);
        return mk('How many times does this show ' + w + '?', 'def repeat(n):\n    def deco(f):\n        def wrap():\n            for _ in range(n):\n                f()\n        return wrap\n    return deco\n@repeat(' + n + ')\ndef hello():\n    print("' + w + '")\nhello()', [[String(n), 'repeat(' + n + ') makes a wrapper that calls the function ' + n + ' times.'], [String(n - 1), 'range(' + n + ') runs ' + n + ' times, from 0 to ' + (n - 1) + '.'], ['1', 'The wrapper loops: one call to hello() runs it ' + n + ' times.'], [String(n + 1), 'range does not include ' + n + ' itself.']]); }
'''
