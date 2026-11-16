KEY, IDX = 'files', 18
META = dict(tag='Files · Second floor', title='Files: saving for tomorrow', topic='files',
            lastBtn='Open the attic', doneTitle='The attic is open!',
            doneText='You learned to read and write files with open and with, the "w" and "a" modes, reading line by line, CSV rows, and catching a missing file. The attic light is on: it keeps things after you go to sleep, like a file. Your filing cabinet is in the house.')
QUIZ = [
 ('Which mode adds to the end of a file and keeps what was there?', 'open("notes.txt", "?")', ['"a"', '"w"', '"r"', '"x"'], 0,
  ['"a" means append: new text goes on the end.', '"w" wipes the file first, then writes.', '"r" only reads. It cannot write.', '"x" makes a brand new file and fails if it exists.']),
 ('What is the danger of this line?', 'open("diary.txt", "w")', ['It wipes the diary first', 'It cannot write', 'It reads the diary', 'Nothing'], 0,
  ['"w" empties the file before writing, so the old diary is gone.', '"w" is for writing.', 'This opens the file for writing, not reading.', '"w" is risky: it wipes the file.']),
 ('Why use with open(...) as f:?', 'with open("notes.txt") as f:\n    text = f.read()', ['It closes the file for you', 'It reads faster', 'It makes a new file', 'It hides errors'], 0,
  ['When the indented part ends, the file is closed, even if something goes wrong.', 'Speed is the same. The point is closing safely.', 'Without a mode, this opens a file to read.', 'Errors still show up.']),
 ('What does this show?', 'row = "Mia,9,blue"\nprint(row.split(",")[2])', ['blue', '9', 'Mia', 'Mia,9,blue'], 0,
  ['split gives [Mia, 9, blue], and [2] is blue.', '9 is at position 1.', 'Mia is at position 0.', '[2] picks one part of the split.']),
 ('What happens if notes.txt does not exist?', 'open("notes.txt")', ['A FileNotFoundError', 'An empty file', 'None', 'A new file is made'], 0,
  ['Reading a file that is not there is a FileNotFoundError.', 'Python does not pretend it is empty.', 'open does not give None.', 'Read mode never makes a file. "w" would.']),
 ('What does this show?', 'line = "Hi!\\n"\nprint(len(line.strip()))', ['3', '4', '5', '2'], 0,
  ['strip removes the new line at the end, leaving Hi!: 3 characters.', 'That counts the \\n too. strip removed it.', 'Count again: H, i and !.', 'The ! counts as a character too.']),
 ('Where does open("notes.txt") look?', '# no folder in the name', ['The same folder as the program', 'The whole computer', 'The internet', 'The attic'], 0,
  ['A plain file name means: next to your program.', 'Python does not search everywhere.', 'open reads files on the computer.', 'Only in our house!']),
]
CARDS = [
 ('fi1', 'talk', 18, 'What is the difference between `"w"` and `"a"`?', '`"w"` wipes the file and writes; `"a"` adds to the end.'),
 ('fi2', 'talk', 18, 'Why `with open(...) as f:`?', 'It closes the file for you, even if something goes wrong.'),
 ('fi3', 'talk', 18, 'How do you read a file line by line?', '`for line in f:` and `line.strip()` to drop the new line.'),
 ('fi4', 'bugs', 18, 'What error comes from opening a file that is not there?', 'FileNotFoundError. Catch it with try / except.'),
]
GEN_JS = r'''
      function () { var cols = [pickOne(['Mia', 'Ali', 'Sam', 'Zoe']), String(ri(5, 15)), pickOne(['blue', 'red', 'green'])], i = ri(0, 2);
        return mk('What does this show?', 'row = "' + cols.join(',') + '"\nprint(row.split(",")[' + i + '])', [[cols[i], 'split gives ' + pyList(cols) + ', and [' + i + '] is ' + cols[i] + '.'], [cols[(i + 1) % 3], 'That is at position ' + ((i + 1) % 3) + '.'], [cols.join(','), '[' + i + '] picks one part of the split.'], [i, '[' + i + '] gives the part, not the number.']]); },
      function () { var n = ri(2, 4), cols = []; for (var k = 0; k < n; k++) cols.push(pickOne(['a', 'b', 'c', 'x']) + k);
        return mk('What does this show?', 'row = "' + cols.join(',') + '"\nprint(len(row.split(",")))', [[n, 'split cuts at each comma, giving ' + n + ' parts.'], [n - 1, 'That counts the commas. There is one more part than commas.'], [cols.join(',').length, 'That is how many characters. split counts parts.'], [1, 'split cuts the row at every comma.']]); },
      function () { var w = pickOne(['Hi!', 'tea', 'cake', 'Done']);
        return mk('What does this show?', 'line = "' + w + '\\n"\nprint(len(line.strip()))', [[w.length, 'strip removes the new line, leaving ' + w + ': ' + w.length + ' characters.'], [w.length + 1, 'That counts the \\n too. strip removed it.'], [w.length + 2, 'The \\n is one character, and strip removes it.'], [0, 'strip only removes the spaces and new lines at the ends.']]); }
'''
