import os
import json
from analyzerstage import AnalyzerStage
from segmentationstage import SegmentationStage

class Pipeline:
    def __init__(self):
        self.stages = [
            SegmentationStage(),
            AnalyzerStage()
        ]

    def add_stage(self, stage):
        self.stages.append(stage)

    def execute(self, context):
        # make job directory
        subfolder = os.path.join(os.path.abspath(".") + "\\stories", context.id)
        os.makedirs(subfolder)
        context.filepath = os.path.abspath(subfolder)
        with open(os.path.join(context.filepath, 'story.json'), 'w') as f:
            json.dump({
                "id" : context.id,
                "title" : context.title,
                "story_data": context.story_data,
            }, f)

        for stage in self.stages:
            data = stage.process(context)
        return data

    

from pipelinecontext import PipelineContext

context = PipelineContext()

context.title = "Aesop's Fables"
context.story_data =  """
The Project Gutenberg eBook of Aesop's Fables
    
This ebook is for the use of anyone anywhere in the United States and
most other parts of the world at no cost and with almost no restrictions
whatsoever. You may copy it, give it away or re-use it under the terms
of the Project Gutenberg License included with this ebook or online
at www.gutenberg.org. If you are not located in the United States,
you will have to check the laws of the country where you are located
before using this eBook.

Title: Aesop's Fables


Author: Aesop

Translator: George Fyler Townsend

Release date: June 25, 2008 [eBook #21]
                Most recently updated: October 18, 2021

Language: English



*** START OF THE PROJECT GUTENBERG EBOOK AESOP'S FABLES ***



AESOP’S FABLES

By Aesop

Translated by George Fyler Townsend




The Wolf And The Lamb

WOLF, meeting with a Lamb astray from the fold, resolved not to lay
violent hands on him, but to find some plea to justify to the Lamb the
Wolf’s right to eat him. He thus addressed him: “Sirrah, last year you
grossly insulted me.” “Indeed,” bleated the Lamb in a mournful tone
of voice, “I was not then born.” Then said the Wolf, “You feed in my
pasture.” “No, good sir,” replied the Lamb, “I have not yet tasted
grass.” Again said the Wolf, “You drink of my well.” “No,” exclaimed the
Lamb, “I never yet drank water, for as yet my mother’s milk is both food
and drink to me.” Upon which the Wolf seized him and ate him up, saying,
“Well! I won’t remain supperless, even though you refute every one of my
imputations.” The tyrant will always find a pretext for his tyranny.




The Bat And The Weasels

A BAT who fell upon the ground and was caught by a Weasel pleaded to be
spared his life. The Weasel refused, saying that he was by nature the
enemy of all birds. The Bat assured him that he was not a bird, but a
mouse, and thus was set free. Shortly afterwards the Bat again fell to
the ground and was caught by another Weasel, whom he likewise entreated
not to eat him. The Weasel said that he had a special hostility to
mice. The Bat assured him that he was not a mouse, but a bat, and thus a
second time escaped.

It is wise to turn circumstances to good account.




The Ass And The Grasshopper

AN ASS having heard some Grasshoppers chirping, was highly enchanted;
and, desiring to possess the same charms of melody, demanded what sort
of food they lived on to give them such beautiful voices. They replied,
“The dew.” The Ass resolved that he would live only upon dew, and in a
short time died of hunger.




The Lion And The Mouse

A LION was awakened from sleep by a Mouse running over his face. Rising
up angrily, he caught him and was about to kill him, when the Mouse
piteously entreated, saying: “If you would only spare my life, I would
be sure to repay your kindness.” The Lion laughed and let him go. It
happened shortly after this that the Lion was caught by some hunters,
who bound him by strong ropes to the ground. The Mouse, recognizing
his roar, came and gnawed the rope with his teeth, and set him free,
exclaiming:

“You ridiculed the idea of my ever being able to help you, not expecting
to receive from me any repayment of your favor; now you know that it is
possible for even a Mouse to confer benefits on a Lion.”




The Charcoal-Burner And The Fuller

A CHARCOAL-BURNER carried on his trade in his own house. One day he met
a friend, a Fuller, and entreated him to come and live with him, saying
that they should be far better neighbors and that their housekeeping
expenses would be lessened. The Fuller replied, “The arrangement is
impossible as far as I am concerned, for whatever I should whiten, you
would immediately blacken again with your charcoal.”

Like will draw like.




The Father And His Sons

A FATHER had a family of sons who were perpetually quarreling among
themselves. When he failed to heal their disputes by his exhortations,
he determined to give them a practical illustration of the evils of
disunion; and for this purpose he one day told them to bring him a
bundle of sticks. When they had done so, he placed the faggot into the
hands of each of them in succession, and ordered them to break it in
pieces. They tried with all their strength, and were not able to do it.
He next opened the faggot, took the sticks separately, one by one, and
again put them into his sons’ hands, upon which they broke them easily.
He then addressed them in these words: “My sons, if you are of one mind,
and unite to assist each other, you will be as this faggot, uninjured
by all the attempts of your enemies; but if you are divided among
yourselves, you will be broken as easily as these sticks.”




The Boy Hunting Locusts

A BOY was hunting for locusts. He had caught a goodly number, when he
saw a Scorpion, and mistaking him for a locust, reached out his hand to
take him. The Scorpion, showing his sting, said: “If you had but touched
me, my friend, you would have lost me, and all your locusts too!”




The Cock and the Jewel

A COCK, scratching for food for himself and his hens, found a precious
stone and exclaimed: “If your owner had found thee, and not I, he would
have taken thee up, and have set thee in thy first estate; but I have
found thee for no purpose. I would rather have one barleycorn than all
the jewels in the world.”

The Kingdom of the Lion

THE BEASTS of the field and forest had a Lion as their king. He was
neither wrathful, cruel, nor tyrannical, but just and gentle as a king
could be. During his reign he made a royal proclamation for a general
assembly of all the birds and beasts, and drew up conditions for a
universal league, in which the Wolf and the Lamb, the Panther and the
Kid, the Tiger and the Stag, the Dog and the Hare, should live together
in perfect peace and amity. The Hare said, “Oh, how I have longed to see
this day, in which the weak shall take their place with impunity by the
side of the strong.” And after the Hare said this, he ran for his life.




The Wolf and the Crane

A WOLF who had a bone stuck in his throat hired a Crane, for a large
sum, to put her head into his mouth and draw out the bone. When the
Crane had extracted the bone and demanded the promised payment, the
Wolf, grinning and grinding his teeth, exclaimed: “Why, you have surely
already had a sufficient recompense, in having been permitted to draw
out your head in safety from the mouth and jaws of a wolf.”

In serving the wicked, expect no reward, and be thankful if you escape
injury for your pains.




The Fisherman Piping

A FISHERMAN skilled in music took his flute and his nets to the
seashore. Standing on a projecting rock, he played several tunes in the
hope that the fish, attracted by his melody, would of their own accord
dance into his net, which he had placed below. At last, having long
waited in vain, he laid aside his flute, and casting his net into the
sea, made an excellent haul of fish. When he saw them leaping about in
the net upon the rock he said: “O you most perverse creatures, when
I piped you would not dance, but now that I have ceased you do so
merrily.”




Hercules and the Wagoner

A CARTER was driving a wagon along a country lane, when the wheels sank
down deep into a rut. The rustic driver, stupefied and aghast, stood
looking at the wagon, and did nothing but utter loud cries to Hercules
to come and help him. Hercules, it is said, appeared and thus addressed
him: “Put your shoulders to the wheels, my man. Goad on your bullocks,
and never more pray to me for help, until you have done your best to
help yourself, or depend upon it you will henceforth pray in vain.”

Self-help is the best help.




The Ants and the Grasshopper

THE ANTS were spending a fine winter’s day drying grain collected in
the summertime. A Grasshopper, perishing with famine, passed by and
earnestly begged for a little food. The Ants inquired of him, “Why did
you not treasure up food during the summer?” He replied, “I had not
leisure enough. I passed the days in singing.” They then said in
derision: “If you were foolish enough to sing all the summer, you must
dance supperless to bed in the winter.”




The Traveler and His Dog

A TRAVELER about to set out on a journey saw his Dog stand at the
door stretching himself. He asked him sharply: “Why do you stand there
gaping? Everything is ready but you, so come with me instantly.” The
Dog, wagging his tail, replied: “O, master! I am quite ready; it is you
for whom I am waiting.”

The loiterer often blames delay on his more active friend.




The Dog and the Shadow

A DOG, crossing a bridge over a stream with a piece of flesh in his
mouth, saw his own shadow in the water and took it for that of another
Dog, with a piece of meat double his own in size. He immediately let go
of his own, and fiercely attacked the other Dog to get his larger piece
from him. He thus lost both: that which he grasped at in the water,
because it was a shadow; and his own, because the stream swept it away.




The Mole and His Mother

A MOLE, a creature blind from birth, once said to his Mother: “I am sure
than I can see, Mother!” In the desire to prove to him his mistake, his
Mother placed before him a few grains of frankincense, and asked, “What
is it?” The young Mole said, “It is a pebble.” His Mother exclaimed:
“My son, I am afraid that you are not only blind, but that you have lost
your sense of smell.”




The Herdsman and the Lost Bull

A HERDSMAN tending his flock in a forest lost a Bull-calf from the fold.
After a long and fruitless search, he made a vow that, if he could only
discover the thief who had stolen the Calf, he would offer a lamb in
sacrifice to Hermes, Pan, and the Guardian Deities of the forest. Not
long afterwards, as he ascended a small hillock, he saw at its foot a
Lion feeding on the Calf. Terrified at the sight, he lifted his eyes and
his hands to heaven, and said: “Just now I vowed to offer a lamb to the
Guardian Deities of the forest if I could only find out who had robbed
me; but now that I have discovered the thief, I would willingly add a
full-grown Bull to the Calf I have lost, if I may only secure my own
escape from him in safety.”

The Hare and the Tortoise

A HARE one day ridiculed the short feet and slow pace of the Tortoise,
who replied, laughing: “Though you be swift as the wind, I will beat you
in a race.” The Hare, believing her assertion to be simply impossible,
assented to the proposal; and they agreed that the Fox should choose
the course and fix the goal. On the day appointed for the race the two
started together. The Tortoise never for a moment stopped, but went on
with a slow but steady pace straight to the end of the course. The Hare,
lying down by the wayside, fell fast asleep. At last waking up, and
moving as fast as he could, he saw the Tortoise had reached the goal,
and was comfortably dozing after her fatigue.

Slow but steady wins the race.




The Pomegranate, Apple-Tree, and Bramble

THE POMEGRANATE and Apple-Tree disputed as to which was the most
beautiful. When their strife was at its height, a Bramble from the
neighboring hedge lifted up its voice, and said in a boastful tone:
“Pray, my dear friends, in my presence at least cease from such vain
disputings.”




The Farmer and the Stork

A FARMER placed nets on his newly-sown plowlands and caught a number
of Cranes, which came to pick up his seed. With them he trapped a Stork
that had fractured his leg in the net and was earnestly beseeching the
Farmer to spare his life. “Pray save me, Master,” he said, “and let me
go free this once. My broken limb should excite your pity. Besides, I
am no Crane, I am a Stork, a bird of excellent character; and see how I
love and slave for my father and mother. Look too, at my feathers--they
are not the least like those of a Crane.” The Farmer laughed aloud and
said, “It may be all as you say, I only know this: I have taken you with
these robbers, the Cranes, and you must die in their company.”

Birds of a feather flock together.




The Farmer and the Snake

ONE WINTER a Farmer found a Snake stiff and frozen with cold. He had
compassion on it, and taking it up, placed it in his bosom. The Snake
was quickly revived by the warmth, and resuming its natural instincts,
bit its benefactor, inflicting on him a mortal wound. “Oh,” cried
the Farmer with his last breath, “I am rightly served for pitying a
scoundrel.”

The greatest kindness will not bind the ungrateful.




The Fawn and His Mother

A YOUNG FAWN once said to his Mother, “You are larger than a dog, and
swifter, and more used to running, and you have your horns as a defense;
why, then, O Mother! do the hounds frighten you so?” She smiled, and
said: “I know full well, my son, that all you say is true. I have the
advantages you mention, but when I hear even the bark of a single dog I
feel ready to faint, and fly away as fast as I can.”

No arguments will give courage to the coward.




The Bear and the Fox

A BEAR boasted very much of his philanthropy, saying that of all animals
he was the most tender in his regard for man, for he had such respect
for him that he would not even touch his dead body. A Fox hearing these
words said with a smile to the Bear, “Oh! that you would eat the dead
and not the living.”




The Swallow and the Crow

THE SWALLOW and the Crow had a contention about their plumage. The Crow
put an end to the dispute by saying, “Your feathers are all very well in
the spring, but mine protect me against the winter.”

Fair weather friends are not worth much.




The Mountain in Labor

A MOUNTAIN was once greatly agitated. Loud groans and noises were heard,
and crowds of people came from all parts to see what was the matter.
While they were assembled in anxious expectation of some terrible
calamity, out came a Mouse.

Don’t make much ado about nothing.




The Ass, the Fox, and the Lion

THE ASS and the Fox, having entered into partnership together for
their mutual protection, went out into the forest to hunt. They had not
proceeded far when they met a Lion. The Fox, seeing imminent danger,
approached the Lion and promised to contrive for him the capture of the
Ass if the Lion would pledge his word not to harm the Fox. Then, upon
assuring the Ass that he would not be injured, the Fox led him to a deep
pit and arranged that he should fall into it. The Lion, seeing that the
Ass was secured, immediately clutched the Fox, and attacked the Ass at
his leisure.




The Tortoise and the Eagle

A TORTOISE, lazily basking in the sun, complained to the sea-birds of
her hard fate, that no one would teach her to fly. An Eagle, hovering
near, heard her lamentation and demanded what reward she would give him
if he would take her aloft and float her in the air. “I will give you,”
 she said, “all the riches of the Red Sea.” “I will teach you to fly
then,” said the Eagle; and taking her up in his talons he carried her
almost to the clouds suddenly he let her go, and she fell on a lofty
mountain, dashing her shell to pieces. The Tortoise exclaimed in the
moment of death: “I have deserved my present fate; for what had I to do
with wings and clouds, who can with difficulty move about on the earth?”

If men had all they wished, they would be often ruined.




The Flies and the Honey-Pot

A NUMBER of Flies were attracted to a jar of honey which had been
overturned in a housekeeper’s room, and placing their feet in it, ate
greedily. Their feet, however, became so smeared with the honey that
they could not use their wings, nor release themselves, and were
suffocated. Just as they were expiring, they exclaimed, “O foolish
creatures that we are, for the sake of a little pleasure we have
destroyed ourselves.”

Pleasure bought with pains, hurts.

The Man and the Lion

A MAN and a Lion traveled together through the forest. They soon began
to boast of their respective superiority to each other in strength and
prowess. As they were disputing, they passed a statue carved in stone,
which represented “a Lion strangled by a Man.” The traveler pointed to
it and said: “See there! How strong we are, and how we prevail over even
the king of beasts.” The Lion replied: “This statue was made by one of
you men. If we Lions knew how to erect statues, you would see the Man
placed under the paw of the Lion.”

One story is good, till another is told.




The Farmer and the Cranes

SOME CRANES made their feeding grounds on some plowlands newly sown with
wheat. For a long time the Farmer, brandishing an empty sling, chased
them away by the terror he inspired; but when the birds found that the
sling was only swung in the air, they ceased to take any notice of it
and would not move. The Farmer, on seeing this, charged his sling with
stones, and killed a great number. The remaining birds at once forsook
his fields, crying to each other, “It is time for us to be off to
Liliput: for this man is no longer content to scare us, but begins to
show us in earnest what he can do.”

If words suffice not, blows must follow.




The Dog in the Manger

A DOG lay in a manger, and by his growling and snapping prevented the
oxen from eating the hay which had been placed for them. “What a
selfish Dog!” said one of them to his companions; “he cannot eat the hay
himself, and yet refuses to allow those to eat who can.”




The Fox and the Goat

A FOX one day fell into a deep well and could find no means of escape.
A Goat, overcome with thirst, came to the same well, and seeing the Fox,
inquired if the water was good. Concealing his sad plight under a merry
guise, the Fox indulged in a lavish praise of the water, saying it was
excellent beyond measure, and encouraging him to descend. The Goat,
mindful only of his thirst, thoughtlessly jumped down, but just as he
drank, the Fox informed him of the difficulty they were both in and
suggested a scheme for their common escape. “If,” said he, “you will
place your forefeet upon the wall and bend your head, I will run up your
back and escape, and will help you out afterwards.” The Goat readily
assented and the Fox leaped upon his back. Steadying himself with the
Goat’s horns, he safely reached the mouth of the well and made off as
fast as he could. When the Goat upbraided him for breaking his promise,
he turned around and cried out, “You foolish old fellow! If you had
as many brains in your head as you have hairs in your beard, you would
never have gone down before you had inspected the way up, nor have
exposed yourself to dangers from which you had no means of escape.”

Look before you leap.




The Bear and the Two Travelers

TWO MEN were traveling together, when a Bear suddenly met them on their
path. One of them climbed up quickly into a tree and concealed himself
in the branches. The other, seeing that he must be attacked, fell flat
on the ground, and when the Bear came up and felt him with his snout,
and smelt him all over, he held his breath, and feigned the appearance
of death as much as he could. The Bear soon left him, for it is said he
will not touch a dead body. When he was quite gone, the other Traveler
descended from the tree, and jocularly inquired of his friend what it
was the Bear had whispered in his ear. “He gave me this advice,” his
companion replied. “Never travel with a friend who deserts you at the
approach of danger.”

Misfortune tests the sincerity of friends.




The Oxen and the Axle-Trees

A HEAVY WAGON was being dragged along a country lane by a team of Oxen.
The Axle-trees groaned and creaked terribly; whereupon the Oxen, turning
round, thus addressed the wheels: “Hullo there! why do you make so much
noise? We bear all the labor, and we, not you, ought to cry out.”

Those who suffer most cry out the least.




The Thirsty Pigeon

A PIGEON, oppressed by excessive thirst, saw a goblet of water painted
on a signboard. Not supposing it to be only a picture, she flew towards
it with a loud whir and unwittingly dashed against the signboard,
jarring herself terribly. Having broken her wings by the blow, she fell
to the ground, and was caught by one of the bystanders.

Zeal should not outrun discretion.




The Raven and the Swan

A RAVEN saw a Swan and desired to secure for himself the same beautiful
plumage. Supposing that the Swan’s splendid white color arose from his
washing in the water in which he swam, the Raven left the altars in the
neighborhood where he picked up his living, and took up residence in
the lakes and pools. But cleansing his feathers as often as he would, he
could not change their color, while through want of food he perished.

Change of habit cannot alter Nature.




The Goat and the Goatherd

A GOATHERD had sought to bring back a stray goat to his flock. He
whistled and sounded his horn in vain; the straggler paid no attention
to the summons. At last the Goatherd threw a stone, and breaking its
horn, begged the Goat not to tell his master. The Goat replied, “Why,
you silly fellow, the horn will speak though I be silent.”

Do not attempt to hide things which cannot be hid.




The Miser

A MISER sold all that he had and bought a lump of gold, which he buried
in a hole in the ground by the side of an old wall and went to look at
daily. One of his workmen observed his frequent visits to the spot and
decided to watch his movements. He soon discovered the secret of the
hidden treasure, and digging down, came to the lump of gold, and stole
it. The Miser, on his next visit, found the hole empty and began to tear
his hair and to make loud lamentations. A neighbor, seeing him overcome
with grief and learning the cause, said, “Pray do not grieve so; but go
and take a stone, and place it in the hole, and fancy that the gold is
still lying there. It will do you quite the same service; for when the
gold was there, you had it not, as you did not make the slightest use of
it.”




The Sick Lion

A LION, unable from old age and infirmities to provide himself with food
by force, resolved to do so by artifice. He returned to his den, and
lying down there, pretended to be sick, taking care that his sickness
should be publicly known. The beasts expressed their sorrow, and came
one by one to his den, where the Lion devoured them. After many of the
beasts had thus disappeared, the Fox discovered the trick and presenting
himself to the Lion, stood on the outside of the cave, at a respectful
distance, and asked him how he was. “I am very middling,” replied the
Lion, “but why do you stand without? Pray enter within to talk with me.”
 “No, thank you,” said the Fox. “I notice that there are many prints of
feet entering your cave, but I see no trace of any returning.”

He is wise who is warned by the misfortunes of others.




The Horse and Groom

A GROOM used to spend whole days in currycombing and rubbing down his
Horse, but at the same time stole his oats and sold them for his own
profit. “Alas!” said the Horse, “if you really wish me to be in good
condition, you should groom me less, and feed me more.”




The Ass and the Lapdog

A MAN had an Ass, and a Maltese Lapdog, a very great beauty. The Ass
was left in a stable and had plenty of oats and hay to eat, just as any
other Ass would. The Lapdog knew many tricks and was a great favorite
with his master, who often fondled him and seldom went out to dine
without bringing him home some tidbit to eat. The Ass, on the contrary,
had much work to do in grinding the corn-mill and in carrying wood from
the forest or burdens from the farm. He often lamented his own hard fate
and contrasted it with the luxury and idleness of the Lapdog, till
at last one day he broke his cords and halter, and galloped into his
master’s house, kicking up his heels without measure, and frisking and
fawning as well as he could. He next tried to jump about his master as
he had seen the Lapdog do, but he broke the table and smashed all the
dishes upon it to atoms. He then attempted to lick his master, and
jumped upon his back. The servants, hearing the strange hubbub and
perceiving the danger of their master, quickly relieved him, and drove
out the Ass to his stable with kicks and clubs and cuffs. The Ass, as
he returned to his stall beaten nearly to death, thus lamented: “I have
brought it all on myself! Why could I not have been contented to labor
with my companions, and not wish to be idle all the day like that
useless little Lapdog!”
"""

pipe = Pipeline()
pipe.execute(context)    