  // ================= fresh quizzes =================
  // Every time a quiz starts it is built again: some questions are made with new values, the hand-written ones fill
  // the rest, and the order of the questions and of their answers is shuffled. A replay is never the same quiz twice.
  function ri(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pickOne(a) { return a[Math.floor(Math.random() * a.length)]; }
  function shuffled(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function pyList(a) { return '[' + a.map(function (x) { return typeof x === 'string' ? "'" + x + "'" : String(x); }).join(', ') + ']'; }
  function pyStr(x) { return typeof x === 'string' ? '"' + x + '"' : String(x); }
  var HL_FN = { print: 1, input: 1, int: 1, float: 1, len: 1, range: 1, str: 1, round: 1, type: 1 };
  var HL_KW = { 'if': 1, 'elif': 1, 'else': 1, 'for': 1, 'in': 1, 'while': 1, 'break': 1, 'continue': 1, 'and': 1, 'or': 1, 'not': 1, 'True': 1, 'False': 1, 'del': 1 };
  function hlCode(code) {
    function esc(t) { return t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
    return code.split('\n').map(function (line) {
      return line.split(/("(?:[^"\\]|\\.)*"|#.*$)/).map(function (p) {
        if (!p) return '';
        if (p[0] === '"') return '<span class="s">' + esc(p) + '</span>';
        if (p[0] === '#') return '<span class="c">' + esc(p) + '</span>';
        return esc(p).replace(/[A-Za-z_]+/g, function (w) { return HL_FN[w] ? '<span class="f">' + w + '</span>' : HL_KW[w] ? '<span class="o">' + w + '</span>' : w; });
      }).join('');
    }).join('\n');
  }
  // q(text, code, [[option, why], ...]) — the first pair is the right answer; it is shuffled later
  function mk(text, code, pairs) {
    var seen = {};
    for (var i = 0; i < pairs.length; i++) { var k = String(pairs[i][0]); if (seen[k]) return null; seen[k] = 1; } // two equal options: try new values
    return { text: text, code: hlCode(code), options: pairs.map(function (p) { return String(p[0]); }), answer: 0, why: pairs.map(function (p) { return p[1]; }) };
  }
  var WORDS = ['tiger', 'robot', 'mango', 'pixel', 'castle', 'planet', 'dragon', 'lemon'];
  var THINGS = ['oak', 'pine', 'ash', 'elm', 'fir', 'yew', 'birch', 'maple'];
  var PHRASES = [['Open the door', 'Walk inside'], ['Wake up', 'Brush teeth'], ['Pack the bag', 'Catch the bus'], ['Mix the dough', 'Bake the cake']];
  var GEN = {
    hello: [
      function () { var a = ri(2, 9), b = ri(2, 9);
        return mk('What does this show on screen?', 'print(' + a + ' + ' + b + ')', [[a + b, 'Python works out the sum first, then shows the answer: ' + (a + b) + '.'], [a + ' + ' + b, 'Without quotes, Python does the maths instead of showing the sum.'], ['' + a + b, 'These are numbers, so + adds them. It only glues text.'], ['"' + (a + b) + '"', 'print shows the value without quote marks.']]); },
      function () { var w = pickOne(['I am', 'Score:', 'Level', 'Age']), n = ri(3, 99);
        return mk('What does this show on screen?', 'print("' + w + '", ' + n + ')', [[w + ' ' + n, 'A comma shows both parts with a space between them.'], [w + n, 'A comma adds a space between the parts.'], ['"' + w + '", ' + n, 'print shows the values, not the code with quotes and commas.'], ['An error', 'Mixing text and a number with a comma is allowed.']]); },
      function () { var ph = pickOne(PHRASES);
        return mk('What shows on the screen first?', 'print("' + ph[0] + '")\nprint("' + ph[1] + '")', [[ph[0], 'Python reads from top to bottom, so the first line runs first.'], [ph[1], 'That is on the second line, so it comes after.'], ['Both at the same time', 'Python runs one line at a time, never two at once.'], ['Python picks one at random', 'Python always follows the same order: top to bottom.']]); }
    ],
    vars: [
      function () { var a = ri(2, 9), b = ri(10, 30), n = pickOne(['pens', 'coins', 'apples', 'stars']);
        return mk('What does this show?', n + ' = ' + a + '\n' + n + ' = ' + b + '\nprint(' + n + ')', [[b, 'The second line puts ' + b + ' in the box, and the ' + a + ' is gone.'], [a, 'A box holds one value. The new value replaced ' + a + '.'], [a + b, 'The second line replaces the value. It does not add to it.'], [n, 'Without quotes, ' + n + ' is a box, so print shows what is inside.']]); },
      function () { var a = ri(3, 20), b = ri(2, 9), n = pickOne(['score', 'points', 'level']);
        return mk('What is ' + n + ' now?', n + ' = ' + a + '\n' + n + ' += ' + b, [[a + b, n + ' += ' + b + ' means ' + n + ' = ' + n + ' + ' + b + ', so ' + a + ' + ' + b + ' = ' + (a + b) + '.'], [b, '+= adds to what is already in the box.'], ['' + a + b, 'These are numbers, so they are added, not glued.'], [a, 'The box changed: += added ' + b + ' to it.']]); },
      function () { var p = ri(1, 9), q = ri(10, 19);
        return mk('What does this show?', 'a, b = ' + p + ', ' + q + '\na, b = b, a\nprint(a)', [[q, 'The swap gives a the value b had: ' + q + '.'], [p, 'That was a before the swap. a, b = b, a swaps them.'], ['(' + q + ', ' + p + ')', 'print(a) shows just a, not both boxes.'], ['An error', 'Swapping in one line is allowed in Python.']]); }
    ],
    nums: [
      function () { var b = ri(3, 6), a = b * ri(2, 6) + ri(1, b - 1);
        return mk('What does this give?', 'print(' + a + ' % ' + b + ')', [[a % b, b + ' fits into ' + a + ' ' + Math.floor(a / b) + ' times, and ' + (a % b) + ' is left over.'], [Math.floor(a / b), 'That is how many times ' + b + ' fits. % gives what is left over.'], [0, 'There is a leftover: ' + a + ' is not a multiple of ' + b + '.'], [b, '% gives the leftover, which is always smaller than ' + b + '.']]); },
      function () { var b = pickOne([2, 4, 5]), a = b * ri(2, 9) + ri(1, b - 1), exact = a / b;
        return mk('What does this give?', 'print(' + a + ' // ' + b + ')', [[Math.floor(exact), '// keeps only the whole number: ' + Math.floor(exact) + '.'], [exact, 'That is one slash. Two slashes drop the decimal part.'], [Math.floor(exact) + 1, '// always rounds down, never up.'], [a % b, 'That is the leftover, from %.']]); },
      function () { var a = ri(2, 9), b = ri(2, 6), c = ri(2, 5);
        return mk('What does this give?', 'print(' + a + ' + ' + b + ' * ' + c + ')', [[a + b * c, 'Times first: ' + b + ' * ' + c + ' = ' + (b * c) + ', then + ' + a + ' = ' + (a + b * c) + '.'], [(a + b) * c, 'That would be (' + a + ' + ' + b + ') * ' + c + '. Times happens first.'], [a * b + c, 'The times is between ' + b + ' and ' + c + ', not ' + a + ' and ' + b + '.'], [a + b + c, '* means times, not plus.']]); },
      function () { var a = ri(2, 5), b = ri(2, 3);
        return mk('What does this give?', 'print(' + a + ' ** ' + b + ')', [[Math.pow(a, b), a + ' ** ' + b + ' is ' + a + ' multiplied by itself ' + b + ' times: ' + Math.pow(a, b) + '.'], [a * b, 'That would be ' + a + ' * ' + b + '. Two stars mean power.'], ['' + a + b, 'Two stars do maths, they do not join digits.'], [a + b, 'That would be ' + a + ' + ' + b + '.']]); },
      function () { var a = ri(2, 6), b = ri(a + 2, 12);
        return mk('What does this give?', 'print(' + a + ' - ' + b + ')', [[a - b, a + ' take away ' + b + ' goes below zero: ' + (a - b) + '.'], [b - a, 'That is ' + b + ' - ' + a + '. Here we take ' + b + ' away from ' + a + '.'], [a + b, 'That would be ' + a + ' + ' + b + '.'], ['An error', 'Negative numbers are fine in Python.']]); }
    ],
    strings: [
      function () { var w = pickOne(WORDS), i = ri(0, w.length - 2);
        return mk('What does this give?', 'print("' + w + '"[' + i + '])', [[w[i], 'Counting starts at 0, so [' + i + '] is ' + w[i] + '.'], [w[i + 1], 'That is position ' + (i + 1) + '. Counting starts at 0.'], [i, '[' + i + '] picks a letter, it does not show the number.'], [i > 0 ? w[i - 1] : 'An error', i > 0 ? 'That is position ' + (i - 1) + '.' : 'Position 0 exists: it is the first letter.']]); },
      function () { var w = pickOne(WORDS);
        return mk('What does this give?', 'word = "' + w + '"\nprint(word[-1])', [[w[w.length - 1], '-1 means the last letter: ' + w[w.length - 1] + '.'], [w[0], 'That is [0], the first letter. -1 counts from the end.'], [-1, '[-1] picks a letter, it does not show the number.'], ['An error', 'Negative positions are allowed: they count from the end.']]); },
      function () { var w = pickOne(WORDS);
        return mk('What does this give?', 'print(len("' + w + '"))', [[w.length, 'len counts the letters: ' + w.split('').join(' · ') + '.'], [w.length - 1, 'Count again from 1: len counts every letter.'], [w.length + 2, 'The quotes are not counted, only the letters.'], [w, 'len gives a number, not the word.']]); },
      function () { var w = pickOne(WORDS), k = ri(2, 4);
        return mk('What does this give?', 'print("' + w + '"[0:' + k + '])', [[w.slice(0, k), 'From 0, stopping before ' + k + ': ' + w.slice(0, k) + '.'], [w.slice(0, k + 1), 'A slice stops before ' + k + ', so position ' + k + ' is left out.'], [w.slice(1, k + 1), 'The slice starts at 0, the first letter.'], [w[k], 'That is one letter at [' + k + ']. A slice gives several.']]); },
      function () { var t = pickOne(['ha', 'yo', 'la', 'go']), n = ri(2, 4);
        return mk('What does this give?', 'print("' + t + '" * ' + n + ')', [[new Array(n + 1).join(t), 'A star repeats the text ' + n + ' times.'], [t + n, '* repeats, it does not glue on the number.'], [t, 'The text is repeated, not shown once.'], ['An error', 'Text times a whole number is allowed.']]); }
    ],
    input: [
      function () { var n = ri(3, 9), k = ri(1, 5);
        return mk('You type ' + n + '. What does this show?', 'x = int(input())\nprint(x + ' + k + ')', [[n + k, 'int() turned "' + n + '" into the number ' + n + ', so ' + n + ' + ' + k + ' = ' + (n + k) + '.'], ['' + n + k, 'int() made it a number, so + adds instead of gluing.'], ['An error', 'int("' + n + '") works, because ' + n + ' is all digits.'], [n, 'The + ' + k + ' is added before printing.']]); },
      function () { var n = ri(2, 9);
        return mk('You type ' + n + '. What does this show?', 'x = input()\nprint(x * 2)', ['' + n + n, n * 2, 'An error', n].map(function (o, i) { return [o, ['input() gives text, and text times 2 repeats it: ' + n + n + '.', 'x is the text "' + n + '", not a number, so * repeats it.', 'Repeating text with * is allowed.', 'The * 2 repeats the text.'][i]]; })); }
    ],
    bool: [
      function () { var a = ri(1, 20), b = ri(1, 20), op = pickOne(['>', '<', '>=', '<=', '==', '!=']);
        var r = { '>': a > b, '<': a < b, '>=': a >= b, '<=': a <= b, '==': a === b, '!=': a !== b }[op];
        return mk('What does this show?', 'print(' + a + ' ' + op + ' ' + b + ')', [[r ? 'True' : 'False', a + ' ' + op + ' ' + b + ' is ' + (r ? 'True' : 'False') + '.'], [r ? 'False' : 'True', 'Check again: is ' + a + ' ' + op + ' ' + b + '? It is ' + (r ? 'True' : 'False') + '.'], [a, 'A comparison gives True or False, not a number.'], ['An error', 'Comparing two numbers is always allowed.']]); },
      function () { var x = ri(1, 12), lo = ri(2, 6), hi = ri(7, 11), r = x > lo && x < hi;
        return mk('What does this show?', 'x = ' + x + '\nprint(x > ' + lo + ' and x < ' + hi + ')', [[r ? 'True' : 'False', r ? 'Both sides are True, so and gives True.' : 'At least one side is False, so and gives False.'], [r ? 'False' : 'True', 'and needs both sides True. Check ' + x + ' > ' + lo + ' and ' + x + ' < ' + hi + '.'], [x, 'The comparison gives True or False, not x.'], ['An error', 'Combining checks with and is allowed.']]); }
    ],
    'if': [
      function () { var age = ri(2, 17), r = age < 6 ? 'small' : age < 13 ? 'kid' : 'teen';
        var why = {
          small: age < 6 ? age + ' < 6 is True, so the first branch runs.' : age + ' is not less than 6.',
          kid: r === 'kid' ? age + ' < 6 is False, then ' + age + ' < 13 is True: kid.' : age < 6 ? 'The first True branch wins, and that was age < 6.' : age + ' is not less than 13.',
          teen: r === 'teen' ? 'Nothing above was True, so else runs: teen.' : 'else only runs when nothing above was True.'
        };
        var pairs = [[r, why[r]]].concat(['small', 'kid', 'teen'].filter(function (k) { return k !== r; }).map(function (k) { return [k, why[k]]; }), [['kid then teen', 'Only the first True branch runs.']]);
        return mk('What does this show?', 'age = ' + age + '\nif age < 6:\n    print("small")\nelif age < 13:\n    print("kid")\nelse:\n    print("teen")', pairs); },
      function () { var t = ri(10, 35), lim = pickOne([20, 25, 30]), hot = t > lim;
        return mk('What does this show?', 'temp = ' + t + '\nif temp > ' + lim + ':\n    print("Shorts")\nelse:\n    print("Jumper")', [[hot ? 'Shorts' : 'Jumper', t + ' > ' + lim + ' is ' + (hot ? 'True, so the if branch runs.' : 'False, so else runs.')], [hot ? 'Jumper' : 'Shorts', 'Check ' + t + ' > ' + lim + ' again: it is ' + (hot ? 'True' : 'False') + '.'], ['Shorts then Jumper', 'Only one branch runs, never both.'], ['Nothing', 'One of the two branches always runs.']]); }
    ],
    loop: [
      function () { var a = ri(0, 3), s = ri(2, 3), b = a + s * ri(2, 3) + 1, seq = []; for (var i = a; i < b; i += s) seq.push(i);
        var all = []; for (var j = a; j < b; j++) all.push(j);
        return mk('What does this show?', 'for i in range(' + a + ', ' + b + ', ' + s + '):\n    print(i)', [[seq.join(' '), 'Start at ' + a + ', jump by ' + s + ', stop before ' + b + '.'], [seq.concat([b]).join(' '), 'range stops before ' + b + ', so ' + b + ' is not shown.'], [all.join(' '), 'The third number, ' + s + ', means jump by ' + s + '.'], [seq.slice(1).join(' ') || 'Nothing', 'range starts at ' + a + ', the first number.']]); },
      function () { var k = ri(3, 6), sum = k * (k - 1) / 2;
        return mk('What is total at the end?', 'total = 0\nfor n in range(' + k + '):\n    total += n', [[sum, 'range(' + k + ') gives 0 to ' + (k - 1) + ', and they add up to ' + sum + '.'], [sum + k, 'range(' + k + ') stops before ' + k + ', so ' + k + ' is not added.'], [k, 'Each turn adds n to total, not 1.'], [0, 'total changes on every turn of the loop.']]); },
      function () { var m = ri(2, 4), n = ri(m + 2, 8), a = [], b = []; for (var i = 0; i < m; i++) a.push(i); for (var j = 0; j <= m; j++) b.push(j);
        var all = []; for (var k = 0; k < n; k++) all.push(k);
        return mk('What does this show?', 'for n in range(' + n + '):\n    if n == ' + m + ':\n        break\n    print(n)', [[a.join(' '), 'When n reaches ' + m + ', break stops the loop before printing.'], [b.join(' '), 'break happens before print(' + m + '), so ' + m + ' is never shown.'], [all.join(' '), 'break stops the loop early.'], [m, 'The numbers before ' + m + ' are printed first.']]); }
    ],
    lists1: [
      function () { var x = shuffled(THINGS).slice(0, ri(3, 4)), i = ri(0, x.length - 2);
        return mk('What does this show?', 'beams = ' + pyList(x).replace(/'/g, '"') + '\nprint(beams[' + i + '])', [[x[i], 'Positions start at 0, so [' + i + '] is ' + x[i] + '.'], [x[i + 1], 'That is position ' + (i + 1) + '. Positions start at 0.'], [i, '[' + i + '] picks an item, it does not show the number.'], ['An error', 'Position ' + i + ' exists in a list of ' + x.length + '.']]); },
      function () { var x = shuffled(THINGS).slice(0, ri(3, 5));
        return mk('What does this show?', 'beams = ' + pyList(x).replace(/'/g, '"') + '\nprint(beams[-1])', [[x[x.length - 1], '-1 counts from the end: ' + x[x.length - 1] + '.'], [x[0], 'That is [0], the first item.'], [x[x.length - 2], 'That is [-2], one before the end.'], [-1, '[-1] picks an item, it does not show the number.']]); },
      function () { var x = [ri(1, 9), ri(1, 9), ri(1, 9)], v = ri(10, 20);
        return mk('What does this show?', 'x = ' + pyList(x) + '\nx.append(' + v + ')\nprint(x)', [[pyList(x.concat([v])), 'append puts ' + v + ' on the end.'], [pyList([v].concat(x)), 'append adds to the end. insert(0, ' + v + ') would put it first.'], [pyList(x), 'append changes the list, so ' + v + ' is now in it.'], [v, 'We print the whole list, not just the new item.']]); },
      function () { var x = [ri(1, 9), ri(10, 19), ri(20, 29), ri(30, 39)].slice(0, ri(3, 4));
        return mk('What does this show?', 'x = ' + pyList(x) + '\nx.pop()\nprint(x)', [[pyList(x.slice(0, -1)), 'pop() takes the last item off.'], [pyList(x.slice(1)), 'pop() takes from the end. pop(0) would take the first.'], [pyList(x), 'pop changes the list, so the last item is gone.'], [x[x.length - 1], 'pop gives back that item, but here we print the list.']]); },
      function () { var x = [10, 20, 30, 40, 50].slice(0, ri(4, 5)), a = ri(0, 1), b = a + 2;
        return mk('What does this give?', 'print(' + pyList(x) + '[' + a + ':' + b + '])', [[pyList(x.slice(a, b)), 'From ' + a + ', stopping before ' + b + '.'], [pyList(x.slice(a, b + 1)), 'The slice stops before position ' + b + '.'], [pyList(x.slice(a + 1, b + 1)), 'Position ' + a + ' is ' + x[a] + ', the start of the slice.'], [x[a], 'A slice gives a list, not one item.']]); },
      function () { var x = shuffled(THINGS).slice(0, ri(2, 5));
        return mk('What does this give?', 'print(len(' + pyList(x).replace(/'/g, '"') + '))', [[x.length, 'len counts the items: ' + x.length + '.'], [x.length - 1, 'That is the last position. len counts every item.'], [x.join('').length, 'len counts items, not letters.'], [x[x.length - 1], 'len gives a number, not an item.']]); }
    ]
  };
  function makeQuiz(ld) {
    var n = ld.quiz.length, gens = shuffled(GEN[ld.key] || []), made = [];
    // about half the quiz is made fresh (never more than the generators available), the rest is hand-written
    var want = Math.min(gens.length, Math.ceil(n / 2));
    for (var g = 0; g < gens.length && made.length < want; g++) {
      for (var t = 0; t < 8; t++) { var q = gens[g](); if (q) { made.push(q); break; } }
    }
    // skip hand-written questions that test the same thing as a fresh one (two pop() questions in a row feels repetitive)
    var TOPIC = [/\.pop\(/, /\.append\(/, /\[-1\]/, /\[\d:\d\]/, /len\(/, /\s%\s/, /\/\//, /\*\*/, /\+=/, /range\(\d+, \d+, \d+\)/, /break/, /elif/, / and /, / - /];
    function topicOf(code) { var plain = code.replace(/<[^>]+>/g, '').replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&'); for (var i = 0; i < TOPIC.length; i++) if (TOPIC[i].test(plain)) return i; return -1; }
    var taken = made.map(function (q) { return topicOf(q.code); });
    var pool = shuffled(ld.quiz), fresh = [];
    pool.forEach(function (q) { var t = topicOf(q.code); if (t < 0 || taken.indexOf(t) < 0) { fresh.push(q); if (t >= 0) taken.push(t); } }); // one question per idea
    var fixed = fresh.concat(pool.filter(function (q) { return fresh.indexOf(q) < 0; })).slice(0, n - made.length); // repeats only if nothing else is left
    return shuffled(fixed.concat(made)).map(function (q) {
      var order = shuffled(q.options.map(function (o, i) { return i; }));
      return { text: q.text, code: q.code, options: order.map(function (i) { return q.options[i]; }), why: order.map(function (i) { return q.why[i]; }), answer: order.indexOf(q.answer) };
    });
  }
