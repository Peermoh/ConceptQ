KEY, IDX = 'logging', 40
META = dict(tag='Logging and timing · Rooftop garden', title='Logging and timing: measure, do not guess', topic='logging and timing',
            lastBtn='Fit the smart meter', doneTitle='The smart meter is on!',
            doneText='You learned logging levels, basicConfig, a logger per module, logging to a file, timeit, comparing two ways, and the profiler. A smart meter now sits on the garden shed. It is in your garden: run the sprinkler and read its log.')
QUIZ = [
 ('What does this show on the screen?', 'import logging\nlogging.basicConfig(level=logging.WARNING)\nlogging.info("watering")', ['Nothing', 'INFO:root:watering', 'watering', 'An error'], 0,
  ['info is below WARNING, so it is hidden.', 'Only WARNING and above are shown.', 'info is hidden at this level.', 'Hidden messages are not errors.'], 2),
 ('The water tank is low but still works. Which level?', '# tank low', ['warning', 'debug', 'error', 'critical'], 0,
  ['Something looks wrong, but it still works: warning.', 'debug is for tiny details.', 'error is for something that failed.', 'critical is for the whole program failing.'], 1),
 ('Which list goes from the lowest level to the highest?', '# five levels', ['debug, info, warning, error, critical', 'info, debug, warning, critical, error', 'critical, error, warning, info, debug', 'debug, warning, info, error, critical'], 0,
  ['From tiny details up to the whole program failing.', 'debug is the lowest.', 'That is highest to lowest.', 'info comes before warning.'], 1),
 ('Why use logging.getLogger(__name__)?', 'log = logging.getLogger(__name__)', ['Each log line says which module it came from', 'It makes logs faster', 'It hides errors', 'It is needed to print'], 0,
  ['__name__ is the module name, so you can tell where messages came from.', 'It is about naming, not speed.', 'It shows where errors came from.', 'print does not need it.'], 3),
 ('What does timeit give back?', 'timeit("sum(xs)", number=1000)', ['The total seconds for 1000 runs', 'The answer of sum(xs)', 'The seconds for one run', 'How many times it can run'], 0,
  ['It runs the code 1000 times and gives the total time.', 'It times the code, it does not give its answer.', 'It is the total for all 1000 runs.', 'You choose the number of runs.'], 5),
 ('Which is usually faster for "is x in it?"', 'big_list = list(range(100000))\nbig_set = set(big_list)', ['x in big_set', 'x in big_list', 'They are always the same', 'Neither works'], 0,
  ['A set jumps straight to x; a list checks one by one.', 'A list checks every item until it finds x.', 'Measure it: the set wins easily.', 'in works on both.'], 6),
 ('What is cProfile for?', 'python -m cProfile garden.py', ['Finding which function takes the time', 'Checking for spelling mistakes', 'Making the code faster by itself', 'Writing a log file'], 0,
  ['It lists each function and how long it took.', 'That is a different tool.', 'It measures; you do the fixing.', 'That is logging.'], 7),
]
CARDS = [
 ('lg1', 'world', 40, 'What are the five logging levels, lowest first?', 'debug, info, warning, error, critical'),
 ('lg2', 'world', 40, 'What does `basicConfig(level=logging.INFO)` hide?', 'debug messages. info and above are shown.'),
 ('lg3', 'world', 40, 'How do you measure how fast some code is?', '`timeit("code", number=1000)`: total seconds for 1000 runs.'),
 ('lg4', 'world', 40, 'Why is `x in a_set` faster than `x in a_list`?', 'A set jumps straight to x; a list checks every item one by one.'),
]
GEN_STEPS = [2, 1]
GEN_JS = r'''
      function () { var LV = ['DEBUG', 'INFO', 'WARNING', 'ERROR'], lv = ri(0, 3), msgs = [['debug', 'leaf'], ['info', 'water'], ['warning', 'low'], ['error', 'broken']];
        var pick = shuffled(msgs).slice(0, 3).sort(function (a, b) { return msgs.indexOf(a) - msgs.indexOf(b); }), shown = pick.filter(function (m) { return msgs.indexOf(m) >= lv; }).map(function (m) { return m[1]; });
        if (!shown.length) { lv = 0; shown = pick.map(function (m) { return m[1]; }); }
        var all = pick.map(function (m) { return m[1]; }), code = 'import logging, sys\nlogging.basicConfig(level=logging.' + LV[lv] + ', stream=sys.stdout, format="%(message)s")\n' + pick.map(function (m) { return 'logging.' + m[0] + '("' + m[1] + '")'; }).join('\n');
        var wrong1 = all.join(' ') === shown.join(' ') ? all.slice(1).join(' ') || 'Nothing' : all.join(' '), wrong2 = shown.length > 1 ? shown.slice(-1).join(' ') : 'Nothing';
        if (wrong2 === wrong1) wrong2 = shown.slice(0, 1).join(' ') + ' ' + all[0]; if (wrong2 === shown.join(' ')) wrong2 = 'Everything, twice';
        return mk('What does this show?', code, [[shown.join(' '), 'Only ' + LV[lv] + ' and the levels above it are shown.'], [wrong1, 'Some messages are below ' + LV[lv] + ', so they are hidden.'], [wrong2, 'Every message at ' + LV[lv] + ' or above is shown.'], ['An error', 'Logging below the level is just hidden.']]); },
      function () { var L = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], a = ri(0, 4), b = ri(0, 4); if (a === b) b = (a + 2) % 5;
        return mk('What does this show?', 'import logging\nprint(logging.' + L[a] + ' > logging.' + L[b] + ')', [[a > b ? 'True' : 'False', L[a] + (a > b ? ' is higher than ' : ' is lower than ') + L[b] + '.'], [a > b ? 'False' : 'True', 'The order is DEBUG, INFO, WARNING, ERROR, CRITICAL.'], ['An error', 'Levels are numbers, so they can be compared.'], [L[Math.max(a, b)], '> gives True or False.']]); }
'''
