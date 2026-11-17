# Grade 2 Maths (Number Town · Market Street) and English (Story Library · Picture-book Corner).
# Each lesson: what it builds, its home card, the done screen, hand-written questions, quiz generators and flashcards.
# A question: (text, picture, step it tests, (right, why), (wrong, why), (wrong, why)[, sounds to play])
# Generators are JavaScript functions returning mq(text, picture, [[right, why], [wrong, why], ...]) (or null to retry).

def G(n, k, item, box=''):  # n groups of k, each in its basket / box / bundle
    return ''.join('<span class="qg">' + ('<i>%s</i>' % box if box else '') + (item * k if k <= 6 else '<span class="qgrid">' + ('<span>%s</span>' % item) * k + '</span>' if k <= 10 else item + '<b class="qn">×%d</b>' % k) + '</span>' for _ in range(n))
def MANY(n, item):  # loose things in rows of five
    if n > 20: return '<span class="qg">%s<b class="qn">×%d</b></span>' % (item, n)
    return ''.join('<span class="qrow">' + item * min(5, n - i) + '</span>' for i in range(0, n, 5))
def KIDS(n): return '<span class="qg qk">' + '🧒' * n + '</span>'
def COINS(*v): return ''.join('<span class="qc%s">₹%d</span>' % (' note' if x >= 20 else '', x) for x in v)

def Q(text, pic, step, *opts, snd=None):
    return dict(text=text, pic=pic, step=step, opts=list(opts), snd=snd)

