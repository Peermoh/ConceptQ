  // ---- more Maths questions (tools/maths_extra.js, put in place by tools/add_maths_extra.py) ----
  // Topics the Grade 2–3 quizzes were missing (odd and even, tables 6–9, remainders, rounding, conversions,
  // elapsed time, two-step problems), harder numbers at the Hard level, and the 🌟 challenge questions.
  // Every generator returns mq(text, picture, [[right, why], [wrong, why], [wrong, why]]), or null to try again.
  function inr(n) { return Number(n).toLocaleString('en-IN'); }
  function pickN(a, n) { return shuffled(a).slice(0, n); }
  function addGen(key, step, f) { (GEN[key] = GEN[key] || []).push(f); (GEN_STEPS[key] = GEN_STEPS[key] || []).push(step); }
  var NAMES = ['Ravi', 'Asha', 'Meera', 'Arjun', 'Zara', 'Kabir', 'Isha', 'Dev', 'Anya', 'Sam'];

  // Grade 2
  addGen('m2_numbers', 3, function () { // odd and even
    var even = pickOne([true, false]), r = ri(lv(1, 10, 50), lv(20, 60, 99)); if ((r % 2 === 0) !== even) r++;
    var w = [r + 1, r + 3], ask = even ? 'even' : 'odd';
    return mq('Which number is ' + ask + '?', '', [[r, r + ' ends in ' + (r % 10) + ', so it is ' + ask + '.'], [w[0], w[0] + ' ends in ' + (w[0] % 10) + ': it is ' + (even ? 'odd' : 'even') + '.'], [w[1], w[1] + ' ends in ' + (w[1] % 10) + ': it is ' + (even ? 'odd' : 'even') + '.']]);
  });
  addGen('m2_numbers', 2, function () { // 10 more, 10 less
    var n = ri(lv(11, 15, 21), lv(40, 80, 89)), more = pickOne([true, false]), r = more ? n + 10 : n - 10;
    return mq('What is 10 ' + (more ? 'more' : 'less') + ' than ' + n + '?', '', [[r, 'The tens go ' + (more ? 'up' : 'down') + ' by one: ' + r + '.'], [more ? n + 1 : n - 1, 'That is 1 ' + (more ? 'more' : 'less') + ', not 10.'], [more ? n + 100 : n + 10, more ? 'That is 100 more.' : 'That is 10 more. We need 10 less.']]);
  });
  addGen('m2_addsub', 4, function () { // two steps
    var who = pickOne(NAMES), a = ri(lv(20, 30, 40), lv(40, 60, 80)), b = ri(lv(5, 8, 12), lv(15, 25, 35)), c = ri(lv(5, 8, 10), lv(15, 25, 30)); if (c >= a + b) return null;
    var r = a + b - c;
    return mq(who + ' has ' + a + ' marbles, wins ' + b + ' more, then gives ' + c + ' to a friend. How many now?', '', [[r, a + ' + ' + b + ' = ' + (a + b) + ', then ' + (a + b) + ' − ' + c + ' = ' + r + '.'], [a + b, 'That is before giving ' + c + ' away.'], [a + b + c, 'Giving away means take away ' + c + ', not add.']]);
  });

  // Grade 3
  addGen('m3_thousand', 1, function () { // value of a digit
    var n = ri(lv(100, 300, 1000), lv(999, 999, 9999)), s = String(n), i = ri(0, s.length - 1), d = +s[i]; if (!d) return null;
    var place = [1, 10, 100, 1000][s.length - 1 - i], name = { 1: 'ones', 10: 'tens', 100: 'hundreds', 1000: 'thousands' }[place];
    var w = [place === 1 ? d * 10 : d, place === 1000 ? d * 100 : d * place * 10];
    return mq('What is the value of the digit ' + d + ' in ' + inr(n) + '?', '', [[inr(d * place), d + ' is in the ' + name + ' place: ' + d + ' × ' + place + ' = ' + inr(d * place) + '.'], [inr(w[0]), 'Look at which place the ' + d + ' is in: the ' + name + '.'], [inr(w[1]), 'That is one place too far to the left.']]);
  });
  addGen('m3_thousand', 4, function () { // rounding
    var to = lv(10, 10, 100), n = ri(to === 10 ? 101 : 120, 989); if (n % to === 0 || n % to === to / 2) return null;
    var down = Math.floor(n / to) * to, up = down + to, r = n - down < to / 2 ? down : up;
    return mq('Round ' + n + ' to the nearest ' + to + '.', '', [[r, n + ' is between ' + down + ' and ' + up + ', and closer to ' + r + '.'], [r === down ? up : down, n + ' is closer to ' + r + '.'], [to === 10 ? Math.round(n / 100) * 100 : Math.round(n / 10) * 10, 'That rounds to the nearest ' + (to === 10 ? 100 : 10) + ', not ' + to + '.']]);
  });
  addGen('m3_thousand', 3, function () { // compare with symbols
    var a = ri(lv(100, 300, 1000), lv(500, 999, 9999)), b = a + pickOne([-1, 1]) * pickOne([1, 10, 100, 90, 9]); if (b < 100 || a === b) return null;
    var s = a > b ? '>' : '<';
    return mq('Which sign makes it true? ' + inr(a) + ' __ ' + inr(b), '', [[s, inr(a) + (s === '>' ? ' is bigger than ' : ' is smaller than ') + inr(b) + '. Compare from the left.'], [s === '>' ? '<' : '>', 'The open side of the sign faces the bigger number.'], ['=', 'They are different numbers.']]);
  });
  addGen('m3_add', 3, function () { // two steps, bigger numbers
    var a = rl([110, 300], [200, 500], [1200, 4000]), b = rl([100, 300], [150, 400], [800, 3000]), c = rl([50, 150], [100, 300], [500, 1500]), r = a + b + c;
    return mq('A library has ' + inr(a) + ' story books, ' + inr(b) + ' science books and ' + inr(c) + ' comics. How many books in all?', '', [[inr(r), inr(a) + ' + ' + inr(b) + ' = ' + inr(a + b) + ', then + ' + inr(c) + ' = ' + inr(r) + '.'], [inr(a + b), 'Add the comics too.'], [inr(r + 100), 'Check the carrying in the hundreds.']]);
  });
  addGen('m3_add', 2, function () { // estimate
    var a = ri(lv(110, 210, 1200), lv(390, 480, 4800)), b = ri(lv(110, 210, 1200), lv(390, 480, 4800)), to = lv(100, 100, 1000), e = Math.round(a / to) * to + Math.round(b / to) * to;
    return mq('About how much is ' + inr(a) + ' + ' + inr(b) + '? Round each to the nearest ' + inr(to) + ' first.', '', [[inr(e), inr(Math.round(a / to) * to) + ' + ' + inr(Math.round(b / to) * to) + ' = ' + inr(e) + '.'], [inr(e + to), 'Round each number first, then add.'], [inr(e - to), 'Round each number first, then add.']]);
  });
  addGen('m3_sub', 1, function () { // borrowing across a zero
    var a = pickOne(lv([200, 300, 400, 500], [300, 400, 600, 700, 800], [2000, 3000, 5000, 7000])) + lv(0, pickOne([0, 4, 6]), 0), b = ri(lv(111, 121, 1111), a - lv(20, 30, 200)), r = a - b;
    return mq(inr(a) + ' − ' + inr(b) + ' = ?', '', [[inr(r), 'Borrow from the hundreds when the tens are 0. ' + inr(b) + ' + ' + inr(r) + ' = ' + inr(a) + '.'], [inr(r + 100), 'You borrowed but did not take 1 from the hundreds.'], [inr(Math.abs(r - 10)), 'Check by adding back: it must make ' + inr(a) + '.']]);
  });
  addGen('m3_sub', 3, function () { // how many more, then two steps
    var a = rl([150, 300], [300, 600], [1500, 6000]), b = rl([60, 140], [120, 280], [600, 1400]), c = rl([20, 50], [40, 100], [200, 500]), r = a - b - c; if (r <= 0) return null;
    return mq('A shop had ' + inr(a) + ' kites. It sold ' + inr(b) + ' on Monday and ' + inr(c) + ' on Tuesday. How many are left?', '', [[inr(r), inr(a) + ' − ' + inr(b) + ' = ' + inr(a - b) + ', then − ' + inr(c) + ' = ' + inr(r) + '.'], [inr(a - b), 'Take away Tuesday too.'], [inr(a - b + c), 'Both days are sold: take both away.']]);
  });
  addGen('m3_times', 3, function () { // tables 6 to 9
    var a = ri(lv(2, 6, 6), lv(5, 9, 9)), b = ri(lv(2, 3, 6), lv(6, 9, 12)), r = a * b;
    return mq(a + ' × ' + b + ' = ?', '', [[r, a + ' groups of ' + b + ' make ' + r + '.'], [r + a, 'That is ' + (b + 1) + ' groups of ' + a + '.'], [a + b, 'That adds. × means groups of.']]);
  });
  addGen('m3_times', 2, function () { // missing number
    var a = ri(lv(2, 3, 6), lv(5, 9, 9)), b = ri(lv(2, 3, 6), lv(5, 9, 12)), r = a * b;
    return mq('__ × ' + a + ' = ' + r + '. What is the missing number?', '', [[b, b + ' × ' + a + ' = ' + r + '.'], [r - a, 'Think: how many ' + a + 's make ' + r + '?'], [b + 1, (b + 1) + ' × ' + a + ' = ' + (b + 1) * a + '.']]);
  });
  addGen('m3_times', 0, function () { // rows word problem
    var rows = ri(lv(3, 4, 6), lv(5, 8, 12)), per = ri(lv(2, 5, 6), lv(5, 9, 15)), r = rows * per, t = pickOne(['chairs', 'plants', 'children', 'stalls']);
    return mq('A hall has ' + rows + ' rows of ' + t + ', with ' + per + ' in each row. How many ' + t + '?', '', [[r, rows + ' × ' + per + ' = ' + r + '.'], [rows + per, 'That adds. We need ' + rows + ' groups of ' + per + '.'], [r - per, 'That is only ' + (rows - 1) + ' rows.']]);
  });
  addGen('m3_divide', 3, function () { // remainders
    var k = ri(lv(2, 3, 4), lv(4, 6, 9)), each = ri(lv(2, 3, 5), lv(5, 8, 12)), left = ri(1, k - 1), n = k * each + left;
    return mq(n + ' sweets are shared equally by ' + k + ' children. How many does each get, and how many are left?', '', [[each + ' each, ' + left + ' left', k + ' × ' + each + ' = ' + k * each + ', and ' + n + ' − ' + k * each + ' = ' + left + ' left over.'], [(each + 1) + ' each, 0 left', k + ' × ' + (each + 1) + ' = ' + k * (each + 1) + ', more than ' + n + '.'], [each + ' each, ' + (left + k) + ' left', 'The left-over must be less than ' + k + ', or everyone could get one more.']]);
  });
  addGen('m3_divide', 2, function () { // times backwards
    var d = ri(lv(2, 3, 6), lv(5, 9, 12)), q = ri(lv(2, 3, 6), lv(5, 9, 12)), n = d * q;
    return mq(n + ' ÷ ' + d + ' = ?', '', [[q, d + ' × ' + q + ' = ' + n + ', so ' + n + ' ÷ ' + d + ' = ' + q + '.'], [n - d, 'Dividing is sharing, not taking away.'], [q + 1, d + ' × ' + (q + 1) + ' = ' + d * (q + 1) + ', not ' + n + '.']]);
  });
  addGen('m3_fractions', 0, function () { // compare unit fractions
    var a = pickOne([2, 3, 4, 5, 6, 8, 10]), b = pickOne([2, 3, 4, 5, 6, 8, 10].filter(function (x) { return x !== a; })), big = Math.min(a, b);
    return mq('Which is bigger: 1/' + a + ' or 1/' + b + '?', '', [['1/' + big, 'Fewer equal parts means each part is bigger: 1/' + big + ' is bigger.'], ['1/' + Math.max(a, b), 'More parts means smaller pieces.'], ['They are the same', 'The wholes are cut into different numbers of parts.']]);
  });
  addGen('m3_fractions', 4, function () { // fraction of a number
    var d = pickOne(lv([2, 4], [2, 3, 4], [3, 4, 5, 6])), k = lv(1, 1, ri(1, d - 1)), n = d * ri(lv(2, 3, 4), lv(6, 9, 12)), r = n / d * k;
    return mq('What is ' + k + '/' + d + ' of ' + n + '?', '', [[r, n + ' ÷ ' + d + ' = ' + n / d + (k > 1 ? ', and ' + k + ' of those is ' + r : '') + '.'], [n - r, 'That is what is left over.'], [n * d === r ? r + 1 : n / k === r ? r + 2 : Math.round(n / (d + 1)), 'Share ' + n + ' into ' + d + ' equal parts.']]);
  });
  addGen('m3_measure', 1, function () { // conversions
    var U = lv([['m', 'cm', 100]], [['m', 'cm', 100], ['kg', 'g', 1000]], [['m', 'cm', 100], ['kg', 'g', 1000], ['L', 'mL', 1000], ['km', 'm', 1000]]), u = pickOne(U), a = ri(1, lv(5, 9, 12)), b = u[2] === 100 ? ri(1, 99) : ri(1, 19) * 50, r = a * u[2] + b;
    return mq(a + ' ' + u[0] + ' ' + b + ' ' + u[1] + ' = how many ' + u[1] + '?', '', [[inr(r) + ' ' + u[1], '1 ' + u[0] + ' = ' + inr(u[2]) + ' ' + u[1] + ', so ' + a + ' ' + u[0] + ' = ' + inr(a * u[2]) + ' ' + u[1] + ', plus ' + b + '.'], [(a + b) + ' ' + u[1], 'Change the ' + u[0] + ' into ' + u[1] + ' first.'], [inr(a * 10 + b) + ' ' + u[1], '1 ' + u[0] + ' is ' + inr(u[2]) + ' ' + u[1] + ', not 10.']]);
  });
  addGen('m3_time', 2, function () { // elapsed time
    var h = ri(1, 10), m = pickOne([0, 15, 30, 45]), dh = ri(lv(0, 1, 1), lv(1, 2, 3)), dm = pickOne(lv([30], [15, 30, 45], [15, 30, 45, 50])), t = h * 60 + m + dh * 60 + dm;
    var fmt = function (x) { var hh = Math.floor(x / 60) % 12 || 12, mm = x % 60; return hh + ':' + (mm < 10 ? '0' : '') + mm; };
    var dur = (dh ? dh + ' hour' + (dh > 1 ? 's' : '') + ' ' : '') + dm + ' minutes';
    return mq('A film starts at ' + fmt(h * 60 + m) + ' and lasts ' + dur + '. When does it end?', '', [[fmt(t), 'Add the hours, then the minutes: ' + fmt(t) + '.'], [fmt(t - 60), 'Add the ' + (dh ? dh + ' hour' + (dh > 1 ? 's' : '') + ' too' : 'minutes carefully') + '.'], [fmt(t + 60 - (dm >= 30 ? 0 : 60) + 10), 'Count on from ' + fmt(h * 60 + m) + ': first the hours, then the minutes.']]);
  });
  addGen('m3_time', 3, function () { // weeks and days
    var w = ri(2, lv(3, 5, 8)), d = ri(1, 6), r = w * 7 + d;
    return mq(w + ' weeks and ' + d + (d === 1 ? ' day' : ' days') + ' is how many days?', '📅', [[r, w + ' × 7 = ' + w * 7 + ', plus ' + d + ' = ' + r + '.'], [w + d, 'A week is 7 days, so ' + w + ' weeks is ' + w * 7 + ' days.'], [w * 10 + d, 'A week has 7 days, not 10.']]);
  });
  addGen('m3_money', 2, function () { // buy several and get change
    var n = ri(2, lv(3, 4, 6)), p = ri(lv(5, 8, 15), lv(15, 25, 45)), extra = ri(lv(10, 20, 40), lv(20, 50, 120)), cost = n * p + extra, pay = cost <= 100 ? 100 : cost <= 200 ? 200 : 500, r = pay - cost;
    return mq('You buy ' + n + ' pens at ₹' + p + ' each and a book for ₹' + extra + '. You pay with a ₹' + pay + ' note. How much change?', '', [['₹' + r, n + ' × ₹' + p + ' = ₹' + n * p + ', + ₹' + extra + ' = ₹' + cost + '. ₹' + pay + ' − ₹' + cost + ' = ₹' + r + '.'], ['₹' + (pay - p - extra), 'You bought ' + n + ' pens, not 1.'], ['₹' + cost, '₹' + cost + ' is what you spend. Change is what you get back.']]);
  });
  addGen('m3_shapes', 1, function () { // perimeter
    var sq = pickOne([true, false]), l = ri(lv(3, 4, 6), lv(6, 9, 15)), w = sq ? l : ri(2, l - 1), r = 2 * (l + w);
    return mq('A ' + (sq ? 'square' : 'rectangle') + ' has sides of ' + (sq ? l + ' cm' : l + ' cm and ' + w + ' cm') + '. What is its perimeter?', '', [[r + ' cm', 'Add all ' + 4 + ' sides: ' + (sq ? '4 × ' + l : l + ' + ' + w + ' + ' + l + ' + ' + w) + ' = ' + r + ' cm.'], [(l + w) + ' cm', 'That is only two sides. There are four.'], [l * w + ' cm', 'That multiplies. Perimeter adds all the sides.']]);
  });
  addGen('m3_shapes', 0, function () { // sides of shapes
    var S = [['triangle', 3], ['square', 4], ['pentagon', 5], ['hexagon', 6], ['octagon', 8]], s = pickOne(S), o = pickN(S.filter(function (x) { return x !== s; }), 2);
    return mq('How many sides does ' + an(s[0]) + ' have?', '', [[s[1], an(s[0])[0].toUpperCase() + an(s[0]).slice(1) + ' has ' + s[1] + ' sides and ' + s[1] + ' corners.'], [o[0][1], 'That is a ' + o[0][0] + '.'], [o[1][1], 'That is a ' + o[1][0] + '.']]);
  });
  addGen('m3_data', 2, function () { // pictograph key
    var k = pickOne(lv([2, 5], [5, 10], [5, 10, 20])), n = ri(2, 7), it = pickOne(['🍎', '🍌', '⚽', '📚']);
    return mq('In a pictograph, each ' + it + ' stands for ' + k + '. One row has ' + n + ' ' + it + '. How many is that?', rpt(it, n), [[n * k, n + ' × ' + k + ' = ' + n * k + '.'], [n, 'Each picture stands for ' + k + ', not 1.'], [n + k, 'Count ' + k + ' for every picture: ' + n + ' × ' + k + '.']]);
  });
  addGen('m3_fair', 3, function () { // takings
    var a = ri(lv(10, 20, 40), lv(20, 40, 90)), pa = pickOne([5, 10, 20]), b = ri(lv(5, 10, 20), lv(15, 30, 60)), pb = pickOne([10, 20, 50]), r = a * pa + b * pb;
    return mq('The fair sold ' + a + ' juice cups at ₹' + pa + ' and ' + b + ' games at ₹' + pb + '. How much money in all?', '', [['₹' + inr(r), a + ' × ₹' + pa + ' = ₹' + inr(a * pa) + ', ' + b + ' × ₹' + pb + ' = ₹' + inr(b * pb) + ', together ₹' + inr(r) + '.'], ['₹' + inr(a * pa), 'Add the games too.'], ['₹' + inr((a + b) * pa), 'The games cost ₹' + pb + ', not ₹' + pa + '.']]);
  });

  // 🌟 challenge questions: several steps; one ends every Maths quiz (a bonus: it never stops a pass)
  var CHALLENGE = { 2: [], 3: [], 4: typeof G4CHAL !== 'undefined' ? G4CHAL : [] }; // Grade 4's are in maths_g4_gens.js
  function addChal(g, f) { CHALLENGE[g].push(f); }
  addChal(2, function () { var b = ri(2, 4), l = ri(3, 9), g = ri(5, b * 10 + l - 5), r = b * 10 + l - g;
    return mq('Asha has ' + b + ' boxes of 10 crayons and ' + l + ' loose crayons. She gives ' + g + ' to her brother. How many are left?', grp(b, 10, '🖍️', '📦'), [[r, b + ' tens and ' + l + ' ones = ' + (b * 10 + l) + '. ' + (b * 10 + l) + ' − ' + g + ' = ' + r + '.'], [b * 10 + l, 'She gave ' + g + ' away.'], [b + l + 10 - g > 0 && b + l + 10 - g !== r ? b + l + 10 - g : r + 10, 'Each box holds 10.']]); });
  addChal(2, function () { var s = ri(30, 50), off = ri(8, 19), on = ri(5, 15), r = s - off + on;
    return mq('A bus has ' + s + ' people. At the stop ' + off + ' get off and ' + on + ' get on. How many are on the bus now?', '🚌', [[r, s + ' − ' + off + ' = ' + (s - off) + ', then + ' + on + ' = ' + r + '.'], [s - off - on, 'The ' + on + ' people get ON: add them.'], [s - off, 'Do not forget the ' + on + ' who got on.']]); });
  addChal(2, function () { var p = pickOne([5, 6, 8]), n = ri(3, 6), pay = n * p <= 20 ? 20 : 50, r = pay - n * p;
    return mq('Pencils cost ₹' + p + ' each. You buy ' + n + ' and pay with ₹' + pay + '. How much change?', '✏️', [['₹' + r, n + ' × ₹' + p + ' = ₹' + n * p + '. ₹' + pay + ' − ₹' + n * p + ' = ₹' + r + '.'], ['₹' + n * p, 'That is the cost. The change is what comes back.'], ['₹' + (pay - p), 'You bought ' + n + ' pencils, not 1.']]); });
  addChal(3, function () { var rows = ri(6, 9), per = ri(6, 9), bad = ri(5, 15), r = rows * per - bad;
    return mq('A farmer plants ' + rows + ' rows of ' + per + ' mango trees. ' + bad + ' trees do not grow. How many trees grow?', '🌳', [[r, rows + ' × ' + per + ' = ' + rows * per + ', then − ' + bad + ' = ' + r + '.'], [rows * per, bad + ' did not grow: take them away.'], [rows + per - bad > 0 ? rows + per - bad : r + 9, rows + ' rows of ' + per + ' means ' + rows + ' × ' + per + '.']]); });
  addChal(3, function () { var b = ri(4, 8), per = pickOne([12, 24, 36]), k = pickOne([3, 4, 6]), t = b * per; if (t % k) return null; var r = t / k;
    return mq(b + ' boxes have ' + per + ' mangoes each. They are shared equally by ' + k + ' families. How many mangoes does each family get?', '🥭', [[r, b + ' × ' + per + ' = ' + t + ', then ' + t + ' ÷ ' + k + ' = ' + r + '.'], [t, 'Now share the ' + t + ' between ' + k + ' families.'], [per / k * 1 === r ? r + k : per / k, 'Share all the boxes, not just one.']]); });
  addChal(3, function () { var a = ri(250, 480), b = ri(150, 390), c = ri(100, 300), r = a + b - c; if (r <= 0) return null;
    return mq('A school has ' + a + ' girls and ' + b + ' boys. ' + c + ' children go on a trip. How many stay at school?', '🏫', [[r, a + ' + ' + b + ' = ' + (a + b) + ', then − ' + c + ' = ' + r + '.'], [a + b, c + ' went on the trip: take them away.'], [a - c + b - 100 === r ? r + 10 : a - c, 'Add the boys too.']]); });
  addChal(3, function () { var h = ri(2, 5), m = pickOne([10, 20, 40, 50]), dur = pickOne([35, 45, 50, 55, 70, 85]), t = h * 60 + m + dur;
    var f = function (x) { return Math.floor(x / 60) + ':' + (x % 60 < 10 ? '0' : '') + x % 60; };
    return mq('A match starts at ' + f(h * 60 + m) + ' and lasts ' + dur + ' minutes. When does it end?', '⚽', [[f(t), 'Count on ' + dur + ' minutes from ' + f(h * 60 + m) + ': ' + f(t) + '.'], [f(h * 60 + m).replace(/:\d+/, ':' + ((m + dur) < 10 ? '0' : '') + (m + dur)), 'There are only 60 minutes in an hour.'], [f(t + 60), 'Only ' + dur + ' minutes, not an extra hour.']]); });
  addChal(3, function () { var p = ri(12, 35), n = ri(3, 6), d = pickOne([10, 20]), cost = n * p - d, pay = cost <= 100 ? 100 : 200; if (cost <= 0) return null; var r = pay - cost;
    return mq('Notebooks cost ₹' + p + ' each. You buy ' + n + ' and get ₹' + d + ' off. You pay with ₹' + pay + '. How much change?', '📒', [['₹' + r, n + ' × ₹' + p + ' = ₹' + n * p + ', − ₹' + d + ' = ₹' + cost + '. ₹' + pay + ' − ₹' + cost + ' = ₹' + r + '.'], ['₹' + (pay - n * p), 'Take the ₹' + d + ' off the price first.'], ['₹' + cost, 'That is what you pay. Change comes back to you.']]); });

  // which challenge pool a lesson uses: m2_ → 2, m3_ → 3, m4_ → 4
  function challengeFor(key) { var g = +((/^m(\d)_/.exec(key) || [])[1] || 0); return CHALLENGE[g] && CHALLENGE[g].length ? CHALLENGE[g] : null; }
