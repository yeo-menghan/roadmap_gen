import os
import sys
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import json

from langchain_community.tools import Tool, DuckDuckGoSearchResults
from langchain_community.utilities import SerpAPIWrapper
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

llm = ChatOpenAI(model="gpt-4-turbo-preview", openai_api_key=OPENAI_API_KEY, temperature=0)


# Defining classes
# from pydantic import BaseModel, Field
# from typing import List

# class ContentPointer(BaseModel):
#     sub_topic: str = Field(..., description="A specific area within a topic")
#     content_pointers: List[str] = Field(..., description="Key points or concepts related to the sub-topic")

# class Topic(BaseModel):
#     topic: str = Field(..., description="A major area of study or discussion within the course")
#     sub_topics: List[ContentPointer] = Field(..., description="Detailed breakdowns of specific areas within the topic")

# class Course_Outline(BaseModel):
#     name: str = Field(..., description="The overall title or theme of the course")
#     topics: List[Topic] = Field(..., description="A collection of major topics covered in the course")

# Write in LCEL format for better readability
def generate_course_outline(overall_topic):
    prompt = PromptTemplate.from_template(
        f"""
        Create a detailed course outline for teaching '{overall_topic}' to a total beginner,
        progressing from basic concepts to advanced {overall_topic} techniques.
        The outline should be structured in JSON format, with explicit headers for topics and sub-topics,
        each including detailed content pointers for learning objectives.
        Organize the outline to facilitate easy understanding and navigation through the course material.

        JSON Structure:
        {{{{"
        "name": "{overall_topic}",
        "topics": [
            {{{{
            "topic": "Introduction to SQL",
            "sub-topics": [
                {{{{
                "sub-topic": "What is SQL?",
                "content pointers": [
                    "Definition and purpose of SQL",
                    "History and evolution of SQL",
                    "SQL vs. NoSQL databases"
                ]
                }}}},
                {{{{
                ...additional sub-topics...
                }}}}
            ]
            }}}},
            {{{{
            ...additional topics...
            }}}}
        ]
        }}}}
        """
    )
    # print("class of course outline: ", type(Course_Outline))
    # output_parser = JsonOutputParser(pydantic_object=Course_Outline)
    llm_chain = prompt | llm

    response = llm_chain.invoke({"overall_topic": overall_topic})

    json_response = response.content
    json_response = json_response.strip('```json').strip('```')
    filename = f"{overall_topic}.json"
    with open(filename, "w") as file:
        file.write(json_response)
    print(f"Course outline saved as {filename}")

    return response

### MAIN ###

generate_course_outline("SQL")
