# Floor 2 (Intermediate) lessons, added on top of the full ground floor.
from lesson_content_full import L, add  # noqa: F401  (add() checks every cue against the narration)
def lesson(key, steps):
    L[key] = dict(labels=[], steps=[])
    for i, (label, lines, say, cue) in enumerate(steps):
        add(key, i, '%d. %s' % (i + 1, label), lines, say, cue)

lesson('lists1', [
 ('List', [['title','A row of things'],['code','beams = ["oak", "pine", "ash"]'],['chalk','a list keeps things in order'],['code','print(beams)'],['out',"→ ['oak', 'pine', 'ash']"]],
  "A list keeps many things in one row, like beams laid across a floor. beams equals, square bracket, oak, pine, ash. A list keeps them in order. print beams shows all three, inside square brackets.",
  ['A list keeps many','beams equals','A list keeps them in order','print beams','inside square brackets']),
 ('[0] [-1]', [['title','First and last'],['chalk','positions start at 0, like letters'],['code','beams[0]'],['out','→ "oak"'],['code','beams[-1]'],['out','→ "ash"']],
  "Each item has a position, starting at zero, just like letters in a string. beams, square bracket zero, gives oak. beams, square bracket minus one, gives the last one: ash.",
  ['Each item has a position','just like letters','beams, square bracket zero','gives oak','beams, square bracket minus one','the last one: ash']),
 ('len, in', [['title','Count and check'],['code','len(beams)'],['out','→ 3'],['code','"oak" in beams'],['out','→ True']],
  "len counts the items: len of beams is three. The word in checks if something is there: quote oak in beams is True.",
  ['len counts','len of beams','is three','The word in','is True']),
 ('Change', [['title','Change one item'],['code','beams[1] = "elm"'],['code','print(beams)'],['out',"→ ['oak', 'elm', 'ash']"],['note','the pine is gone']],
  "Lists can change, unlike strings. beams, square bracket one, equals elm. Now print beams shows oak, elm, ash. The pine was swapped out.",
  ['Lists can change','beams, square bracket one','Now print beams','shows oak, elm, ash','The pine was swapped']),
 ('Add', [['title','Add items'],['code','beams.append("fir")'],['out',"→ ['oak', 'elm', 'ash', 'fir']"],['code','beams.insert(0, "yew")'],['out','→ yew goes first']],
  "append adds to the end. beams dot append fir puts fir after ash. insert puts an item at a position: beams dot insert, zero, yew, puts yew first.",
  ['append adds','beams dot append fir','puts fir after ash','insert puts','puts yew first']),
 ('Remove', [['title','Take items out'],['code','beams.remove("ash")'],['chalk','removes by name'],['code','beams.pop()'],['chalk','takes the last one'],['code','del beams[0]'],['chalk','removes by position']],
  "There are three ways to take items out. beams dot remove ash removes it by name. beams dot pop takes the last one off the end. And del beams, square bracket zero, removes by position.",
  ['There are three ways','beams dot remove ash','removes it by name','beams dot pop','takes the last one','And del beams','removes by position']),
 ('Slices', [['title','Slices'],['code','beams = ["oak", "pine", "ash", "fir"]'],['code','beams[1:3]'],['out',"→ ['pine', 'ash']"],['chalk','stops before 3']],
  "A slice takes part of a list. beams equals oak, pine, ash, fir. beams, square bracket one colon three, gives pine and ash. It stops before three, like string slices.",
  ['A slice takes','beams equals oak','beams, square bracket one colon three','gives pine and ash','It stops before three']),
 ('Mixed', [['title','Anything, or nothing'],['code','mix = [3, "hi", True]'],['chalk','any kind of value'],['code','empty = []'],['out','→ len(empty) is 0']],
  "A list can hold any kind of value. mix equals three, quote hi, and True. Numbers, text and True or False, all together. An empty list is just two square brackets: empty equals square brackets. Its len is zero.",
  ['A list can hold','mix equals three','Numbers, text','An empty list','Its len is zero']),
])
lesson('lists2', [
 ('for', [['title','for walks the list'],['code','pets = ["cat", "dog", "fish"]'],['code','for p in pets:'],['code','    print(p)'],['out','→ cat  dog  fish']],
  "A for loop walks through a list, one item at a time. pets equals cat, dog, fish. for p in pets, colon. Indented: print p. It shows cat, then dog, then fish.",
  ['A for loop walks','pets equals cat','for p in pets','Indented: print p','It shows cat']),
 ('Positions', [['title','With positions'],['code','for i in range(len(pets)):'],['code','    print(i, pets[i])'],['out','→ 0 cat  1 dog  2 fish']],
  "Need the position too? for i in range of len of pets. Then print i and pets, square bracket i. It shows zero cat, one dog, two fish.",
  ['Need the position','for i in range of len','Then print i','It shows zero cat']),
 ('sum, max', [['title','Add up, smallest, biggest'],['code','scores = [7, 3, 9]'],['code','sum(scores)'],['out','→ 19'],['code','min(scores)   max(scores)'],['out','→ 3   9']],
  "Python has helpers for lists of numbers. scores equals seven, three, nine. sum of scores adds them up: nineteen. min gives the smallest and max gives the biggest: three and nine.",
  ['Python has helpers','scores equals seven','sum of scores','nineteen','min gives the smallest','three and nine']),
 ('Sort', [['title','Sorting'],['code','scores.sort()'],['out','→ [3, 7, 9]'],['code','sorted(scores, reverse=True)'],['out','→ [9, 7, 3]'],['note','sort() changes the list itself']],
  "scores dot sort puts the list in order: three, seven, nine. sorted gives you a new sorted list, and reverse equals True puts the biggest first: nine, seven, three. Remember: sort changes the list itself.",
  ['scores dot sort','puts the list in order','three, seven, nine','sorted gives you','nine, seven, three','Remember']),
 ('Find', [['title','Find and count'],['code','pets.index("dog")'],['out','→ 1'],['code','[1, 2, 2, 3].count(2)'],['out','→ 2']],
  "index finds where an item is: pets dot index dog gives one. count says how many times something appears: in one, two, two, three, the count of two is two.",
  ['index finds','pets dot index dog','gives one','count says','the count of two is two']),
 ('Copy', [['title','Same list, or a copy?'],['code','a = [1, 2]'],['code','b = a'],['code','b.append(3)'],['out','→ a is [1, 2, 3] too!'],['code','c = a[:]'],['chalk','a[:] makes a real copy']],
  "Careful! a equals one, two. Then b equals a. That does not copy the list: b is a second name for the same list. So b dot append three changes a too! To copy, write c equals a, square bracket, colon. That makes a real copy.",
  ['Careful!','a equals one, two','Then b equals a','So b dot append three','changes a too','To copy, write c','That makes a real copy']),
 ('Grids', [['title','Lists inside lists'],['code','floor = [[1, 2], [3, 4]]'],['chalk','pick the row, then the column'],['code','floor[1][0]'],['out','→ 3']],
  "A list can hold other lists, like rows of floorboards. floor equals one, two, and three, four. Pick the row first, then the column. floor, square bracket one, square bracket zero, is row one, column zero: three.",
  ['A list can hold other lists','floor equals one, two','Pick the row first','floor, square bracket one','column zero: three']),
 ('Stacks', [['title','Stacks and queues'],['code','stack.append(x)   stack.pop()'],['chalk','last in, first out'],['code','queue.append(x)   queue.pop(0)'],['chalk','first in, first out']],
  "A stack is like a pile of plates. stack dot append adds to the top, and stack dot pop takes from the top: last in, first out. A queue is like a line at the shop. queue dot append joins the end, and queue dot pop zero serves the front: first in, first out.",
  ['A stack is like','stack dot append adds','last in, first out','queue dot append joins','first in, first out']),
 ('Build', [['title','Build a list with a loop'],['code','squares = []'],['code','for n in range(4):'],['code','    squares.append(n * n)'],['out','→ [0, 1, 4, 9]']],
  "You can build a list step by step. squares equals an empty list. for n in range four: squares dot append, n times n. Now squares is zero, one, four, nine.",
  ['You can build','squares equals an empty','for n in range four','squares dot append','Now squares is']),
])
if __name__ == '__main__':
    print(L['lists1']['labels'])
