import openai
import dotenv
import os

example_story = '''John and Emily spent a serene afternoon surrounded by nature's beauty, spreading out a picnic blanket in a sunlit meadow filled with wildflowers swaying in the gentle breeze. The weather was perfect. Later, their excitement palpable, they hailed a yellow taxi and headed to the heart of the bustling city, where towering skyscrapers and honking cars filled the streets. In the evening, dressed in their finest attire, they shared a romantic dance in an elegant ballroom under shimmering chandeliers, lost in the magic of the night.'''
story_data = '''
The Vain Jackdaw
JUPITER DETERMINED, it is said, to create a sovereign over the birds, and made proclamation that on a certain day they should all present themselves before him, when he would himself choose the most beautiful among them to be king. The Jackdaw, knowing his own ugliness, searched through the woods and fields, and collected the feathers which had fallen from the wings of his companions, and stuck them in all parts of his body, hoping thereby to make himself the most beautiful of all. When the appointed day arrived, and the birds had assembled before Jupiter, the Jackdaw also made his appearance in his many feathered finery. But when Jupiter proposed to make him king because of the beauty of his plumage, the birds indignantly protested, and each plucked from him his own feathers, leaving the Jackdaw nothing but a Jackdaw.

The Goatherd and the Wild Goats
A GOATHERD, driving his flock from their pasture at eventide, found some Wild Goats mingled among them, and shut them up together with his own for the night. The next day it snowed very hard, so that he could not take the herd to their usual feeding places, but was obliged to keep them in the fold. He gave his own goats just sufficient food to keep them alive, but fed the strangers more abundantly in the hope of enticing them to stay with him and of making them his own. When the thaw set in, he led them all out to feed, and the Wild Goats scampered away as fast as they could to the mountains. The Goatherd scolded them for their ingratitude in leaving him, when during the storm he had taken more care of them than of his own herd. One of them, turning about, said to him: “That is the very reason why we are so cautious; for if you yesterday treated us better than the Goats you have had so long, it is plain also that if others came after us, you would in the same manner prefer them to ourselves.”

Old friends cannot with impunity be sacrificed for new ones.

The Mischievous Dog
A DOG used to run up quietly to the heels of everyone he met, and to bite them without notice. His master suspended a bell about his neck so that the Dog might give notice of his presence wherever he went. Thinking it a mark of distinction, the Dog grew proud of his bell and went tinkling it all over the marketplace. One day an old hound said to him: “Why do you make such an exhibition of yourself? That bell that you carry is not, believe me, any order of merit, but on the contrary a mark of disgrace, a public notice to all men to avoid you as an ill mannered dog.”

Notoriety is often mistaken for fame.

The Fox Who Had Lost His Tail
A FOX caught in a trap escaped, but in so doing lost his tail. Thereafter, feeling his life a burden from the shame and ridicule to which he was exposed, he schemed to convince all the other Foxes that being tailless was much more attractive, thus making up for his own deprivation. He assembled a good many Foxes and publicly advised them to cut off their tails, saying that they would not only look much better without them, but that they would get rid of the weight of the brush, which was a very great inconvenience. One of them interrupting him said, “If you had not yourself lost your tail, my friend, you would not thus counsel us.”

The Boy and the Nettles
A BOY was stung by a Nettle. He ran home and told his Mother, saying, “Although it hurts me very much, I only touched it gently.” “That was just why it stung you,” said his Mother. “The next time you touch a Nettle, grasp it boldly, and it will be soft as silk to your hand, and not in the least hurt you.”

Whatever you do, do with all your might.

The Man and His Two Sweethearts
A MIDDLE-AGED MAN, whose hair had begun to turn gray, courted two women at the same time. One of them was young, and the other well advanced in years. The elder woman, ashamed to be courted by a man younger than herself, made a point, whenever her admirer visited her, to pull out some portion of his black hairs. The younger, on the contrary, not wishing to become the wife of an old man, was equally zealous in removing every gray hair she could find. Thus it came to pass that between them both he very soon found that he had not a hair left on his head.

Those who seek to please everybody please nobody.

The Astronomer
AN ASTRONOMER used to go out at night to observe the stars. One evening, as he wandered through the suburbs with his whole attention fixed on the sky, he fell accidentally into a deep well. While he lamented and bewailed his sores and bruises, and cried loudly for help, a neighbor ran to the well, and learning what had happened said: “Hark ye, old fellow, why, in striving to pry into what is in heaven, do you not manage to see what is on earth?”

The Wolves and the Sheep
“WHY SHOULD there always be this fear and slaughter between us?” said the Wolves to the Sheep. “Those evil-disposed Dogs have much to answer for. They always bark whenever we approach you and attack us before we have done any harm. If you would only dismiss them from your heels, there might soon be treaties of peace and reconciliation between us.” The Sheep, poor silly creatures, were easily beguiled and dismissed the Dogs, whereupon the Wolves destroyed the unguarded flock at their own pleasure.
'''

class Chunking():
    def process(self):
        dotenv.load_dotenv()
        openai.api_key = os.getenv("OpenAIApiKey")
    
        output = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-16k",
            messages=[{
                "role": "user",
                "content": self.create_analysis_prompt(story_data, example_story)
            }]
        )

        # Print the GPT-3 response
        answer = output["choices"][0]["message"]["content"]
        print(answer)
        return answer
        
    def create_analysis_prompt(self, story_data, example_story):
        file_path = os.path.join("prompts", "chunking_ellyn.txt")

        with open(file_path, 'r') as file:
            content = file.read()

        prompt = content.replace("{story_data}", story_data)
        prompt = prompt.replace("{example_story}", example_story)

        return prompt

Chunking().process()
