# Code Development - Jupyter & SPARQL Notebooks

This folder contains various notebooks as follows:

- [Main Solution](concepts_based_solution.ipynb): This is the pipeline for the developed solution, starting from generating a query based on the user's question, to compiling the final answer using the retrieved decisions from that query.
- [Question Example Selector](./question_example_selector.ipynb): Code to utilize example selectors by LangChain in the pipeline. Ideally, in the case where a large dataset of example user questions and corresponding SPARQL queries is generated, this tool would effectively match the user’s question to an existing example question and use its SPARQL query. As a result, better quality answers can be generated.
- [SPARQL notebook](./labels_querying.sparqlbook): This notebook was used to test out different queries which were later on used when making the example questions & queries json file.
- [Label Narrowing](./label_narrowing.ipynb): This was a test for extending the label export script to also include all children of a label. All off it's functionality is included in the label export script now.
