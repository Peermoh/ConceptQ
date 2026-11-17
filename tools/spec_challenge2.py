KEY, IDX = 'challenge2', 45
META = dict(tag='Master Builder · Rooftop garden', title='Master Builder: The smart garden', topic='the Master Builder challenge',
            lastBtn='Let the garden water itself', doneTitle='The garden waters itself!',
            doneText='You beat the last Master Builder challenge: JSON from the antenna, a dataclass for each bed, a generator for the dry ones, async watering, a decorator to time it, logging, type hints and tests, all working together. The garden now waters itself. You finished the whole Python course!')
QUIZ = [
 ('What does this show?', 'def water_needed(f: dict) -> bool:\n    return not f["rain"] and f["temp"] > 20\nprint(water_needed({"rain": False, "temp": 24}))', ['True', 'False', '24', 'An error'], 0,
  ['No rain and warmer than 20: water needed.', 'Both parts are True, so the answer is True.', 'The function returns True or False.', 'The dictionary has both keys.'], 5),
 ('What does this show?', 'import json\nf = json.loads(\'{"rain": false, "temp": 24}\')\nprint(f["rain"])', ['False', 'false', '"false"', 'None'], 0,
  ['JSON false becomes Python False.', 'That is how JSON writes it, not Python.', 'It is a real bool, not a string.', 'false becomes False, not None.'], 0),
 ('What does this show?', 'from dataclasses import dataclass\n@dataclass\nclass Bed:\n    name: str\n    dry: bool\nbeds = [Bed("peas", True), Bed("kale", False), Bed("leek", True)]\nprint(sum(1 for b in beds if b.dry))', ['2', '3', '1', 'True'], 0,
  ['peas and leek are dry.', 'kale is not dry.', 'Two beds are dry.', 'sum counts them: a number.'], 2),
 ('Three dry beds, each watered with await asyncio.sleep(2), all gathered. About how long?', 'await asyncio.gather(*(water(b) for b in dry))', ['About 2 seconds', 'About 6 seconds', 'About 3 seconds', 'It never ends'], 0,
  ['gather lets them all wait together.', 'That would be one after another.', 'Each wait is 2 seconds.', 'gather finishes when all of them do.'], 3),
 ('What is @timed above async def water?', '@timed\nasync def water(bed): ...', ['A decorator that wraps water', 'A comment', 'A type hint', 'A test'], 0,
  ['The @ line wraps water in another function.', 'Comments start with #.', 'Hints use a colon and ->.', 'Tests use assert.'], 4),
 ('What happens?', 'def water_needed(f):\n    return not f["rain"] and f["temp"] > 20\nassert not water_needed({"rain": True, "temp": 30})\nprint("pass")', ['pass', 'An AssertionError', 'True', 'False'], 0,
  ['It is raining, so no water is needed; not False is True, so the test passes.', 'water_needed gives False on a rainy day.', 'Only pass is printed.', 'assert prints nothing itself.'], 6),
]
CARDS = [
 ('sg1', 'world', 45, 'Smart garden: which tool reads the forecast?', '`json.loads(text)` turns the API answer into a dict.'),
 ('sg2', 'mach', 45, 'Smart garden: how do you water every dry bed at once?', '`await asyncio.gather(*(water(b) for b in dry))`'),
]
GEN_STEPS = [5, 2]
GEN_JS = r'''
      function () { var rain = pickOne([true, false]), t = pickOne([15, 18, 20, 21, 25, 30]), need = !rain && t > 20;
        return mk('What does this show?', 'def water_needed(f: dict) -> bool:\n    return not f["rain"] and f["temp"] > 20\nprint(water_needed({"rain": ' + (rain ? 'True' : 'False') + ', "temp": ' + t + '}))', [[need ? 'True' : 'False', rain ? 'It is raining, so no water is needed.' : t > 20 ? 'No rain and warmer than 20: water needed.' : t + ' is not more than 20, so no water is needed.'], [need ? 'False' : 'True', 'Both parts must be true: no rain, and warmer than 20.'], [String(t), 'The function gives True or False.'], ['An error', 'The dictionary has both keys.']]); },
      function () { var names = shuffled(['peas', 'kale', 'leek', 'bean', 'corn']).slice(0, ri(3, 5)), dry = names.map(function () { return pickOne([true, false]); }); if (dry.every(function (d) { return d; })) dry[0] = false; if (dry.every(function (d) { return !d; })) dry[1] = true;
        var n = dry.filter(function (d) { return d; }).length;
        return mk('What does this show?', 'from dataclasses import dataclass\n@dataclass\nclass Bed:\n    name: str\n    dry: bool\nbeds = [' + names.map(function (nm, i) { return 'Bed("' + nm + '", ' + (dry[i] ? 'True' : 'False') + ')'; }).join(', ') + ']\nprint(sum(1 for b in beds if b.dry))', [[String(n), 'Count the beds where dry is True.'], [String(names.length), 'Not every bed is dry.'], [String(names.length - n), 'That counts the beds that are not dry.'], ['True', 'sum counts them: the answer is a number.']]); }
'''
