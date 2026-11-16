KEY, IDX = 'challenge', 34
META = dict(tag='Master Builder · Third floor', title='Master Builder: The smart roof', topic='the Master Builder challenge',
            lastBtn='Light up the roof', doneTitle='The smart roof is on!',
            doneText='You beat the Master Builder challenge: a file of readings, a class for each sensor, comprehensions, lambda, tests and a function for the lights, all working together. The weather station is up and the roof lights shine at night. Your house is finished!')
QUIZ = [
 ('What does lines hold?', 'text = "kitchen,21\\nloft,14"\nlines = text.splitlines()', ["['kitchen,21', 'loft,14']", "['kitchen', '21', 'loft', '14']", "'kitchen,21'", '2'], 0,
  ['splitlines gives one string per line.', 'That would need a split on commas too.', 'That is only the first line.', 'len(lines) would be 2.'], 0),
 ('What does this show?', 'class Sensor:\n    def __init__(self, room, temp):\n        self.room = room\n        self.temp = int(temp)\ns = Sensor("loft", "14")\nprint(s.temp + 1)', ['15', '141', '"14"1', 'An error'], 0,
  ['int("14") makes temp the number 14, so 14 + 1 is 15.', 'That would happen with strings, but temp is an int.', 'temp was turned into a number.', 'The code runs fine.'], 1),
 ('What does this show?', 'temps = {"kitchen": 21, "loft": 14, "hall": 17}\nprint([r for r in temps if temps[r] < 18])', ["['loft', 'hall']", "['loft']", "['kitchen']", '[14, 17]'], 0,
  ['loft (14) and hall (17) are both below 18.', '17 is below 18 too.', '21 is not below 18.', 'The comprehension keeps r, the room names.'], 3),
 ('What does this show?', 'temps = [21, 14, 17]\nprint(sorted(temps, key=lambda t: -t))', ['[21, 17, 14]', '[14, 17, 21]', '[21, 14, 17]', 'An error'], 0,
  ['The key -t puts the biggest first.', 'That is the order without the minus.', 'sorted does change the order.', 'lambda works fine as a key.'], 4),
 ('What happens?', 'def roof_lights(hour):\n    return hour >= 19 or hour < 6\nassert roof_lights(12) == False\nprint("ok")', ['ok', 'An AssertionError', 'True', 'False'], 0,
  ['At 12 it is daytime: the lights are off, so the test passes.', 'roof_lights(12) really is False.', 'assert prints nothing itself.', 'Only "ok" is printed.'], 5),
 ('What does this show?', 'def roof_lights(hour):\n    return hour >= 19 or hour < 6\nprint(roof_lights(3))', ['True', 'False', '3', 'None'], 0,
  ['3 is less than 6: still night, so the lights are on.', '3 < 6 is True.', 'The function returns True or False.', 'It always returns a value.'], 6),
]
CARDS = [
 ('ch1', 'blue', 34, 'How do you build many objects from a list of lines?', 'A comprehension: `[Sensor(*l.split(",")) for l in lines]`.'),
 ('ch2', 'coll', 34, 'How do you sort sensors coldest first?', '`sensors.sort(key=lambda s: s.temp)`'),
]
GEN_STEPS = [6, 3, 4]
GEN_JS = r'''
      function () { var h = pickOne([2, 5, 6, 8, 12, 18, 19, 21, 23]), on = h >= 19 || h < 6;
        return mk('What does this show?', 'def roof_lights(hour):\n    return hour >= 19 or hour < 6\nprint(roof_lights(' + h + '))', [[on ? 'True' : 'False', on ? h + ' is night time, so the lights are on.' : h + ' is daytime, so the lights stay off.'], [on ? 'False' : 'True', 'Check both: is ' + h + ' >= 19, or is ' + h + ' < 6?'], [String(h), 'The function returns True or False.'], ['None', 'It always returns a value.']]); },
      function () { var rooms = shuffled(['kitchen', 'loft', 'hall', 'den']).slice(0, 3), t = rooms.map(function () { return ri(12, 24); }), lim = 18;
        if (t.every(function (x) { return x >= lim; })) t[1] = ri(12, 16); if (t.every(function (x) { return x < lim; })) t[0] = ri(19, 24); for (var k = 0; k < 3; k++) if (t[k] === lim) t[k] = 17;
        var cold = rooms.filter(function (r, i) { return t[i] < lim; }), warm = rooms.filter(function (r, i) { return t[i] >= lim; });
        var code = 'temps = {' + rooms.map(function (r, i) { return '"' + r + '": ' + t[i]; }).join(', ') + '}\nprint([r for r in temps if temps[r] < ' + lim + '])';
        return mk('What does this show?', code, [[pyList(cold), 'Keep each room whose temperature is below ' + lim + '.'], [pyList(warm), 'Those are the warm rooms: < keeps the cold ones.'], [pyList(rooms), 'The if leaves some rooms out.'], ['[' + t.filter(function (x) { return x < lim; }).join(', ') + ']', 'The comprehension keeps r, the room names, not the numbers.']]); },
      function () { var t = shuffled([ri(10, 13), ri(14, 17), ri(18, 21), ri(22, 25)]).slice(0, 3), up = pickOne([true, false]);
        var asc = t.slice().sort(function (a, b) { return a - b; }), desc = asc.slice().reverse();
        return mk('What does this show?', 'temps = [' + t.join(', ') + ']\nprint(sorted(temps, key=lambda t: ' + (up ? 't' : '-t') + '))', [['[' + (up ? asc : desc).join(', ') + ']', up ? 'key t sorts smallest first.' : 'The key -t puts the biggest first.'], ['[' + (up ? desc : asc).join(', ') + ']', up ? 'There is no minus, so it is smallest first.' : 'The minus flips the order: biggest first.'], ['[' + t.join(', ') + ']', 'sorted does change the order.'], ['An error', 'lambda works fine as a key.']]); }
'''
