KEY, IDX = 'regex', 44
META = dict(tag='Regular expressions · Rooftop garden', title='Regular expressions: find by shape', topic='regular expressions',
            lastBtn='Sift the seeds', doneTitle='The seed sieve is ready!',
            doneText='You learned why patterns help, re.search, character classes, how many, findall, groups, re.sub and compiled patterns. A seed sieve now sits on the potting bench. It is in your garden: pour in some text and keep only what matches.')
QUIZ = [
 ('What does this show?', 'import re\nm = re.search(r"\\d+", "bed 12 is dry")\nprint(m.group())', ['12', '1', 'bed', '"bed 12 is dry"'], 0,
  ['\\d+ is one or more digits, so it finds 12.', '+ keeps going while there are digits.', 'bed has no digits.', 'search gives just the part that matched.'], 1),
 ('What does \\d match?', 'r"\\d"', ['Any one digit', 'Any letter', 'A space', 'The letter d'], 0,
  ['\\d means a digit, 0 to 9.', 'That is closer to \\w.', 'That is \\s.', 'The backslash makes it special.'], 2),
 ('What does + mean in a pattern?', 'r"\\d+"', ['One or more', 'Zero or more', 'Maybe one', 'Add two numbers'], 0,
  ['\\d+ is one or more digits.', 'That is *.', 'That is ?.', 'In a pattern, + is about how many.'], 3),
 ('What does this show?', 'import re\nprint(re.findall(r"\\d+", "beds 3, 7 and 12"))', ["['3', '7', '12']", "['3']", "['3', '7', '1', '2']", '[3, 7, 12]'], 0,
  ['findall gives every match, as strings.', 'That is only the first one, like search.', '+ keeps 12 together.', 'Matches are strings, not numbers.'], 4),
 ('What does this show?', 'import re\nm = re.search(r"(\\d+)-(\\d+)", "rows 4-9")\nprint(m.group(2))', ['9', '4', '4-9', '-'], 0,
  ['group(2) is the second pair of round brackets.', 'That is group(1).', 'That is group(0), the whole match.', 'The dash is not in a group.'], 5),
 ('What does this show?', 'import re\nprint(re.sub(r"\\s+", " ", "too    many   spaces"))', ['too many spaces', 'toomanyspaces', 'too    many   spaces', 'too_many_spaces'], 0,
  ['Every run of spaces becomes one space.', 'They are replaced by one space, not removed.', 'sub changes the spaces.', 'They become spaces, not underscores.'], 6),
 ('Which code matches r"[A-Z]{2}-\\d{3}" fully?', 'PLANT = re.compile(r"[A-Z]{2}-\\d{3}")', ['TM-042', 'tm-042', 'TM-42', 'TMX-042'], 0,
  ['Two capitals, a dash, then exactly three digits.', '[A-Z] means capital letters.', '\\d{3} needs exactly three digits.', '{2} means exactly two letters.'], 7),
]
CARDS = [
 ('rx1', 'world', 44, 'What do `\\d`, `\\w` and `\\s` match?', 'A digit; a letter, digit or underscore; a space.'),
 ('rx2', 'world', 44, 'What do `+`, `*` and `?` mean in a pattern?', 'One or more; zero or more; maybe one.'),
 ('rx3', 'world', 44, '`re.search` or `re.findall`?', '`search` finds the first match; `findall` gives a list of all of them.'),
 ('rx4', 'world', 44, 'How do you replace every run of spaces with one space?', '`re.sub(r"\\s+", " ", text)`'),
]
GEN_STEPS = [4, 6, 7]
GEN_JS = r'''
      function () { var ns = shuffled([3, 7, 12, 25, 40, 8, 101]).slice(0, ri(2, 3)), words = ['beds', 'rows', 'trays'], text = pickOne(words) + ' ' + ns.join(', ');
        var digits = ns.join('').split('');
        return mk('What does this show?', 'import re\nprint(re.findall(r"\\d+", "' + text + '"))', [[pyList(ns.map(String)), 'findall gives every run of digits, as strings.'], [pyList([String(ns[0])]), 'That is just the first, like search.'], ['[' + ns.join(', ') + ']', 'Matches are strings, so they have quotes.'], [pyList(digits), '+ keeps the digits of each number together.']]); },
      function () { var t = pickOne(['peas 12, kale 7', 'bed 3 row 45', 'tray 9 of 10']), ch = pickOne(['#', '*', '?']);
        var out = t.replace(/\d/g, ch), out2 = t.replace(/\d+/g, ch);
        return mk('What does this show?', 'import re\nprint(re.sub(r"\\d", "' + ch + '", "' + t + '"))', [[out, '\\d matches one digit, so every digit is replaced.'], [out2 === out ? t.replace(/\d/, ch) : out2, '\\d without + is one digit at a time.'], [t, 'sub replaces every match.'], [t.replace(/\d/g, ''), 'Each digit becomes ' + ch + ', it is not removed.']]); },
      function () { var good = pickOne([true, false]), L = 'ABCDEKLMPTZ', a = L[ri(0, 10)] + L[ri(0, 10)], d = String(ri(100, 999));
        var code = good ? a + '-' + d : pickOne([a.toLowerCase() + '-' + d, a + '-' + d.slice(0, 2), a + d, a + 'X-' + d]);
        return mk('What does this show?', 'import re\nprint(bool(re.fullmatch(r"[A-Z]{2}-\\d{3}", "' + code + '")))', [[good ? 'True' : 'False', good ? 'Two capitals, a dash and three digits: it matches.' : code + ' does not have exactly two capitals, a dash and three digits.'], [good ? 'False' : 'True', 'Check each part: [A-Z]{2}, then -, then \\d{3}.'], ['None', 'bool() gives True or False.'], ['An error', 'fullmatch works on any string.']]); }
'''