MATHS = dict(id='maths', name='Maths', place='Number Town', grade='Grade 2', icon='➗', bg='#C3A6FF',
  floors=[('Market Street', 12)], levels=[('Grade 2', 'Market Street', '12 lessons: groups, shapes, numbers to 100, lines, adding and taking away, measuring, sharing, time, money, tallies, Market Day')],
  lessons=[
 dict(key='m2_groups', title='Counting in groups', part='fruit stall', icon='tx:2·4·6', bg='#FFC861',
  text='Count in twos, fives and tens instead of one by one.',
  done='You can count in groups! Come and see the fruit stall open on Market Street.',
  quiz=[Q('Count the shells in twos. How many?', G(4, 2, '🐚'), 0, ('8', '2, 4, 6, 8: four pairs make 8.'), ('4', '4 is how many pairs. Each pair has 2 shells.'), ('6', 'Count one more pair: 2, 4, 6, 8.')),
        Q('Count the fingers in fives. How many?', G(4, 1, '✋'), 1, ('20', '5, 10, 15, 20.'), ('4', 'That is how many hands. Each hand has 5 fingers.'), ('15', 'There are four hands: 5, 10, 15, 20.')),
        Q('Each bunch has 10 bananas. How many bananas?', G(3, 10, '🍌'), 2, ('30', '10, 20, 30.'), ('3', '3 is how many bunches, not bananas.'), ('13', 'Count in tens: 10, 20, 30.')),
        Q('3 plates with 4 laddoos on each. How many laddoos?', G(3, 4, '🟡', '🍽️'), 3, ('12', '4, 8, 12: three groups of 4 make 12.'), ('7', 'That adds 3 and 4. We need 3 groups of 4.'), ('10', 'Count again in fours: 4, 8, 12.')),
        Q('What comes next? 10, 20, 30, 40, __', '', 4, ('50', 'Every jump is 10, so 40 + 10 = 50.'), ('41', 'The jump is 10, not 1.'), ('45', 'That jump is 5. Here every jump is 10.'))],
  gen=[("""function () { var s = pickOne([2, 5, 10]), a = s * ri(1, 6), seq = [a, a + s, a + 2 * s, a + 3 * s];
        return mq('What comes next? ' + seq.join(', ') + ', __', '', [[a + 4 * s, 'Every jump is ' + s + ', so ' + seq[3] + ' + ' + s + ' = ' + (a + 4 * s) + '.'], [seq[3] + 1, 'The jump is ' + s + ', not 1.'], [a + 5 * s, 'That jumps twice. Add ' + s + ' once.']]); }""", 4),
       ("""function () { var g = ri(2, 5), k = ri(2, 5), f = pickOne(['🥭', '🍎', '🍊', '🍋']);
        return mq(g + ' baskets with ' + k + ' fruits each. How many fruits?', grp(g, k, f, '🧺'), [[g * k, 'Count in ' + k + 's ' + g + ' times: ' + g + ' groups of ' + k + ' make ' + g * k + '.'], [g + k, 'That adds ' + g + ' and ' + k + '. Count every fruit in every basket.'], [g * k + k, 'That counts one basket too many.']]); }""", 3),
       ("""function () { var n = ri(2, 9);
        return mq('Each bundle has 10 sticks. How many sticks in ' + n + ' bundles?', grp(n, 10, '🥢', '🪢'), [[n * 10, 'Count in tens: ' + n + ' tens make ' + n * 10 + '.'], [n, n + ' is how many bundles, not sticks.'], [n + 10, 'Count in tens, not ones.']]); }""", 2)],
  cards=[('How do you count in twos?', '2, 4, 6, 8, 10: jump 2 each time.'), ('Count in fives', '5, 10, 15, 20, 25'), ('4 groups of 3 makes how many?', '12: 3, 6, 9, 12.')]),

 dict(key='m2_shapes', title='Solid shapes', part='toy-block shop', icon='em:🎲', bg='#9FE3FF',
  text='Spheres, cubes, cylinders, cones and cuboids are all around you.',
  done='You know your solid shapes! Come and see the toy-block shop on Market Street.',
  quiz=[Q('Which one is a sphere?', '', 1, ('⚽ ball', 'A ball is round all over, so it is a sphere.'), ('🎲 dice', 'A dice has flat square faces: it is a cube.'), ('🥫 tin', 'A tin is a cylinder.')),
        Q('Which one is a cube?', '', 2, ('🎲 dice', 'A dice has 6 flat square faces, all the same.'), ('🍊 orange', 'An orange is round: a sphere.'), ('🍦 cone', 'That is a cone: round at one end, pointy at the other.')),
        Q('A tin of beans is shaped like a…', '🥫', 3, ('cylinder', 'Round at the top and bottom, straight sides: a cylinder.'), ('cube', 'A cube has square faces. A tin is round.'), ('cone', 'A cone has a point. A tin does not.')),
        Q('Which shape can roll and also stack?', '', 3, ('🥫 cylinder', 'It rolls on its side and stacks on its flat ends.'), ('⚽ sphere', 'A sphere rolls, but it will not stack.'), ('🎲 cube', 'A cube stacks, but it does not roll.')),
        Q('A brick is shaped like a…', '🧱', 4, ('cuboid', 'A brick is like a long box: a cuboid.'), ('sphere', 'A sphere is round like a ball.'), ('cylinder', 'A cylinder is round like a tin.'))],
  gen=[("""function () { var S = [['⚽ ball', 'sphere'], ['🍊 orange', 'sphere'], ['🌍 globe', 'sphere'], ['🎲 dice', 'cube'], ['🧊 ice cube', 'cube']], x = pickOne(S), other = x[1] === 'sphere' ? 'cube' : 'sphere';
        return mq('What shape is ' + an(x[0].split(' ').slice(1).join(' ')) + '?', x[0].split(' ')[0], [[x[1], x[1] === 'sphere' ? 'It is round all over, like a ball.' : 'It has 6 flat square faces.'], [other, other === 'cube' ? 'A cube has flat square faces.' : 'A sphere is round all over.'], ['cone', 'A cone has a point at the top.']]); }""", 1),
       ("""function () { var S = [['🥫 tin', 'cylinder'], ['🕯️ candle', 'cylinder'], ['🍦 ice-cream cone', 'cone'], ['🥳 party hat', 'cone'], ['🧱 brick', 'cuboid'], ['📕 book', 'cuboid']], x = pickOne(S), all = ['cylinder', 'cone', 'cuboid'];
        var why = { cylinder: 'Round ends and straight sides: a cylinder.', cone: 'Round at one end and pointy at the other: a cone.', cuboid: 'Like a long box with flat faces: a cuboid.' };
        return mq('What shape is ' + an(x[0].split(' ').slice(1).join(' ')) + '?', x[0].split(' ')[0], [[x[1], why[x[1]]]].concat(all.filter(function (s) { return s !== x[1]; }).map(function (s) { return [s, 'A ' + s + ' is different. ' + why[s]]; }))); }""", 3)],
  cards=[('What shape is a ball?', 'A sphere: round all over. It rolls.'), ('What shape is a dice?', 'A cube: 6 flat square faces.'), ('Which shape rolls and stacks?', 'A cylinder, like a tin.')]),

 dict(key='m2_numbers', title='Numbers to 100', part='house numbers', icon='tx:47', bg='#FFB547',
  text='Tens and ones, reading big numbers, and which is bigger.',
  done='You can read numbers up to 100! Come and see the house numbers go up on Market Street.',
  quiz=[Q('How many tens are in 47?', '▮▮▮▮ •••••••', 0, ('4', '47 is 4 tens and 7 ones.'), ('7', '7 is the ones. The tens digit is 4.'), ('47', '47 is the whole number. It has 4 tens.')),
        Q('Which number is sixty-three?', '', 1, ('63', 'Sixty is 6 tens, three is 3 ones: 63.'), ('36', '36 is thirty-six. The tens come first.'), ('603', 'We write sixty-three with just two digits.')),
        Q('What comes just after 59?', '', 2, ('60', '59 + 1 = 60: the ones are full, so we get a new ten.'), ('50', '50 comes before 59.'), ('510', 'After 59 comes 60, not 510.')),
        Q('Which is bigger?', '', 3, ('72', '72 has 7 tens; 27 has only 2 tens.'), ('27', '27 has only 2 tens. 72 has 7 tens.'), ('They are the same', 'They use the same digits, but 72 has more tens.')),
        Q('How many tens make 100?', '', 4, ('10', '10 tens are 100.'), ('100', '100 ones make 100, but we need tens: 10 of them.'), ('5', '5 tens are only 50.'))],
  gen=[("""function () { var t = ri(1, 9), o = ri(1, 9), n = t * 10 + o, askT = pickOne([true, false]);
        return mq('How many ' + (askT ? 'tens' : 'ones') + ' are in ' + n + '?', new Array(t + 1).join('▮') + ' ' + new Array(o + 1).join('•'), [[askT ? t : o, n + ' is ' + t + ' tens and ' + o + ' ones.'], [askT ? o : t, askT ? o + ' is the ones digit.' : t + ' is the tens digit.'], [n, n + ' is the whole number.']]); }""", 0),
       ("""function () { var n = ri(12, 98), after = pickOne([true, false]);
        return mq('What comes just ' + (after ? 'after ' : 'before ') + n + '?', '', [[after ? n + 1 : n - 1, after ? n + ' + 1 = ' + (n + 1) + '.' : n + ' − 1 = ' + (n - 1) + '.'], [after ? n - 1 : n + 1, after ? 'That comes before ' + n + '.' : 'That comes after ' + n + '.'], [after ? n + 10 : n - 10, 'That jumps a whole ten.']]); }""", 2),
       ("""function () { var a = ri(1, 9), b = ri(1, 9); if (a === b) return null; var x = a * 10 + b, y = b * 10 + a, big = Math.max(x, y), small = Math.min(x, y), lo = small - ri(1, 5);
        return mq('Which number is the biggest?', '', [[big, big + ' has the most tens.'], [small, small + ' has fewer tens than ' + big + '.'], [lo, lo + ' is smaller still.']]); }""", 3)],
  cards=[('What is 47 in tens and ones?', '4 tens and 7 ones.'), ('Which is bigger, 72 or 27?', '72: compare the tens first. 7 tens beats 2 tens.'), ('What comes after 59?', '60')]),

 dict(key='m2_flat', title='Flat shapes and shadows', part='shop signboards', icon='tx:● ▲ ■', bg='#FF8FC7',
  text='Circles, triangles, squares and rectangles, and their corners.',
  done='You know your flat shapes! Come and see the shop signboards go up.',
  quiz=[Q('A coin makes a shadow shaped like a…', '🪙', 0, ('circle', 'A coin is round, so its shadow is a circle.'), ('square', 'A square has corners. A coin has none.'), ('triangle', 'A triangle has 3 corners. A coin has none.')),
        Q('How many corners does a triangle have?', '▲', 2, ('3', 'A triangle has 3 sides and 3 corners.'), ('4', 'That is a square or rectangle.'), ('0', 'A circle has no corners. A triangle has 3.')),
        Q('Which shape has no corners?', '', 1, ('● circle', 'A circle is round all the way, with no corners.'), ('■ square', 'A square has 4 corners.'), ('▲ triangle', 'A triangle has 3 corners.')),
        Q('Which shape has 4 sides, all the same length?', '', 3, ('■ square', 'All 4 sides of a square are the same.'), ('▬ rectangle', 'A rectangle has 2 long and 2 short sides.'), ('▲ triangle', 'A triangle has only 3 sides.')),
        Q('A book cover is shaped like a…', '📕', 3, ('rectangle', '2 long sides and 2 short sides: a rectangle.'), ('circle', 'A book has corners. A circle does not.'), ('triangle', 'A book has 4 corners, not 3.'))],
  gen=[("""function () { var S = [['● circle', 0], ['▲ triangle', 3], ['■ square', 4], ['▬ rectangle', 4]], x = pickOne(S);
        var opts = [[x[1], 'A ' + x[0].split(' ')[1] + ' has ' + (x[1] || 'no') + ' corners.']].concat(shuffled([0, 3, 4, 5].filter(function (n) { return n !== x[1]; })).slice(0, 2).map(function (n) { return [n, 'Count the corners again.']; }));
        return mq('How many corners does a ' + x[0].split(' ')[1] + ' have?', x[0].split(' ')[0], opts); }""", 2),
       ("""function () { var S = [['🪙', 'coin', 'circle'], ['🕐', 'clock', 'circle'], ['🍪', 'biscuit', 'circle'], ['📕', 'book', 'rectangle'], ['🚪', 'door', 'rectangle'], ['📱', 'phone', 'rectangle'], ['⛺', 'tent', 'triangle'], ['🍕', 'pizza slice', 'triangle']], x = pickOne(S);
        return mq('The ' + x[1] + ' is shaped like a…', x[0], [[x[2], 'Look at its edges and corners: it is a ' + x[2] + '.']].concat(['circle', 'rectangle', 'triangle'].filter(function (s) { return s !== x[2]; }).map(function (s) { return [s, 'A ' + s + ' has a different number of corners.']; }))); }""", 0)],
  cards=[('How many corners does a triangle have?', '3 corners and 3 sides.'), ('Square or rectangle: which has all sides the same?', 'A square.'), ('Which flat shape has no corners?', 'A circle.')]),

 dict(key='m2_lines', title='Lines', part='road markings', icon='tx:| — /', bg='#B8F27C',
  text='Standing, sleeping, slanting and curved lines.',
  done='You know your lines! Come and see Nibb paint the road markings.',
  quiz=[Q('A lamp post is like a…', '|', 1, ('standing line', 'It goes straight up and down, like you standing tall.'), ('sleeping line', 'A sleeping line lies flat, like the road.'), ('curved line', 'A lamp post is straight, not curved.')),
        Q('The edge of the road is like a…', '—', 2, ('sleeping line', 'It lies flat from side to side.'), ('standing line', 'A standing line goes up and down.'), ('slanting line', 'The edge of the road is flat, not tilted.')),
        Q('A slide in the park is like a…', '/', 3, ('slanting line', 'It leans, high at one end and low at the other.'), ('sleeping line', 'A slide is not flat, or you would not slide!'), ('curved line', 'A straight slide is a slanting line.')),
        Q('A rainbow is like a…', '🌈', 4, ('curved line', 'A rainbow bends like an arch.'), ('standing line', 'A rainbow is not straight.'), ('slanting line', 'A rainbow bends: it is curved.')),
        Q('Which line is straight up and down?', '', 1, ('|', 'That is a standing line.'), ('—', 'That is a sleeping line.'), ('⌒', 'That is a curved line.'))],
  gen=[("""function () { var S = [['🧍 a flagpole', 'standing', 1], ['🛏️ a bed', 'sleeping', 2], ['🛝 a slide', 'slanting', 3], ['🌉 a bridge arch', 'curved', 4], ['🚪 a door edge', 'standing', 1], ['🎢 a ramp', 'slanting', 3]], x = pickOne(S);
        var q = mq(x[0].split(' ').slice(1).join(' ').replace(/^./, function (c) { return c.toUpperCase(); }) + ' is like a…', x[0].split(' ')[0], [[x[1] + ' line', 'Look at which way it goes.']].concat(shuffled(['standing', 'sleeping', 'slanting', 'curved'].filter(function (s) { return s !== x[1]; })).slice(0, 2).map(function (s) { return [s + ' line', 'Look again: it is a ' + x[1] + ' line.']; })));
        if (q) q.step = x[2]; return q; }""", 1),
       ("""function () { var S = [['|', 'standing', 1], ['—', 'sleeping', 2], ['/', 'slanting', 3], ['⌒', 'curved', 4]], x = pickOne(S);
        var q = mq('What kind of line is this?', x[0], [[x[1], 'This is a ' + x[1] + ' line.']].concat(shuffled(['standing', 'sleeping', 'slanting', 'curved'].filter(function (s) { return s !== x[1]; })).slice(0, 2).map(function (s) { return [s, 'Look again: it is ' + x[1] + '.']; })));
        if (q) q.step = x[2]; return q; }""", 1)],
  cards=[('A lamp post is like which line?', 'A standing line: |'), ('A slide is like which line?', 'A slanting line: /'), ('A rainbow is like which line?', 'A curved line: ⌒')]),

 dict(key='m2_addsub', title='Adding and taking away', part='festival lights', icon='tx:+ −', bg='#FFD27A',
  text='Add tens and ones, carry a ten, and take away.',
  done='You can add and take away! Come and see the festival lights shine on Market Street.',
  quiz=[Q('24 + 13 = ?', '', 0, ('37', 'Ones: 4 + 3 = 7. Tens: 2 + 1 = 3. So 37.'), ('27', 'Check the tens: 2 + 1 = 3.'), ('11', 'That adds the digits, not the numbers.')),
        Q('28 + 15 = ?', '', 1, ('43', '8 + 5 = 13: write 3, carry 1 ten. 2 + 1 + 1 = 4 tens.'), ('33', 'Do not forget the ten you carry.'), ('313', '13 ones is 1 ten and 3 ones. Carry the ten.')),
        Q('36 lights, 9 break. How many still shine?', '💡', 2, ('27', '36 − 9 = 27.'), ('45', 'That adds. Broken lights are taken away.'), ('33', 'Take away 9, not 3.')),
        Q('50 − 20 = ?', '', 3, ('30', '5 tens − 2 tens = 3 tens = 30.'), ('70', 'That adds the tens.'), ('48', 'Take away 2 tens, not 2 ones.')),
        Q('27 + 9 = 36. So 36 − 9 = ?', '', 4, ('27', 'Adding back checks it: 27 + 9 = 36.'), ('45', '36 + 9 is 45. We take away.'), ('9', '9 is the part we take away.'))],
  gen=[("""function () { var a = ri(1, 4) * 10 + ri(1, 4), b = ri(1, 4) * 10 + ri(1, 5), r = a + b;
        return mq(a + ' + ' + b + ' = ?', '', [[r, 'Ones: ' + a % 10 + ' + ' + b % 10 + ' = ' + (a % 10 + b % 10) + '. Tens: ' + Math.floor(a / 10) + ' + ' + Math.floor(b / 10) + ' = ' + Math.floor(r / 10) + '.'], [r + 10, 'Check the tens again.'], [r - 1, 'Check the ones again.']]); }""", 0),
       ("""function () { var ao = ri(5, 9), bo = ri(10 - ao, 9), a = ri(1, 4) * 10 + ao, b = ri(1, 4) * 10 + bo, r = a + b;
        return mq(a + ' + ' + b + ' = ?', '', [[r, ao + ' + ' + bo + ' = ' + (ao + bo) + ': write ' + (ao + bo - 10) + ', carry 1 ten.'], [r - 10, 'You forgot to carry the ten.'], [r + 1, 'Check the ones: ' + ao + ' + ' + bo + ' = ' + (ao + bo) + '.']]); }""", 1),
       ("""function () { var b = ri(3, 9), a = ri(2, 6) * 10 + ri(0, b - 1), r = a - b, f = pickOne([['💡', 'lights', 'break'], ['🎈', 'balloons', 'pop'], ['🪔', 'lamps', 'go out']]);
        return mq(a + ' ' + f[1] + ', ' + b + ' ' + f[2] + '. How many are left?', f[0], [[r, a + ' − ' + b + ' = ' + r + '.'], [a + b, 'That adds. We take away.'], [r + 10, 'You need to break a ten: ' + a + ' − ' + b + ' = ' + r + '.']]); }""", 2),
       ("""function () { var a = ri(4, 9), b = ri(1, a - 1);
        return mq(a * 10 + ' − ' + b * 10 + ' = ?', '', [[(a - b) * 10, a + ' tens − ' + b + ' tens = ' + (a - b) + ' tens.'], [(a + b) * 10, 'That adds the tens.'], [a * 10 - b, 'Take away ' + b + ' tens, not ' + b + ' ones.']]); }""", 3)],
  cards=[('What do you do when the ones add up to 10 or more?', 'Carry 1 ten to the tens.'), ('36 − 9 = ?', '27'), ('How can you check 36 − 9 = 27?', 'Add back: 27 + 9 = 36.')]),

 dict(key='m2_measure', title='Long, short, heavy, light', part="tailor's shop", icon='em:📏', bg='#8FD3FF',
  text='Measure with hand spans and centimetres; compare heavy and light.',
  done="You can measure! Come and see the tailor's shop open.",
  quiz=[Q('Which ribbon is longer?', '', 2, ('21 cm', '21 is more than 12, so it is longer.'), ('12 cm', '12 cm is shorter than 21 cm.'), ('They are the same', '12 and 21 are different numbers.')),
        Q('Why do we use a ruler instead of hand spans?', '📏', 2, ('A ruler is the same for everyone', 'Hands are different sizes; centimetres are not.'), ('Hands are too small', 'Hands work, but they are not all the same size.'), ('Rulers are heavy', 'Weight does not matter for measuring length.')),
        Q('Which is heavier?', '', 3, ('🍉 watermelon', 'A watermelon is much heavier than a feather.'), ('🪶 feather', 'A feather is very light.'), ('They are the same', 'A watermelon is far heavier.')),
        Q('On a balance, which side goes down?', '⚖️', 4, ('The heavier side', 'The heavier thing pulls its side down.'), ('The lighter side', 'The lighter side goes up.'), ('Both sides', 'Only the heavier side goes down.')),
        Q('A table is 5 hand spans long. You measure 1 more span. How many spans now?', '✋✋✋✋✋', 1, ('6', '5 + 1 = 6 spans.'), ('5', 'You added one more span.'), ('4', 'That takes one away.'))],
  gen=[("""function () { var a = ri(8, 25), b = ri(3, a - 2), t = pickOne([['✏️', 'pencil', 'crayon'], ['🎀', 'red ribbon', 'blue ribbon'], ['🥢', 'stick', 'straw']]);
        return mq('The ' + t[1] + ' is ' + a + ' cm. The ' + t[2] + ' is ' + b + ' cm. How much longer is the ' + t[1] + '?', t[0], [[(a - b) + ' cm', a + ' − ' + b + ' = ' + (a - b) + '.'], [(a + b) + ' cm', 'That adds them. We want the difference.'], [a + ' cm', 'That is the whole ' + t[1] + '.']]); }""", 2),
       ("""function () { var P = [['🍉 watermelon', '🍓 strawberry'], ['🐘 elephant', '🐭 mouse'], ['🎒 school bag', '✏️ pencil'], ['🧱 brick', '🪶 feather'], ['🎃 pumpkin', '🥜 peanut']], x = pickOne(P);
        return mq(an(x[0].split(' ').slice(1).join(' ')).replace(/^./, function (c) { return c.toUpperCase(); }) + ' and ' + an(x[1].split(' ').slice(1).join(' ')) + ' are on a balance. Which side goes down?', '⚖️', [[x[0], 'The ' + x[0].split(' ').slice(1).join(' ') + ' is heavier, so its side goes down.'], [x[1], 'The ' + x[1].split(' ').slice(1).join(' ') + ' is lighter, so its side goes up.'], ['They stay level', 'They only stay level when both weigh the same.']]); }""", 4)],
  cards=[('Why use centimetres instead of hand spans?', 'A ruler is the same for everyone; hands are different sizes.'), ('On a balance, which side goes down?', 'The heavier side.'), ('Which is longer: 12 cm or 21 cm?', '21 cm.')]),

 dict(key='m2_share', title='Equal groups and sharing', part='sweet-box shop', icon='tx:12÷3', bg='#FFB0D8',
  text='Groups of the same size, times, and sharing fairly.',
  done='You can share fairly! Come and see the sweet-box shop on Market Street.',
  quiz=[Q('3 boxes with 4 sweets in each. How many sweets?', G(3, 4, '🍬', '📦'), 0, ('12', '4, 8, 12: 3 groups of 4.'), ('7', 'That adds 3 and 4.'), ('34', 'We count the sweets, not write the digits together.')),
        Q('What does 3 × 4 mean?', '', 1, ('3 groups of 4', '× means groups of.'), ('3 plus 4', 'That is 3 + 4. × means groups of.'), ('3 take away 4', 'That would be −. × means groups of.')),
        Q('12 sweets shared equally by 3 friends. How many each?', MANY(12, '🍬') + KIDS(3), 2, ('4', '12 ÷ 3 = 4: each friend gets 4.'), ('9', 'That takes 3 away. We share.'), ('3', '3 is how many friends.')),
        Q('3 × 4 = 12. So 12 ÷ 3 = ?', '', 3, ('4', 'Times and sharing are partners.'), ('12', '12 is how many sweets in all.'), ('36', 'That multiplies again.')),
        Q('7 sweets shared by 2 friends. How many are left over?', MANY(7, '🍬') + KIDS(2), 4, ('1', 'Each gets 3, which uses 6. One is left.'), ('0', '7 does not share evenly by 2.'), ('3', '3 is how many each friend gets.'))],
  gen=[("""function () { var a = ri(2, 5), b = ri(2, 5);
        return mq(a + ' × ' + b + ' = ?', grp(a, b, '🍬', '📦'), [[a * b, a + ' groups of ' + b + ' make ' + a * b + '.'], [a + b, 'That adds. × means groups of.'], [a * b + b, 'Count the groups again: there are ' + a + '.']]); }""", 1),
       ("""function () { var k = ri(2, 5), e = ri(2, 6), n = k * e, f = pickOne([['🍬', 'sweets'], ['🍪', 'biscuits'], ['🟡', 'laddoos']]);
        return mq(n + ' ' + f[1] + ' shared equally by ' + k + ' friends. How many each?', many(n, f[0]) + kids(k), [[e, n + ' ÷ ' + k + ' = ' + e + '.'], [n - k, 'That takes ' + k + ' away. We share.'], [k, k + ' is how many friends.']]); }""", 2),
       ("""function () { var k = pickOne([2, 3]), n = ri(5, 14); if (n % k === 0) return null;
        return mq(n + ' sweets shared by ' + k + ' friends. How many are left over?', many(n, '🍬') + kids(k), [[n % k, 'Each gets ' + Math.floor(n / k) + ', which uses ' + (Math.floor(n / k) * k) + '. ' + (n % k) + ' left.'], [0, n + ' does not share evenly by ' + k + '.'], [Math.floor(n / k), 'That is how many each friend gets.']]); }""", 4)],
  cards=[('What does × mean?', 'Groups of: 3 × 4 is 3 groups of 4.'), ('12 ÷ 3 = ?', '4: share 12 into 3 equal groups.'), ('7 shared by 2: how many left over?', '1 (each gets 3).')]),

 dict(key='m2_time', title='Time and seasons', part='clock tower', icon='em:🕗', bg='#C3A6FF',
  text="Days, months, o'clock, half past and the seasons.",
  done='You can tell the time! Come and see the clock tower rise over Market Street.',
  quiz=[Q('What day comes after Tuesday?', '', 0, ('Wednesday', 'Monday, Tuesday, Wednesday.'), ('Monday', 'Monday comes before Tuesday.'), ('Friday', 'Friday is later in the week.')),
        Q('How many months are in a year?', '', 1, ('12', 'January to December: 12 months.'), ('7', '7 is the days in a week.'), ('10', 'Count again: there are 12.')),
        Q('What time is it?', '🕗', 2, ("8 o'clock", 'The long hand is on 12, the short hand on 8.'), ('half past 8', 'For half past, the long hand points to 6.'), ("12 o'clock", 'The short hand shows the hour: 8.')),
        Q('The long hand points to 6. It is…', '🕣', 3, ('half past', 'Long hand on 6 means half past.'), ("o'clock", "For o'clock, the long hand is on 12."), ('midnight', 'Look at where the hands point.')),
        Q('When do mangoes grow?', '🥭', 4, ('summer', 'Mangoes come in the hot summer.'), ('winter', 'Winter is cold. Mangoes come in summer.'), ('monsoon', 'The monsoon brings rain. Mangoes come before it, in summer.'))],
  gen=[("""function () { var h = ri(1, 12), half = pickOne([true, false]), cp = String.fromCodePoint(0x1F54F + h + (half ? 12 : 0)), right = half ? 'half past ' + h : h + " o'clock", h2 = h % 12 + 1;
        return mq('What time is it?', cp, [[right, half ? 'The long hand is on 6, so it is half past ' + h + '.' : 'The long hand is on 12 and the short hand on ' + h + '.'], [half ? h + " o'clock" : 'half past ' + h, half ? "For o'clock the long hand is on 12." : 'For half past the long hand is on 6.'], [h2 + " o'clock", 'The short hand shows the hour: ' + h + '.']]); }""", 2),
       ("""function () { var D = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], i = ri(0, 6), after = pickOne([true, false]);
        return mq('What day comes ' + (after ? 'after ' : 'before ') + D[i] + '?', '📅', [[D[(i + (after ? 1 : 6)) % 7], 'The week goes Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.'], [D[(i + (after ? 6 : 1)) % 7], after ? 'That comes before ' + D[i] + '.' : 'That comes after ' + D[i] + '.'], [D[(i + 3) % 7], 'That is further away in the week.']]); }""", 0),
       ("""function () { var M = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], i = ri(0, 11);
        return mq('Which month comes after ' + M[i] + '?', '🗓️', [[M[(i + 1) % 12], 'The months go in order, January to December, then back to January.'], [M[(i + 11) % 12], 'That comes before ' + M[i] + '.'], [M[(i + 2) % 12], 'That is two months later.']]); }""", 1)],
  cards=[('How many days are in a week?', '7'), ("Where is the long hand at o'clock?", 'On 12.'), ('Where is the long hand at half past?', 'On 6.')]),

 dict(key='m2_money', title='Money', part='coin stall', icon='tx:₹20', bg='#7CF5C8',
  text='Coins and notes, adding prices and giving change.',
  done='You can pay and give change! Come and see the coin stall at the fair.',
  quiz=[Q('₹10 + ₹5 + ₹5 = ?', COINS(10, 5, 5), 1, ('₹20', '10 + 5 + 5 = 20.'), ('₹15', 'Add both ₹5 coins.'), ('₹105', 'Add the amounts, do not write them side by side.')),
        Q('A balloon costs ₹15. You pay ₹20. How much change?', '🎈 ' + COINS(20), 3, ('₹5', '₹20 − ₹15 = ₹5.'), ('₹35', 'That adds. Change is what is left.'), ('₹15', 'That is the price.')),
        Q('A kite costs ₹12 and a ball ₹8. How much for both?', '🪁 ⚽', 4, ('₹20', '12 + 8 = 20.'), ('₹4', 'That takes away. For both, we add.'), ('₹12', 'That is only the kite.')),
        Q('Which is the biggest note?', '', 0, ('₹100', '100 is the most.'), ('₹50', '50 is less than 100.'), ('₹20', '20 is less than 100.')),
        Q('You have ₹20. A toy costs ₹25. Can you buy it?', '🧸', 2, ('No, you need ₹5 more', '25 is more than 20.'), ('Yes, with ₹5 left', '25 is more than 20, so there is not enough.'), ('Yes, exactly', '₹20 is not the same as ₹25.'))],
  gen=[("""function () { var c = [pickOne([1, 2, 5, 10]), pickOne([1, 2, 5, 10]), pickOne([1, 2, 5])], t = c[0] + c[1] + c[2];
        return mq(c.map(function (x) { return '₹' + x; }).join(' + ') + ' = ?', coins(c), [['₹' + t, c.join(' + ') + ' = ' + t + '.'], ['₹' + (t - c[2]), 'Add all three coins.'], ['₹' + (t + 1), 'Add again carefully.']]); }""", 1),
       ("""function () { var pay = pickOne([20, 50]), p = ri(pay - 18, pay - 2), t = pickOne([['🎈', 'A balloon'], ['🍦', 'An ice cream'], ['🪀', 'A yo-yo'], ['📒', 'A notebook']]);
        return mq(t[1] + ' costs ₹' + p + '. You pay ₹' + pay + '. How much change?', t[0] + ' ' + coins([pay]), [['₹' + (pay - p), '₹' + pay + ' − ₹' + p + ' = ₹' + (pay - p) + '.'], ['₹' + (pay + p), 'That adds. Change is what is left.'], ['₹' + p, 'That is the price.']]); }""", 3),
       ("""function () { var a = ri(5, 25), b = ri(3, 20), t = shuffled([['🪁', 'kite'], ['⚽', 'ball'], ['🍫', 'chocolate'], ['🧃', 'juice']]).slice(0, 2);
        return mq('A ' + t[0][1] + ' costs ₹' + a + ' and a ' + t[1][1] + ' ₹' + b + '. How much for both?', t[0][0] + ' ' + t[1][0], [['₹' + (a + b), a + ' + ' + b + ' = ' + (a + b) + '.'], ['₹' + Math.abs(a - b), 'That takes away. For both, we add.'], ['₹' + a, 'That is only the ' + t[0][1] + '.']]); }""", 4)],
  cards=[('₹10 + ₹5 + ₹5 = ?', '₹20'), ('How do you work out change?', 'Take the price away from what you pay: ₹20 − ₹15 = ₹5.'), ('Name three coins.', '₹1, ₹2, ₹5 (and ₹10).')]),

 dict(key='m2_data', title='Counting with tallies', part='tally board', icon='tx:||||', bg='#FF9A8B',
  text='Tally marks, picture charts, most and least.',
  done='You can count with tallies! Come and see the tally board at the market gate.',
  quiz=[Q('How many tally marks?', '<s>||||</s> ||', 1, ('7', 'A crossed group is 5, then 2 more: 7.'), ('6', 'The crossed group counts as 5. Then add 2.'), ('5', 'Do not forget the 2 marks after the group.')),
        Q('Why do we cross the fifth tally mark?', '<s>||||</s>', 0, ('To make groups of 5, easy to count', 'Then we count in fives.'), ('Because it is wrong', 'It is not wrong: it closes a group of 5.'), ('To make it look nice', 'It helps us count in fives.')),
        Q('🍎 7 · 🍌 3 · 🍊 5. Which fruit has the most?', '', 2, ('🍎 apples', '7 is the biggest number.'), ('🍌 bananas', '3 is the least.'), ('🍊 oranges', '5 is less than 7.')),
        Q('🍎 7 · 🍌 3. How many more apples than bananas?', '', 4, ('4', '7 − 3 = 4.'), ('10', 'That adds them. We want how many more.'), ('3', '3 is the bananas.')),
        Q('In a picture chart, each 🍌 is one banana. How many?', '🍌🍌🍌', 3, ('3', 'Count the pictures: 3.'), ('1', 'Each picture is one. There are 3 pictures.'), ('5', 'Count the pictures again.'))],
  gen=[("""function () { var n = ri(3, 14), g = Math.floor(n / 5), r = n % 5, s = new Array(g + 1).join('<s>||||</s> ') + new Array(r + 1).join('|');
        return mq('How many tally marks?', s.trim(), [[n, g ? g + ' crossed group' + (g > 1 ? 's' : '') + ' of 5' + (r ? ' and ' + r + ' more' : '') + ': ' + n + '.' : 'Count each mark: ' + n + '.'], [n + 1, 'A crossed group is 5 marks, not 6.'], [g + r, 'Each crossed group is 5, not 1.']]); }""", 1),
       ("""function () { var F = shuffled([['🍎', 'apples'], ['🍌', 'bananas'], ['🍊', 'oranges'], ['🍇', 'grapes']]).slice(0, 3), c = shuffled([ri(1, 3), ri(4, 5), ri(6, 8)]), most = pickOne([true, false]);
        var ix = c.indexOf(most ? Math.max.apply(null, c) : Math.min.apply(null, c));
        return mq(F.map(function (f, i) { return f[0] + ' ' + c[i]; }).join(' · ') + '. Which has the ' + (most ? 'most' : 'least') + '?', '', [[F[ix][0] + ' ' + F[ix][1], c[ix] + ' is the ' + (most ? 'biggest' : 'smallest') + ' number.']].concat(F.filter(function (f, i) { return i !== ix; }).map(function (f) { return [f[0] + ' ' + f[1], 'Compare the numbers again.']; }))); }""", 2),
       ("""function () { var a = ri(5, 9), b = ri(1, a - 1);
        return mq('🍎 ' + a + ' · 🍌 ' + b + '. How many more apples than bananas?', new Array(a + 1).join('🍎') + '\\n' + new Array(b + 1).join('🍌'), [[a - b, a + ' − ' + b + ' = ' + (a - b) + '.'], [a + b, 'That adds them.'], [b, 'That is the bananas.']]); }""", 4)],
  cards=[('What does a crossed group of tally marks mean?', '5'), ('How do you find which has the most?', 'Find the biggest number.'), ('7 apples, 3 bananas: how many more apples?', '4 (7 − 3).')]),

 dict(key='m2_challenge', title='the Market Day challenge', part='market gate', icon='boss', bg='#FF7A6B', challenge=True,
  text='Run a stall: count the stock, share it, add prices and give change.',
  done='You finished Market Street! The market gate is up, with bunting. Come and see.',
  quiz=[Q('4 crates with 5 mangoes each. How many mangoes?', G(4, 5, '🥭', '📦'), 1, ('20', '5, 10, 15, 20.'), ('9', 'That adds 4 and 5.'), ('45', 'Count in fives, 4 times.')),
        Q('20 mangoes into 4 bags equally. How many in each bag?', MANY(20, '🥭') + '<span class="qg">🛍️🛍️🛍️🛍️</span>', 2, ('5', '20 ÷ 4 = 5.'), ('16', 'That takes 4 away. We share.'), ('4', '4 is how many bags.')),
        Q('₹25 + ₹14 = ?', '', 3, ('₹39', '25 + 14 = 39.'), ('₹11', 'That takes away. We add.'), ('₹29', 'Check the tens: 2 + 1 = 3.')),
        Q('A customer pays ₹50 for ₹39. How much change?', '💵', 4, ('₹11', '50 − 39 = 11.'), ('₹89', 'That adds. Change is what is left.'), ('₹21', 'Check: 39 + 11 = 50.')),
        Q('Which shape is the mango crate?', '📦', 0, ('cuboid', 'A crate is a box: a cuboid.'), ('sphere', 'A sphere is round like a ball.'), ('cone', 'A cone has a point.'))],
  gen=[("""function () { var c = ri(2, 6), k = pickOne([5, 10]);
        return mq(c + ' crates with ' + k + ' fruits each. How many fruits?', grp(c, k, pickOne(['🍎', '🥭', '🍊']), '📦'), [[c * k, 'Count in ' + k + 's: ' + c + ' groups of ' + k + ' make ' + c * k + '.'], [c + k, 'That adds ' + c + ' and ' + k + '.'], [c * k + k, 'That counts one crate too many.']]); }""", 1),
       ("""function () { var k = ri(2, 5), e = ri(2, 6), n = k * e;
        return mq(n + ' mangoes into ' + k + ' bags equally. How many in each bag?', many(n, '🥭') + '<span class="qg">' + rpt('🛍️', k) + '</span>', [[e, n + ' ÷ ' + k + ' = ' + e + '.'], [n - k, 'That takes ' + k + ' away. We share.'], [k, k + ' is how many bags.']]); }""", 2),
       ("""function () { var p = ri(21, 48);
        return mq('A customer pays ₹50 for ₹' + p + '. How much change?', coins([50]), [['₹' + (50 - p), '₹50 − ₹' + p + ' = ₹' + (50 - p) + '.'], ['₹' + (50 + p), 'That adds. Change is what is left.'], ['₹' + (60 - p), 'Check by adding back: ' + p + ' + ' + (50 - p) + ' = 50.']]); }""", 4)],
  cards=[('Market Day: 4 crates of 5. How many?', '20'), ('Market Day: ₹50 for ₹39. Change?', '₹11'), ('How do you check change?', 'Add it back to the price: ₹39 + ₹11 = ₹50.')]),
])

