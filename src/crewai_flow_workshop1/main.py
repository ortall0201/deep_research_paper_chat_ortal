#!/usr/bin/env python
from random import randint

from crewai.flow import Flow, listen, start, router
from pydantic import BaseModel
from typing import Literal, List
from datetime import datetime
from crewai import LLM
import json

from crewai_flow_workshop1.crews.poem_crew.poem_crew import PoemCrew

class Message(BaseModel):
    role: Literal["user", "assistant"] = "user" 
    content: str
    timestamp: datetime = datetime.now()

class FlowState(BaseModel):
    user_message: str = "Hi! How are you?"
    message_history: List[Message] = []

class RouterIntent(BaseModel):
    intent: Literal["research", "conversation"]

# @persist()
class PoemFlow(Flow[FlowState]):

    def add_message(self, role: str, content: str):
        """Add a message to the message history"""
        new_message = Message(role=role, content=content)
        self.state.message_history.append(new_message)


    @start()
    def starting_flow(self):
        # Add the user message to history
        if self.state.user_message:
            self.add_message("user", self.state.user_message)

    @router(starting_flow)
    def routing_intent(self):

        llm = LLM(model="gpt-4.1-mini", 
            temperature=0.3,
            response_format=RouterIntent)

        response = llm.call(
            "Analyze the following messages and return the intent of the message, that can either be research or conversation."
            "use research when the query of the user is a follow up questions on a research that has been done already in the "
            "conversation history or a new query that can be reasearched on and passed to the deep research crew."
            f"User message:  {self.state.user_message}"
            f"Conversation history: {self.state.message_history}"
        )

        print(response)

        # Response is already a dict with the intent key
        if isinstance(response, str):
            response = json.loads(response)
        
        return response["intent"]

    @listen("conversation")
    def follow_up_conversation(self):

        llm = LLM(model="gpt-4.1-mini", temperature=0.3)

        response = llm.call(
            "As expert conversation handler, answer the user's message based on the conversation history."
            "Your task is to guide the user through the conversation based on the conversation history and the user's message "
            "making sure the scope is clear: guide the user to perform a deep research on scientific papers and pass it to the deep research crew."
            "or guide the user to perform a follow up conversation based on the conversation history and the user's message."
            f"User message:  {self.state.user_message}"
            f"Conversation history: {self.state.message_history}"
        )

        print(response)

    @listen("research")
    def handle_research(self):
        print("Research intent detected - starting deep research process")
        # TODO: Integrate with deep research crew
        # For now, just acknowledge the research request
        self.add_message("assistant", "I understand you want to do research. This will be handled by the research crew.")

    # @listen(generate_sentence_count)
    # def generate_poem(self):
    #     print("Answering user message")
        
    #     # Generate a sample response (you can replace this with actual CrewAI logic)
    #     assistant_response = "I'm doing well, thank you! I'd be happy to write you a poem. Here's a short one about the beauty of conversation."
        
    #     new_message = Message(role="assistant", content=assistant_response)
    #     self.state.message_history.append(new_message)
        
    #     # Display the current message history
    #     print(self.state.model_dump())
        
    #     return 'Finished'
        # Example of using extend_message_history with multiple messages
        # additional_messages = [
        #     Message(role="user", content="That's a nice poem!"),
        #     Message(role="assistant", content="Thank you! I'm glad you enjoyed it.")
        # ]
        # self.extend_message_history(additional_messages)
        
        # return self.state.model_dump()

        # Uncomment for actual CrewAI integration:
        # result = (
        #     PoemCrew()
        #     .crew()
        #     .kickoff(inputs={"sentence_count": self.state.sentence_count})
        # )
        # assistant_response = result.raw
        # self.add_message("assistant", assistant_response)
        # return assistant_response


def kickoff():
    poem_flow = PoemFlow(tracing=True)
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
