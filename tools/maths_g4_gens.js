  // ---- Grade 4 (Market Square) question generators: tools/maths_g4_gens.js ----
  // Each returns mq(text, picture, [[right, why], [wrong, why], [wrong, why]]), or null to try again. lv / rl pick by level.
  function in4(n) { return Number(n).toLocaleString('en-IN'); }
  function g4(key, step, f) { (GEN[key] = GEN[key] || []).push(f); (GEN_STEPS[key] = GEN_STEPS[key] || []).push(step); }
  // a bar graph picture: rows [[label, value]], each grid line stands for `per`
  function barsPic(rows, per) {
    var top = Math.max.apply(null, rows.map(function (r) { return r[1]; })), lines = Math.ceil(top / per), u = 16, ax = '', bars = '', labs = '';
    for (var k = 0; k <= lines; k++) ax += '<b style="bottom:' + k * u + 'px">' + k * per + '</b>';
    rows.forEach(function (r) { bars += '<i style="height:' + Math.round(r[1] / per * u) + 'px"></i>'; labs += '<b>' + r[0] + '</b>'; });
    return '<span class="qgraph"><span class="qplot" style="height:' + lines * u + 'px"><span class="qax">' + ax + '</span>' + bars + '</span><span class="qlab">' + labs + '</span></span>';
  }
  var DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  // numbers to one lakh
  g4('m4_lakh', 1, function () {
    var n = ri(lv(1000, 10000, 10000), lv(9999, 99999, 99999)), s = String(n), i = ri(0, s.length - 2), d = +s[i]; if (!d || s.indexOf(String(d)) !== i) return null;
    var place = Math.pow(10, s.length - 1 - i), nm = { 10: 'tens', 100: 'hundreds', 1000: 'thousands', 10000: 'ten thousands' }[place];
    return mq('What is the value of the ' + d + ' in ' + in4(n) + '?', '', [[in4(d * place), d + ' is in the ' + nm + ' place: ' + in4(d * place) + '.'], [in4(d * place / 10), 'That is one place too far to the right.'], [in4(d * place * 10), 'That is one place too far to the left.']]);
  });
  g4('m4_lakh', 0, function () {
    var n = pickOne([9999, 19999, 29999, 39999, 49999, 59999, 69999, 89999, 99999, 9099, 45099, 70999]), after = pickOne([true, false]), r = after ? n + 1 : n - 1;
    return mq('What comes just ' + (after ? 'after ' : 'before ') + in4(n) + '?', '', [[in4(r), in4(n) + (after ? ' + 1 = ' : ' − 1 = ') + in4(r) + '.'], [in4(after ? n + 10 : n - 10), 'Just ' + (after ? 'after' : 'before') + ' means one ' + (after ? 'more' : 'less') + ', not ten.'], [in4(after ? n + 1001 : n + 1), after ? 'Count on just 1.' : 'Before means one less.']]);
  });
  g4('m4_lakh', 4, function () {
    var n = ri(lv(1100, 10100, 10100), lv(9899, 98899, 98899)); if (n % 1000 === 500 || n % 1000 === 0) return null;
    var down = Math.floor(n / 1000) * 1000, r = n % 1000 < 500 ? down : down + 1000;
    return mq('Round ' + in4(n) + ' to the nearest thousand.', '', [[in4(r), 'The hundreds digit is ' + Math.floor(n % 1000 / 100) + ', so round ' + (r > n ? 'up' : 'down') + ' to ' + in4(r) + '.'], [in4(r === down ? down + 1000 : down), in4(n) + ' is closer to ' + in4(r) + '.'], [in4(Math.round(n / 100) * 100), 'That rounds to the nearest hundred.']]);
  });
  g4('m4_lakh', 3, function () {
    var a = ri(lv(1000, 10000, 10000), lv(9999, 99999, 99999)), sw = String(a).split(''), i = ri(1, sw.length - 2), j = i + 1; if (sw[i] === sw[j]) return null;
    var t = sw[i]; sw[i] = sw[j]; sw[j] = t; var b = +sw.join(''), big = Math.max(a, b);
    return mq('Which is bigger: ' + in4(a) + ' or ' + in4(b) + '?', '', [[in4(big), 'Compare from the left: the first different digit decides.'], [in4(Math.min(a, b)), 'Look at the first place where the digits differ.'], ['They are the same', 'Same digits, but in different places.']]);
  });
  g4('m4_lakh', 0, function () {
    var t = ri(1, 9), th = ri(0, 9), h = ri(0, 9), te = ri(0, 9), o = ri(1, 9), n = t * 10000 + th * 1000 + h * 100 + te * 10 + o;
    var parts = [t * 10000, th * 1000, h * 100, te * 10, o].filter(Boolean).map(in4).join(' + ');
    var squashed = +[t, th, h, te, o].filter(Boolean).join(''); // the slip: leaving out the zeros
    return mq(parts + ' = ?', '', [[in4(n), 'Put each digit in its place: ' + in4(n) + '.'], [in4(squashed === n ? n + 100 : squashed), squashed === n ? 'Check the hundreds place.' : 'An empty place still needs a 0.'], [in4(n + 1000), 'Check the thousands place.']]);
  });

  // multiplying bigger numbers
  g4('m4_mult', 0, function () {
    var a = ri(lv(12, 23, 105), lv(99, 99, 999)), k = pickOne(lv([10], [10, 100], [10, 100, 1000])), r = a * k;
    return mq(in4(a) + ' × ' + in4(k) + ' = ?', '', [[in4(r), 'Times ' + in4(k) + ' moves each digit ' + (String(k).length - 1) + ' place' + (k > 10 ? 's' : '') + ' left: ' + in4(a) + ' × ' + in4(k) + ' = ' + in4(r) + '.'], [in4(r / 10 === a ? r * 10 : r / 10), 'Count the zeros in ' + in4(k) + '.'], [in4(a + k), 'That adds ' + in4(k) + '.']]);
  });
  g4('m4_mult', 1, function () {
    var a = ri(lv(12, 21, 104), lv(29, 89, 499)), b = ri(lv(2, 3, 4), lv(5, 9, 9)), r = a * b, t = pickOne([['buses', 'seats'], ['boxes', 'pencils'], ['crates', 'mangoes'], ['shelves', 'books']]);
    return mq('There are ' + a + ' ' + t[0] + ' with ' + b + ' ' + t[1] + ' in each. How many ' + t[1] + '?', '', [[in4(r), a + ' × ' + b + ' = ' + in4(r) + '.'], [in4(a + b), 'That adds. We need ' + a + ' groups of ' + b + '.'], [in4(r - b), 'That is only ' + (a - 1) + ' groups.']]);
  });
  g4('m4_mult', 2, function () {
    var a = ri(lv(12, 23, 112), lv(29, 98, 489)), b = ri(lv(3, 3, 3), lv(5, 9, 9)), r = a * b, ones = a % 10 * b;
    if (ones < 10) return null; // a carry makes it worth doing in columns
    return mq(a + ' × ' + b + ' = ?', '', [[in4(r), 'Ones first: ' + a % 10 + ' × ' + b + ' = ' + ones + ', carry ' + Math.floor(ones / 10) + '.'], [in4(r - Math.floor(ones / 10) * 10), 'Remember the carried ' + Math.floor(ones / 10) + '.'], [in4(r + b), 'Check: that is ' + (a + 1) + ' × ' + b + '.']]);
  });
  g4('m4_mult', 3, function () {
    var a = ri(lv(11, 12, 23), lv(19, 39, 89)), b = ri(lv(11, 12, 13), lv(15, 19, 39)), r = a * b;
    return mq(a + ' × ' + b + ' = ?', '', [[in4(r), a + ' × ' + Math.floor(b / 10) * 10 + ' = ' + in4(a * Math.floor(b / 10) * 10) + ', ' + a + ' × ' + b % 10 + ' = ' + a * (b % 10) + ', together ' + in4(r) + '.'], [in4(a * Math.floor(b / 10) * 10), 'That is only ' + a + ' × ' + Math.floor(b / 10) * 10 + '.'], [in4(a * (b % 10) + a * Math.floor(b / 10)), 'The tens digit of ' + b + ' means ' + Math.floor(b / 10) * 10 + ', not ' + Math.floor(b / 10) + '.']]);
  });
  g4('m4_mult', 4, function () {
    var a = ri(lv(18, 31, 41), lv(29, 89, 98)), b = ri(3, 9), near = Math.round(a / 10) * 10; if (near === a) return null;
    return mq('Which is the best estimate for ' + a + ' × ' + b + '?', '', [[in4(near * b), a + ' is about ' + near + ', and ' + near + ' × ' + b + ' = ' + in4(near * b) + '.'], [in4(near * b * 10), 'That is ' + near + ' × ' + b * 10 + '.'], [a + b, 'That adds.']]);
  });

  // dividing bigger numbers
  g4('m4_div', 1, function () {
    var d = ri(lv(2, 3, 4), lv(5, 9, 9)), q = ri(lv(11, 21, 112), lv(32, 99, 199)), n = d * q;
    return mq(in4(n) + ' ÷ ' + d + ' = ?', '', [[in4(q), d + ' × ' + q + ' = ' + in4(n) + '.'], [in4(q + 1), 'Check: ' + d + ' × ' + (q + 1) + ' = ' + in4(d * (q + 1)) + '.'], [in4(n - d), 'Dividing is sharing, not taking away.']]);
  });
  g4('m4_div', 2, function () {
    var d = ri(lv(3, 4, 6), lv(5, 9, 9)), q = ri(lv(6, 11, 21), lv(12, 25, 99)), r = ri(1, d - 1), n = d * q + r;
    return mq(n + ' ÷ ' + d + ' = ?', '', [[q + ' r ' + r, d + ' × ' + q + ' = ' + d * q + ', and ' + r + ' is left over.'], [q + ' r ' + (r + d), 'The remainder must be smaller than ' + d + '.'], [(q + 1) + ' r 0', d + ' × ' + (q + 1) + ' = ' + d * (q + 1) + ', more than ' + n + '.']]);
  });
  g4('m4_div', 4, function () {
    var per = ri(lv(4, 5, 6), lv(6, 8, 12)), kids = ri(lv(20, 40, 60), lv(40, 99, 150)); if (kids % per === 0) return null;
    var v = Math.ceil(kids / per), t = pickOne([['children', 'van', 'seats'], ['eggs', 'box', 'holds'], ['books', 'shelf', 'holds']]);
    return mq(kids + ' ' + t[0] + '. Each ' + t[1] + ' ' + t[2] + ' ' + per + '. How many ' + (t[1] === 'box' ? 'boxes' : t[1] === 'shelf' ? 'shelves' : t[1] + 's') + ' are needed?', '', [[v, kids + ' ÷ ' + per + ' = ' + Math.floor(kids / per) + ' r ' + kids % per + ': the last ' + kids % per + ' need one more.'], [v - 1, 'Then ' + kids % per + ' ' + t[0] + ' have no place.'], [kids % per === v ? v + 2 : kids % per, 'That is the remainder.']]);
  });
  g4('m4_div', 3, function () {
    var d = ri(3, 9), q = ri(lv(5, 11, 21), lv(12, 25, 60)), r = ri(1, d - 1), n = d * q + r;
    return mq('Which checks that ' + n + ' ÷ ' + d + ' = ' + q + ' r ' + r + '?', '', [[q + ' × ' + d + ' + ' + r, q + ' × ' + d + ' = ' + d * q + ', and ' + d * q + ' + ' + r + ' = ' + n + '.'], [q + ' + ' + d + ' + ' + r, 'Multiply back, then add the remainder.'], [q + ' × ' + d + ' − ' + r, 'The remainder is added back on.']]);
  });

  // equal fractions
  g4('m4_frac', 1, function () {
    var b = pickOne([2, 3, 4, 5]), a = ri(1, b - 1), k = ri(2, lv(3, 4, 6));
    return mq(a + '/' + b + ' = __/' + b * k + '. What is the missing number?', '', [[a * k, 'The bottom was multiplied by ' + k + ', so the top is too: ' + a * k + '.'], [a + k, 'Multiply the top by ' + k + ', do not add.'], [a * k + 1, a + ' × ' + k + ' = ' + a * k + '.']]);
  });
  g4('m4_frac', 2, function () {
    var b = pickOne([5, 6, 8, 10, 12]), a = ri(1, b - 1), c = ri(1, b - 1); if (a === c) return null;
    return mq('Which is bigger: ' + a + '/' + b + ' or ' + c + '/' + b + '?', '', [[Math.max(a, c) + '/' + b, 'Same bottoms: the bigger top is bigger.'], [Math.min(a, c) + '/' + b, Math.min(a, c) + ' pieces is fewer than ' + Math.max(a, c) + ' pieces of the same size.'], ['They are the same', 'They have different numbers of pieces.']]);
  });
  g4('m4_frac', 3, function () {
    var b = pickOne([5, 6, 7, 8, 9, 10]), a = ri(1, b - 2), c = ri(1, b - 1 - a);
    return mq(a + '/' + b + ' + ' + c + '/' + b + ' = ?', '', [[(a + c) + '/' + b, 'Add the tops, keep the bottom: ' + (a + c) + '/' + b + '.'], [(a + c) + '/' + 2 * b, 'Keep the bottom: the pieces are still ' + b + 'ths.'], [a * c + '/' + b === (a + c) + '/' + b ? (a + c + 1) + '/' + b : a * c + '/' + b, 'Add the tops, do not multiply.']]);
  });
  g4('m4_frac', 4, function () {
    var b = pickOne(lv([2, 4], [3, 4, 5], [4, 5, 6, 8])), a = lv(1, ri(1, b - 1), ri(2, b - 1)), n = b * ri(lv(2, 3, 5), lv(6, 10, 15)), r = n / b * a;
    var w1 = n - r !== r ? n - r : r + b, w2 = a > 1 ? n / b : n - b; // the part left over; one part only (or taking b away)
    return mq('What is ' + a + '/' + b + ' of ' + n + '?', '', [[r, n + ' ÷ ' + b + ' = ' + n / b + (a > 1 ? ', and ' + a + ' × ' + n / b + ' = ' + r : '') + '.'], [w1, w1 === n - r ? 'That is the part left over.' : 'Share ' + n + ' into ' + b + ' equal parts.'], [w2, a > 1 ? 'That is only 1/' + b + '.' : 'Divide by ' + b + ', do not take ' + b + ' away.']]);
  });

  // decimals
  g4('m4_dec', 0, function () {
    var t = ri(1, 9), w = lv(0, ri(0, 3), ri(1, 9)), r = w + '.' + t;
    return mq('Which decimal means ' + (w ? w + ' wholes and ' : '') + t + ' tenths?', '', [[r, (w ? w + ' wholes' : 'No wholes') + ' before the point, ' + t + ' tenths after it.'], [t + '.' + w, 'Wholes go before the point, tenths after it.'], [w + '.0' + t, 'That is ' + t + ' hundredths.']]);
  });
  g4('m4_dec', 3, function () {
    var a = ri(lv(1, 1, 10), lv(9, 59, 99)) / 10, b = ri(lv(1, 1, 10), lv(9, 59, 99)) / 10; if (a === b) return null;
    return mq('Which is bigger: ' + a.toFixed(1) + ' or ' + b.toFixed(1) + '?', '', [[Math.max(a, b).toFixed(1), 'Compare the wholes first, then the tenths.'], [Math.min(a, b).toFixed(1), 'Look at the whole number before the point first.'], ['They are the same', 'They are different numbers.']]);
  });
  g4('m4_dec', 4, function () {
    var a = ri(lv(2, 5, 25), lv(9, 49, 199)), ap = pickOne([0, 25, 50, 75]), b = ri(lv(1, 2, 10), lv(5, 30, 150)), bp = pickOne([0, 25, 50, 75]), tot = a * 100 + ap + b * 100 + bp;
    var f = function (p) { return '₹' + Math.floor(p / 100) + '.' + (p % 100 < 10 ? '0' : '') + p % 100; };
    return mq(f(a * 100 + ap) + ' + ' + f(b * 100 + bp) + ' = ?', '', [[f(tot), 'Line up the points and add: ' + f(tot) + '.'], [f(tot - (ap + bp >= 100 ? 100 : -100)), ap + bp >= 100 ? 'The paise make one more rupee: carry it.' : 'Add the rupees and the paise separately.'], [f(Math.abs(a * 100 + ap - b * 100 - bp)), 'That takes away.']]);
  });
  g4('m4_dec', 2, function () {
    var r = ri(1, lv(5, 20, 99)), p = pickOne([10, 25, 50, 75]), tot = r * 100 + p;
    return mq('₹' + r + '.' + p + ' is how many paise?', '🪙', [[in4(tot), r + ' rupees = ' + r * 100 + ' paise, plus ' + p + ' = ' + in4(tot) + '.'], [in4(r + p), '1 rupee is 100 paise.'], [in4(r * 10 + p), '1 rupee is 100 paise, not 10.']]);
  });

  // changing units
  g4('m4_units', 0, function () {
    var U = pickOne([['km', 'm', 1000], ['kg', 'g', 1000], ['L', 'mL', 1000], ['m', 'cm', 100]]), a = ri(2, lv(5, 9, 25)), r = a * U[2];
    return mq(a + ' ' + U[0] + ' = how many ' + U[1] + '?', '', [[in4(r) + ' ' + U[1], '1 ' + U[0] + ' = ' + in4(U[2]) + ' ' + U[1] + ', so ' + a + ' ' + U[0] + ' = ' + in4(r) + ' ' + U[1] + '.'], [in4(a * U[2] / 10) + ' ' + U[1], '1 ' + U[0] + ' is ' + in4(U[2]) + ' ' + U[1] + '.'], [in4(a * U[2] * 10) + ' ' + U[1], 'That is too many: 1 ' + U[0] + ' = ' + in4(U[2]) + ' ' + U[1] + '.']]);
  });
  g4('m4_units', 1, function () {
    var U = pickOne([['kg', 'g'], ['L', 'mL'], ['km', 'm']]), a = ri(1, lv(4, 9, 19)), b = ri(1, 19) * 50, r = a * 1000 + b;
    return mq(a + ' ' + U[0] + ' ' + b + ' ' + U[1] + ' = how many ' + U[1] + '?', '', [[in4(r) + ' ' + U[1], a + ' ' + U[0] + ' = ' + in4(a * 1000) + ' ' + U[1] + ', plus ' + b + '.'], [in4(a * 100 + b) + ' ' + U[1], '1 ' + U[0] + ' = 1000 ' + U[1] + ', not 100.'], [in4(a + b) + ' ' + U[1], 'Change the ' + U[0] + ' into ' + U[1] + ' first.']]);
  });
  g4('m4_units', 4, function () {
    var a = ri(1, lv(3, 5, 9)), b = ri(2, 9) * 100, c = ri(2, 9) * 100, g = b + c, kg = a + Math.floor(g / 1000), rest = g % 1000;
    var f = function (k, gm) { return k + ' kg ' + gm + ' g'; };
    return mq(f(a, b) + ' + ' + c + ' g = ?', '🍎', [[f(kg, rest), b + ' g + ' + c + ' g = ' + in4(g) + ' g' + (g >= 1000 ? ' = 1 kg ' + rest + ' g' : '') + ', plus ' + a + ' kg.'], [f(a, g), g >= 1000 ? in4(g) + ' g is more than 1 kg: change it.' : 'Check the adding.'], [f(a + c / 100, b), 'The ' + c + ' is grams, not kilograms.']]);
  });

  // area and perimeter
  g4('m4_area', 2, function () {
    var l = ri(lv(3, 4, 8), lv(6, 12, 25)), w = ri(2, lv(5, 9, 15));
    return mq('What is the area of a rectangle ' + l + ' cm long and ' + w + ' cm wide?', '', [[l * w + ' square cm', l + ' × ' + w + ' = ' + l * w + '.'], [2 * (l + w) + ' square cm', 2 * (l + w) + ' cm is the perimeter.'], [(l + w) + ' square cm', 'That adds. Area is length × width.']]);
  });
  g4('m4_area', 3, function () {
    var sq = pickOne([true, false]), l = ri(lv(3, 5, 8), lv(9, 15, 40)), w = sq ? l : ri(2, l - 1), r = 2 * (l + w);
    return mq('What is the perimeter of a ' + (sq ? 'square with ' + l + ' cm sides' : 'rectangle ' + l + ' cm by ' + w + ' cm') + '?', '', [[in4(r) + ' cm', 'Add all four sides: ' + in4(r) + ' cm.'], [in4(l * w) + ' cm', 'That multiplies: that is the area.'], [(l + w) + ' cm', 'That is only two sides.']]);
  });
  g4('m4_area', 1, function () {
    var w = ri(2, lv(4, 7, 9)), l = ri(lv(3, 4, 6), lv(6, 9, 15)), a = l * w;
    return mq('A rectangle has an area of ' + a + ' square cm. It is ' + w + ' cm wide. How long is it?', '', [[l + ' cm', w + ' × ' + l + ' = ' + a + ', so it is ' + l + ' cm long.'], [(a - w) + ' cm', 'Divide the area by the width.'], [(l + 1) + ' cm', w + ' × ' + (l + 1) + ' = ' + w * (l + 1) + '.']]);
  });
  g4('m4_area', 4, function () {
    var x = pickOne([['a fence around a field', 'perimeter', 'A fence goes around the edge.'], ['carpet to cover a floor', 'area', 'The carpet covers the inside.'], ['a ribbon around a box lid', 'perimeter', 'The ribbon goes around the edge.'], ['paint for a wall', 'area', 'Paint covers the whole surface.'], ['tiles for a kitchen floor', 'area', 'Tiles cover the inside.'], ['a frame around a photo', 'perimeter', 'The frame goes around the edge.']]);
    return mq('For ' + x[0] + ', do you need the area or the perimeter?', '', [[x[1], x[2]], [x[1] === 'area' ? 'perimeter' : 'area', x[2]], ['neither', 'One of them is just right: ' + x[2].toLowerCase()]]);
  });

  // angles and turns
  g4('m4_angles', 4, function () {
    var T = [[3, 'a quarter turn'], [6, 'a half turn'], [9, 'a three-quarter turn'], [12, 'a full turn']], s = pickOne([12, 3, 6, 9]), t = pickOne(T), e = (s + t[0] - 1) % 12 + 1;
    var o = T.filter(function (x) { return x !== t; });
    return mq('The minute hand turns clockwise from ' + s + ' to ' + e + (t[0] === 12 ? ', all the way round' : '') + '. What turn is that?', '🕒', [[t[1], 'Each quarter of the clock is 3 numbers: ' + t[1] + '.'], [o[0][1], 'Count the quarters: each is 3 numbers on the clock.'], [o[1][1], 'Count the quarters: each is 3 numbers on the clock.']]);
  });
  g4('m4_angles', 2, function () {
    var X = [['the corner of a book', 'a right angle'], ['the corner of a door', 'a right angle'], ['a slice of pizza at its tip', 'an acute angle'], ['the open blades of scissors, a little apart', 'an acute angle'], ['a reclining chair leaning far back', 'an obtuse angle'], ['a fan opened wide', 'an obtuse angle'], ['an open book lying flat', 'a straight angle']], x = pickOne(X);
    var o = shuffled(['a right angle', 'an acute angle', 'an obtuse angle', 'a straight angle'].filter(function (k) { return k !== x[1]; })).slice(0, 2);
    var why = { 'a right angle': 'A square corner.', 'an acute angle': 'Smaller than a right angle: sharp.', 'an obtuse angle': 'Bigger than a right angle: wide open.', 'a straight angle': 'Two right angles: a straight line.' };
    return mq('What kind of angle is ' + x[0] + '?', '', [[x[1], why[x[1]]], [o[0], o[0][0].toUpperCase() + o[0].slice(1) + ' would be ' + why[o[0]].toLowerCase()], [o[1], o[1][0].toUpperCase() + o[1].slice(1) + ' would be ' + why[o[1]].toLowerCase()]]);
  });
  g4('m4_angles', 1, function () {
    var S = [['a square', 4, 'has'], ['a rectangle', 4, 'has'], ['a right-angled triangle', 1, 'has'], ['a straight angle', 2, 'makes'], ['a full turn', 4, 'makes'], ['a half turn', 2, 'makes']], x = pickOne(S);
    var o = shuffled([0, 1, 2, 3, 4, 5, 6].filter(function (k) { return k !== x[1]; })).slice(0, 2);
    return mq(x[2] === 'has' ? 'How many right angles does ' + x[0] + ' have?' : 'How many right angles make ' + x[0] + '?', '', [[x[1], x[0][0].toUpperCase() + x[0].slice(1) + ': ' + x[1] + ' right angle' + (x[1] > 1 ? 's' : '') + '.'], [o[0], 'Look for square corners, or count quarter turns.'], [o[1], 'Look for square corners, or count quarter turns.']]);
  });

  // factors and multiples
  g4('m4_factors', 0, function () {
    var n = ri(lv(2, 3, 6), lv(5, 9, 12)), r = n * ri(2, lv(5, 9, 12)), w = [r + 1, r + n - 1 === r ? r + 2 : r + n - 1].map(function (x) { return x % n ? x : x + 1; });
    return mq('Which number is a multiple of ' + n + '?', '', [[r, n + ' × ' + r / n + ' = ' + r + '.'], [w[0], w[0] + ' is not in the ' + n + ' times table.'], [w[1], w[1] + ' is not in the ' + n + ' times table.']]);
  });
  g4('m4_factors', 1, function () {
    var n = pickOne(lv([12, 16, 20], [18, 24, 30, 36], [42, 48, 56, 60, 72])), fs = []; for (var i = 2; i < n; i++) if (n % i === 0) fs.push(i);
    var nf = []; for (var j = 2; j < Math.min(n, 13); j++) if (n % j) nf.push(j); if (nf.length < 2) return null;
    var f = pickOne(fs), w = shuffled(nf).slice(0, 2);
    return mq('Which number is a factor of ' + n + '?', '', [[f, f + ' × ' + n / f + ' = ' + n + '.'], [w[0], n + ' ÷ ' + w[0] + ' leaves ' + n % w[0] + ' over.'], [w[1], n + ' ÷ ' + w[1] + ' leaves ' + n % w[1] + ' over.']]);
  });
  g4('m4_factors', 2, function () {
    var even = pickOne([true, false]), r = ri(lv(11, 101, 1001), lv(99, 999, 9999)); if ((r % 2 === 0) !== even) r++;
    return mq('Which number is ' + (even ? 'even' : 'odd') + '?', '', [[in4(r), in4(r) + ' ends in ' + r % 10 + '.'], [in4(r + 1), in4(r + 1) + ' ends in ' + (r + 1) % 10 + '.'], [in4(r + 3), in4(r + 3) + ' ends in ' + (r + 3) % 10 + '.']]);
  });
  g4('m4_factors', 3, function () {
    var P = pickOne(lv([[2, 3], [2, 5], [3, 5]], [[3, 4], [4, 6], [2, 7], [3, 7]], [[4, 6], [6, 8], [6, 9], [4, 10], [8, 12]])), a = P[0], b = P[1], l = a;
    while (l % b) l += a;
    return mq('What is the smallest number that is a multiple of both ' + a + ' and ' + b + '?', '', [[l, l + ' is in both times tables.'], [a + b, 'That adds them.'], [a * b === l ? l * 2 : a * b, a * b === l ? l * 2 + ' is a common multiple, but ' + l + ' is smaller.' : a * b + ' works, but ' + l + ' is smaller.']]);
  });
  g4('m4_factors', 4, function () {
    var k = pickOne([5, 10]), n = ri(lv(11, 101, 1001), lv(99, 999, 9999)), yes = pickOne([true, false]);
    if (yes) n = n - n % k; else if (n % k === 0) n += k === 5 ? 3 : 5;
    return mq('Is ' + in4(n) + ' a multiple of ' + k + '?', '', [[n % k === 0 ? 'Yes' : 'No', k === 5 ? 'Multiples of 5 end in 0 or 5; ' + in4(n) + ' ends in ' + n % 10 + '.' : 'Multiples of 10 end in 0; ' + in4(n) + ' ends in ' + n % 10 + '.'], [n % k === 0 ? 'No' : 'Yes', 'Look at the last digit.'], ['Only sometimes', 'A number either is or is not a multiple.']]);
  });

  // bar graphs
  function barRows() { var per = pickOne(lv([2, 5], [5, 10], [10, 20, 50])), days = shuffled(DAYS).slice(0, 4).sort(function (a, b) { return DAYS.indexOf(a) - DAYS.indexOf(b); }), vals = [];
    days.forEach(function () { var v; do { v = per * ri(1, 8); } while (vals.indexOf(v) >= 0); vals.push(v); }); return { per: per, rows: days.map(function (d, i) { return [d, vals[i]]; }) }; }
  g4('m4_graphs', 2, function () {
    var B = barRows(), most = pickOne([true, false]), s = B.rows.slice().sort(function (a, b) { return a[1] - b[1]; }), r = most ? s[3] : s[0], o = most ? [s[0], s[1]] : [s[3], s[2]];
    return mq('On which day were the ' + (most ? 'most' : 'fewest') + ' papers sold?', barsPic(B.rows, B.per), [[r[0], r[0] + ' has the ' + (most ? 'tallest' : 'shortest') + ' bar: ' + r[1] + '.'], [o[0][0], o[0][0] + ' sold ' + o[0][1] + '.'], [o[1][0], o[1][0] + ' sold ' + o[1][1] + '.']]);
  });
  g4('m4_graphs', 1, function () {
    var B = barRows(), x = pickOne(B.rows);
    return mq('How many papers were sold on ' + x[0] + '?', barsPic(B.rows, B.per), [[x[1], 'The ' + x[0] + ' bar reaches ' + x[1] + ': each line is ' + B.per + '.'], [x[1] / B.per === x[1] ? x[1] + B.per : x[1] / B.per, 'Each line stands for ' + B.per + ', not 1.'], [x[1] + B.per, 'Read the bar against the scale.']]);
  });
  g4('m4_graphs', 3, function () {
    var B = barRows(), p = shuffled(B.rows).slice(0, 2), a = p[0][1] > p[1][1] ? p[0] : p[1], b = a === p[0] ? p[1] : p[0];
    return mq('How many more papers were sold on ' + a[0] + ' than on ' + b[0] + '?', barsPic(B.rows, B.per), [[a[1] - b[1], a[1] + ' − ' + b[1] + ' = ' + (a[1] - b[1]) + '.'], [a[1] + b[1], 'That adds them.'], [a[1], a[1] + ' is ' + a[0] + ' alone.']]);
  });
  g4('m4_graphs', 4, function () {
    var B = barRows(), t = B.rows.reduce(function (s, r) { return s + r[1]; }, 0);
    return mq('How many papers were sold on these four days in all?', barsPic(B.rows, B.per), [[t, B.rows.map(function (r) { return r[1]; }).join(' + ') + ' = ' + t + '.'], [t - B.rows[0][1], 'Add ' + B.rows[0][0] + ' too.'], [t + B.per, 'Check the adding.']]);
  });

  // 24-hour time
  function hhmm(h, m) { return (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m; }
  function twelve(h, m) { var ap = h < 12 ? 'a.m.' : 'p.m.', hh = h % 12 || 12; return hh + ':' + (m < 10 ? '0' : '') + m + ' ' + ap; }
  g4('m4_time24', 1, function () {
    var h = ri(13, 23), m = pickOne(lv([0], [0, 30], [0, 15, 30, 45, 10, 50]));
    return mq(twelve(h, m) + ' in 24-hour time is…', '', [[hhmm(h, m), 'After noon, add 12: ' + (h - 12) + ' + 12 = ' + h + '.'], [hhmm(h - 12, m), 'In 24-hour time, afternoon hours are 13 to 23.'], [hhmm(h === 23 ? 22 : h + 1, m), (h - 12) + ' + 12 = ' + h + '.']]);
  });
  g4('m4_time24', 2, function () {
    var h = ri(13, 23), m = pickOne([0, 15, 30, 45]);
    return mq(hhmm(h, m) + ' is…', '', [[twelve(h, m), h + ' − 12 = ' + (h - 12) + ', after noon.'], [twelve(h - 12, m), 'Hours after 12 are p.m.'], [twelve(h === 23 ? 21 : h + 2, m), h + ' − 12 = ' + (h - 12) + '.']]);
  });
  g4('m4_time24', 3, function () {
    var h = ri(9, 18), m = pickOne([0, 15, 30, 45]), dh = ri(1, lv(2, 3, 4)), dm = pickOne(lv([0, 30], [15, 30, 45], [10, 20, 35, 50])), end = h * 60 + m + dh * 60 + dm;
    var d = function (x) { return Math.floor(x / 60) + ' h' + (x % 60 ? ' ' + x % 60 + ' min' : ''); }, dur = dh * 60 + dm;
    return mq('A film runs from ' + hhmm(h, m) + ' to ' + hhmm(Math.floor(end / 60), end % 60) + '. How long is it?', '🎬', [[d(dur), 'Count the hours, then the minutes: ' + d(dur) + '.'], [d(dur + 60), 'Count the whole hours again.'], [d(dur + (dm >= 30 ? -15 : 15)), 'Count the minutes carefully.']]);
  });
  g4('m4_time24', 4, function () {
    var shows = shuffled([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]).slice(0, 3).sort(function (a, b) { return a - b; }).map(function (h) { return [h, pickOne([0, 15, 30, 45])]; });
    var arrive = shows[0][0] + 1; if (arrive >= shows[1][0]) return null;
    return mq('Shows: ' + shows.map(function (s) { return hhmm(s[0], s[1]); }).join(', ') + '. If you arrive at ' + twelve(arrive, 0) + ', when is the next show?', '🎟️', [[hhmm(shows[1][0], shows[1][1]), twelve(arrive, 0) + ' is ' + hhmm(arrive, 0) + ', so the next show is ' + hhmm(shows[1][0], shows[1][1]) + '.'], [hhmm(shows[0][0], shows[0][1]), 'That show has already started.'], [hhmm(shows[2][0], shows[2][1]), 'There is an earlier show after you arrive.']]);
  });

  // the Big Bazaar: a mix of the lesson's ideas
  g4('m4_bazaar', 1, function () {
    var a = ri(lv(1000, 5000, 10000), lv(9999, 49999, 69999)), b = ri(lv(1000, 5000, 10000), lv(9999, 29999, 29999)), r = a + b;
    return mq(in4(a) + ' people came on Saturday and ' + in4(b) + ' on Sunday. How many in all?', '🛍️', [[in4(r), in4(a) + ' + ' + in4(b) + ' = ' + in4(r) + '.'], [in4(r - 1000), 'Remember the carried thousand.'], [in4(Math.abs(a - b)), 'That takes away.']]);
  });
  g4('m4_bazaar', 2, function () { var g = pickOne(GEN.m4_mult.concat(GEN.m4_div)); return g(); });
  g4('m4_bazaar', 3, function () { return pickOne(GEN.m4_dec.slice(2))(); });
  g4('m4_bazaar', 4, function () { return pickOne(GEN.m4_time24)(); });

  // 🌟 challenges for Grade 4 (several steps)
  // the challenge pool (CHALLENGE[4]) is set from this list in maths_extra.js
  var G4CHAL = [
    function () { var a = ri(12, 25), b = ri(6, 9), c = ri(3, 6), t = a * b; if (t % c) return null;
      return mq(a + ' crates hold ' + b + ' melons each. The melons are shared equally by ' + c + ' shops. How many melons does each shop get?', '🍉', [[t / c, a + ' × ' + b + ' = ' + t + ', then ' + t + ' ÷ ' + c + ' = ' + t / c + '.'], [t, 'Now share the ' + t + ' between ' + c + ' shops.'], [a * b / b === a ? a : t - c, 'Multiply first, then share.']]); },
    function () { var p = pickOne([45, 55, 65, 75, 85]), n = ri(3, 6), d = pickOne([20, 30, 50]), c = n * p - d, pay = c <= 500 ? 500 : 1000;
      return mq('Shirts cost ₹' + p + ' each. You buy ' + n + ' and get ₹' + d + ' off the bill. You pay ₹' + pay + '. How much change?', '👕', [['₹' + (pay - c), n + ' × ₹' + p + ' = ₹' + n * p + ', − ₹' + d + ' = ₹' + c + '. ₹' + pay + ' − ₹' + c + ' = ₹' + (pay - c) + '.'], ['₹' + (pay - n * p), 'Take the ₹' + d + ' off first.'], ['₹' + c, 'That is the bill, not the change.']]); },
    function () { var l = ri(8, 20), w = ri(5, 12), cost = pickOne([5, 10, 20]), per = 2 * (l + w);
      return mq('A garden is ' + l + ' m long and ' + w + ' m wide. Fencing costs ₹' + cost + ' a metre. How much does the fence cost?', '🏡', [['₹' + in4(per * cost), 'Perimeter: 2 × (' + l + ' + ' + w + ') = ' + per + ' m. ' + per + ' × ₹' + cost + ' = ₹' + in4(per * cost) + '.'], ['₹' + in4(l * w * cost), 'A fence goes around: use the perimeter, not the area.'], ['₹' + in4((l + w) * cost), 'A fence goes all the way round: four sides.']]); },
    function () { var h = ri(9, 14), m = pickOne([15, 30, 45]), a = ri(1, 2), b = pickOne([20, 40, 50]), e = h * 60 + m + a * 60 + b, end = hhmm(Math.floor(e / 60), e % 60);
      return mq('A train leaves at ' + hhmm(h, m) + ' and the journey takes ' + a + ' h ' + b + ' min. When does it arrive?', '🚆', [[end, 'Add the hours, then the minutes: ' + end + '.'], [hhmm(h + a, (m + b) % 60), 'There are only 60 minutes in an hour: carry the hour.'], [hhmm(Math.floor(e / 60) + 1, e % 60), 'Only ' + a + ' hour' + (a > 1 ? 's' : '') + ' and ' + b + ' minutes.']]); },
    function () { var k = ri(2, 5), t = k * 1000 + ri(1, 9) * 100, gl = pickOne([200, 250, 500]); if (t % gl) return null;
      return mq('A jug holds ' + k + ' L ' + (t - k * 1000) + ' mL of juice. How many ' + gl + ' mL glasses can be filled?', '🧃', [[t / gl, k + ' L ' + (t - k * 1000) + ' mL = ' + in4(t) + ' mL, and ' + in4(t) + ' ÷ ' + gl + ' = ' + t / gl + '.'], [Math.floor((k * 100 + (t - k * 1000)) / gl) || t / gl + 2, '1 L = 1000 mL, not 100 mL.'], [t / gl + 1, 'Check: ' + (t / gl + 1) + ' × ' + gl + ' = ' + in4((t / gl + 1) * gl) + ' mL.']]); },
  ];
