'''
This script tries to export all annotations from the probe.stad.gent SPARQL endpoint, get the corresponding labels from the stad.gent SPARQL endpoint and write them to a CSV file.

The idea is to use this CSV file as context when using an LLM to write queries for the probe.stad.gent SPARQL endpoint.
'''
from SPARQLWrapper import SPARQLWrapper, JSON
from tqdm import tqdm
import json

# Config variables

# SparQL endpoint for the probe.stad.gent SPARQL endpoint
probe_endpoint = "https://probe.stad.gent/sparql"
# SparQL endpoint for the stad.gent SPARQL endpoint
stadgent_endpoint = "https://stad.gent/sparql"
# The file to write the annotations to in CSV format, set to false to disable
annotations_csv = "annotations.csv"
# The file to write the annotations to in JSON format, set to false to disable
annotations_json = "annotations.json"
# Whether to run this in test mode, AKA only get the first batch of annotations
test_mode = False

def escape_commas(string):
    # Check if the string contains a comma
    if "," in string:
        # If so, wrap the string in double quotes
        return "\"" + string + "\""
    else:
        # Otherwise return the string as is
        return string

def export_json(uri_label_dict):
    # First we change the structure from URI: Label to something more JSON-like
    # [ { "URI": URI, "Label": Label }, ... ]
    json_data = []
    for i in range(len(uri_label_dict.values())):
        json_data.append({ "uri": list(uri_label_dict.keys())[i], "label": list(uri_label_dict.values())[i] })

    return json_data

# Create a SPARQLWrapper object for the probe endpoint
probe = SPARQLWrapper(
    probe_endpoint
)
probe.setReturnFormat(JSON)

# Create a SPARQLWrapper object for the stadgent endpoint
stadgent = SPARQLWrapper(
    stadgent_endpoint
)
stadgent.setReturnFormat(JSON)

# Create a dictionary to store all URIs
URIs = {}

if test_mode:
    annotationCount = 100
else:
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

# Check if we need to write the annotations to a CSV file
if annotations_csv:
    print("Writing annotations to CSV file")
    # Write a file mapping all URIs to labels
    with open("annotations.csv", "w") as file:
        for i in range(len(URIs.values())):
            file.write(list(URIs.keys())[i] + "," + escape_commas(list(URIs.values())[i]) + "\n")

if annotations_json:
    print("Writing annotations to JSON file")
    # Also write a file mapping all URIs to labels in JSON format
    json_data = export_json(URIs)

    # Write the JSON data to a file
    with open("annotations.json", "w") as file:
        json.dump(json_data, file)

# Output the JSON to the console if we're not writing it to any file
if not annotations_csv and not annotations_json:
    print(json.dumps(export_json(URIs), indent=4))