# ---------------- English ----------------
# picture words for the phonics questions (every one has a clip w_<word>)
PIC = {'cat': '🐱', 'hat': '🎩', 'bat': '🦇', 'map': '🗺️', 'pan': '🍳', 'pin': '📌', 'pig': '🐷', 'dog': '🐶', 'sun': '☀️', 'bus': '🚌',
       'cup': '☕', 'net': '🥅', 'hen': '🐔', 'pen': '🖊️', 'bed': '🛏️', 'pot': '🍲', 'tap': '🚰', 'hut': '🛖', 'bag': '👜', 'bun': '🍞',
       'ant': '🐜', 'rat': '🐀', 'log': '🪵', 'leg': '🦵', 'cap': '🧢', 'egg': '🥚', 'bin': '🗑️', 'nut': '🥜', 'ten': '🔟', 'bug': '🐛',
       'man': '👨', 'lip': '👄', 'kid': '🧒', 'fin': '🦈', 'red': '🟥', 'six': '6️⃣',
       'ship': '🚢', 'fish': '🐟', 'shell': '🐚', 'chips': '🍟', 'chick': '🐤', 'cheese': '🧀', 'thumb': '👍', 'bath': '🛁', 'moth': '🦋',
       'ring': '💍', 'king': '👑', 'swing': '🛝', 'rain': '🌧️', 'train': '🚂', 'snail': '🐌', 'tree': '🌳', 'bee': '🐝', 'sheep': '🐑',
       'boat': '⛵', 'goat': '🐐', 'coat': '🧥', 'cake': '🎂', 'kite': '🪁', 'bike': '🚲', 'bone': '🦴', 'rose': '🌹', 'cube': '🧊'}
