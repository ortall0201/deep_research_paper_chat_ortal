#!/usr/bin/env python
from random import randint

from crewai.flow import Flow, listen, start
from pydantic import BaseModel

from crewai_flow_workshop1.crews.poem_crew.poem_crew import PoemCrew


class FlowState(BaseModel):
    user_message: str = ""
    message_history: list[dict] = {}


class PoemFlow(Flow[FlowState]):
    # def __init__(self):
    #     super().__init__()
    #     self.custom_state = InnerState()

    @start()
    def generate_sentence_count(self):
        print("Determine intent of user message")

        self.state.user_message = "Hello, how are you?"

    @listen(generate_sentence_count)
    def generate_poem(self):
        print("Answering user message")
        # result = (
        #     PoemCrew()
        #     .crew()
        #     .kickoff(inputs={"sentence_count": self.state.sentence_count})
        # )

        return self.state.user_message

        # print("Poem generated", result.raw)
        # self.state.poem = result.raw


def kickoff():
    poem_flow = PoemFlow(tracing=True)
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
