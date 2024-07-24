'''
This script tries to export all annotations from the probe.stad.gent SPARQL endpoint, get the corresponding labels from the stad.gent SPARQL endpoint and write them to a CSV file.

The idea is to use this CSV file as context when using an LLM to write queries for the probe.stad.gent SPARQL endpoint.
'''
import os
from SPARQLWrapper import SPARQLWrapper, JSON
from tqdm import tqdm
import json
from dotenv import load_dotenv
import argparse

# Config variables

# Load in environment variables
load_dotenv()

# Load in command line arguments
arg_parser = argparse.ArgumentParser(description="Export annotations from the probe.stad.gent SPARQL endpoint and get the corresponding labels from the stad.gent SPARQL endpoint")
arg_parser.add_argument("--probe-endpoint", help="The SPARQL endpoint for the probe.stad.gent SPARQL endpoint")
arg_parser.add_argument("--stadgent-endpoint", help="The SPARQL endpoint for the stad.gent SPARQL endpoint")
arg_parser.add_argument("--annotations-csv", help="The file to write the annotations to in CSV format, set to false to disable")
arg_parser.add_argument("--annotations-json", help="The file to write the annotations to in JSON format, set to false to disable")
arg_parser.add_argument("--test-mode", help="Whether to run this in test mode, AKA only get the first batch of annotations")
arg_parser.add_argument("--fetch-children", help="Optionally, all narrowers of the concepts can also be retrieved, only works if at least annotations_json is enabled, or if the output is not written to a file")
args = arg_parser.parse_args()

# Set the config variables, first looking for a command line argument, then for an environment variable, then for a default value
# SparQL endpoint for the probe.stad.gent SPARQL endpoint
probe_endpoint = args.probe_endpoint if args.probe_endpoint else os.getenv("PROBE_ENDPOINT", "https://probe.stad.gent/sparql")
# SparQL endpoint for the stad.gent SPARQL endpoint
stadgent_endpoint = args.stadgent_endpoint if args.stadgent_endpoint else os.getenv("STADGENT_ENDPOINT", "https://stad.gent/sparql")
# The file to write the annotations to in CSV format, set to false to disable
annotations_csv = args.annotations_csv if args.annotations_csv else os.getenv("ANNOTATIONS_CSV", "annotations.csv")
# The file to write the annotations to in JSON format, set to false to disable
annotations_json = args.annotations_json if args.annotations_json else os.getenv("ANNOTATIONS_JSON", "annotations.json")
# Whether to run this in test mode, AKA only get the first batch of annotations
test_mode = args.test_mode if args.test_mode else os.getenv("TEST_MODE", False)
# Optionally, all narrowers of the concepts can also be retrieved, only works if at least annotations_json is enabled, or if the output is not written to a file
fetch_children = args.fetch_children if args.fetch_children else os.getenv("FETCH_CHILDREN", True)

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
        if fetch_children:
            json_data.append({ "uri": list(uri_label_dict.keys())[i], "label": list(uri_label_dict.values())[i], "children": [] })
        else:
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
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT (COUNT(DISTINCT ?body) AS ?bodyCount)
        WHERE {
            ?entity rdf:type oa:Annotation ;
                    oa:hasBody ?body .
        }
        """
    )

    # Execute the query
    ret = probe.queryAndConvert()

    # Get the count
    annotationCount = int(ret["results"]["bindings"][0]["bodyCount"]["value"])

print("Annotation count:", annotationCount)

# Start for loop based on the count
offset = 0

for i in tqdm(range(0, annotationCount, 100)):
    # Set the query to get the next batch
    probe.setQuery("""
        PREFIX oa: <http://www.w3.org/ns/oa#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT DISTINCT ?body
        WHERE {
            ?entity rdf:type oa:Annotation ;
                oa:hasBody ?body .
        }
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

# Order the dictionary by URI (alphabetically)
URIs = dict(sorted(URIs.items()))

if annotations_json or not annotations_csv:
    # Already remap all data to a JSON-like structure
    json_data = export_json(URIs)

# Check if we also need to fetch the children
if fetch_children and (annotations_json or not annotations_csv):
    stadgent.setQuery("""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT *
        WHERE {
            <http://stad.gent/id/concepts/decision_making_themes/concept_20> skos:narrower+ ?id .
            ?id skos:prefLabel ?label ;
                skos:broader ?parent .
        }
    """)

    ret = stadgent.queryAndConvert()

    results = ret["results"]["bindings"]

    # Now we need to place all children in the correct place in `json_data` (aka under the item children from their parent, which in some cases might not exist yet)
    for result in results:
        # Get the ID and label
        id = result["id"]["value"]
        label = result["label"]["value"]
        parent = result["parent"]["value"]

        # Check if the parent already exists in the JSON data
        parent_index = -1
        for i in range(len(json_data)):
            if json_data[i]["uri"] == parent:
                parent_index = i
                break
        
        # If the parent doesn't exist, we need to add it
        if parent_index == -1:
            # Add the parent to the JSON data
            json_data.append({ "uri": parent, "label": URIs[parent], "children": [] })
            parent_index = len(json_data) - 1
        
        # Add the child to the parent
        json_data[parent_index]["children"].append({ "uri": id, "label": label })

# Check if we need to write the annotations to a CSV file
if annotations_csv:
    print("Writing annotations to CSV file")
    # Write a file mapping all URIs to labels
    with open("annotations.csv", "w") as file:
        for i in range(len(URIs.values())):
            file.write(list(URIs.keys())[i] + "," + escape_commas(list(URIs.values())[i]) + "\n")

if annotations_json:
    print("Writing annotations to JSON file")

    # Write the JSON data to a file
    with open("annotations.json", "w") as file:
        json.dump(json_data, file, indent=4)

# Output the JSON to the console if we're not writing it to any file
if not annotations_csv and not annotations_json:
    print(json.dumps(json_data, indent=4))