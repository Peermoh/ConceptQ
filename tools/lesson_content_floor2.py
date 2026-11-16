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
if __name__ == '__main__':
    print(L['lists1']['labels'])
