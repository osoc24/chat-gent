# Label Export

This tool attempts to read all annotations of the decisions in [PROBE](https://probe.stad.gent/sparql) and queries the human readable labels for them. These are then exported to a CSV file and a JSON file.

```mermaid
flowchart
1[Index all annotations from PROBE] -->
2{Check each label} --> |Doesn't exist in library| 4[Save label in dictionary] --> 5
2 --> |Exists in library| 3[Skip]
5[Query labels from SPARQL] --> 6[Save labels in dictionary] --> 7[Export to CSV and JSON]
```

## Data

A rough structure of how the labels are organized in SPARQL, while this is not the exact structure, it gives a good idea of how the data is organized, and how it can be queried.

```mermaid
erDiagram
    DECISION ||--o{ ANNOTATION : has
    ANNOTATION ||--|{ LABEL : has
    ANNOTATION }o--|{ CONCEPT : has
    LABEL }o--|| CONCEPT : has

    DECISION {
        string uri
        string title
        string hasAnnotation FK "Annotation"
    }

    ANNOTATION {
        string uri
        string hasLabel FK "Label"
        string hasBody FK "Concept"
        string hasTarget FK "Decision"
    }

    LABEL {
        string uri 
        string isTaxonomy FK "Concept"
    }

    CONCEPT {
        string uri
        string inScheme FK "Scheme this uses, e.g. ghent_words"
        string narrower FK "Narrower concept"
        string broader FK "Broader concept"
        string prefLabel "Human-readable label"
    }
```

## Usage

To run the tool, simply run the following command:

```bash
python label_export.py
```

Optionally, parameters can be passed to the script to specify a variety of options:

```bash
python label_export.py --help
```

All these parameters can also be set using environment variables or a `.env` file. The following environment variables are supported:

```env
PROBE_ENDPOINT=https://probe.stad.gent/sparql
STADGENT_ENDPOINT=https://stad.gent/sparql
ANNOTATIONS_CSV=annotations.csv
ANNOTATIONS_JSON=annotations.json
TEST_MODE=False
FETCH_CHILDREN=False
```

All these are also in the [`.env.example`](.env.example) file.

## Automation

This tool is run automatically every sunday at 03:00 AM. The tool will then query all annotations and labels from PROBE and export them to a CSV and JSON file, and push them to the repository.
