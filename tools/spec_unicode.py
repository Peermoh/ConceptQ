KEY, IDX = 'unicode', 23
META = dict(tag='Text and Unicode · Third floor', title='Text and Unicode: every letter is a number', topic='Unicode',
            lastBtn='Set up the parcel sorter', doneTitle='The parcel sorter is ready!',
            doneText='You learned that every character is a number: ASCII, Unicode, UTF-8 bytes, str and bytes, character checks, and sorting text. Parts for the loft arrive with labels in many languages, and the parcel sorter reads them all. It is in the house: drop in a parcel to see its number.')
QUIZ = [
 ('What does this show?', 'print(ord("B"))', ['66', '65', 'B', '98'], 0,
  ['A is 65, so B is 66.', '65 is A. B comes next.', 'ord gives the number, not the letter.', '98 is small b.'], 0),
 ('What does this show?', 'print(chr(99))', ['c', '99', 'C', 'b'], 0,
  ['99 is small c (a is 97).', 'chr gives the character, not the number.', 'Capital C is 67.', 'b is 98.'], 1),
 ('What does this show?', 'print(len("é".encode()))', ['2', '1', '3', 'An error'], 0,
  ['In UTF-8, é takes 2 bytes.', 'len of the text is 1, but encoded it is 2 bytes.', 'é needs 2 bytes, not 3.', 'encode() works on any text.'], 5),
 ('What does this show?', 'print("Z" < "a")', ['True', 'False', 'Z', 'An error'], 0,
  ['Z is 90 and a is 97, and capitals come first.', 'Capital letters have smaller numbers.', '< gives True or False.', 'Comparing text is allowed.'], 7),
 ('What does this show?', 'print(sorted(["b", "A", "c"]))', ["['A', 'b', 'c']", "['b', 'A', 'c']", "['c', 'b', 'A']", "['A', 'c', 'b']"], 0,
  ['Capital A (65) comes before the small letters.', 'sorted puts them in order.', 'That is backwards.', 'b comes before c.'], 8),
 ('What does this show?', 'print(b"hi".decode())', ['hi', "b'hi'", '"hi"', 'An error'], 0,
  ['decode turns the bytes back into text: hi.', 'After decode it is text, so there is no b.', 'print shows text without quotes.', 'decode works on bytes.'], 4),
 ('What does this show?', 'print("x7".isalnum())', ['True', 'False', 'x7', 'An error'], 0,
  ['isalnum is True when every character is a letter or a digit.', 'x is a letter and 7 is a digit, so it is True.', 'isalnum gives True or False.', 'isalnum works on any string.'], 6),
 ('Which one is bytes, not text?', '# pick one', ['b"cat"', '"cat"', "'cat'", '"""cat"""'], 0,
  ['A b in front of the quotes makes bytes.', 'That is text (a str).', 'Single quotes are still text.', 'Triple quotes are still text.'], 4),
]
CARDS = [
 ('u1', 'types', 23, 'What do `ord("A")` and `chr(97)` give?', '65 and "a".'),
 ('u2', 'types', 23, 'What is UTF-8?', 'The usual way to turn Unicode text into bytes: `"é".encode()`.'),
 ('u3', 'types', 23, 'Is `"Z" < "a"` True?', 'Yes: capitals have smaller numbers (Z is 90, a is 97).'),
 ('u4', 'types', 23, 'How do you sort words ignoring capitals?', '`sorted(words, key=str.lower)`'),
]
GEN_STEPS = [0, 1, 7, 5]
GEN_JS = r'''
      function () { var L = String.fromCharCode(ri(66, 89)), n = L.charCodeAt(0);
        return mk('What does this show?', 'print(ord("' + L + '"))', [[n, 'A is 65, so ' + L + ' is ' + n + '.'], [n + 32, 'That is small ' + L.toLowerCase() + '. Capitals come first.'], [n - 1, 'That is ' + String.fromCharCode(n - 1) + '. Count again from A = 65.'], [L, 'ord gives the number, not the letter.']]); },
      function () { var n = ri(98, 121), c = String.fromCharCode(n);
        return mk('What does this show?', 'print(chr(' + n + '))', [[c, n + ' is small ' + c + ' (a is 97).'], [c.toUpperCase(), 'Capitals are 32 smaller: ' + c.toUpperCase() + ' is ' + (n - 32) + '.'], [String.fromCharCode(n + 1), 'That is ' + (n + 1) + '. Count again from a = 97.'], [n, 'chr gives the character, not the number.']]); },
      function () { var pairs = [['Zebra', 'apple'], ['cat', 'Cat'], ['Bee', 'ant'], ['dog', 'Dog'], ['ant', 'bee']], p = pickOne(pairs), r = p[0] < p[1];
        return mk('What does this show?', 'print("' + p[0] + '" < "' + p[1] + '")', [[r ? 'True' : 'False', 'Python compares the first different letters by their numbers: ' + p[0][0] + ' is ' + p[0].charCodeAt(0) + ', ' + p[1][0] + ' is ' + p[1].charCodeAt(0) + '.'], [r ? 'False' : 'True', 'Remember: capitals have smaller numbers than small letters.'], [p[0], '< gives True or False.'], ['An error', 'Comparing text is allowed.']]); },
      function () { var w = pickOne(['café', 'naïve', 'hello', 'über', 'cat', 'Zoë']), b = new TextEncoder().encode(w).length;
        return mk('What does this show?', 'print(len("' + w + '".encode()))', [[b, w + ' takes ' + b + ' bytes in UTF-8' + (b > w.length ? ': the accented letter needs 2.' : '.')], [w.length === b ? b + 1 : w.length, w.length === b ? 'Plain letters need 1 byte each.' : 'That counts characters. Encoded, the accented letter takes 2 bytes.'], [b + 2, 'Count the bytes again: plain letters 1, accented 2.'], ['An error', 'encode() works on any text.']]); }
'''
