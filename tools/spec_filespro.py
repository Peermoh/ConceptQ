KEY, IDX = 'filespro', 30
META = dict(tag='Files pro · Third floor', title='Files pro: text, bytes and paths', topic='files and paths',
            lastBtn='Fill the archive', doneTitle='The archive room is ready!',
            doneText='You learned every file mode, binary files and bytes, and pathlib: joining paths, checking they exist, reading and writing in one line, and finding files with glob. The loft archive keeps photos and notes on labelled shelves. Your archive cabinet is in the house: open a drawer by its path.')
QUIZ = [
 ('Which mode makes a file only if it does not exist yet?', 'open("log.txt", "?")', ['"x"', '"w"', '"a"', '"r"'], 0,
  ['"x" refuses with FileExistsError if the file is already there.', '"w" would wipe an existing file.', '"a" adds to an existing file.', '"r" only reads.'], 1),
 ('How do you open a picture?', 'open("photo.png", "?")', ['"rb"', '"r"', '"w"', '"a"'], 0,
  ['Pictures are bytes, so read them in binary: "rb".', '"r" reads text, and a picture is not text.', '"w" would wipe the picture.', '"a" adds to the end.'], 2),
 ('What does this show?', 'from pathlib import Path\np = Path("archive") / "photos" / "cat.png"\nprint(p.name)', ['cat.png', 'archive', 'photos', 'archive/photos/cat.png'], 0,
  ['.name is just the last part of the path.', 'archive is the first folder.', 'photos is the folder it is in.', 'That is the whole path. .name is the last part.'], 5),
 ('What does this show?', 'from pathlib import Path\nprint(Path("cat.png").suffix)', ['.png', 'cat', 'png', 'cat.png'], 0,
  ['.suffix is the ending, with its dot.', 'That is the .stem.', '.suffix keeps the dot.', 'That is the .name.'], 5),
 ('What does read() give in "rb" mode?', 'with open("photo.png", "rb") as f:\n    data = f.read()', ['bytes, like b\'\\x89PNG…\'', 'text', 'a list of lines', 'a Path'], 0,
  ['Binary mode gives bytes.', 'Text needs "r" mode.', 'read() gives everything at once.', 'Path is for the file\'s name, not its contents.'], 3),
 ('What does this show?', 'from pathlib import Path\nprint(Path("no_such_file.txt").exists())', ['False', 'True', 'An error', 'None'], 0,
  ['exists() checks, and the file is not there.', 'There is no such file.', 'exists() never raises an error.', 'exists() gives True or False.'], 6),
 ('What finds every .png in a folder?', 'Path("archive").glob("?")', ['"*.png"', '".png"', '"png*"', '"all png"'], 0,
  ['* means any name, so "*.png" matches every .png file.', 'That only matches a file called exactly ".png".', 'That matches names starting with png.', 'glob uses * patterns.'], 8),
]
CARDS = [
 ('fp1', 'talk', 30, 'What do the modes "x" and "rb" mean?', '"x": make a new file only (error if it exists). "rb": read bytes.'),
 ('fp2', 'talk', 30, 'How do you join paths with pathlib?', '`Path("archive") / "photos" / "cat.png"`'),
 ('fp3', 'talk', 30, 'What are `.name`, `.stem` and `.suffix` of cat.png?', 'cat.png, cat and .png'),
 ('fp4', 'talk', 30, 'How do you find all the .png files in a folder?', '`Path("archive").glob("*.png")`'),
]
GEN_STEPS = [5, 5]
GEN_JS = r'''
      function () { var a = pickOne(['archive', 'data', 'loft']), b = pickOne(['photos', 'notes', 'music']), c = pickOne(['cat.png', 'list.txt', 'song.mp3']);
        return mk('What does this show?', 'from pathlib import Path\nprint(Path("' + a + '") / "' + b + '" / "' + c + '")', [[a + '/' + b + '/' + c, 'The slash joins the parts into one path.'], [a + b + c, 'The parts are joined with slashes between them.'], [c, 'print shows the whole path, not just the last part.'], [a + ' / ' + b + ' / ' + c, 'There are no spaces in the path.']]); },
      function () { var f = pickOne([['cat', '.png'], ['notes', '.txt'], ['song', '.mp3'], ['map', '.json']]), full = f[0] + f[1], attr = pickOne(['name', 'stem', 'suffix']);
        var val = { name: full, stem: f[0], suffix: f[1] }[attr];
        var all = [[full, '.name is the whole file name.'], [f[0], '.stem is the name without its ending.'], [f[1], '.suffix is the ending, with its dot.'], [f[1].slice(1), 'The suffix keeps its dot.']];
        return mk('What does this show?', 'from pathlib import Path\nprint(Path("loft/' + full + '").' + attr + ')', [[val, '.' + attr + ' of ' + full + ' is ' + val + '.']].concat(all.filter(function (x) { return x[0] !== val; }).slice(0, 3))); }
'''