del PIC['six'], PIC['moth']  # x is not taught yet; a moth emoji looks like a butterfly
# letter sounds: how the voice says the pure sound, a word that shows it
SOUNDS = {'s': ('sss', 'sun'), 'a': ('ah', 'ant'), 't': ('tuh', 'tap'), 'p': ('puh', 'pen'), 'i': ('ih', 'ink'), 'n': ('nnn', 'net'),
          'm': ('mmm', 'map'), 'd': ('duh', 'dog'), 'g': ('guh', 'gate'), 'o': ('aw', 'on'), 'c': ('kuh', 'cat'), 'k': ('kuh', 'kite'),
          'e': ('eh', 'egg'), 'u': ('uh', 'up'), 'r': ('rrr', 'rat'), 'h': ('hhh', 'hat'), 'b': ('buh', 'bat'), 'f': ('fff', 'fish'), 'l': ('lll', 'leg'),
          'sh': ('shhh', 'ship'), 'ch': ('chuh', 'chips'), 'th': ('thhh', 'thumb'), 'ng': ('ng', 'ring'),
          'ai': ('ay', 'rain'), 'ee': ('ee', 'tree'), 'oa': ('oh', 'boat')}

JS_EN = r"""
  // ---- English: picture words and phonics sounds (clips live in one sound sheet per voice) ----
  var EPIC = %(PIC)s;
  var CVC = Object.keys(EPIC).filter(function (w) { return w.length === 3 && /^[^aeiou][aeiou][^aeiou]$/.test(w); });
  var VOW = ['a', 'e', 'i', 'o', 'u'];
  var REAL = {}; ('bat cat hat mat rat sat pat fat bed red fed led wed big dig pig wig fig dog log hog fog jog cog bog bun fun run sun gun nun pun cap map tap nap lap gap sap hen pen ten den men pin bin tin win fin sin din pot hot dot not got cot lot rot bus cup pup hut nut cut but gut rut bag rag tag wag sag nag net wet set get let pet met jet bet pan can man fan ran tan van ban mad sad dad bad had pad lad mud bud hop mop top pop cop sip tip hip dip lip rip sit bit hit pit kit fit bib cab dab jab nab tab cub hub rub sub tub web gum hum mum sum bug hug jug mug rug dug pug tug ham jam ram yam dam him dim rim hem gem peg leg beg keg mob cob job rob sob nod pod rod cod hid lid kid bid did rid mid pet pit pat put ant').split(' ').forEach(function (w) { REAL[w] = 1; });
  function wopt(w) { return EPIC[w] + ' ' + w; }
  // Which picture starts with this sound? (letters: the sounds taught so far)
  function genStart(letters) { return function () {
    var pool = CVC.concat(['ant', 'egg']).filter(function (w) { return letters.indexOf(w[0]) >= 0; }); if (!pool.length) return null;
    var w = pickOne(pool), first = function (x) { return x[0] === 'k' ? 'c' : x[0]; }, others = shuffled(Object.keys(EPIC).filter(function (x) { return first(x) !== first(w) && x.slice(0, 2) !== 'ch' && x.slice(0, 2) !== 'sh' && x.slice(0, 2) !== 'th'; })).slice(0, 2);
    var q = mq('Which picture starts with this sound?', '🔊', [[wopt(w), w + ' starts with ' + w[0] + '.']].concat(others.map(function (x) { return [wopt(x), x + ' starts with ' + x[0] + ', not ' + w[0] + '.']; })));
    if (q) q.snd = ['q_start', 'snd_' + w[0]]; return q; }; }
  // Blend the sounds: which word is it?
  function genBlend(letters) { return function () {
    var pool = CVC.filter(function (w) { return w.split('').every(function (c) { return letters.indexOf(c) >= 0; }); }); if (pool.length < 3) return null;
    var w = pickOne(pool), near = shuffled(CVC.filter(function (x) { return x !== w && (x[0] === w[0] || x[1] === w[1] || x[2] === w[2]); }));
    if (near.length < 2) near = near.concat(shuffled(CVC.filter(function (x) { return x !== w && near.indexOf(x) < 0; })));
    var q = mq('Blend the sounds. Which word is it?', '🔊 ' + w.split('').join(' · '), [[wopt(w), w.split('').join(', ') + ' makes ' + w + '.']].concat(near.slice(0, 2).map(function (x) { return [wopt(x), x + ' is ' + x.split('').join(', ') + '.']; })));
    if (q) { q.snd = ['q_blend'].concat(w.split('').map(function (c) { return 'snd_' + c; })); q.gap = 380; } return q; }; }
  // Which sound is missing? (never an option that also makes a real word)
  function genMissing(letters) { return function () {
    var pool = CVC.filter(function (w) { return w.split('').every(function (c) { return letters.indexOf(c) >= 0; }); }); if (!pool.length) return null;
    var w = pickOne(pool), pos = ri(0, 2), L = w[pos], cands = pos === 1 ? VOW : letters.filter(function (c) { return c.length === 1 && VOW.indexOf(c) < 0 && c !== 'k'; });
    var wrong = shuffled(cands.filter(function (c) { return c !== L && !REAL[w.slice(0, pos) + c + w.slice(pos + 1)]; })).slice(0, 2); if (wrong.length < 2) return null;
    var q = mq('Which sound is missing? ' + w.split('').map(function (c, i) { return i === pos ? '_' : c; }).join(' '), EPIC[w], [[L, w + ' is ' + w.split('').join(', ') + '.']].concat(wrong.map(function (c) { return [c, w.slice(0, pos) + c + w.slice(pos + 1) + ' is not the word in the picture.']; })));
    if (q) q.snd = ['q_miss', 'w_' + w]; return q; }; }
  // Which word has this sound? (groups: [sound, [words]])
  function genHas(groups) { return function () {
    var g = pickOne(groups), w = pickOne(g[1]), others = shuffled(groups.filter(function (h) { return h !== g; })).slice(0, 2).map(function (h) { return pickOne(h[1]); });
    if (others.length < 2) others = others.concat(shuffled(CVC).slice(0, 2 - others.length));
    var q = mq('Which word has the "' + g[0] + '" sound?', '🔊 ' + g[0], [[wopt(w), w + ' has ' + g[0] + '.']].concat(others.map(function (x) { return [wopt(x), x + ' does not have ' + g[0] + '.']; })));
    if (q) q.snd = ['snd_' + g[0]]; return q; }; }
  // Which letter makes this sound? (c and k sound the same, so never both)
  function genLetter(letters) { return function () {
    var L = pickOne(letters), pool = 'satpinmdgocerhbfl'.split('').filter(function (c) { return c !== L && !(L === 'c' && c === 'k') && !(L === 'k' && c === 'c'); }), w = shuffled(pool).slice(0, 2);
    var q = mq('Which letter makes this sound?', '🔊', [[L, L + ' says ' + L + ', like in ' + (CVC.filter(function (x) { return x[0] === L; })[0] || L) + '.']].concat(w.map(function (c) { return [c, c + ' makes a different sound.']; })));
    if (q) q.snd = ['snd_' + L]; return q; }; }
  // Change the first sound: cat → hat (both picture words)
  function genChange() { return function () {
    var pairs = []; CVC.forEach(function (a) { CVC.forEach(function (b) { if (a !== b && a.slice(1) === b.slice(1)) pairs.push([a, b]); }); }); if (!pairs.length) return null;
    var x = pickOne(pairs), others = shuffled(CVC.filter(function (w) { return w !== x[1] && w !== x[0] && w[0] === x[1][0]; }).concat(CVC.filter(function (w) { return w !== x[1] && w !== x[0] && w.slice(1) !== x[0].slice(1); }))).slice(0, 2);
    if (others.length < 2) return null;
    return mq('Change ' + x[0][0] + ' in "' + x[0] + '" to ' + x[1][0] + '. What new word do you get?', EPIC[x[0]] + ' → ?', [[wopt(x[1]), x[1][0] + ', ' + x[1].slice(1).split('').join(', ') + ' makes ' + x[1] + '.']].concat(others.map(function (w) { return [wopt(w), w + ' is not ' + x[1][0] + ' + ' + x[0].slice(1) + '.']; }))); }; }
  // Which sound pair is missing? _ _ i p
  function genPair(groups) { return function () {
    var g = pickOne(groups), w = pickOne(g[1]), i = w.indexOf(g[0]); if (i < 0) return null;
    var shown = w.slice(0, i).split('').join(' ') + (i ? ' ' : '') + '_ _' + (w.slice(i + 2) ? ' ' + w.slice(i + 2).split('').join(' ') : '');
    var q = mq('Which sound pair is missing? ' + shown, EPIC[w], [[g[0], w + ' has ' + g[0] + '.']].concat(shuffled(groups.filter(function (h) { return h !== g && w.indexOf(h[0]) < 0; })).slice(0, 2).map(function (h) { return [h[0], w.slice(0, i) + h[0] + w.slice(i + 2) + ' is not the word in the picture.']; })));
    if (q) q.snd = ['w_' + w]; return q; }; }
"""

