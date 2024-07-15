'''
This script tries to export all annotations from the probe.stad.gent SPARQL endpoint, get the corresponding labels from the stad.gent SPARQL endpoint and write them to a CSV file.

The idea is to use this CSV file as context when using an LLM to write queries for the probe.stad.gent SPARQL endpoint.
'''
from SPARQLWrapper import SPARQLWrapper, JSON
from tqdm import tqdm
import json

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

# Create a dictionary to store all URIs
URIs = {}

# First we select a count, so we know how many results we have
probe.setQuery("""
    PREFIX oa: <http://www.w3.org/ns/oa#>

    SELECT (COUNT(?entity) AS ?count)
    WHERE {
        ?entity a oa:Annotation ;
        oa:hasBody ?body .
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

        SELECT ?body ?entity
        WHERE {
        ?entity a oa:Annotation ;
        oa:hasBody ?body .
        }
        ORDER BY ?entity

        LIMIT 100
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
            URIs[body] = True
    
    # Increase the offset
    offset += 100

# Print the label count
print("URI count:", len(URIs))

# Start for loop based on the count
offset = 0

for i in tqdm(range(0, len(URIs.keys()), 1)):
    # Set the query to get the next batch
    stadgent.setQuery("""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT DISTINCT ?prefLabel
        WHERE {
        <""" + list(URIs.keys())[i] + """> skos:prefLabel ?prefLabel .
        }
        """
    )
    
    # Execute the query
    ret = stadgent.queryAndConvert()

    # Get the results
    results = ret["results"]["bindings"]

    # Add the first result to the labels
    if len(results) > 0:
        URIs[list(URIs.keys())[i]] = results[0]["prefLabel"]["value"]
    
    # Increase the offset
    offset += 1

# Write a file mapping all URIs to labels
with open("annotations.csv", "w") as file:
    for i in range(len(URIs.values())):
        file.write(list(URIs.keys())[i] + "," + escape_commas(list(URIs.values())[i]) + "\n")


# Also write a file mapping all URIs to labels in JSON format
# First we change the structure from URI: Label to something more JSON-like
# [ { "URI": URI, "Label": Label }, ... ]
json_data = []
for i in range(len(URIs.values())):
    json_data.append({ "uri": list(URIs.keys())[i], "label": list(URIs.values())[i] })

# Write the JSON data to a file
with open("annotations.json", "w") as file:
    json.dump(json_data, file)