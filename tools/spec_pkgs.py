KEY, IDX = 'pkgs', 21
META = dict(tag='Packages · Third floor', title='Packages: your own toolboxes', topic='packages',
            lastBtn='Build the workshop', doneTitle='The workshop is built!',
            doneText='You learned to make your own modules and packages, run or import them, and install new ones with pip. The garage workshop is built, ready to make the loft. Your workbench is in the house: every drawer is a module.')
QUIZ = [
 ('What does this show?', 'import math as m\nprint(m.floor(2.7))', ['2', '3', '2.7', 'An error'], 0,
  ['as gives math the short name m, and floor rounds down: 2.', 'floor rounds down, not up.', 'floor gives a whole number.', 'm is a nickname for math, so this works.'], 2),
 ('Why avoid from tools import *?', '# from tools import *', ['You cannot tell where names come from', 'It is slower', 'It is a SyntaxError', 'It imports nothing'], 0,
  ['* pours in every name, so later you cannot see which module a name came from.', 'Speed is not the problem. Mystery names are.', 'It is allowed, which is why it is risky.', 'It imports everything, which is the problem.'], 2),
 ('When does the print run?', 'if __name__ == "__main__":\n    print("Hi")', ['Only when you run this file', 'Every time it is imported', 'Never', 'Only inside a package'], 0,
  ['When you run the file itself, its __name__ is "__main__".', 'When imported, __name__ is the module name, so it is skipped.', 'Running the file makes the check True.', 'It depends on how the file is used, not where it is.'], 4),
 ('What makes a folder a package, the classic way?', '# workshop/ …', ['An __init__.py file inside it', 'A requirements.txt file', 'A .venv folder', 'A __pycache__ folder'], 0,
  ['__init__.py marks the folder as a package.', 'requirements.txt lists what to install, it does not make a package.', 'A virtual environment is separate from packages.', 'Python makes __pycache__ by itself.'], 5),
 ('What does pip do?', 'pip install requests', ['Downloads and installs a package', 'Runs your program', 'Deletes a module', 'Makes a new folder'], 0,
  ['pip is the delivery van: it brings packages other people made.', 'python runs your program. pip installs packages.', 'pip install adds, it does not delete.', 'It installs a package, not a folder.'], 7),
 ('What kind of thing is sys.path?', 'import sys\nprint(type(sys.path))', ["<class 'list'>", "<class 'str'>", "<class 'dict'>", 'An error'], 0,
  ['sys.path is a list of the folders Python searches.', 'It holds many folders, so it is a list.', 'It is a list of folders, not a dictionary.', 'sys.path is always there.'], 3),
 ('Why use a virtual environment?', 'python -m venv .venv', ['Each project gets its own packages', 'It makes code faster', 'You need it to print', 'It backs up your files'], 0,
  ['A venv keeps one project\'s packages apart from another\'s.', 'It does not change speed.', 'print works anywhere.', 'It is not a backup.'], 8),
 ('What is __pycache__ for?', '__pycache__/', ['Ready-to-run copies of modules', 'Your passwords', 'Things pip downloaded', 'Old versions of your code'], 0,
  ['Python saves ready-to-run copies there so imports are faster.', 'Nothing secret is kept there.', 'pip keeps its packages elsewhere.', 'Old versions are Git\'s job.'], 6),
]
CARDS = [
 ('pk1', 'talk', 21, 'What is a package?', 'A folder of modules, marked with an `__init__.py` file.'),
 ('pk2', 'talk', 21, 'What does `if __name__ == "__main__":` mean?', 'Run this part only when the file itself is run, not when it is imported.'),
 ('pk3', 'talk', 21, 'What do `pip install` and `requirements.txt` do?', 'pip installs a package; requirements.txt lists what a project needs.'),
 ('pk4', 'bugs', 21, 'Why avoid `from tools import *`?', 'You can no longer tell where each name came from.'),
]
GEN_STEPS = [2, 3, 4]
GEN_JS = r'''
      function () { var a = ri(1, 9), f = ri(1, 8), x = (a + f / 10).toFixed(1), fn = pickOne(['floor', 'ceil']), al = pickOne(['m', 'M', 'mth']);
        var r = fn === 'floor' ? a : a + 1;
        return mk('What does this show?', 'import math as ' + al + '\nprint(' + al + '.' + fn + '(' + x + '))', [[r, al + ' is a nickname for math, and ' + fn + ' rounds ' + (fn === 'floor' ? 'down' : 'up') + ': ' + r + '.'], [fn === 'floor' ? a + 1 : a, fn + ' rounds ' + (fn === 'floor' ? 'down' : 'up') + '.'], [x, fn + ' gives a whole number.'], ['An error', 'import math as ' + al + ' makes ' + al + ' work like math.']]); },
      function () { var name = pickOne(['sqrt', 'pi', 'floor', 'banana', 'hammer', 'ceil']), r = ['sqrt', 'pi', 'floor', 'ceil'].indexOf(name) >= 0;
        return mk('What does this show?', 'import math\nprint("' + name + '" in dir(math))', [[r ? 'True' : 'False', r ? 'dir(math) lists every name in math, and ' + name + ' is one of them.' : 'math has no ' + name + ', so it is not in dir(math).'], [r ? 'False' : 'True', 'Look at what math really contains.'], [name, 'in gives True or False.'], ['An error', 'dir() works on any module.']]); },
      function () { var a = pickOne(['Run', 'Go', 'Main']), b = pickOne(['Imported', 'Library', 'Module']);
        return mk('You run this file. What does it show?', 'if __name__ == "__main__":\n    print("' + a + '")\nelse:\n    print("' + b + '")', [[a, 'When you run the file itself, __name__ is "__main__".'], [b, 'That only shows when another file imports this one.'], [a + ' ' + b, 'Only one branch runs.'], ['__main__', 'The code prints the word in quotes, not __name__.']]); }
'''
