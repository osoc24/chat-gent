from openai import OpenAI
import json
import requests
import streamlit as st
import re

# openai_api_key = st.secrets['OPENAI_API_KEY']
endpoint_url = "https://probe.stad.gent/sparql"

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

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
    The following are all the labels for the decisions in the decisions dataset and their URIs:

    {concepts_and_labels}

    Based on the user's question: {user_question}, go through all the labels then choose at least 1 label that best matches the question's theme and context. 

    Get the URIs of the chosen label(s), these will be used in the next step.

    NEXT STEP:

    The following are examples of user questions in Dutch and their corresponding SPARQL queries:

    {example_queries}

    Use these examples only, and only, to know how to structure the SPARQL query.

    Based on the examples' structure above and the URIs of the chosen labels, generate a SPARQL query for the following user question:

    User Question: {user_question}
    SPARQL Query:

    But please make sure to use the URIs of the chosen labels in the "?annotation oa:hasBody" part of the query like in the examples. 
    
    If there is more than one URI, you can separate them with a comma. 
    
    Make sure to not include any extra spaces or '\n' characters in the query.

    Give only the query as the answer.
    """
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates SPARQL queries to be run on a SPARQL endpoint containing data about decisions of the city of Gent based on user questions and labels of decisions related to their questions. Your language is Dutch."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0
        )

    return response

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    user_question = prompt

    sparql_query = generate_sparql_query(user_question, label_data=label_data, examples_data=example_data)
    query_content = sparql_query.choices[0].message.content
    query_content_no_newlines = query_content.replace("\n", " ")

    print(sparql_query)

    headers = {
        "Accept": "application/sparql-results+json"
    }
    params = {
        "query": query_content_no_newlines
    }

    response = requests.get(endpoint_url, headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()
        print(f"Results for question '{user_question}':", results)
    else:
        print(f"Failed to execute query for question '{user_question}':", response.status_code)
    
    results_content = results['results']['bindings']

    cleaned_decisions = []

    for decision in results_content:
        cleaned_decision = {}
        for key, detail in decision.items():
            # Extract the value and remove any \n or extra spaces
            cleaned_value = re.sub(r'\s+', ' ', detail['value']).strip()
            cleaned_decision[key] = cleaned_value
        cleaned_decisions.append(cleaned_decision)

    # Print or use the cleaned_decisions as needed
    for d in cleaned_decisions:
        print(d)

    prompt_2 = f"""
    The following is the question the user asked:

    {user_question}

    Based on the following data only, generate a response that answers their question, don't hallucinate:

    Data: {cleaned_decisions}
    Answer in the language the user asked in. Be sure to be friendly and explain in a way an ordinary person can understand. The language city officials use is often very different from the language citizens use (officials wind up speaking in departments and form numbers instead of needs in big organizations).

    Show resources, meaning the source pages of the decisions which you used to compile your response. These resources are the links from the derivedFrom property of the decision.
    """

    completion_2 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant for the citizens of Gent when they ask a question on the city's website regarding the decisions made by the city. Be friendly, speak in easy to use terms. You use both the user's question and relevant decisions passed to you."},
        {"role": "user", "content": prompt_2}
    ],
    temperature=0
    )
    
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = completion_2.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)