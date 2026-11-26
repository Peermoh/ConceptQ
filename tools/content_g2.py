# Grade 2 Maths (Number Town, Market Street) and English (Story Library, Picture-book Corner).
# Each board line appears as the matching sentence of Nibb's narration starts.
import re
from content_f2 import L, add  # noqa: F401
def auto(lines, say):
    sents = [s for s in re.split(r'(?<=[.!?])\s+', say.strip()) if s]
    assert len(sents) >= len(lines), (lines[0], len(sents), len(lines))
    cues, pos = [], -1
    for i in range(len(lines)):
        words = sents[i].split()
        c = ' '.join(words[:4]) if len(words) >= 4 else sents[i]
        c = c.rstrip('.,!?:;')
        p = say.find(c, pos + 1); assert p > pos, (lines[0], c); pos = p; cues.append(c)
    return cues
def lesson(key, steps):
    L[key] = dict(labels=[], steps=[])
    for i, (label, lines, say) in enumerate(steps):
        add(key, i, '%d. %s' % (i + 1, label), lines, say, auto(lines, say))
T = lambda t: ['title', t]
C = lambda t: ['chalk', t]
K = lambda t: ['code', t]
O = lambda t: ['out', t]

# ---------------- Maths, Grade 2 (Joyful Mathematics order) ----------------
lesson('m2_groups', [
 ('Groups of two', [T('Counting in groups'), C('🐚🐚  🐚🐚  🐚🐚'), K('2, 4, 6')],
  "Welcome to Market Street! At the beach, Ravi puts his shells in pairs. Now count in twos: two, four, six. That is much faster than one by one."),
 ('Groups of five', [T('Groups of five'), C('✋  ✋  ✋'), K('5, 10, 15')],
  "A hand has five fingers. Here are three hands. Count in fives: five, ten, fifteen."),
 ('Groups of ten', [T('Groups of ten'), C('🍌×10   🍌×10   🍌×10   🍌×10'), K('10, 20, 30, 40')],
  "Bananas come in bunches of ten. Here are four bunches. Count in tens: ten, twenty, thirty, forty bananas."),
 ('How many in all', [T('How many in all?'), C('🥭🥭🥭  🥭🥭🥭  🥭🥭🥭  🥭🥭🥭'), K('4 groups of 3 = 12')],
  "The fruit stall packs mangoes in crates of three. There are four crates. Count in threes: three, six, nine, twelve, so four groups of three make twelve."),
 ('Skip counting', [T('Skip counting'), K('2, 4, 6, 8, 10'), K('5, 10, 15, 20, 25'), C('every jump is the same size')],
  "Skip counting means jumping the same amount each time. Jumping in twos goes two, four, six, eight, ten. Jumping in fives goes five, ten, fifteen, twenty, twenty-five. Every jump is the same size, so you never lose count."),
])
lesson('m2_shapes', [
 ('Shapes you hold', [T('Shapes you can hold'), C('⚽   🎲   🥫   🍦')],
  "At the toy-block shop, every toy has a shape you can hold. A ball, a dice, a tin can and an ice cream cone all have different shapes."),
 ('Sphere', [T('Sphere'), C('⚽  🍊  🌍'), C('round all over · it rolls')],
  "A ball is a sphere. An orange and the Earth are spheres too. A sphere is round all over, so it rolls in every direction."),
 ('Cube', [T('Cube'), C('🎲  📦'), C('6 flat square faces · it stacks')],
  "A dice is a cube. Some boxes are cubes too. A cube has six flat faces, all squares, so it stacks but does not roll."),
 ('Cylinder and cone', [T('Cylinder and cone'), C('🥫 cylinder'), C('🍦 cone')],
  "Some shapes have curved faces. A tin can is a cylinder: two flat circles and a curved side, so it can roll and stack. An ice cream cone is a cone: one point and one flat circle."),
 ('Cuboid', [T('Cuboid'), C('📦  🧱  📕')],
  "A box, a brick and a book are cuboids. A cuboid is like a cube, but some of its faces are longer rectangles."),
])
lesson('m2_numbers', [
 ('Tens and ones', [T('Tens and ones'), C('▮▮▮▮  •••••••'), K('47 = 4 tens + 7 ones')],
  "Every house on Market Street has a number. Look at house forty-seven. It is four tens and seven ones."),
 ('Reading numbers', [T('Reading numbers'), K('63 → sixty-three'), K('80 → eighty')],
  "Read the tens first, then the ones. Six tens and three ones is sixty-three. Eight tens and no ones is eighty."),
 ('Before and after', [T('Before and after'), K('58, 59, 60'), C('after 59 comes 60')],
  "Count on from fifty-eight. Fifty-eight, fifty-nine, sixty. After fifty-nine comes sixty, the start of a new ten."),
 ('Bigger or smaller', [T('Bigger or smaller?'), K('72 > 27'), C('compare the tens first')],
  "Which is bigger, seventy-two or twenty-seven? The arrow opens towards the bigger number. Compare the tens first: seven tens beat two tens."),
 ('All the way to 100', [T('All the way to 100'), K('10, 20, 30 … 100'), C('10 tens = 100')],
  "Count the house numbers in tens. Ten, twenty, thirty, all the way to one hundred. Ten tens make one hundred."),
])
lesson('m2_flat', [
 ('Shadows', [T('Shadow shapes'), C('🪙 → ●'), C('📕 → ▬')],
  "Hold things up to the sun and look at their shadows. A coin makes a circle shadow. A book makes a rectangle shadow."),
 ('Circle', [T('Circle'), C('●  no corners, no sides')],
  "A circle is perfectly round. It has no corners and no straight sides."),
 ('Triangle', [T('Triangle'), C('▲  3 sides · 3 corners')],
  "A triangle has three straight sides and three corners. A slice of watermelon looks like a triangle."),
 ('Square and rectangle', [T('Square and rectangle'), C('■  4 sides, all the same'), C('▬  2 long sides, 2 short sides')],
  "Squares and rectangles both have four sides and four corners. A square has four sides, all the same length. A rectangle has two long sides and two short sides."),
 ('Shop signs', [T('Shop signs'), C('●  ▲  ■  ▬')],
  "Now every shop on Market Street gets a sign. The baker has a circle, the toy shop a triangle, and the others squares and rectangles."),
])
lesson('m2_lines', [
 ('Lines everywhere', [T('Lines on the road'), C('|   —   /   ⌒')],
  "Look at the road outside the shops. It is full of lines: standing, sleeping, slanting and curved."),
 ('Standing line', [T('Standing line'), C('|  like a lamp post')],
  "A standing line goes straight up and down. It stands tall, like a lamp post."),
 ('Sleeping line', [T('Sleeping line'), C('—  like the edge of the road')],
  "A sleeping line lies flat from side to side. It lies down, like the edge of the road."),
 ('Slanting line', [T('Slanting line'), C('/  like a slide')],
  "A slanting line leans over. It leans, like a slide in the park."),
 ('Curved line', [T('Curved line'), C('⌒  like a rainbow')],
  "A curved line bends smoothly. It bends, like a rainbow or a road going round a corner."),
])
lesson('m2_addsub', [
 ('Adding', [T('Adding'), K('24 + 13 = 37'), C('ones: 4 + 3 = 7 · tens: 2 + 1 = 3')],
  "It is festival time on Market Street, and we are hanging lights. Twenty-four lights plus thirteen lights makes thirty-seven. Add the ones first, then the tens."),
 ('Adding with a carry', [T('Adding with a carry'), K('28 + 15 = 43'), C('8 + 5 = 13 → write 3, carry 1 ten')],
  "Sometimes the ones make a new ten. Twenty-eight plus fifteen makes forty-three. Eight and five make thirteen, so write three and carry one ten."),
 ('Taking away', [T('Taking away'), K('36 − 9 = 27'), C('💡 36 lights, 9 break')],
  "Some lights break. Thirty-six take away nine leaves twenty-seven. Twenty-seven lights still shine."),
 ('Taking away tens', [T('Taking away tens'), K('50 − 20 = 30'), C('5 tens − 2 tens = 3 tens')],
  "Taking away tens is quick. Fifty take away twenty is thirty. Five tens take away two tens leaves three tens."),
 ('Check by adding back', [T('Check by adding back'), K('27 + 9 = 36 ✓')],
  "You can always check a take-away by adding back. Twenty-seven plus nine gives thirty-six again, so the answer was right."),
])
lesson('m2_measure', [
 ('Long and short', [T('Long and short'), C('🎀 long ribbon · ✂️ short ribbon')],
  "At the tailor's shop, ribbons come long and short. Put them side by side, with the ends lined up, to see which is longer."),
 ('Hand spans', [T('Hand spans'), C('✋✋✋✋✋ = 5 spans')],
  "Stretch your hand wide: that is a hand span. The ribbon is five spans long."),
 ('Centimetres', [T('Centimetres'), K('12 cm'), C('a ruler is the same for everyone')],
  "But your hand and Mum's hand are different sizes. A ruler always measures the same, in centimetres. This ribbon is twelve centimetres long."),
 ('Heavy and light', [T('Heavy and light'), C('🍉 heavy · 🪶 light')],
  "Some things are heavy and some are light. A watermelon is heavy and a feather is light."),
 ('The balance', [T('Using a balance'), C('⚖️ the heavier side goes down')],
  "To compare two things, put them on a balance. The heavier side goes down and the lighter side goes up."),
])
lesson('m2_share', [
 ('Equal groups', [T('Equal groups'), C('🍬🍬🍬🍬 | 🍬🍬🍬🍬 | 🍬🍬🍬🍬'), K('3 groups of 4 = 12')],
  "The sweet shop packs sweets in boxes of four. Here are three boxes. Three groups of four make twelve sweets."),
 ('Times', [T('Times'), K('3 × 4 = 12'), C('× means groups of')],
  "There is a short way to write it. Three times four equals twelve. The times sign means groups of."),
 ('Sharing equally', [T('Sharing equally'), C('12 🍬 → 3 friends'), K('12 ÷ 3 = 4')],
  "Now share twelve laddoos between three friends. Give one each, again and again, until none are left. Each friend gets four, so twelve shared by three is four."),
 ('Partners', [T('Times and sharing are partners'), K('3 × 4 = 12'), K('12 ÷ 3 = 4')],
  "Times and sharing go together. Three times four is twelve. So twelve shared by three is four."),
 ('Left over', [T('Some left over'), C('7 🍬 → 2 friends: 3 each, 1 left')],
  "Sometimes sharing does not come out even. Seven sweets shared by two friends gives three each, with one left over."),
])
lesson('m2_time', [
 ('Days of the week', [T('Days of the week'), K('Mon Tue Wed Thu Fri Sat Sun'), C('7 days in a week')],
  "The clock tower on Market Street shows the day and the time. The days go Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. There are seven days in a week."),
 ('Months', [T('Months of the year'), C('January … December · 12 months')],
  "A year has twelve months. They start with January and end with December."),
 ("O'clock", [T("O'clock"), C('🕗  long hand on 12 · short hand on 8')],
  "When the long hand points to twelve, it is something o'clock. Here the short hand points to eight, so it is eight o'clock."),
 ('Half past', [T('Half past'), C('🕣  long hand on 6 · half past 8')],
  "When the long hand points to six, it is half past. Here it is half past eight."),
 ('Seasons', [T('Seasons'), C('☀️ summer · 🌧️ monsoon · ❄️ winter')],
  "The year also has seasons. Summer is hot, the monsoon brings rain, and winter is cold."),
])
lesson('m2_money', [
 ('Coins and notes', [T('Coins and notes'), C('₹1  ₹2  ₹5  ₹10'), C('₹20  ₹50  ₹100')],
  "Welcome to the coin stall. Coins come as one, two, five and ten rupees. Notes come as twenty, fifty and one hundred rupees."),
 ('Making an amount', [T('Making ₹20'), K('₹10 + ₹5 + ₹5 = ₹20')],
  "There are many ways to make twenty rupees. Ten plus five plus five makes twenty."),
 ('Paying', [T('Paying'), C('🎈 costs ₹15 · you pay ₹20')],
  "A balloon costs fifteen rupees. You pay with a twenty-rupee note."),
 ('Change', [T('Change'), K('₹20 − ₹15 = ₹5')],
  "You paid more than the price, so you get change. Twenty take away fifteen is five, so you get five rupees back."),
 ('Two things', [T('Buying two things'), K('₹12 + ₹8 = ₹20')],
  "To buy two things, add the prices. A pencil for twelve and an eraser for eight cost twenty rupees in all."),
])
lesson('m2_data', [
 ('Tally marks', [T('Tally marks'), C('||||  = 4'), C('5th mark crosses the four')],
  "At the market gate we count with tally marks. Make one line for each thing: four lines show four. The fifth line crosses the four, making a bundle of five."),
 ('Counting cars', [T('Counting cars'), C('🚗  |||| ||  = 7')],
  "Make a tally for each car that passes. One bundle of five and two more is seven cars."),
 ('Most and least', [T('Most and least'), C('🍎 7 · 🍌 3 · 🍊 5')],
  "The fruit stall counted its fruit. Apples have the most, with seven, and bananas have the least, with three."),
 ('Picture chart', [T('Picture chart'), C('🍎🍎🍎🍎🍎🍎🍎'), C('🍌🍌🍌')],
  "A picture chart shows the same counts with pictures. Here is a row of seven apples, and under it a row of three bananas. The longest row has the most."),
 ('Asking questions', [T('Asking questions'), K('7 − 3 = 4 more apples')],
  "Charts help us answer questions. How many more apples than bananas? Seven take away three is four more apples."),
])
lesson('m2_challenge', [
 ('Market Day', [T('Market Day!'), C('🏪 count · share · add · give change')],
  "Challenge time: it is Market Day, and you run the fruit stall! You will count, share, add up prices and give change."),
 ('Count the stock', [T('Count the stock'), C('🥭🥭🥭🥭🥭 ×4 crates'), K('5, 10, 15, 20')],
  "First count the mangoes. There are four crates of five. Five, ten, fifteen, twenty mangoes."),
 ('Share into bags', [T('Share into bags'), K('20 ÷ 4 = 5')],
  "Four customers want the same number. Twenty shared by four is five each."),
 ('Add the prices', [T('Add the prices'), K('₹25 + ₹14 = ₹39')],
  "A customer buys mangoes for twenty-five rupees and bananas for fourteen. Twenty-five plus fourteen is thirty-nine rupees."),
 ('Give change', [T('Give change'), K('₹50 − ₹39 = ₹11')],
  "They pay with fifty rupees. Fifty take away thirty-nine is eleven rupees change. You ran the market stall!"),
])

