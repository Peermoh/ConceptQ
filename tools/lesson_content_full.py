# Full ground-floor coverage: the original steps plus the missing concepts, inserted where they belong.
import json, copy
from lesson_content import L as BASE
L = copy.deepcopy(BASE)
_v = json.load(open("lessons.json"))['vars']
L['vars'] = dict(labels=_v['labels'], steps=[tuple(x) for x in _v['steps']])
def add(key, at, label, lines, say, cue):
    assert len(lines) == len(cue), (key, label)
    pos = -1
    for c in cue:
        p = say.index(c); assert p > pos, (key, label, c); pos = p
    L[key]['steps'].insert(at, (lines, say, cue)); L[key]['labels'].insert(at, label)
def relabel(key):
    L[key]['labels'] = ['%d. %s' % (i + 1, l.split('. ', 1)[1]) for i, l in enumerate(L[key]['labels'])]

add('hello', 5, '6. # notes', [['title','Notes with #'],['code','# say hello to Mia'],['code','print("Hi Mia")'],['out','→ Hi Mia'],['chalk','Python skips # notes']],
 "A hash sign starts a note for humans. hash, say hello to Mia. Then print Hi Mia. Python shows only: Hi Mia. It skips every note.",
 ['A hash sign','hash, say hello','Then print Hi Mia','Python shows only','It skips every note'])
add('hello', 6, '7. Lines', [['title','Quotes and new lines'],['code',"print('Hi')"],['out','→ Hi'],['code','print("Hi\\nBye")'],['out','→ Hi, then Bye below']],
 "Single quotes work too. print, single quote Hi, shows Hi. A backslash n inside text starts a new line. print Hi backslash n Bye shows Hi, then Bye on the line below.",
 ['Single quotes work','print, single quote Hi','shows Hi.','A backslash n','shows Hi, then Bye'])

add('vars', 6, '7. +=', [['title','Add to a box'],['code','score = 10'],['code','score += 5'],['out','→ score is 15'],['chalk','same as score = score + 5']],
 "To add to a box, there is a shortcut. score equals ten. score plus equals five. Now score is fifteen. It is the same as score equals score plus five.",
 ['To add to a box','score equals ten','score plus equals five','Now score is fifteen','It is the same'])
add('vars', 7, '8. type()', [['title','What kind is it?'],['code','type(9)'],['out',"→ <class 'int'>"],['code','type("9")'],['out',"→ <class 'str'>"]],
 "type tells you what kind of value is in a box. type of nine says int, a whole number. type of quote nine says str, a string of text.",
 ['type tells you','type of nine','says int','type of quote nine','says str'])

add('nums', 1, '2. Minus', [['title','Take away'],['code','print(10 - 4)'],['out','→ 6'],['code','print(3 - 5)'],['out','→ -2']],
 "The minus sign takes away. print ten minus four gives six. Go below zero and you get a negative: print three minus five gives minus two.",
 ['The minus sign','print ten minus four','gives six','Go below zero','gives minus two'])
add('nums', 6, '7. round()', [['title','Decimals'],['code','6 / 2'],['out','→ 3.0'],['code','round(3.7)'],['out','→ 4'],['code','round(3.14159, 2)'],['out','→ 3.14']],
 "Numbers with a decimal point are called floats. six slash two gives three point zero, a float. round makes it neat: round three point seven gives four. round three point one four one five nine, comma two, keeps two decimals: three point one four.",
 ['Numbers with a decimal','six slash two','gives three point zero','round makes it neat','gives four','round three point one four one five nine','keeps two decimals'])

add('strings', 4, '5. Slices', [['title','From the end, and slices'],['code','word = "python"'],['code','word[-1]'],['out','→ "n"'],['code','word[0:2]'],['out','→ "py"'],['chalk','stops before 2']],
 "Minus one counts from the end. word equals python. word, square bracket minus one, gives n, the last letter. A colon cuts a slice: word, square bracket zero colon two, gives p y. It stops before two.",
 ['Minus one counts','word equals python','word, square bracket minus one','gives n','A colon cuts','gives p y','It stops before two'])