ENGLISH = dict(id='english', name='English', place='Story Library', grade='Grade 2', icon='🔤', bg='#FF8FC7',
  floors=[('Picture-book Corner', 13)], levels=[('Grade 2', 'Picture-book Corner', '13 lessons: letter sounds, blending, sound pairs, long vowels, tricky words, naming, doing and describing words, plurals, sentences, poems and stories')],
  lessons=[
 dict(key='e2_s1', title='First sounds', part='alphabet bunting', icon='tx:s a t', bg='#FFC861',
  text='Letters have sounds: s, a, t, p, i and n.',
  done='You know your first six sounds! Come and see the alphabet bunting go up in the Picture-book Corner.',
  quiz=[Q('Which letter says sss, like a snake?', '🐍', 1, ('s', 'S says sss, like in sun.'), ('t', 'T says t, like in tap.'), ('n', 'N says nnn, like in net.'), snd=['snd_s']),
        Q('Which picture starts with p?', '', 2, ('🖊️ pen', 'Pen starts with p.'), ('☀️ sun', 'Sun starts with s.'), ('🥅 net', 'Net starts with n.'), snd=['snd_p']),
        Q('What sound does a make, like in ant?', '🐜', 1, ('a, as in ant', 'A says a, like the start of ant.'), ('ay, like its name', 'Its name is ay; its short sound is a.'), ('t', 't is a different letter.'), snd=['snd_a']),
        Q('Net starts with which sound?', '🥅', 4, ('n', 'N says nnn: net.'), ('t', 'T is at the end of net.'), ('e', 'E is in the middle of net.'), snd=['w_net']),
        Q('Which picture starts with t?', '', 2, ('🚰 tap', 'Tap starts with t.'), ('📌 pin', 'Pin starts with p.'), ('🐜 ant', 'Ant starts with a.'), snd=['snd_t'])],
  gen=[("genStart(['s', 'a', 't', 'p', 'i', 'n'])", 4)],
  cards=[('What sound does s make?', 'sss, like in sun.'), ('Letters have a name and a…', 'Sound. To read, we use the sounds.'), ('Which word starts with p: pen or net?', 'pen')]),

 dict(key='e2_s2', title='More sounds', part='sound wall', icon='tx:m d g', bg='#FFB547',
  text='m, d, g, o, c and k, and your first blending.',
  done='Six more sounds! Come and see the sound wall in the Picture-book Corner.',
  quiz=[Q('Which letter says mmm?', '🗺️', 1, ('m', 'M says mmm, like in map.'), ('d', 'D says d, like in dog.'), ('n', 'N says nnn, like in net.'), snd=['snd_m']),
        Q('Dog starts with which sound?', '🐶', 1, ('d', 'D says d: dog.'), ('g', 'G is at the end of dog.'), ('o', 'O is in the middle of dog.'), snd=['w_dog']),
        Q('Which two letters make the same sound?', '🐱 🪁', 3, ('c and k', 'Cat starts with c, kite with k: the same sound.'), ('m and n', 'mmm and nnn are different sounds.'), ('d and g', 'd and g sound different.')),
        Q('Blend m, a, p. Which word is it?', '', 4, ('🗺️ map', 'm, a, p makes map.'), ('🍳 pan', 'pan is p, a, n.'), ('🚰 tap', 'tap is t, a, p.'), snd=['q_blend', 'snd_m', 'snd_a', 'snd_p']),
        Q('Blend d, o, g. Which word is it?', '', 4, ('🐶 dog', 'd, o, g makes dog.'), ('🍲 pot', 'pot is p, o, t.'), ('🎩 hat', 'hat is h, a, t.'), snd=['q_blend', 'snd_d', 'snd_o', 'snd_g'])],
  gen=[("genStart(['m', 'd', 'g', 'o', 'c'])", 1), ("genBlend(['s', 'a', 't', 'p', 'i', 'n', 'm', 'd', 'g', 'o', 'c'])", 4)],
  cards=[('Which two letters say the same sound?', 'c and k: cat and kite.'), ('Blend m, a, p', 'map'), ('What sound does o make?', 'o, like in on.')]),

 dict(key='e2_s3', title='The rest of the short sounds', part='letter blocks', icon='tx:e u r', bg='#7CF5C8',
  text='e, u, r, h, b, f and l, and the five vowels.',
  done='You know all the short sounds! Come and see the letter blocks stacked up.',
  quiz=[Q('Egg starts with which sound?', '🥚', 1, ('e', 'E says e: egg.'), ('a', 'A says a, like in ant.'), ('g', 'G is at the end of egg.'), snd=['w_egg']),
        Q('Which letter says hhh, like a little breath?', '🎩', 2, ('h', 'H says hhh, like in hat.'), ('b', 'B says b, like in bat.'), ('r', 'R says rrr, like in rat.'), snd=['snd_h']),
        Q('Which picture starts with f?', '', 3, ('🐟 fish', 'Fish starts with f.'), ('🦇 bat', 'Bat starts with b.'), ('🦵 leg', 'Leg starts with l.'), snd=['snd_f']),
        Q('Which of these is a vowel?', '', 4, ('u', 'a, e, i, o and u are the vowels.'), ('b', 'b is not a vowel.'), ('r', 'r is not a vowel.')),
        Q('Which sound is missing? h _ t', '🎩', 4, ('a', 'h, a, t makes hat.'), ('e', 'h, e, t is not a word.'), ('u', 'h, u, t makes hut, not hat.'), snd=['q_miss', 'w_hat'])],
  gen=[("genStart(['e', 'u', 'r', 'h', 'b', 'f', 'l'])", 1), ("genMissing(['s', 'a', 't', 'p', 'i', 'n', 'm', 'd', 'g', 'o', 'c', 'e', 'u', 'r', 'h', 'b', 'f', 'l'])", 4)],
  cards=[('What are the five vowels?', 'a, e, i, o, u'), ('What sound does h make?', 'hhh, like a little breath: hat.'), ('What sound does u make?', 'u, like in up.')]),

 dict(key='e2_blend', title='Blending words', part='picture-book shelf', icon='tx:c·a·t', bg='#8FD3FF',
  text='Push sounds together to read words, then a whole sentence.',
  done='You can read words! Come and see the picture-book shelf fill up.',
  quiz=[Q('Blend c, a, t. Which word is it?', '', 0, ('🐱 cat', 'c, a, t makes cat.'), ('🎩 hat', 'hat is h, a, t.'), ('🐶 dog', 'dog is d, o, g.'), snd=['q_blend', 'snd_c', 'snd_a', 'snd_t']),
        Q('Blend s, u, n. Which word is it?', '', 1, ('☀️ sun', 's, u, n makes sun.'), ('🍞 bun', 'bun is b, u, n.'), ('🚌 bus', 'bus is b, u, s.'), snd=['q_blend', 'snd_s', 'snd_u', 'snd_n']),
        Q('Change c in cat to h. What new word do you get?', '🐱 → ?', 2, ('🎩 hat', 'h, a, t makes hat.'), ('🦇 bat', 'bat starts with b.'), ('🛖 hut', 'hut has u in the middle.')),
        Q('What should you do when you meet a new word?', '', 3, ('Sound it out', 'Say each sound, then push them together.'), ('Guess from the picture', 'Pictures help, but sound it out first.'), ('Skip it', 'Sound it out: you can read it!')),
        Q('Read: The cat sat on a mat. Where did the cat sit?', '🐱', 4, ('on a mat', 'The cat sat on a mat.'), ('on a hat', 'Read again: it says mat.'), ('in a box', 'The sentence says on a mat.'))],
  gen=[("genBlend(['s', 'a', 't', 'p', 'i', 'n', 'm', 'd', 'g', 'o', 'c', 'e', 'u', 'r', 'h', 'b', 'f', 'l'])", 1), ("genMissing(['s', 'a', 't', 'p', 'i', 'n', 'm', 'd', 'g', 'o', 'c', 'e', 'u', 'r', 'h', 'b', 'f', 'l'])", 3)],
  cards=[('How do you read a new word?', 'Sound it out, then push the sounds together.'), ('Blend p, i, g', 'pig'), ('cat → change c to h', 'hat')]),

 dict(key='e2_digraph', title='Two letters, one sound', part='reading mat', icon='tx:sh ch', bg='#FFB0D8',
  text='sh, ch, th and ng: two letters that make one sound.',
  done='You know the sound pairs! Come and see the reading mat rolled out.',
  quiz=[Q('Which word starts with sh?', '', 1, ('🚢 ship', 'Ship starts with sh.'), ('☀️ sun', 'Sun starts with just s.'), ('🍟 chips', 'Chips starts with ch.'), snd=['snd_sh']),
        Q('Which word starts with ch?', '', 2, ('🧀 cheese', 'Cheese starts with ch.'), ('🐱 cat', 'Cat starts with c.'), ('👍 thumb', 'Thumb starts with th.'), snd=['snd_ch']),
        Q('Which sound pair is at the end of ring?', '💍', 4, ('ng', 'Ring ends with ng.'), ('sh', 'sh is at the end of fish.'), ('th', 'th is at the end of bath.'), snd=['w_ring']),
        Q('Which word ends with th?', '', 3, ('🛁 bath', 'Bath ends with th.'), ('🐟 fish', 'Fish ends with sh.'), ('👑 king', 'King ends with ng.')),
        Q('In "ship", how many sounds do s and h make together?', '🚢', 0, ('one', 's and h together make one sound: sh.'), ('two', 'Together they make one new sound.'), ('none', 'They make the sh sound.'))],
  gen=[("genHas([['sh', ['ship', 'fish', 'shell']], ['ch', ['chips', 'chick', 'cheese']], ['th', ['thumb', 'bath']], ['ng', ['ring', 'king', 'swing']]])", 1)],
  cards=[('What is a sound pair?', 'Two letters that make one sound: sh, ch, th, ng.'), ('Which sound pair is in fish?', 'sh'), ('Which sound pair ends ring and king?', 'ng')]),

 dict(key='e2_long', title='Long vowel sounds', part='window seat', icon='tx:ai ee', bg='#B8F27C',
  text='ai, ee, oa and the magic e.',
  done='You know the long vowels! Come and see the window seat in the Picture-book Corner.',
  quiz=[Q('Which word has the ee sound?', '', 2, ('🌳 tree', 'Tree has ee.'), ('🌧️ rain', 'Rain has ai.'), ('⛵ boat', 'Boat has oa.'), snd=['snd_ee']),
        Q('Which word has the ai sound?', '', 1, ('🚂 train', 'Train has ai.'), ('🐝 bee', 'Bee has ee.'), ('🐐 goat', 'Goat has oa.'), snd=['snd_ai']),
        Q('Add a magic e to cap. What word do you get?', '🧢 + e', 4, ('cape', 'The magic e makes a say its name: cape.'), ('caps', 'That adds s, not e.'), ('cup', 'That changes the vowel.')),
        Q('What does the magic e at the end do?', '', 4, ('Makes the vowel say its name', 'kit becomes kite: i says its name.'), ('Says eee', 'The magic e is silent.'), ('Makes the word plural', 'That is s. The magic e changes the vowel sound.')),
        Q('Which word has the oa sound?', '', 3, ('🐐 goat', 'Goat has oa.'), ('🌳 tree', 'Tree has ee.'), ('🐌 snail', 'Snail has ai.'), snd=['snd_oa'])],
  gen=[("genHas([['ai', ['rain', 'train', 'snail']], ['ee', ['tree', 'bee', 'sheep']], ['oa', ['boat', 'goat', 'coat']]])", 2),
       ("""function () { var P = [['cap', 'cape'], ['kit', 'kite'], ['tap', 'tape'], ['hop', 'hope'], ['pin', 'pine'], ['not', 'note'], ['cub', 'cube'], ['rob', 'robe']], x = pickOne(P);
        return mq('Add a magic e to ' + x[0] + '. What word do you get?', x[0] + ' + e', [[x[1], 'The magic e makes the vowel say its name: ' + x[1] + '.'], [x[0] + 's', 'That adds s, not e.'], [x[0], 'The magic e changes the word.']]); }""", 4)],
  cards=[('What does the magic e do?', 'It is silent and makes the vowel say its name: kit → kite.'), ('Which sound is in rain and train?', 'ai'), ('Which sound is in tree and bee?', 'ee')]),

 dict(key='e2_tricky', title='Tricky words', part='word wall', icon='tx:the', bg='#FFD27A',
  text='the, said, was, they and come: words we learn by sight.',
  done='You know the tricky words! Come and see the word wall.',
  quiz=[Q('Which word fits? "Hi," ___ Ravi.', '', 2, ('said', '"Hi," said Ravi.'), ('sed', 'It sounds like sed, but we write said.'), ('sad', 'Sad means unhappy.')),
        Q('Which word fits? It ___ hot.', '☀️', 2, ('was', 'It was hot.'), ('wos', 'It sounds like wos, but we write was.'), ('saw', 'Saw means you looked.')),
        Q('Which word fits? ___ come to play.', '', 3, ('They', 'They come to play.'), ('Thay', 'It sounds like thay, but we write they.'), ('The', 'The cannot start this sentence.')),
        Q('Why are some words called tricky?', '', 0, ('They do not follow the sounds', 'So we learn them by sight.'), ('They are very long', 'Tricky words are often short, like the.'), ('They are rude', 'They are just words that do not follow the sounds.')),
        Q('How many tricky words? They said the cat was hot.', '', 4, ('4', 'They, said, the, was.'), ('2', 'Look again: they, said, the, was.'), ('7', 'cat and hot follow the sounds.'))],
  gen=[("""function () { var S = [['The dog ___ hot.', 'was', ['wos', 'saw']], ['"Look!" ___ Mina.', 'said', ['sed', 'sad']], ['___ like to play.', 'They', ['Thay', 'Then']], ['Please ___ here.', 'come', ['cum', 'came']], ['I see ___ sun.', 'the', ['thu', 'then']], ['___ go to school.', 'They', ['Thay', 'The']], ['It ___ a big bus.', 'was', ['wos', 'saw']]], x = pickOne(S);
        return mq('Which word fits? ' + x[0], '', [[x[1], x[0].replace('___', x[1])]].concat(x[2].map(function (w) { return [w, 'It is a tricky word: we write ' + x[1] + '.']; }))); }""", 2)],
  cards=[('What is a tricky word?', 'A word that does not follow the sounds, like said or was.'), ('Spell the tricky word: sed', 'said'), ('Name three tricky words.', 'the, said, was (also they, come).')]),

 dict(key='e2_words', title='Naming and doing words', part='puppet shelves', icon='tx:dog runs', bg='#C3A6FF',
  text='Naming words name things; doing words tell what they do.',
  done='You know naming and doing words! Come and see the puppet shelves.',
  quiz=[Q('Which is a naming word?', '', 0, ('🐶 dog', 'Dog names an animal.'), ('🏃 run', 'Run is a doing word.'), ('🦘 jump', 'Jump is a doing word.')),
        Q('Which is a doing word?', '', 2, ('eat', 'Eat tells us what someone does.'), ('apple', 'Apple names a thing.'), ('school', 'School names a place.')),
        Q('The dog runs. Which is the doing word?', '🐶🏃', 3, ('runs', 'Runs tells what the dog does.'), ('dog', 'Dog is the naming word.'), ('The', 'The is a little helper word.')),
        Q('Pick the doing word: The bird sings.', '🐦🎵', 4, ('sings', 'Sings tells what the bird does.'), ('bird', 'Bird names an animal.'), ('The', 'The is a little helper word.')),
        Q('Which is a naming word for a place?', '', 1, ('🏫 school', 'School names a place.'), ('🍽️ eat', 'Eat is a doing word.'), ('😊 happy', 'Happy is a describing word.'))],
  gen=[("""function () { var N = ['dog', 'cat', 'bus', 'tree', 'school', 'apple', 'Mum', 'ball', 'book', 'park'], V = ['run', 'jump', 'eat', 'sing', 'swim', 'sleep', 'read', 'clap', 'hop', 'draw'], noun = pickOne([true, false]);
        var r = pickOne(noun ? N : V), w = shuffled(noun ? V : N).slice(0, 2);
        return mq('Which is a ' + (noun ? 'naming' : 'doing') + ' word?', '', [[r, noun ? r + ' names a person, place, animal or thing.' : r + ' tells what someone does.']].concat(w.map(function (x) { return [x, noun ? x + ' is a doing word.' : x + ' is a naming word.']; }))); }""", 2),
       ("""function () { var S = [['The frog jumps.', 'frog', 'jumps'], ['The baby sleeps.', 'baby', 'sleeps'], ['Ravi kicks the ball.', 'Ravi', 'kicks'], ['The fish swims.', 'fish', 'swims'], ['Mina reads.', 'Mina', 'reads']], x = pickOne(S), doing = pickOne([true, false]);
        return mq(x[0] + ' Which is the ' + (doing ? 'doing' : 'naming') + ' word?', '', [[doing ? x[2] : x[1], doing ? x[2] + ' tells what ' + x[1] + ' does.' : x[1] + ' is who the sentence is about.'], [doing ? x[1] : x[2], doing ? x[1] + ' is the naming word.' : x[2] + ' is the doing word.'], ['The', 'The is a little helper word.']]); }""", 3)],
  cards=[('What is a naming word?', 'A word that names a person, place, animal or thing: dog, school, Mum.'), ('What is a doing word?', 'A word for what someone does: run, jump, eat.'), ('The dog runs: which is the doing word?', 'runs')]),

 dict(key='e2_describe', title='Describing words and a / an', part='cushions', icon='tx:a / an', bg='#FF8FC7',
  text='Words that tell us more, and when to say a or an.',
  done='You can describe things! Come and see the cushions in every colour.',
  quiz=[Q('Which is a describing word?', '', 0, ('red', 'Red tells us more about a thing: a red ball.'), ('ball', 'Ball is a naming word.'), ('run', 'Run is a doing word.')),
        Q('a big red ball. Which words describe the ball?', '⚽', 1, ('big and red', 'They tell us its size and colour.'), ('a and ball', 'Ball is the thing; a is a helper word.'), ('only ball', 'Ball is the naming word.')),
        Q('___ apple: a or an?', '🍎', 3, ('an', 'Apple starts with a vowel sound, so we say an.'), ('a', 'Before a vowel sound we say an.'), ('the an', 'Just one: an apple.')),
        Q('___ cat: a or an?', '🐱', 3, ('a', 'Cat starts with c, not a vowel, so we say a.'), ('an', 'An goes before a vowel sound: a, e, i, o, u.'), ('an a', 'Just one: a cat.')),
        Q('Which tells us how something feels?', '', 2, ('soft', 'A soft cushion: soft tells how it feels.'), ('cushion', 'Cushion is a naming word.'), ('sit', 'Sit is a doing word.'))],
  gen=[("""function () { var AN = [['apple', '🍎', 'an'], ['egg', '🥚', 'an'], ['owl', '🦉', 'an'], ['umbrella', '☂️', 'an'], ['ant', '🐜', 'an'], ['ice cream', '🍦', 'an'], ['cat', '🐱', 'a'], ['ball', '⚽', 'a'], ['dog', '🐶', 'a'], ['kite', '🪁', 'a'], ['banana', '🍌', 'a'], ['tree', '🌳', 'a']], x = pickOne(AN), other = x[2] === 'a' ? 'an' : 'a';
        return mq('___ ' + x[0] + ': a or an?', x[1], [[x[2], x[2] === 'an' ? x[0] + ' starts with a vowel sound, so we say an.' : x[0] + ' does not start with a vowel sound, so we say a.'], [other, other === 'an' ? 'An goes only before a vowel sound.' : 'Before a vowel sound we say an.']]); }""", 3),
       ("""function () { var A = ['big', 'red', 'soft', 'happy', 'tiny', 'old', 'hot', 'tall'], N = ['ball', 'cat', 'tree', 'bus', 'girl'], V = ['run', 'jump', 'sing', 'eat'];
        var r = pickOne(A);
        return mq('Which is a describing word?', '', [[r, r + ' tells us more about a thing.'], [pickOne(N), 'That is a naming word.'], [pickOne(V), 'That is a doing word.']]); }""", 0)],
  cards=[('What does a describing word do?', 'Tells us more about a naming word: big, red, soft.'), ('When do we say an?', 'Before a vowel sound: an apple, an egg.'), ('a or an: ___ cat', 'a cat')]),

 dict(key='e2_plural', title='One and many', part='toy baskets', icon='tx:cats', bg='#9FE3FF',
  text='Add s or es for more than one, and the special words.',
  done='You can say one and many! Come and see the toy baskets.',
  quiz=[Q('One cat, two ___', '🐱🐱', 1, ('cats', 'Most words just add s.'), ('cates', 'Cat only needs s.'), ('cat', 'For two, the word changes.')),
        Q('One box, two ___', '📦📦', 2, ('boxes', 'Words ending in x add es.'), ('boxs', 'We add es after x, so you can hear it.'), ('box', 'For two, the word changes.')),
        Q('One bus, two ___', '🚌🚌', 2, ('buses', 'Words ending in s add es.'), ('buss', 'We add es after s.'), ('bus', 'For two, the word changes.')),
        Q('One mouse, two ___', '🐭🐭', 3, ('mice', 'Mouse is a special word: mice.'), ('mouses', 'Mouse changes in its own way: mice.'), ('mousees', 'Mouse becomes mice.')),
        Q('One child, two ___', '🧒🧒', 3, ('children', 'Child is a special word: children.'), ('childs', 'Child changes in its own way.'), ('childes', 'Child becomes children.'))],
  gen=[("""function () { var P = [['dog', 'dogs', 'doges'], ['pen', 'pens', 'penes'], ['book', 'books', 'bookes'], ['box', 'boxes', 'boxs'], ['bus', 'buses', 'buss'], ['dish', 'dishes', 'dishs'], ['bench', 'benches', 'benchs'], ['fox', 'foxes', 'foxs'], ['man', 'men', 'mans'], ['mouse', 'mice', 'mouses'], ['child', 'children', 'childs'], ['tree', 'trees', 'treees'], ['tooth', 'teeth', 'tooths']], x = pickOne(P);
        var why = /es$/.test(x[1]) ? x[0] + ' ends in ' + x[0].slice(-2).replace(/^[^sc]/, '') + ', so we add es.' : /s$/.test(x[1]) ? 'Most words just add s.' : x[0] + ' is a special word: ' + x[1] + '.';
        return mq('One ' + x[0] + ', two ___', '', [[x[1], why], [x[2], 'Not quite: we write ' + x[1] + '.'], [x[0], 'For more than one, the word changes.']]); }""", 2)],
  cards=[('When do you add es?', 'After s, x, sh or ch: boxes, buses, dishes.'), ('One mouse, two…', 'mice'), ('One child, two…', 'children')]),

 dict(key='e2_sentence', title='Capitals, full stops and a poem', part='poem cushion', icon='tx:A.', bg='#FFC861',
  text='Start with a capital, end with a full stop, and find rhymes.',
  done='You can write sentences and spot rhymes! Come and see the poem cushion.',
  quiz=[Q('Which sentence is written correctly?', '', 2, ('I like mangoes.', 'It starts with a capital and ends with a full stop.'), ('i like mangoes.', 'A sentence starts with a capital letter.'), ('I like mangoes', 'A sentence ends with a full stop.')),
        Q('Which name is written correctly?', '', 1, ('Delhi', 'Names always start with a capital letter.'), ('delhi', 'Names need a capital letter.'), ('dELHI', 'Only the first letter is a capital.')),
        Q('Which word rhymes with sun?', '☀️', 3, ('fun', 'Sun and fun end with the same sound: un.'), ('sit', 'Sit starts like sun but does not end like it.'), ('cat', 'Cat ends with at, not un.')),
        Q('Which word rhymes with cat?', '🐱', 3, ('hat', 'Cat and hat end with at.'), ('cup', 'Cup ends with up.'), ('can', 'Can ends with an.')),
        Q('What does every sentence end with?', '', 2, ('a full stop', 'Like this.'), ('a capital letter', 'Capitals go at the start.'), ('a comma', 'A comma goes in the middle.'))],
  gen=[("""function () { var R = [['cat', ['hat', 'mat', 'bat', 'rat']], ['sun', ['fun', 'run', 'bun']], ['pig', ['big', 'dig', 'wig']], ['hen', ['pen', 'ten', 'men']], ['dog', ['log', 'fog', 'frog']], ['bed', ['red', 'fed', 'shed']], ['cake', ['lake', 'bake', 'snake']]], g = pickOne(R), r = pickOne(g[1]);
        var w = shuffled([].concat.apply([], R.filter(function (h) { return h !== g; }).map(function (h) { return h[1]; }))).slice(0, 2);
        return mq('Which word rhymes with ' + g[0] + '?', '', [[r, g[0] + ' and ' + r + ' end with the same sound.']].concat(w.map(function (x) { return [x, x + ' does not end like ' + g[0] + '.']; }))); }""", 3),
       ("""function () { var S = ['the sun is hot', 'my cat is black', 'we like to play', 'ravi has a kite', 'the bus is red', 'mina can swim'], s = pickOne(S), good = s.charAt(0).toUpperCase() + s.slice(1).replace(/\\b(ravi|mina)\\b/g, function (m) { return m.charAt(0).toUpperCase() + m.slice(1); }) + '.';
        return mq('Which sentence is written correctly?', '', [[good, 'A capital letter at the start, a full stop at the end' + (/Ravi|Mina/.test(good) ? ', and a capital for the name.' : '.')], [good.charAt(0).toLowerCase() + good.slice(1), 'A sentence starts with a capital letter.'], [good.slice(0, -1), 'A sentence ends with a full stop.']]); }""", 2)],
  cards=[('How does a sentence start and end?', 'With a capital letter, and a full stop.'), ('Which words rhyme with cat?', 'hat, mat, bat'), ('Do names need a capital?', 'Yes: Ravi, Delhi.')]),

 dict(key='e2_story', title='Picture talk and a story', part='storytelling chair', icon='em:📖', bg='#7CF5C8',
  text='Ask who, where and what, then read a short story.',
  done='You read a whole story! Come and see the storytelling chair.',
  quiz=[Q('Who had a little kitten?', '🐱', 1, ('Mina', 'Mina had a little kitten.'), ('Ravi', 'Read again: it was Mina.'), ('Nibb', 'Nibb told the story. It was Mina’s kitten.')),
        Q('Where did Mina look first?', '🛏️', 2, ('under the bed', 'Mina looked under the bed.'), ('up the tree', 'That was next.'), ('in a box', 'The story says under the bed.')),
        Q('Where was the kitten?', '🌳', 3, ('in the tree', 'The kitten was in the tree!'), ('under the bed', 'It was not there.'), ('in the kitchen', 'The story says in the tree.')),
        Q('How did Mina feel at the end?', '😊', 3, ('happy', 'She found her kitten, so she was happy.'), ('sad', 'She was sad when it was lost, but happy at the end.'), ('angry', 'She was happy.')),
        Q('When you look at a picture, which questions help?', '🖼️', 0, ('Who? Where? What is happening?', 'They help you talk about it.'), ('How heavy is it?', 'That does not help you tell the story.'), ('What colour is the sky, only', 'Ask who, where and what is happening.'))],
  gen=[("""function () { var N = ['Mina', 'Ravi', 'Anu', 'Sam'], P = [['dog', '🐶'], ['cat', '🐱'], ['hen', '🐔'], ['fish', '🐟']], C = ['red', 'black', 'big', 'little'], n = pickOne(N), p = pickOne(P), c = pickOne(C), ask = ri(0, 2);
        var story = n + ' has a ' + c + ' ' + p[0] + '. The ' + p[0] + ' likes to play.';
        if (ask === 0) return mq(story + ' Who has the ' + p[0] + '?', p[1], [[n, story.split('.')[0] + '.'], [pickOne(N.filter(function (x) { return x !== n; })), 'Read again: ' + n + ' has it.'], ['Nibb', 'The story is about ' + n + '.']]);
        if (ask === 1) return mq(story + ' What pet does ' + n + ' have?', '📖', [[p[0], n + ' has a ' + c + ' ' + p[0] + '.']].concat(shuffled(P.filter(function (x) { return x !== p; })).slice(0, 2).map(function (x) { return [x[0], 'Read again: it is a ' + p[0] + '.']; })));
        return mq(story + ' What is the ' + p[0] + ' like?', p[1], [[c, 'It is a ' + c + ' ' + p[0] + '.']].concat(shuffled(C.filter(function (x) { return x !== c; })).slice(0, 2).map(function (x) { return [x, 'Read again: the story says ' + c + '.']; }))); }""", 4)],
  cards=[('Three questions for a picture', 'Who? Where? What is happening?'), ('Where was the lost kitten?', 'In the tree.'), ('Good readers ask…', 'Questions about the story.')]),

 dict(key='e2_challenge', title='the Story Time challenge', part='puppet theatre', icon='boss', bg='#FF7A6B', challenge=True,
  text='Sound out new words, read a story and answer the questions.',
  done='You finished the Picture-book Corner! The puppet theatre is ready for Story Time. Come and see.',
  quiz=[Q('Blend f, i, sh. Which word is it?', '', 1, ('🐟 fish', 'f, i, sh makes fish.'), ('🚢 ship', 'ship is sh, i, p.'), ('🦈 fin', 'fin is f, i, n.'), snd=['q_blend', 'snd_f', 'snd_i', 'snd_sh']),
        Q('Where did the fish swim?', '🐟', 2, ('in the pond', 'A fish swam in the pond.'), ('in the sea', 'Read again: the pond.'), ('in a cup', 'The story says the pond.')),
        Q('Who came to play?', '🦆', 2, ('a duck', 'A duck came to play.'), ('a cat', 'Read again: a duck.'), ('a frog', 'The story says a duck.')),
        Q('What did they do at the end?', '😴', 3, ('went to sleep', 'Then they went to sleep.'), ('went to school', 'Read again: they went to sleep.'), ('ate cake', 'The story says they went to sleep.')),
        Q('Which word in the story has the ai sound?', '🌧️', 3, ('rain', 'They had fun in the rain: ai.'), ('pond', 'Pond has a short o.'), ('duck', 'Duck has a short u.'), snd=['snd_ai'])],
  gen=[("genBlend(['s', 'a', 't', 'p', 'i', 'n', 'm', 'd', 'g', 'o', 'c', 'e', 'u', 'r', 'h', 'b', 'f', 'l'])", 1),
       ("genHas([['sh', ['ship', 'fish', 'shell']], ['ch', ['chips', 'chick']], ['ee', ['tree', 'bee']], ['oa', ['boat', 'goat', 'coat']]])", 3)],
  cards=[('Story Time: who came to play with the fish?', 'A duck.'), ('Blend f, i, sh', 'fish'), ('What do good readers do with new words?', 'Sound them out.')]),
])

