'''
This script tries to export all annotations from the probe.stad.gent SPARQL endpoint, get the corresponding labels from the stad.gent SPARQL endpoint and write them to a CSV file.

The idea is to use this CSV file as context when using an LLM to write queries for the probe.stad.gent SPARQL endpoint.
'''
from SPARQLWrapper import SPARQLWrapper, JSON
from tqdm import tqdm

def escape_commas(string):
    # Check if the string contains a comma
    if "," in string:
        # If so, wrap the string in double quotes
        return "\"" + string + "\""
    else:
        # Otherwise return the string as is
        return string

probe = SPARQLWrapper(
    "https://probe.stad.gent/sparql"
)
probe.setReturnFormat(JSON)

stadgent = SPARQLWrapper(
    "https://stad.gent/sparql"
)
stadgent.setReturnFormat(JSON)

# Create a way to store all used labels
URIs = []

# First we select a count, so we know how many results we have
probe.setQuery("""
    PREFIX oa: <http://www.w3.org/ns/oa#>

    SELECT (COUNT(?entity) AS ?count)
    WHERE {
        ?entity a oa:Annotation .
    }
    """
)

# Execute the query
ret = probe.queryAndConvert()

# Get the count
annotationCount = int(ret["results"]["bindings"][0]["count"]["value"])

print("Annotation count:", annotationCount)

# Start for loop based on the count
offset = 0

for i in tqdm(range(0, annotationCount, 100)):
    # Set the query to get the next batch
    probe.setQuery("""
        PREFIX oa: <http://www.w3.org/ns/oa#>

        SELECT ?body
        WHERE {
        ?entity a oa:Annotation ;
        oa:hasBody ?body .
        }
        ORDER BY ?entity

        LIMIT 10
        OFFSET """ + str(i))
    
    # Execute the query
    ret = probe.queryAndConvert()

    # Get the results
    results = ret["results"]["bindings"]

    # Loop over the results
    for result in results:
        # Get the body
        body = result["body"]["value"]

        # Add the body to the labels, if it's not already there
        if body not in URIs:
            URIs.append(body)

# Print the label count
print("URI count:", len(URIs))

# Create a way to store all used labels
labels = []

# Start for loop based on the count
offset = 0

for i in tqdm(range(0, len(URIs), 1)):
    # Set the query to get the next batch
    stadgent.setQuery("""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT DISTINCT ?prefLabel
        WHERE {
        <""" + URIs[i] + """> skos:prefLabel ?prefLabel .
        }
        """
    )
    
    # Execute the query
    ret = stadgent.queryAndConvert()

    # Get the results
    results = ret["results"]["bindings"]

    # Add the first result to the labels
    if len(results) > 0:
        labels.append(results[0]["prefLabel"]["value"])


# Print the label count
print("Label count:", len(labels))

# Write a file mapping all URIs to labels
with open("annotations.csv", "w") as file:
    for i in range(len(URIs)):
        file.write(URIs[i] + "," + escape_commas(labels[i]) + "\n")

