from openai import OpenAI
import json
import requests
import streamlit as st
import re
from datetime import date
import time

## OPENAI_API_KEY is defined in the secrets in StreamLit
openai_api_key = st.secrets['OPENAI_API_KEY']
endpoint_url = "https://probe.stad.gent/sparql"
today = date.today()

## uncomment to test out with local host
# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

with open('questions_and_queries.json', 'r', encoding='utf-8') as file:
    example_data = json.load(file)

with open('annotations.json', 'r', encoding='utf-8') as file:
    label_data = json.load(file)

def generate_sparql_query(user_question, label_data, examples_data):
    concepts_and_labels = "\n".join(
        f"URI of Label: {pair['uri']}\nLabel: {pair['label']}\n" for pair in label_data
    )
    example_queries = "\n".join(
        f"User Question: {pair['user_question']}\nSPARQL Query: {pair['sparql_query']}\n" for pair in examples_data
    )

    prompt = f"""

    GIVE ONLY THE QUERY AS AN ANSWER TO THE FOLLOWING PROMPT:

    The following are all the labels for the decisions in the decisions dataset and their URIs:

    {concepts_and_labels}

    Based on the user's question: {user_question}, go through all the labels then choose all possible labels that best matches the question's theme and context.

    NEXT STEP:

    The following are examples of user questions in Dutch and their corresponding SPARQL queries:

    {example_queries}

    Based on the examples above and the URIs of the chosen labels, generate a SPARQL query for the following user question:

    User Question: {user_question}
    SPARQL Query:

    But please make sure to use the URIs of the chosen labels in the "?annotation oa:hasBody" part of the query like in the examples. If there is more than one label chosen query for them using the same structure in the second example query in {example_queries}. This utilizes VALUES.
    
    If the user doesn't set a limit to the number of decisions they want to see, limit them to 3.

    Always choose the most recent decision (by ordering on publication date "eli:date_publication") unless prompted otherwise by the user.
    
    Don't add '`' as you wish.

    Then after filtering on label, add a filter for the title or description or motivering with keywords that you extract from the question. (NOTE: Do not use generic words that apply to all decisions about Gent, like 'Gent', as a keyword).

    """
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            #model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates SPARQL queries to be run on a SPARQL endpoint containing data about decisions of the city of Gent based on user questions and labels of decisions related to their questions. Your language is Dutch."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0
        )

    return response

def check_sparql_query(query):

    prompt = f"""
    If the query generated {query} contains looking for keywords, generate the same SPARQL query but remove the keywords filtering.
    Don't add '`' to the query as you wish.
    """
    response_2 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            #model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a SPARQL query refiner."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0
        )

    return response_2

def run_query(query):
        headers = {
            "Accept": "application/sparql-results+json"
        }
        params = {
            "query": query
        }

        response = requests.get(endpoint_url, headers=headers, params=params)
        results = None
        if response.status_code == 200:
            results = response.json()
            #print(f"Results for question '{user_question}':", results)
        else:
            #print(f"Failed to execute query for question '{user_question}':", response.status_code)
            return []
        
        if results is None:
            return []
        
        results_content = results['results']['bindings']

        cleaned_decisions = []

        for decision in results_content:
            cleaned_decision = {}
            for key, detail in decision.items():
                # Extract the value and remove any \n or extra spaces
                cleaned_value = re.sub(r'\s+', ' ', detail['value']).strip()
                cleaned_decision[key] = cleaned_value
            cleaned_decisions.append(cleaned_decision)

        return cleaned_decisions

st.title("💬 ChatGent")
st.caption("🚀 Vragen beantwoorden over besluiten van de stad Gent")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hoe kan ik u helpen?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Stel hier uw vraag..."):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    user_question = prompt

    with st.spinner('Generating response...'):
        sparql_query = generate_sparql_query(user_question, label_data=label_data, examples_data=example_data)
        print(sparql_query)
        query_content = sparql_query.choices[0].message.content
        prefix_position = query_content.find("PREFIX")
        if prefix_position != -1:
            query_content = query_content[prefix_position:]

        cleaned_decisions = run_query(query_content)
        print(cleaned_decisions)

        if not cleaned_decisions:
            sparql_query_2 = check_sparql_query(query_content)
            query_content_2 = sparql_query_2.choices[0].message.content
            prefix_position = query_content.find("PREFIX")
            if prefix_position != -1:
                query_content_2 = query_content_2[prefix_position:]

            print("SECOND SPARQL:", query_content_2)

            cleaned_decisions = run_query(query_content_2)
            print("AGAIN:", cleaned_decisions)
        
        resources = []
        resources_names = []

        # Print or use the cleaned_decisions as needed
        for d in cleaned_decisions:
            print(d)

        for d in cleaned_decisions:
            resources.append(d['derivedFrom'])
            resources_names.append(d['title'])

        prompt_2 = f"""
        ELEMENTS TO USE:
        1. User's question: {user_question}
        2. Data to use for answer: {cleaned_decisions}

        YOUR ROLE: 
        - You answer the user's question. However, chat normally if the user's prompt is not a question.
        - You answer in the language the user asked in. For example,if they ask in English, you answer in English, and if they ask in Dutch, you answer in Dutch.

        INSTRUCTIONS:
        - If it is a question, generate a response using ONLY the given data.
        - The date today is {today}. Answer with that in mind.
        - If you do not have data, the only external links you are allowed to refer to when looking for an answer are:
            - https://stad.gent
            - https://gentsefeesten.stad.gent
        - If the question is asking about a date of an event and the data provided is from the past, say you do not know.

        REQUIREMENTS YOU MUST FOLLOW:
        1. If the retrieved decisions' dates do not match the current date's year: {today}, you must tell the user that it's not recent.
        2. If you don't have an answer, you are only allowed to refer the user to https://stad.gent website.
        3. You are only allowed to use the provided data to compile the answer.
        4. Use the word "besluiten" when referring to decisions in the Dutch language. Don't use "beslissingen".
        5. Be friendly and use plain language, avoiding bureaucratic terms.

        LAST IMPORTANT STEPS YOU MUST FOLLOW: Before showing your answer, ensure it matches the user's question:
        - If it relates but doesn't answer exactly, mention: "It might relate but isn't necessarily the answer you want."
        - Provide the resources in bullet points: {resources}, formatted with the {resources_names} as links ({resources}).
        
        """
        
        completion_2 = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for the citizens of Gent when they ask a question on the city's website regarding the decisions made by the city."},
            {"role": "user", "content": prompt_2}
        ],
        temperature=0
        )
        
        # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg_2 = completion_2.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg_2})
        st.chat_message("assistant").write(msg_2)

# Clear context button
if st.button("Clear Context"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