# ---------------- more question makers, so a quiz rarely repeats ----------------
# names, things and places are picked at random inside each one
_N = "['Ravi', 'Mina', 'Anu', 'Sam', 'Zara', 'Kabir', 'Meera', 'Arjun']"
EXTRA = {
 'm2_groups': [
  ("""function () { var n = ri(2, 6), who = pickOne(%s);
        return mq(who + ' has ' + n + ' pairs of socks. How many socks?', grp(n, 2, '🧦'), [[n * 2, 'Count in twos: ' + n + ' pairs make ' + n * 2 + '.'], [n, n + ' is the number of pairs.'], [n + 2, 'Each pair has 2 socks. Count in twos.']]); }""" % _N, 0),
  ("""function () { var s = pickOne([2, 5, 10]), a = s * ri(1, 5), seq = [a, a + s, a + 2 * s, a + 3 * s], gap = ri(1, 2), right = seq[gap];
        seq[gap] = '__'; return mq('Which number is missing? ' + seq.join(', '), '', [[right, 'The jump is ' + s + ' each time.'], [right + 1, 'The jump is ' + s + ', not 1.'], [right + s, 'That skips one jump too many.']]); }""", 4),
  ("""function () { var n = ri(2, 6);
        return mq(n + ' children each hold up one hand. How many fingers?', grp(n, 1, '✋'), [[n * 5, 'Count in fives: ' + n + ' hands make ' + n * 5 + ' fingers.'], [n, n + ' is the number of hands.'], [n * 5 + 5, 'Count the hands again: ' + n + '.']]); }""", 1)],
 'm2_shapes': [
  ("""function () { var roll = pickOne([true, false]), R = ['⚽ ball', '🍊 orange', '🥫 tin', '🌍 globe'], N = ['🎲 dice', '📦 box', '🧱 brick', '📕 book'], r = pickOne(roll ? R : N), w = shuffled(roll ? N : R).slice(0, 2);
        return mq('Which one can ' + (roll ? 'roll' : 'not roll') + '?', '', [[r, roll ? 'It has a curved side, so it rolls.' : 'It has only flat faces, so it slides but does not roll.']].concat(w.map(function (x) { return [x, roll ? 'It has only flat faces, so it does not roll.' : 'It has a curved side, so it can roll.']; }))); }""", 3),
  ("""function () { var F = [['How many faces does a cube have?', 6, [4, 8], '🎲'], ['How many corners does a cube have?', 8, [6, 4], '🎲'], ['How many flat ends does a cylinder have?', 2, [1, 0], '🥫'], ['How many flat faces does a sphere have?', 0, [1, 2], '⚽']], x = pickOne(F);
        return mq(x[0], x[3], [[x[1], 'Look closely and count: ' + x[1] + '.']].concat(x[2].map(function (v) { return [v, 'Count again carefully.']; }))); }""", 2)],
 'm2_numbers': [
  ("""function () { var t = ri(1, 9), o = ri(0, 9);
        return mq(t + ' tens and ' + o + ' ones make which number?', rpt('▮', t) + ' ' + rpt('•', o), [[t * 10 + o, t + ' tens is ' + t * 10 + ', and ' + o + ' more is ' + (t * 10 + o) + '.'], [o * 10 + t, 'The tens come first: ' + t + ', then the ones: ' + o + '.'], [t + o, 'Tens are worth 10 each.']]); }""", 0),
  ("""function () { var W = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'], O = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'], t = ri(2, 9), o = ri(1, 9), n = t * 10 + o;
        return mq('Which number is ' + W[t - 2] + '-' + O[o] + '?', '', [[n, W[t - 2] + ' is ' + t + ' tens, ' + O[o] + ' is ' + o + ' ones.'], [o * 10 + t, 'The tens digit comes first.'], [t * 100 + o, 'Two digits are enough: ' + n + '.']]); }""", 1),
  ("""function () { var a = ri(11, 96);
        return mq('Which number comes between ' + a + ' and ' + (a + 2) + '?', '', [[a + 1, a + ', ' + (a + 1) + ', ' + (a + 2) + '.'], [a + 3, 'That comes after ' + (a + 2) + '.'], [a - 1, 'That comes before ' + a + '.']]); }""", 2)],
 'm2_flat': [
  ("""function () { var S = [['▲', 'triangle', 3], ['■', 'square', 4], ['▬', 'rectangle', 4]], x = pickOne(S);
        return mq('How many sides does a ' + x[1] + ' have?', x[0], [[x[2], 'A ' + x[1] + ' has ' + x[2] + ' straight sides.'], [x[2] + 1, 'Count the sides again.'], [x[2] === 3 ? 4 : 3, 'Count the sides again.']]); }""", 2),
  ("""function () { var S = [['●', 'circle'], ['▲', 'triangle'], ['■', 'square'], ['▬', 'rectangle']], x = pickOne(S);
        return mq('What is this shape called?', x[0], [[x[1], 'This is a ' + x[1] + '.']].concat(shuffled(S.filter(function (y) { return y !== x; })).slice(0, 2).map(function (y) { return [y[1], 'A ' + y[1] + ' looks like ' + y[0] + '.']; }))); }""", 1)],
 'm2_lines': [
  ("""function () { var C = [['🌈 rainbow', 'curved'], ['🍌 banana', 'curved'], ['⭕ ring', 'curved'], ['📏 ruler', 'straight'], ['✏️ pencil', 'straight'], ['🚪 door edge', 'straight']], x = pickOne(C), want = pickOne(['curved', 'straight']);
        var right = pickOne(C.filter(function (c) { return c[1] === want; })), w = shuffled(C.filter(function (c) { return c[1] !== want; })).slice(0, 2);
        return mq('Which one has a ' + want + ' line?', '', [[right[0], 'A ' + right[0].split(' ').slice(1).join(' ') + ' is ' + want + '.']].concat(w.map(function (c) { return [c[0], 'A ' + c[0].split(' ').slice(1).join(' ') + ' is ' + c[1] + '.']; }))); }""", 4)],
 'm2_addsub': [
  ("""function () { var who = pickOne(%s), it = pickOne([['🔵', 'marbles'], ['🌸', 'flowers'], ['🖍️', 'crayons'], ['⭐', 'stickers']]), a = ri(12, 45), b = ri(11, 40);
        return mq(who + ' has ' + a + ' ' + it[1] + ' and gets ' + b + ' more. How many now?', it[0], [[a + b, a + ' + ' + b + ' = ' + (a + b) + '.'], [Math.abs(a - b), 'Gets more means add.'], [a + b + 10, 'Add the tens again.']]); }""" % _N, 1),
  ("""function () { var who = pickOne(%s), it = pickOne([['🎈', 'balloons', 'fly away'], ['🍪', 'biscuits', 'are eaten'], ['🐦', 'birds', 'fly off']]), a = ri(25, 60), b = ri(11, 20);
        return mq(who + ' has ' + a + ' ' + it[1] + '. ' + b + ' ' + it[2] + '. How many are left?', it[0], [[a - b, a + ' − ' + b + ' = ' + (a - b) + '.'], [a + b, 'Some went away, so take away.'], [a - b + 10, 'Check the tens: ' + a + ' − ' + b + ' = ' + (a - b) + '.']]); }""" % _N, 2)],
 'm2_measure': [
  ("""function () { var a = ri(5, 40), b = ri(5, 40); if (a === b) return null; var t = pickOne(['ribbon', 'rope', 'stick', 'string']);
        return mq('Which ' + t + ' is longer?', '📏', [[Math.max(a, b) + ' cm', Math.max(a, b) + ' is more than ' + Math.min(a, b) + '.'], [Math.min(a, b) + ' cm', Math.min(a, b) + ' cm is shorter.'], ['They are the same', a + ' and ' + b + ' are different.']]); }""", 2),
  ("""function () { var who = pickOne(%s), n = ri(4, 9), m = ri(2, 3);
        return mq(who + "'s table is " + n + ' hand spans long. The bench is ' + m + ' spans shorter. How long is the bench?', rpt('✋', n), [[n - m, n + ' − ' + m + ' = ' + (n - m) + ' spans.'], [n + m, 'Shorter means take away.'], [m, m + ' is how much shorter.']]); }""" % _N, 1)],
 'm2_share': [
  ("""function () { var k = ri(2, 5), e = ri(2, 5), who = pickOne(%s);
        return mq(who + ' gives ' + e + ' sweets to each of ' + k + ' friends. How many sweets is that?', grp(k, e, '🍬', '🧒'), [[k * e, k + ' groups of ' + e + ' = ' + k * e + '.'], [k + e, 'That adds. Count every sweet.'], [k * e - e, 'Count the friends again: ' + k + '.']]); }""" % _N, 1),
  ("""function () { var a = ri(2, 5), b = ri(2, 5);
        return mq(a + ' × ' + b + ' = ' + a * b + '. So ' + a * b + ' ÷ ' + a + ' = ?', '', [[b, 'Times and sharing are partners.'], [a * b, a * b + ' is the total.'], [a, a + ' is how many groups.']]); }""", 3)],
 'm2_time': [
  ("""function () { var S = [['☀️', 'hot and sunny', 'summer'], ['🌧️', 'rainy, with dark clouds', 'monsoon'], ['❄️', 'cold, with chilly mornings', 'winter']], x = pickOne(S);
        return mq('It is ' + x[1] + '. Which season is it?', x[0], [[x[2], x[2] + ' is ' + x[1] + '.']].concat(S.filter(function (y) { return y !== x; }).map(function (y) { return [y[2], y[2] + ' is ' + y[1] + '.']; }))); }""", 4),
  ("""function () { var h = ri(1, 11), who = pickOne(%s), act = pickOne(['plays football', 'reads a book', 'paints', 'helps cook']);
        return mq(who + ' ' + act + ' for 1 hour, starting at ' + h + " o'clock. When does " + who + ' stop?', String.fromCodePoint(0x1F54F + h), [[(h + 1) + " o'clock", h + " o'clock + 1 hour = " + (h + 1) + " o'clock."], ['half past ' + h, 'That is only half an hour.'], [(h + 2) + " o'clock", 'That is 2 hours.']]); }""" % _N, 2)],
 'm2_money': [
  ("""function () { var a = ri(5, 95), b = ri(5, 95); if (a === b) return null;
        return mq('Which is more money?', '', [['₹' + Math.max(a, b), Math.max(a, b) + ' is more than ' + Math.min(a, b) + '.'], ['₹' + Math.min(a, b), Math.min(a, b) + ' is less.'], ['They are the same', 'They are different amounts.']]); }""", 0),
  ("""function () { var T = pickOne([[10, [5, 5], [5, 2, 1], [10, 5]], [15, [10, 5], [10, 2, 2], [5, 5]], [20, [10, 10], [10, 5, 2], [5, 5, 5]], [12, [10, 2], [5, 5, 1], [10, 1]]]);
        return mq('Which coins make ₹' + T[0] + '?', '🪙', [[T[1].map(function (v) { return '₹' + v; }).join(' + '), T[1].join(' + ') + ' = ' + T[0] + '.'], [T[2].map(function (v) { return '₹' + v; }).join(' + '), 'That makes ₹' + T[2].reduce(function (p, q) { return p + q; }) + '.'], [T[3].map(function (v) { return '₹' + v; }).join(' + '), 'That makes ₹' + T[3].reduce(function (p, q) { return p + q; }) + '.']]); }""", 1)],
 'm2_data': [
  ("""function () { var F = shuffled([['🍎', 'apples'], ['🍌', 'bananas'], ['🍊', 'oranges']]).slice(0, 2), a = ri(2, 7), b = ri(2, 7);
        return mq(F[0][0] + ' ' + a + ' · ' + F[1][0] + ' ' + b + '. How many fruits in all?', many(a, F[0][0]) + many(b, F[1][0]), [[a + b, a + ' + ' + b + ' = ' + (a + b) + '.'], [Math.abs(a - b), 'In all means add them.'], [a + b + 1, 'Count again.']]); }""", 3),
  ("""function () { var n = ri(1, 4);
        return mq('Make the tally for ' + (5 + n) + '. What do you draw?', '', [['<s>||||</s> ' + rpt('|', n), 'A crossed group of 5 and ' + n + ' more.'], [rpt('|', 5 + n), 'After 4 marks, cross them to make the 5th.'], ['<s>||||</s> <s>||||</s>', 'That is 10.']]); }""", 0)],
 'm2_challenge': [
  ("""function () { var a = ri(11, 35), b = ri(10, 30), t = shuffled([['🥭', 'mangoes'], ['🍌', 'bananas'], ['🍉', 'a melon'], ['🍇', 'grapes']]).slice(0, 2);
        return mq('A customer buys ' + t[0][1] + ' for ₹' + a + ' and ' + t[1][1] + ' for ₹' + b + '. How much in all?', t[0][0] + ' ' + t[1][0], [['₹' + (a + b), a + ' + ' + b + ' = ' + (a + b) + '.'], ['₹' + Math.abs(a - b), 'In all means add.'], ['₹' + (a + b + 10), 'Check the tens.']]); }""", 3),
  ("""function () { var n = ri(3, 6) * 5;
        return mq('Tally board: how many customers came?', rpt('<s>||||</s> ', n / 5).trim(), [[n, 'Count in fives: ' + n + '.'], [n / 5, 'Each crossed group is 5, not 1.'], [n + 5, 'Count the groups again.']]); }""", 0)],
 'e2_s1': [("genLetter(['s', 'a', 't', 'p', 'i', 'n'])", 1)],
 'e2_s2': [("genLetter(['m', 'd', 'g', 'o', 'c'])", 1), ("genStart(['s', 'a', 't', 'p', 'i', 'n', 'm', 'd', 'g', 'o', 'c'])", 4)],
 'e2_s3': [("genLetter(['e', 'u', 'r', 'h', 'b', 'f', 'l'])", 2), ("genBlend(['s', 'a', 't', 'p', 'i', 'n', 'm', 'd', 'g', 'o', 'c', 'e', 'u', 'r', 'h', 'b', 'f', 'l'])", 4)],
 'e2_blend': [("genChange()", 2), ("genStart(['s', 'a', 't', 'p', 'i', 'n', 'm', 'd', 'g', 'o', 'c', 'e', 'u', 'r', 'h', 'b', 'f', 'l'])", 0)],
 'e2_digraph': [("genPair([['sh', ['ship', 'shell', 'fish']], ['ch', ['chips', 'chick', 'cheese']], ['th', ['thumb', 'bath']], ['ng', ['ring', 'king', 'swing']]])", 1)],
 'e2_long': [("genPair([['ai', ['rain', 'train', 'snail']], ['ee', ['tree', 'bee', 'sheep']], ['oa', ['boat', 'goat', 'coat']]])", 1)],
 'e2_tricky': [
  ("""function () { var T = ['the', 'said', 'was', 'they', 'come', 'you', 'are', 'my'], D = ['cat', 'sun', 'pig', 'map', 'hen', 'dog', 'bed', 'cup'], t = pickOne(T), d = shuffled(D).slice(0, 2);
        return mq('Which one is a tricky word?', '', [[t, t + ' does not follow the sounds: we learn it by sight.']].concat(d.map(function (w) { return [w, w + ' follows the sounds: ' + w.split('').join(', ') + '.']; }))); }""", 0)],
 'e2_words': [
  ("""function () { var P = [['🏫', 'school', 'place'], ['🏞️', 'park', 'place'], ['👩‍🏫', 'teacher', 'person'], ['👶', 'baby', 'person'], ['🐘', 'elephant', 'animal'], ['🐸', 'frog', 'animal'], ['🪁', 'kite', 'thing'], ['📚', 'book', 'thing']], x = pickOne(P), kinds = ['person', 'place', 'animal', 'thing'];
        return mq('"' + x[1] + '" is a naming word for a…', x[0], [[x[2], x[1] + ' names ' + (x[2] === 'animal' ? 'an ' : 'a ') + x[2] + '.']].concat(shuffled(kinds.filter(function (k) { return k !== x[2]; })).slice(0, 2).map(function (k) { return [k, 'Look again: ' + x[1] + ' is ' + (x[2] === 'animal' ? 'an ' : 'a ') + x[2] + '.']; }))); }""", 1)],
 'e2_describe': [
  ("""function () { var S = [['a ___ elephant', 'big', ['tiny', 'small'], '🐘'], ['a ___ ice cream', 'cold', ['hot', 'warm'], '🍦'], ['the ___ sun', 'hot', ['cold', 'wet'], '☀️'], ['a ___ pillow', 'soft', ['hard', 'sharp'], '🛏️'], ['a ___ ant', 'tiny', ['huge', 'tall'], '🐜'], ['a ___ smile', 'happy', ['sad', 'angry'], '😊']], x = pickOne(S);
        return mq('Pick the best describing word: ' + x[0], x[3], [[x[1], x[0].replace('___', x[1]) + '.']].concat(x[2].map(function (w) { return [w, 'Look at the picture: it is ' + x[1] + '.']; }))); }""", 2)],
 'e2_plural': [
  ("""function () { var P = [['cat', 'cats'], ['hen', 'hens'], ['box', 'boxes'], ['bus', 'buses'], ['man', 'men'], ['child', 'children'], ['mouse', 'mice'], ['dish', 'dishes'], ['cup', 'cups']], x = pickOne(P), many1 = pickOne([true, false]), other = shuffled(P.filter(function (y) { return y !== x; })).slice(0, 2);
        return mq('Which word means more than one?', '', [[x[1], x[1] + ' is more than one ' + x[0] + '.']].concat(other.map(function (y) { return [y[0], y[0] + ' is just one.']; }))); }""", 1)],
 'e2_sentence': [
  ("""function () { var S = ['we went to the park', 'my dog can run fast', 'the bird is in the tree', 'i like red apples', 'the bus is big'], s = pickOne(S), w = s.split(' ')[0];
        return mq('Which word needs a capital letter? ' + s + '.', '', [[w, 'A sentence starts with a capital letter: ' + w.charAt(0).toUpperCase() + w.slice(1) + '.']].concat(shuffled(s.split(' ').slice(1).filter(function (x) { return x !== 'i'; })).slice(0, 2).map(function (x) { return [x, x + ' is in the middle, so it stays small.']; }))); }""", 1)],
 'e2_story': [
  ("""function () { var N = ['Mina', 'Ravi', 'Anu', 'Sam'], P = [['the park', '🏞️'], ['the beach', '🏖️'], ['the zoo', '🦁'], ['school', '🏫']], D = ['Monday', 'Saturday', 'Sunday'], n = pickOne(N), p = pickOne(P), d = pickOne(D), ask = ri(0, 1);
        var story = 'On ' + d + ', ' + n + ' went to ' + p[0] + '. It was fun!';
        if (ask) return mq(story + ' Where did ' + n + ' go?', p[1], [[p[0], story.split('.')[0] + '.']].concat(shuffled(P.filter(function (x) { return x !== p; })).slice(0, 2).map(function (x) { return [x[0], 'Read again: ' + p[0] + '.']; })));
        return mq(story + ' When did ' + n + ' go?', '📅', [[d, 'The story says on ' + d + '.']].concat(D.filter(function (x) { return x !== d; }).map(function (x) { return [x, 'Read again: on ' + d + '.']; }))); }""", 4)],
 'e2_challenge': [("genStart(['s', 'a', 't', 'p', 'i', 'n', 'm', 'd', 'g', 'o', 'c', 'e', 'u', 'r', 'h', 'b', 'f', 'l'])", 1),
  ("""function () { var R = [['fish', 'dish'], ['duck', 'truck'], ['rain', 'train'], ['pond', 'wand'], ['play', 'day']], x = pickOne(R), w = shuffled(['cat', 'sun', 'bed', 'pig', 'cup']).slice(0, 2);
        return mq('Which word rhymes with ' + x[0] + '?', '', [[x[1], x[0] + ' and ' + x[1] + ' end with the same sound.']].concat(w.map(function (y) { return [y, y + ' does not end like ' + x[0] + '.']; }))); }""", 3)],
}
for C in (MATHS, ENGLISH):
    for L in C['lessons']:
        L['gen'] = L['gen'] + EXTRA.get(L['key'], [])
