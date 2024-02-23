from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
import json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4-turbo-preview", openai_api_key=OPENAI_API_KEY)

def generate_course_outline(overall_topic):
    # prompt = ChatPromptTemplate.from_messages([
    #     ("system", "You are world class technical documentation writer."),
    #     ("user", "{input}")
    # ])

    prompt = f"""
    Create a detailed course outline for teaching '{overall_topic}' to a total beginner,
    progressing from basic concepts to advanced {overall_topic} techniques.
    The outline should be structured in JSON format, with explicit headers for topics and sub-topics,
    each including detailed content pointers for learning objectives.
    Organize the outline to facilitate easy understanding and navigation through the course material.

    JSON Structure:
    {{"
    "name": "{overall_topic}",
    "topics": [
        {{
        "topic": "Introduction to SQL",
        "sub-topics": [
            {{
            "sub-topic": "What is SQL?",
            "content pointers": [
                "Definition and purpose of SQL",
                "History and evolution of SQL",
                "SQL vs. NoSQL databases"
            ]
            }},
            {{
            ...additional sub-topics...
            }}
        ]
        }},
        {{
        ...additional topics...
        }}
    ]
    }}
    """

    response = llm.invoke(prompt, max_tokens=1024, temperature=0.5, stop=None)
    json_response = response.content
    json_response = json_response.strip('```json').strip('```')


    # Define the filename based on the overall_topic
    filename = f"{overall_topic}.json"

    # Write the JSON string to a file
    with open(filename, "w") as file:
        file.write(json_response)

    print(f"Course outline saved as {filename}")

    return json_response

def generate_prompt(sub_topic, next_sub_topic, content_pointers):
    prompt = f"Generate the content for the bullet point '{sub_topic}' without delving into '{next_sub_topic}'. Focus on the following content pointers:\n"
    for pointer in content_pointers:
        prompt += f"- {pointer}\n"
    return prompt

def generate_content_with_openai(prompt):
    # Adjust parameters as necessary for your use case
    response = llm.invoke(prompt, max_tokens=1024, temperature=0.5, stop=None)
    content_text = response.content if hasattr(response, 'content') else "Content not found"
    return content_text

def generate_article(course_outline):
    course_output = {"name": course_outline["name"], "topics": []}  # Initialize with course name and empty topics list
    total_sub_topics = sum(len(topic["sub-topics"]) for topic in course_outline["topics"])
    completed_sub_topics = 0

    for topic in course_outline["topics"]:
        topic_name = topic["topic"]
        new_topic = {"topic": topic_name, "sub-topics": []}  # Initialize a new topic dictionary

        for i, sub_topic in enumerate(topic["sub-topics"]):
            sub_topic_name = sub_topic["sub-topic"]
            content_pointers = sub_topic["content pointers"]
            next_sub_topic = topic["sub-topics"][i + 1]["sub-topic"] if i + 1 < len(topic["sub-topics"]) else "the next topic"

            # Generate prompt for each sub-topic
            prompt = generate_prompt(sub_topic_name, next_sub_topic, content_pointers)

            # Generate content based on prompt
            article_content = generate_content_with_openai(prompt)

            # Append generated content to the sub-topic
            new_sub_topic = {"sub-topic": sub_topic_name, "content": article_content}
            new_topic["sub-topics"].append(new_sub_topic)

            # Update progress
            completed_sub_topics += 1
            progress_percentage = (completed_sub_topics / total_sub_topics) * 100
            print(f"Completed: {completed_sub_topics}/{total_sub_topics} sub-topics. Progress: {progress_percentage:.2f}%")

        course_output["topics"].append(new_topic)

    return course_output

### MAIN ###
topic = "SQL"
filename = f"{topic}_output.json"

course_outline = generate_course_outline(topic)
print(course_outline)

course_outline_dict = json.loads(course_outline)
article = generate_article(course_outline_dict)

with open(filename, "w") as file:
    json.dump(article, file)
print(f"Article saved as {filename}")
