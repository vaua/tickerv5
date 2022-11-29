The experiments

Experiment 1.

Input: Start population number, lower population limit.

Goal: Survive as long as possible. 10 times start energy is a win (100 energy gives 100 ticks, if no action. For 1000 you have to do the right things
Senses: Vision. Left, centre, right indication if somebody there.
Actions: Go left (cost 2), Stay (no extra cost), Eat (cost 3), Go right (cost 2). 
Other: Success at eating if somebody else at same position (benefits 5, eaten loses 6). Every living being pays 1 each tick.
Procreation: When lower limit of population is reached, top 10 animals (who have lived the longest this far) are copied into existence. The rest is filled with random individuals.


Hypothesis: As the simulation progresses, the individuals with good genes will live longer and exist in more copies in the population. These individuals will be good at navigating the environment, living much longer than purely random individuals.


Analysis:

- The result will depend on density, as only 1 pixel left and right give input. If the world is sparse, “no input” action becomes important (as it will be the most often received one.
- The fact that it costs to attempt eating while no-one is around should suppress always-eaters. Eating should only be done when someone is present
- The fact that it costs more to be eaten than to eat should suppress situations when two agents eat each other.
- There is no way for animal to understand it is being eaten.

DNA of one animal that achieved age of 237: [[[4, 0], [7, 3], [1, 0], [7, 0], [6, 2], [4, 0], [2, 2], [3, 3]], [[3, 0], [2, 1], [3, 0], [4, 2], [3, 3], [6, 2], [0, 3]], []]
So: 
4, 0: If animal to the left, go left
7, 3: If animal everywhere, go right
1, 0: If animal to the right, go left
7, 0: If animal everywhere, go left
6, 2: if animals to the left and on the spot, EAT
2, 2: If animal in the middle, EAT
and so on.

It has a number of good ones to eat. And also 

Remark: As changes are applied serially to the world, an animal that is seen as being at my spot, may not be there when you attempt to eat. Happens!

Some results:
Running 500/50 does not give long lived individuals, 150-200 maybe.
Running 500/150 for 30K cycles gave 400-500 “old” individuals as best



Kolla lite varför DNA verkar ha flera lister, lite märkligt?
- Ok, found an issue with concept vs senses when it comes to DNA, now fixed. But we’ll see how it goes
- As of right now, there is a list for each sense with genes in DNA. Is this really necessary? Maybe having one list for all could be enough?

Nästa steg:

- mutation - när individerna kopieras så ändras deras gener lite
    - Rena ändringar
    - Kopieringar
    - Borttagning
    - Varianter av alla 3
- tillägg av intern-energy konceptet
    - varelsen vet hur mycket energy det hade innan, kan “känna” skillnaden och även absoluta biten.
    - det ska till ett nytt koncept, samt en till två  nya senses
    - 


Added both of the above.

An issue is that currently, the energy runs out of the world, as cost of living is deducted, but no new energy
apart from new random individuals is added. This means everybody will die eventually. So how do we fill upp?

One possibility could be "The Sun" - an area of the land that provides beings with the energy while in it, 
and moves gradually around. We could even add a special sense, for the sun, to see if the beings learn to follow
the sun (some should at least). That would be a solution to an earlier quest.

A being that then follows the sun would live for ever... if not eaten by other!

Yes, let's do this!

- Add the sun as concept
- Add the sun sense


OK, in some trouble now. I've been noticing, ever since I added the internal sense and the concept of duplication, that
Some animal tend to have lots of offspring, without necessarily loosing a lot of energy. Been trying for one day to figure out what is going on.
Still don't really know, and it is complex. Seems like some changes to the list in senses class do not affect the world class, but 
I cannot figure out how or why.

Will need to reconsider the approach.

Also, figured out the I'm adding multiple concept values as I do that for each sense, which was not ment. So, back to the drawing board, 
architecturally, and try and understand:
- how should concepts, senses and actuators relate to each other
- who should "own" the content of an entity and thus have the right to change it.


Experiment 2

Artificial need, artificial fear

Alter the world so that individuals with artificial fear / artificial need can appear (risk taking)

Idea - change the amount of eating, so that it becomes dangerous to stay in the same position as somebody.

Currently having some 





Experiment 3

Closeness to self - principle

Create and run such a world where individuals start protecting those who are of same / similar DNA
