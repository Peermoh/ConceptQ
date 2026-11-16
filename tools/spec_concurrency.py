KEY, IDX = 'concurrency', 41
META = dict(tag='Concurrency · Rooftop garden', title='Concurrency: many jobs at once', topic='concurrency',
            lastBtn='Start the sprinklers', doneTitle='The sprinklers are in!',
            doneText='You learned why waiting is wasted, threads, processes for heavy maths, async and await, gather, locks, and which to choose. Sprinklers now water every bed on the roof terrace. The sprinkler hub is in your garden: run them one by one, then all at once.')
QUIZ = [
 ('Each bed takes 2 seconds. How long one after another?', 'water("peas")\nwater("kale")\nwater("leeks")', ['About 6 seconds', 'About 2 seconds', 'About 3 seconds', 'About 1 second'], 0,
  ['3 beds × 2 seconds, one after another, is 6.', 'That is how long with gather, all at once.', 'Each one takes 2 seconds, not 1.', 'Each one takes 2 seconds.'], 0),
 ('About how long does this take?', 'async def water(bed):\n    await asyncio.sleep(2)\nasync def main():\n    await asyncio.gather(water("peas"), water("kale"))\nasyncio.run(main())', ['About 2 seconds', 'About 4 seconds', 'About 1 second', 'It never finishes'], 0,
  ['gather lets both wait at the same time.', 'That would be one after another.', 'Each wait is still 2 seconds.', 'gather waits for both, then finishes.'], 5),
 ('What does t.join() do?', 't = threading.Thread(target=water)\nt.start()\nt.join()', ['Waits until the thread has finished', 'Starts the thread', 'Joins two threads into one', 'Stops the thread at once'], 0,
  ['join waits for it to finish.', 'start() starts it.', 'Threads are not merged.', 'join waits; it does not stop it.'], 2),
 ('Counting seeds in 1000 trays is heavy maths. Which fits best?', '# lots of number crunching', ['Processes (multiprocessing)', 'async and await', 'One thread', 'time.sleep()'], 0,
  ['Processes really run on several cores at once.', 'async is for waiting, not for maths.', 'One thread does it all alone.', 'Sleeping does no work.'], 3),
 ('What does await do?', 'await asyncio.sleep(2)', ['Pauses this job and lets others run while it waits', 'Stops the whole program for 2 seconds', 'Makes a new thread', 'Skips the wait'], 0,
  ['While one job waits, the others carry on.', 'Only this job pauses.', 'async runs in one thread.', 'It still waits 2 seconds.'], 4),
 ('Why use a Lock?', 'with lock:\n    tank -= 5', ['So only one thread changes the tank at a time', 'To make it faster', 'To lock the file', 'To stop all threads'], 0,
  ['Two threads changing it at once could lose an update.', 'A lock is about safety, not speed.', 'It is about the shared value.', 'Other threads just wait their turn.'], 6),
 ('Your program waits for a weather website. Which fits best?', 'requests.get(url)', ['async or threads', 'Processes', 'Nothing: it cannot be helped', 'A bigger computer'], 0,
  ['Waiting for the internet is just what async and threads are for.', 'Processes are for heavy maths.', 'You can do other jobs while waiting.', 'Waiting is not about computer power.'], 7),
]
CARDS = [
 ('cc1', 'world', 41, 'What is concurrency for?', 'Doing other jobs while you wait, instead of waiting one by one.'),
 ('cc2', 'world', 41, 'How do you run several async jobs at once?', '`await asyncio.gather(job1(), job2())`'),
 ('cc3', 'world', 41, 'Threads, processes or async for heavy maths?', 'Processes (`multiprocessing.Pool`): they really use several cores.'),
 ('cc4', 'world', 41, 'Why use `threading.Lock()`?', 'So only one thread changes shared data at a time.'),
]
GEN_STEPS = [5, 2]
GEN_JS = r'''
      function () { var names = shuffled(['peas', 'kale', 'leek']), ts = shuffled([1, 3, 5]), order = names.slice().sort(function (a, b) { return ts[names.indexOf(a)] - ts[names.indexOf(b)]; });
        var given = names.join(' '), right = order.join(' '), wrong = given === right ? names.slice().reverse().join(' ') : given, wrong2 = order.slice().reverse().join(' '); if (wrong2 === wrong) wrong2 = order[0];
        return mk('What does this show?', 'import asyncio\nasync def water(bed, t):\n    await asyncio.sleep(t / 100)\n    print(bed)\nasync def main():\n    await asyncio.gather(' + names.map(function (n, i) { return 'water("' + n + '", ' + ts[i] + ')'; }).join(', ') + ')\nasyncio.run(main())', [[right, 'They all wait together, so the shortest wait finishes first.'], [wrong, 'gather starts them in this order, but they finish when their own wait ends.'], [wrong2, 'The shortest wait finishes first, not last.'], ['An error', 'This is fine async code.']]); },
      function () { var n = ri(2, 4), k = ri(2, 5), out = []; for (var j = 0; j < n; j++) out.push(j * k);
        return mk('What does this show?', 'import threading\nout = []\ndef job(i):\n    out.append(i * ' + k + ')\nts = [threading.Thread(target=job, args=(i,)) for i in range(' + n + ')]\nfor t in ts:\n    t.start()\nfor t in ts:\n    t.join()\nprint(sorted(out))', [['[' + out.join(', ') + ']', 'Each of the ' + n + ' threads adds i × ' + k + '; join waits for all of them.'], ['[]', 'join waits for every thread, so the list is full.'], ['[' + out.slice(1).join(', ') + ']', 'range(' + n + ') starts at 0.'], ['[' + out.map(function (x, i) { return i + k; }).join(', ') + ']', 'The job multiplies by ' + k + ', it does not add.']]); }
'''
