# The English lesson lines that teach letter SOUNDS. Each {x} is a phonics sound clip (tools/phonics/build_sounds.py)
# dropped into the recorded sentence, so the narrator says the sound, not the letter's name.
# Captions keep the plain `say` text from the lesson; the template must have the same number of words.
SAY_FIX = {  # content fixes to the caption text itself
    ('e2_s3', 4): ('The sounds a, e, i, o and u are vowels.', 'The letters a, e, i, o and u are vowels.'),
    # "add es" was read as "add s"
    ('e2_plural', 2): ('add es, so you can hear it.', 'add the letters e and s, so you can hear the extra sound.'),
}
LINES = {
 'e2_s1': {
  1: "Here are our first two sounds. S says {s}, like a snake, and sun starts with {s}. A says {a}, like the start of ant.",
  2: "Now t and p are short, quick sounds. T says {t}, like the start of tap. P says {p}, like the start of pen.",
  3: "Next come i and n. I says {i}, like the start of insect. N says {n}, like the start of net.",
  4: "Say a word slowly and listen to how it starts. Sun starts with {s}, pen starts with {p}, and net starts with {n}.",
 },
 'e2_s2': {
  1: "M says {m}, as if something tastes nice. Map starts with {m}. D says {d}, and dog starts with {d}.",
  2: "G says {g}, like the start of gate. Now listen to o. O says {o}, like the start of on.",
  3: "C and k make the same sound. Cat starts with {k}, and kite starts with {k}. Two letters, one sound!",
  4: "Now push sounds together. {m}, {a}, {p} makes map. {d}, {o}, {g} makes dog.",
 },
 'e2_s3': {
  1: "Listen to the short vowels. E says {e}, like the start of egg. U says {u}, like the start of up.",
  2: "R says {r}, like a growling dog. Rat starts with {r}. H says {h}, like a little breath, and hat starts with {h}.",
  3: "B says {b}, like the start of bat. F says {f}, like fish. L says {l}, like lion.",
  4: None,  # caption fix only: re-recorded as written
 },
 'e2_blend': {
  0: "Reading a word is like pushing beads together on a string. Say each sound: {k}, {a}, {t}. Now push them together fast: cat!",
  1: "Let us try more. {p}, {i}, {g} makes pig. {s}, {u}, {n} makes sun.",
  3: "When you meet a new word, do not guess. Sound it out: {b}, {e}, {d}, bed.",
 },
 'e2_digraph': {
  1: "S and h together say {sh}, like asking for quiet. Ship starts with {sh}, and fish ends with {sh}.",
  2: "C and h together say {ch}, like a sneezing train. Chips and cheese start with {ch}.",
  3: "T and h together say {th}: put your tongue between your teeth. Thumb starts with {th}, and bath ends with {th}.",
  4: "N and g together say {ng}, deep in your nose. Ring and king end with {ng}.",
 },
 'e2_long': {
  1: "A and i together say {ai}, the name of the letter a. Rain and train have the {ai} sound.",
  2: "Two e's together say {ee}. Tree and bee have the {ee} sound.",
  3: "O and a together say {oa}. Boat and goat have the {oa} sound.",
 },
 'e2_challenge': {
  1: "First, a new word. {f}, {i}, {sh} makes fish.",
 },
 'e2_plural': {
  2: None,  # caption fix only: re-recorded as written
 },
}

# When a recording cannot load, the phone's own voice reads the line. It cannot say a bare sound either
# ("sss" comes out as "ess ess ess"), so it reads these lines instead, which teach the same thing in words.
DEVICE = {
 ('e2_s1', 1): "Here are our first two sounds. S makes a hissing sound, like a snake, and sun starts with that sound. A makes the sound at the start of ant.",
 ('e2_s1', 2): "Now t and p are short, quick sounds. T makes the sound at the start of tap. P makes the sound at the start of pen.",
 ('e2_s1', 3): "Next come i and n. I makes the sound at the start of insect. N makes the sound at the start of net.",
 ('e2_s1', 4): "Say a word slowly and listen to how it starts. Sun starts with the s sound, pen starts with the p sound, and net starts with the n sound.",
 ('e2_s2', 1): "M makes a humming sound, as if something tastes nice. Map starts with that sound. D makes the sound at the start of dog.",
 ('e2_s2', 2): "G makes the sound at the start of gate. Now listen to o. O makes the sound at the start of on.",
 ('e2_s2', 3): "C and k make the same sound. Cat and kite both start with that sound. Two letters, one sound!",
 ('e2_s2', 4): "Now push sounds together. The sounds of m, a and p make map. The sounds of d, o and g make dog.",
 ('e2_s3', 1): "Listen to the short vowels. E makes the sound at the start of egg. U makes the sound at the start of up.",
 ('e2_s3', 2): "R makes a sound like a growling dog, and rat starts with it. H makes a sound like a little breath, and hat starts with it.",
 ('e2_s3', 3): "B makes the sound at the start of bat. F makes the sound at the start of fish. L makes the sound at the start of lion.",
 ('e2_blend', 0): "Reading a word is like pushing beads together on a string. Say the sound of each letter in cat, one at a time. Now push them together fast: cat!",
 ('e2_blend', 1): "Let us try more. The sounds of p, i and g make pig. The sounds of s, u and n make sun.",
 ('e2_blend', 3): "When you meet a new word, do not guess. Sound it out one letter at a time, then say the word: bed.",
 ('e2_digraph', 1): "S and h together make one new sound, the sound you make when you ask for quiet. Ship starts with it, and fish ends with it.",
 ('e2_digraph', 2): "C and h together make one new sound, like a sneezing train. Chips and cheese start with it.",
 ('e2_digraph', 3): "T and h together make one new sound: put your tongue between your teeth. Thumb starts with it, and bath ends with it.",
 ('e2_digraph', 4): "N and g together make one new sound, deep in your nose. Ring and king end with it.",
 ('e2_long', 1): "A and i together say the name of the letter a. Rain and train have this sound.",
 ('e2_long', 2): "Two e's together say the name of the letter e. Tree and bee have this sound.",
 ('e2_long', 3): "O and a together say the name of the letter o. Boat and goat have this sound.",
 ('e2_challenge', 1): "First, a new word. Sound it out one letter at a time, then push the sounds together: fish.",
}
