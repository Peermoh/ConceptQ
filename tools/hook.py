# Adds test-only hooks to the local test copy (serve/index.html). Never used on the published page.
p='/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/serve/index.html'; s=open(p).read()
k="  document.getElementById('qBack').addEventListener"
s=s.replace(k,"  window.__undo = function (q) { if (answers[q] === Q[q].answer) { firstTry--; earned -= 10; } answers[q] = undefined; qi = q; renderQ(); }; // test copy only\n"+k,1)
open(p,'w').write(s)
s=open(p).read()
s=s.replace(k,"  window.__aud = function () { return { step: lesson.step, mode: lesson.clock && lesson.clock.mode, t: voiceEl.currentTime, clk: clockNow(), voice: VOICE, paused: voiceEl.paused }; }; // test copy only\n"+k,1)
open(p,'w').write(s)
# the guided tour starts by itself only when the address asks for it (?tour), so older tests are not blocked by it
s=open(p).read()
s=s.replace("    setTimeout(startTour, 700);","    if (/[?&]tour\\b/.test(location.search)) setTimeout(startTour, 700);",1)
s=s.replace("if (!profile.toured && !/[?&]notour\\b/.test(location.search)) setTimeout(startTour, 1200);","if (!profile.toured && /[?&]tour\\b/.test(location.search)) setTimeout(startTour, 1200);",1)
open(p,'w').write(s)
