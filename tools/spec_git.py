KEY, IDX = 'git', 32
META = dict(tag='Team coding · Third floor', title='Team coding: building together', topic='team coding with git',
            lastBtn='Fit the solar panels', doneTitle='Solar panels on!',
            doneText='You learned repositories, git status, add and commit, the log, branches, merging, merge conflicts and code review. The team fitted the solar panels, one commit per panel. The shared blueprint table is in the house: scroll its history and try a branch.')
QUIZ = [
 ('What does a commit do?', 'git commit -m "Add panel 2"', ['Saves one change in the history, with a message', 'Deletes the file', 'Sends the code to a teammate', 'Runs the tests'], 0,
  ['A commit is one saved step with a message saying what changed.', 'Commits keep things; they never delete your work.', 'That is push; commit only saves locally.', 'git does not run your tests.'], 3),
 ('Which command shows what changed but is not saved yet?', '# roof.py was edited', ['git status', 'git log', 'git init', 'git merge'], 0,
  ['git status lists the changed files.', 'git log shows the commits already saved.', 'git init starts a new repository.', 'git merge joins a branch in.'], 2),
 ('git log --oneline shows the newest commit…', 'git log --oneline', ['First', 'Last', 'In a random place', 'Only if you ask twice'], 0,
  ['The log starts from the newest commit.', 'The oldest commit is at the bottom.', 'The order is always newest first.', 'One command is enough.'], 4),
 ('Why make a branch?', 'git switch -c test-panel', ['To try something without changing main', 'To delete main', 'To make the code run faster', 'To rename the project'], 0,
  ['A branch is your own copy of the history, so main stays safe.', 'Branches never delete main.', 'Branches do not change speed.', 'The project name stays the same.'], 5),
 ('The test panel works. How does it join main?', 'git switch main', ['git merge test-panel', 'git init test-panel', 'git status test-panel', 'git log test-panel'], 0,
  ['From main, git merge brings the branch\'s commits in.', 'init starts a new repository.', 'status only shows changes.', 'log only shows history.'], 6),
 ('What is a merge conflict?', '<<<<<<< main\ncolour = "blue"\n=======\ncolour = "green"\n>>>>>>> test-panel', ['Two changes to the same line, so you must choose', 'A broken computer', 'A test that failed', 'A typo in a commit message'], 0,
  ['git cannot pick between blue and green, so you decide.', 'Nothing is broken; git just needs your choice.', 'Tests are a different thing.', 'Messages cannot cause conflicts.'], 7),
 ('Why do teams use code review?', '# open a pull request', ['A teammate reads the code before it is merged', 'To make the code longer', 'So nobody has to test', 'To hide the code'], 0,
  ['Two pairs of eyes catch more bugs.', 'Review is about quality, not length.', 'You still test as well.', 'Review means sharing, not hiding.'], 8),
]
CARDS = [
 ('gt1', 'team', 32, 'What is a commit?', 'One saved change in the history, with a message: `git commit -m "Add panel 1"`.'),
 ('gt2', 'team', 32, 'What does `git status` show?', 'Which files changed and are not committed yet.'),
 ('gt3', 'team', 32, 'Why use a branch?', 'To try something on your own copy; `main` stays safe until you merge.'),
 ('gt4', 'team', 32, 'What is a merge conflict?', 'Two changes to the same line. You choose, delete the `<<<<` `====` `>>>>` lines, and commit.'),
]
GEN_STEPS = [4, 6]
GEN_JS = r'''
      function () { var p = shuffled(['north', 'south', 'east', 'west', 'tilt', 'wires']).slice(0, 3);
        return mk('Which commit does git log --oneline show first?', 'git commit -m "Add ' + p[0] + ' panel"\ngit commit -m "Add ' + p[1] + ' panel"\ngit commit -m "Add ' + p[2] + ' panel"\ngit log --oneline', [['Add ' + p[2] + ' panel', 'The log shows the newest commit first.'], ['Add ' + p[0] + ' panel', 'That is the oldest: it is at the bottom.'], ['Add ' + p[1] + ' panel', 'That one is in the middle.'], ['Nothing until you push', 'log shows your saved commits straight away.']]); },
      function () { var b = pickOne(['test-panel', 'blue-roof', 'big-window', 'new-door']);
        return mk('You are on ' + b + ' and it works. What comes next?', 'git switch -c ' + b + '\n# ... commits ...', [['git switch main, then git merge ' + b, 'Go back to main, then merge the branch in.'], ['git merge main', 'That pulls main into your branch, not the other way.'], ['git init ' + b, 'init starts a brand new repository.'], ['git status ' + b, 'status only shows what changed.']]); }
'''