add('strings', 6, '7. * and in', [['title','Repeat and find'],['code','"ha" * 3'],['out','→ "hahaha"'],['code','"a" in "cat"'],['out','→ True']],
 "A star repeats text. quote ha, times three, gives ha ha ha. The word in checks if text is inside: quote a in quote cat is True.",
 ['A star repeats','quote ha, times three','gives ha ha ha','The word in checks','is True'])
add('strings', 7, '8. str()', [['title','Numbers into text'],['code','"Age " + 9'],['note','TypeError!'],['code','"Age " + str(9)'],['out','→ "Age 9"']],
 "You can't glue text and a number. quote Age plus nine is a TypeError. Turn the number into text first with str: quote Age plus str of nine gives Age nine.",
 ["You can't glue",'quote Age plus nine','is a TypeError','Turn the number','gives Age nine'])

add('input', 4, '5. Two', [['title','Ask twice'],['code','a = int(input("First? "))'],['code','b = int(input("Second? "))'],['code','print(a + b)'],['chalk','you type: 2 and 3'],['out','→ 5']],
 "You can ask more than once. a equals int, of input, First? b equals int, of input, Second? Then print a plus b. If you type two and three, it shows five.",
 ['You can ask','a equals int','b equals int','Then print a plus b','If you type two and three','it shows five'])
add('input', 5, '6. Oops', [['title','Not a number?'],['code','age = int(input("Age? "))'],['chalk','you type: nine'],['note','ValueError!'],['chalk','type the digit: 9']],
 "What if the answer is not a number? age equals int, of input, Age? If you type the word nine in letters, int can't turn it into a number. That is a ValueError. Type the digit nine instead.",
 ['What if the answer','age equals int','If you type the word nine','That is a ValueError','Type the digit nine'])

add('bool', 3, '4. Text', [['title','Compare text'],['code','"cat" == "cat"'],['out','→ True'],['code','"Cat" == "cat"'],['out','→ False'],['note','capitals count!']],
 "You can compare text too. quote cat equals equals quote cat is True. But capital Cat equals equals small cat is False. Capitals count!",
 ['You can compare text','quote cat equals equals','is True','But capital Cat','is False','Capitals count'])

add('if', 5, '6. or', [['title','Either one'],['code','if day == "Sat" or day == "Sun":'],['code','    print("Weekend!")'],['chalk','one True is enough']],
 "or runs when either check is True. if day equals equals Sat, or day equals equals Sun: print Weekend. One True is enough.",
 ['or runs when','if day equals equals Sat','print Weekend','One True is enough'])
add('if', 6, '7. Inside', [['title','if inside if'],['code','if hungry:'],['code','    if has_food:'],['code','        print("Eat!")'],['chalk','runs only if both are True']],
 "You can put an if inside another if. if hungry, colon. Indented: if has food, colon. Indented again: print Eat. It runs only if both are True.",
 ['You can put an if','if hungry, colon','Indented: if has food','Indented again','It runs only'])

add('loop', 4, '5. Total', [['title','Keep a total'],['code','total = 0'],['code','for n in range(1, 4):'],['code','    total += n'],['out','→ total is 6']],
 "A loop can add things up. total equals zero. for n in range one comma four: total plus equals n. One plus two plus three, so total is six.",
 ['A loop can add','total equals zero','for n in range one comma four','total plus equals n','so total is six'])
add('loop', 7, '8. continue', [['title','continue skips'],['code','for n in range(4):'],['code','    if n == 2:'],['code','        continue'],['code','    print(n)'],['out','→ 0 1 3']],
 "continue skips the rest of this turn and moves on. for n in range four: if n equals equals two: continue. Then print n. It shows zero, one, three. Two was skipped.",
 ['continue skips','for n in range four','if n equals equals two','two: continue','Then print n','It shows zero'])
add('loop', 8, '9. Forever', [['title','Careful: forever!'],['code','while True:'],['code','    print("Again")'],['note','never stops!'],['chalk','add a break to get out']],
 "Careful! while True, colon, never stops on its own. It will print Again, again and again, forever. Always add a break to get out.",
 ['Careful!','while True','print Again','forever','Always add a break'])
for k in L: relabel(k)
if __name__ == '__main__':
    for k, v in L.items(): print(k, len(v['steps']), v['labels'])
