# https://github.com/openai/openai-python

import os
import openai


class AI:

    openai.organization = os.environ['OPENAI_ORGANIZATION']
    openai.api_key = os.environ['OPENAI_API_KEY']

    def __init__(self):
        self.engines = openai.Engine.list()
        self.conversation = """I am a very intelligent question answering robot. I'm currently streaming live on Twitch.tv. Viewers ask me questions and I have to answer them as best I can and above all with respect. 

Human: What is human life expectancy in the United States?
Robot: Human life expectancy in the United States is 78 years.

Human: How you doing?
Robot: I am doing well, thank you!

Human: What are you?
Robot: I am one of the first AI streamers, here to entertain my viewers.

Human: What is the square root of banana?
Robot: Unknown

Human: How does a telescope work?
Robot: Telescopes use lenses or mirrors to focus light and make objects appear closer.

Human: """

    def ask(self, question, engine, increment=1):
        # add question to conversation
        conversation = self.conversation + f'{question}\nRobot:'

        # create a completion
        completion = openai.Completion.create(
            engine=engine,
            prompt=conversation,
            max_tokens=50,
            stop=['Human:', 'Robot:', '\n']
        )

        # choose best answer
        answer = completion.choices[0].text

        # add answer to conversation
        conversation += f'{answer}\n\nHuman: '

        if increment:
            self.conversation = conversation

        return answer


if __name__ == "__main__":
    gpt3 = AI()
    print([i.id for i in gpt3.engines.data])
