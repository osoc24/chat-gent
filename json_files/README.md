# Json files
This directory includes the json files used in the workflow:
- questions_and_queries.json: Example user questions and their corresponding queries to be used as context by the LLM when generating a SparQL query based on the user's question.
- annotations.json: Annotations of decisions. This file contains all the labels used and their URIs. There was another file made with each label's child labels but it wasn't tested out. It could potentially lead to improvements in query generation.
