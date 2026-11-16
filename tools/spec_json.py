KEY, IDX = 'json', 42
META = dict(tag='JSON and APIs · Rooftop garden', title='JSON and APIs: talk to the outside world', topic='JSON and APIs',
            lastBtn='Raise the antenna', doneTitle='The antenna is up!',
            doneText='You learned JSON, json.loads and dumps, JSON files, what an API is, requests.get, status codes, timeouts and keeping keys safe. An antenna now stands on the roof terrace. It is in your garden: ask the pretend weather service for tomorrow.')
QUIZ = [
 ('What does this show?', 'import json\nd = json.loads(\'{"temp": 18, "rain": true}\')\nprint(d["temp"])', ['18', '"18"', 'temp', 'An error'], 0,
  ['loads turns the text into a dict; d["temp"] is the number 18.', 'JSON numbers become Python numbers.', 'You asked for the value, not the key.', 'The JSON is valid.'], 1),
 ('What does this show?', 'import json\nprint(json.dumps({"rain": True}))', ['{"rain": true}', "{'rain': True}", '{"rain": True}', 'rain: true'], 0,
  ['JSON writes true in lower case, with double quotes.', 'That is how Python prints a dict, not JSON.', 'JSON uses lower-case true.', 'JSON keeps the braces and quotes.'], 2),
 ('What is the difference between json.dump and json.dumps?', 'json.dump(d, f)\njson.dumps(d)', ['dump writes to a file; dumps gives back text', 'They are the same', 'dumps writes to a file', 'dump deletes the data'], 0,
  ['The s means string.', 'One works with files, one with text.', 'It is the other way round.', 'Nothing is deleted.'], 3),
 ('What is an API?', 'https://weather.example/today', ['A web address that answers with data', 'A kind of web page for people', 'A Python module', 'A password'], 0,
  ['It answers programs with data, often JSON.', 'It is for programs, not for reading.', 'It is on the internet, not in Python.', 'Some APIs need a key, but the API is the address.'], 4),
 ('What does status code 404 mean?', 'r = requests.get(url)\nprint(r.status_code)', ['Not found', 'It worked', 'The server broke', 'Too fast'], 0,
  ['404: there is nothing at that address.', 'That is 200.', 'That is 500.', 'That is not 404.'], 6),
 ('Why add timeout=5?', 'requests.get(url, timeout=5)', ['So you never wait forever for an answer', 'To make the answer arrive in 5 seconds', 'To try 5 times', 'To get 5 answers'], 0,
  ['If the server does not answer, you stop after 5 seconds.', 'It is a limit, not a promise.', 'It does not retry.', 'You still get one answer.'], 7),
 ('Where should a secret API key go?', 'key = ...', ['In an environment variable, not in the code', 'Straight in the code', 'In a comment', 'In the JSON you send everyone'], 0,
  ['os.environ keeps it out of the code you share.', 'Code gets shared and copied.', 'Comments are part of the code.', 'Never send keys around.'], 7),
]
CARDS = [
 ('js1', 'world', 42, 'How do you turn JSON text into Python?', '`json.loads(text)` (and `json.load(f)` for a file).'),
 ('js2', 'world', 42, 'How do you turn Python into JSON text?', '`json.dumps(d)` (and `json.dump(d, f)` for a file).'),
 ('js3', 'world', 42, 'What does status code 200 mean? 404? 500?', '200 it worked · 404 not found · 500 the server broke.'),
 ('js4', 'world', 42, 'Two rules for using a web API safely?', 'Always set a timeout; keep keys out of your code (use environment variables).'),
]
GEN_STEPS = [1, 2, 1]
GEN_JS = r'''
      function () { var a = ri(10, 25), b = ri(1, 9), c = ri(1, 9); if (b === c) c = b + 1; var k = ri(0, 1);
        return mk('What does this show?', 'import json\nd = json.loads(\'{"temp": ' + a + ', "beds": [' + b + ', ' + c + ']}\')\nprint(d["beds"][' + k + '])', [[String(k ? c : b), 'd["beds"] is a list, and [' + k + '] picks ' + (k ? 'the second' : 'the first') + ' item.'], [String(k ? b : c), 'Lists count from 0.'], [String(a), 'That is d["temp"].'], ['[' + b + ', ' + c + ']', '[' + k + '] picks one item from the list.']]); },
      function () { var v = pickOne([['True', 'true'], ['False', 'false'], ['None', 'null']]), w = pickOne([['True', 'true'], ['None', 'null']]), n = ri(1, 9);
        return mk('What does this show?', 'import json\nprint(json.dumps({"rain": ' + v[0] + ', "temp": ' + n + ', "wind": ' + w[0] + '}))', [['{"rain": ' + v[1] + ', "temp": ' + n + ', "wind": ' + w[1] + '}', 'JSON writes ' + v[0] + ' as ' + v[1] + ' and ' + w[0] + ' as ' + w[1] + '.'], ['{"rain": ' + v[0] + ', "temp": ' + n + ', "wind": ' + w[0] + '}', 'JSON uses its own words: true, false and null.'], ["{'rain': " + v[0] + ", 'temp': " + n + ", 'wind': " + w[0] + '}', 'That is how Python prints a dict, not JSON.'], ['{"rain": "' + v[1] + '", "temp": ' + n + ', "wind": "' + w[1] + '"}', 'true, false and null have no quotes in JSON.']]); },
      function () { var isList = pickOne([true, false]), text = isList ? '[1, 2, 3]' : '{"a": 1}';
        return mk('What does this show?', 'import json\nprint(type(json.loads(\'' + text + '\')).__name__)', [[isList ? 'list' : 'dict', isList ? 'A JSON array becomes a Python list.' : 'A JSON object becomes a Python dict.'], [isList ? 'dict' : 'list', isList ? 'Square brackets mean a list.' : 'Curly braces mean a dict.'], ['str', 'loads turns the text into Python objects.'], ['json', 'The result is ordinary Python, not a special type.']]); }
'''