# ---------------- English, Grade 2 (phonics first, then words and sentences) ----------------
lesson('e2_s1', [
 ('Sounds, not names', [T('Letters make sounds'), C('s · a · t · p · i · n')],
  "Welcome to the Picture-book Corner! Every letter has a name and a sound, and to read we use the sounds."),
 ('s and a', [T('s and a'), C('s  🐍  sss  ·  sun'), C('a  🐜  a  ·  ant')],
  "Here are our first two sounds. S says sss, like a snake, and sun starts with sss. A says a, like the start of ant."),
 ('t and p', [T('t and p'), C('t  🚰  t  ·  tap'), C('p  🖊️  p  ·  pen')],
  "Now t and p are short, quick sounds. T says t, like the start of tap. P says p, like the start of pen."),
 ('i and n', [T('i and n'), C('i  🐛  i  ·  insect'), C('n  🥅  nnn  ·  net')],
  "Next come i and n. I says i, like the start of insect. N says nnn, like the start of net."),
 ('Hear the first sound', [T('Hear the first sound'), C('sun → s · pen → p · net → n')],
  "Say a word slowly and listen to how it starts. Sun starts with s, pen starts with p, and net starts with n."),
])
lesson('e2_s2', [
 ('More sounds', [T('More sounds'), C('m · d · g · o · c · k')],
  "Here are six more sounds for our wall. Listen to each one, then say it after me."),
 ('m and d', [T('m and d'), C('m  🗺️  mmm  ·  map'), C('d  🐶  d  ·  dog')],
  "M says mmm, as if something tastes nice. Map starts with mmm. D says d, and dog starts with d."),
 ('g and o', [T('g and o'), C('g  🚪  g  ·  gate'), C('o  🐙  o  ·  on')],
  "G says g, like the start of gate. Now listen to o. O says o, like the start of on."),
 ('c and k', [T('c and k'), C('c  🐱  ·  k  🪁'), C('both say the same sound')],
  "C and k make the same sound. Cat starts with c, and kite starts with k. Two letters, one sound!"),
 ('First blend', [T('Blend your first word'), C('m · a · p → map'), C('d · o · g → dog')],
  "Now push sounds together. M, a, p makes map. D, o, g makes dog."),
])
lesson('e2_s3', [
 ('The last short sounds', [T('The rest of the short sounds'), C('e · u · r · h · b · f · l')],
  "Here are the rest of the short sounds. After this lesson you can read lots of words."),
 ('e and u', [T('e and u'), C('e  🥚  e  ·  egg'), C('u  ☂️  u  ·  up')],
  "Listen to the short vowels. E says e, like the start of egg. U says u, like the start of up."),
 ('r and h', [T('r and h'), C('r  🐀  rrr  ·  rat'), C('h  🎩  h  ·  hat')],
  "R says rrr, like a growling dog. Rat starts with r. H says h, like a little breath, and hat starts with h."),
 ('b, f and l', [T('b, f and l'), C('b  🦇 bat · f  🐟 fish'), C('l  🦁 lion')],
  "B says b, like the start of bat. F says fff, like fish. L says lll, like lion."),
 ('Vowels', [T('The five vowels'), C('a  e  i  o  u')],
  "The letters a, e, i, o and u are vowels. Almost every word needs at least one vowel."),
])
lesson('e2_blend', [
 ('Push the sounds together', [T('Blending'), C('c · a · t'), C('cat 🐱')],
  "Reading a word is like pushing beads together on a string. Say each sound: c, a, t. Now push them together fast: cat!"),
 ('Short words', [T('Three-sound words'), C('p · i · g → pig 🐷'), C('s · u · n → sun ☀️')],
  "Let us try more. P, i, g makes pig. S, u, n makes sun."),
 ('Change one sound', [T('Change one sound'), C('cat → hat → hot → hop')],
  "Change just one sound and you get a new word. Cat becomes hat, hat becomes hot, and hot becomes hop."),
 ('Sounding out', [T('Sound it out'), C('b · e · d → bed 🛏️')],
  "When you meet a new word, do not guess. Sound it out: b, e, d, bed."),
 ('Reading a sentence', [T('Read a sentence'), C('The cat sat on a mat.')],
  "Now read a whole sentence, one word at a time. The cat sat on a mat."),
])
lesson('e2_digraph', [
 ('Two letters, one sound', [T('Two letters, one sound'), C('sh · ch · th · ng')],
  "Sometimes two letters work together to make one new sound. We call them sound pairs."),
 ('sh', [T('sh'), C('sh  🚢  ship · fish 🐟')],
  "S and h together say sh, like asking for quiet. Ship starts with sh, and fish ends with sh."),
 ('ch', [T('ch'), C('ch  🍟  chips · 🧀 cheese')],
  "C and h together say ch, like a sneezing train. Chips and cheese start with ch."),
 ('th', [T('th'), C('th  👍  thumb · 🛁 bath')],
  "T and h together say th: put your tongue between your teeth. Thumb starts with th, and bath ends with th."),
 ('ng', [T('ng'), C('ng  💍  ring · 👑 king')],
  "N and g together say ng, deep in your nose. Ring and king end with ng."),
])
lesson('e2_long', [
 ('Long sounds', [T('Long vowel sounds'), C('a → ai · e → ee · o → oa')],
  "Vowels can make a long sound too. A long vowel says its own name."),
 ('ai', [T('ai'), C('ai  🌧️  rain · 🚂 train')],
  "A and i together say ai, the name of the letter a. Rain and train have the ai sound."),
 ('ee', [T('ee'), C('ee  🌳  tree · 🐝 bee')],
  "Two e's together say ee. Tree and bee have the ee sound."),
 ('oa', [T('oa'), C('oa  ⛵  boat · 🐐 goat')],
  "O and a together say oa. Boat and goat have the oa sound."),
 ('Magic e', [T('Magic e'), C('cap 🧢 → cape 🦸'), C('kit → kite 🪁')],
  "An e at the end of a word is magic. It is silent, but it makes the vowel say its name. Cap becomes cape, and kit becomes kite."),
])
lesson('e2_tricky', [
 ('Tricky words', [T('Tricky words'), C('the · said · was · they · come')],
  "Some words do not follow the sounds. We call them tricky words, and we learn them by sight."),
 ('the', [T('the'), C('the  ·  the cat · the sun')],
  "The word the is everywhere. Look at it, say it, and spot it in the cat and the sun."),
 ('said and was', [T('said · was'), C('"Hi," said Ravi.'), C('It was hot.')],
  "Said and was look odd but are very common. Hi, said Ravi. It was hot."),
 ('they and come', [T('they · come'), C('They come to play.')],
  "They and come are tricky too. They come to play."),
 ('Spot them', [T('Spot the tricky words'), C('They said the cat was hot.')],
  "Find the tricky words in this sentence. They said the cat was hot."),
])
lesson('e2_words', [
 ('Naming words', [T('Naming words'), C('🐶 dog · 🏫 school · 👩 Mum')],
  "Words do different jobs. Naming words name a person, a place, an animal or a thing: dog, school and Mum are naming words."),
 ('More naming words', [T('Name it'), C('🍎 apple · 🚌 bus · 🌳 tree')],
  "Look around you and name things. Apple, bus and tree are all naming words."),
 ('Doing words', [T('Doing words'), C('🏃 run · 🦘 jump · 🍽️ eat')],
  "Doing words tell us what someone does. Run, jump and eat are doing words."),
 ('In a sentence', [T('Find them in a sentence'), C('The dog runs.'), C('naming: dog · doing: runs')],
  "A sentence often has both. The dog runs. Dog is the naming word and runs is the doing word."),
 ('Act it out', [T('Act it out'), C('🐸 The frog jumps.')],
  "Doing words are fun to act out. The frog jumps: now you jump too!"),
])
lesson('e2_describe', [
 ('Describing words', [T('Describing words'), C('big · red · soft · happy')],
  "Describing words tell us more about a naming word. Big, red, soft and happy are describing words."),
 ('Colour and size', [T('Colour and size'), C('a big red ball ⚽')],
  "We can describe colour and size. A big red ball."),
 ('How it feels', [T('How it feels'), C('a soft cushion · a happy girl 😊')],
  "We can describe how something feels too. A soft cushion, and a happy girl."),
 ('a or an', [T('a or an'), C('a cat 🐱 · a ball ⚽'), C('an apple 🍎 · an egg 🥚')],
  "Before a word, we use a or an. Use a before most sounds: a cat, a ball. Use an before a vowel sound: an apple, an egg."),
 ('Put it together', [T('Put it together'), C('an old owl 🦉 · a tiny ant 🐜')],
  "Now put them together. An old owl, and a tiny ant."),
])
lesson('e2_plural', [
 ('One and many', [T('One and many'), C('1 cat 🐱 → 2 cats 🐱🐱')],
  "When there is more than one, the word changes. One cat, two cats: we add s."),
 ('Add s', [T('Add s'), C('dog → dogs · pen → pens · book → books')],
  "For most words, just add s. Dog becomes dogs, pen becomes pens, and book becomes books."),
 ('Add es', [T('Add es'), C('box → boxes · bus → buses · dish → dishes')],
  "Words ending in x, s, sh or ch add the letters e and s, so you can hear the extra sound. Box becomes boxes, bus becomes buses, and dish becomes dishes."),
 ('Special words', [T('Special words'), C('man → men · child → children · mouse → mice')],
  "A few words change in their own way. One man, two men. One child, two children, and one mouse, two mice."),
 ('Count and say', [T('Count and say'), C('3 🍎 → three apples')],
  "Count things and say the word for many. Three apples!"),
])
lesson('e2_sentence', [
 ('A sentence', [T('A sentence'), C('The sun is hot.')],
  "A sentence is a group of words that makes sense on its own. The sun is hot."),
 ('Capital letter', [T('Start with a capital'), C('The · My · We'), C('names too: Ravi, Delhi')],
  "Every sentence starts with a capital letter. The, my and we begin with capitals at the start. Names always have capitals too, like Ravi and Delhi."),
 ('Full stop', [T('End with a full stop'), C('I like mangoes.')],
  "Every sentence ends with a full stop. I like mangoes, full stop."),
 ('Rhyming words', [T('Rhyming words'), C('cat · hat · mat'), C('sun · fun · run')],
  "Words rhyme when they end with the same sound. Cat, hat and mat rhyme. Sun, fun and run rhyme too."),
 ('A little poem', [T('A little poem'), C('The cat in a hat'), C('sat on a mat.')],
  "Poems often use rhymes. The cat in a hat. Sat on a mat."),
])
lesson('e2_story', [
 ('Picture talk', [T('Talk about a picture'), C('🧒 🐱 🌳  Who? Where? What?')],
  "Look at a picture and ask questions. Who is in it, where are they, and what is happening?"),
 ('The story begins', [T('The lost kitten'), C('Mina had a little kitten.'), C('One day, the kitten was lost.')],
  "Here is a short story. Mina had a little kitten. One day, the kitten was lost."),
 ('The middle', [T('Looking for it'), C('Mina looked under the bed.'), C('She looked up the tree. 🌳')],
  "Where could it be? Mina looked under the bed, but it was not there. Then she looked up the tree."),
 ('The end', [T('Found!'), C('The kitten was in the tree!'), C('Mina was happy. 😊')],
  "Look up! The kitten was in the tree! Mina helped it down, and she was happy."),
 ('Questions', [T('Who, where and how'), C('Who? Mina · Where? In the tree · How did she feel? Happy')],
  "Good readers ask questions about a story. Who lost the kitten, where was it, and how did Mina feel at the end?"),
])
lesson('e2_challenge', [
 ('Story Time', [T('Story Time!'), C('🎭 sound out · read · answer')],
  "Challenge time: it is Story Time in the puppet theatre! Sound out new words, read the story and answer the questions."),
 ('Sound it out', [T('Sound it out'), C('f · i · sh → fish 🐟')],
  "First, a new word. F, i, sh makes fish."),
 ('Read the story', [T('The fish and the duck'), C('A fish swam in the pond.'), C('A duck came to play.')],
  "Now read the story. A fish swam in the pond. A duck came to play."),
 ('Keep reading', [T('Splash!'), C('They had fun in the rain. 🌧️'), C('Then they went to sleep. 😴')],
  "Splash, splash! They had fun in the rain. Then they went to sleep."),
 ('Answer', [T('Answer the questions'), C('Where did the fish swim? · Who came to play?')],
  "Now answer. Where did the fish swim, and who came to play? You are a reader now!"),
])
