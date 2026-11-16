KEY, IDX = 'stdlib', 43
META = dict(tag='Everyday tools · Rooftop garden', title='Everyday tools: the standard library shed', topic='the standard library',
            lastBtn='Fill the tool wall', doneTitle='The tool wall is full!',
            doneText='You learned os and glob, sys.argv, datetime and timedelta, strftime, decimal for exact money, zlib, statistics and collections. A tool wall now fills the garden shed. It is in your garden: take a tool off the wall and try it.')
QUIZ = [
 ('You run: python grow.py tomato. What is sys.argv[1]?', 'import sys\nprint(sys.argv[1])', ["'tomato'", "'grow.py'", "'python'", 'An error'], 0,
  ['argv[0] is the program name; argv[1] is the first word after it.', 'That is argv[0].', 'python itself is not in argv.', 'There is a word after the program name.'], 1),
 ('What does this show?', 'from datetime import date, timedelta\nprint(date(2026, 1, 30) + timedelta(days=3))', ['2026-02-02', '2026-01-33', '2026-02-03', 'An error'], 0,
  ['timedelta knows January has 31 days.', 'There is no 33rd of January.', 'Count again: 31, 1, 2.', 'Adding a timedelta to a date is fine.'], 2),
 ('What does this show?', 'from datetime import date\nprint(date(2026, 5, 3).strftime("%d %b"))', ['03 May', '3 May', '05 Mar', 'May 03'], 0,
  ['%d is the day with two digits, %b the short month name.', '%d always uses two digits.', '%d is the day, not the month.', 'The day comes first in this pattern.'], 3),
 ('What does this show?', 'print(0.1 + 0.2 == 0.3)', ['False', 'True', '0.3', 'An error'], 0,
  ['Floats are a tiny bit off: 0.30000000000000004.', 'The float sum is not exactly 0.3.', '== gives True or False.', 'It runs fine.'], 4),
 ('Which is best for money?', '# prices in a shop', ['Decimal', 'float', 'int of pounds', 'str'], 0,
  ['Decimal is exact, so pennies never go missing.', 'Floats can be a tiny bit off.', 'You would lose the pennies.', 'You cannot do maths with text.'], 4),
 ('What does this show?', 'from collections import Counter\nprint(Counter("banana")["a"])', ['3', '2', '1', '6'], 0,
  ['banana has three a letters.', 'That is how many n letters.', 'That is how many b letters.', 'That is the whole length.'], 7),
 ('What does this show?', 'from statistics import mean\nprint(mean([2, 4, 9]))', ['5', '4', '15', '9'], 0,
  ['(2 + 4 + 9) / 3 is 5.', 'That is the median.', 'That is the total, not the mean.', 'That is the biggest.'], 6),
]
CARDS = [
 ('sl1', 'world', 43, 'How do you read words given after the program name?', '`sys.argv`: `sys.argv[1]` is the first one.'),
 ('sl2', 'world', 43, 'How do you add 60 days to today?', '`date.today() + timedelta(days=60)`'),
 ('sl3', 'world', 43, 'Why use `Decimal` for money?', 'Floats can be a tiny bit off (0.1 + 0.2); Decimal is exact.'),
 ('sl4', 'world', 43, 'How do you count every letter in a word?', '`Counter("banana")` → a: 3, n: 2, b: 1'),
]
GEN_STEPS = [2, 7, 6]
GEN_JS = r'''
      function () { var y = 2026, m = ri(1, 12), d = ri(20, 28), k = ri(2, 15), t = new Date(Date.UTC(y, m - 1, d + k)), p = function (n) { return (n < 10 ? '0' : '') + n; };
        var right = t.getUTCFullYear() + '-' + p(t.getUTCMonth() + 1) + '-' + p(t.getUTCDate()), t2 = new Date(Date.UTC(y, m - 1, d + k + 1)), w2 = t2.getUTCFullYear() + '-' + p(t2.getUTCMonth() + 1) + '-' + p(t2.getUTCDate());
        var naive = y + '-' + p(m) + '-' + p(d + k); if (naive === right) naive = y + '-' + p(m) + '-' + p(d + k - 1);
        return mk('What does this show?', 'from datetime import date, timedelta\nprint(date(' + y + ', ' + m + ', ' + d + ') + timedelta(days=' + k + '))', [[right, 'timedelta counts the real days in each month.'], [naive, d + k > 28 ? 'Check how many days that month has.' : 'Count the days again.'], [w2, 'Add exactly ' + k + ' days.'], ['An error', 'Adding a timedelta to a date is fine.']]); },
      function () { var w = pickOne(['banana', 'tomato', 'cabbage', 'broccoli', 'parsnip']), letters = w.split('').filter(function (c, i, a) { return a.indexOf(c) === i; }), c = pickOne(letters), n = w.split(c).length - 1;
        return mk('What does this show?', 'from collections import Counter\nprint(Counter("' + w + '")["' + c + '"])', [[String(n), w + ' has ' + n + ' "' + c + '" letter' + (n > 1 ? 's' : '') + '.'], [String(w.length), 'That is the length of the whole word.'], [String(n + 1), 'Count the "' + c + '" letters again.'], [String(letters.length === n ? n + 2 : letters.length), 'Counter counts one letter here, not every kind.']]); },
      function () { var a = ri(1, 6), b = ri(1, 9), c = ri(2, 12); while ((a + b + c) % 3) c++; var m = (a + b + c) / 3;
        var xs = shuffled([a, b, c]), srt = xs.slice().sort(function (p, q) { return p - q; }), med = srt[1], tot = a + b + c, mx = srt[2];
        var opts = [[String(m), 'Add them (' + tot + ') and divide by 3.']]; [[med, 'That is the middle number, the median.'], [tot, 'That is the total, not the mean.'], [mx, 'That is the biggest number.'], [m + 1, 'Divide the total by 3 again.'], [m - 1, 'Divide the total by 3 again.'], [m + 2, 'The mean is the total divided by how many numbers.'], [tot - 1, 'The mean is the total divided by 3.']].forEach(function (o) { if (opts.length < 4 && opts.every(function (q) { return q[0] !== String(o[0]); })) opts.push([String(o[0]), o[1]]); });
        return mk('What does this show?', 'from statistics import mean\nprint(mean([' + xs.join(', ') + ']))', opts); }
'''
