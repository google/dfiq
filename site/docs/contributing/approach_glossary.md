# Approach Glossary

DFIQ's Approaches contain the important "how" to answer the Questions. Approaches are also the most complicated
part of DFIQ, due to the amount of structured information they contain. DFIQ has a detailed
[specification](https://dfiq.org/contributing/specification) that is a useful reference for
creating new Approaches. However, some parts of Approaches need user-defined values that are beyond the specification.
This page is a glossary of currently-used values, generated from the
[DFIQ YAML files](https://github.com/google/dfiq/tree/main/dfiq/data).

When writing new Approaches, check this glossary first to see if there's already an existing term that fits with what
you're trying to do. If not, you are free to create a new one, but trying to reuse existing terms first will increase
consistency throughout DFIQ. These concepts (collection, processing, and analysis steps) also may not be straight-forward at
first; the hope is that seeing some common values (and the linked usages) will help make them more clear.

## Collection Steps

Steps with `stage: collection` describe the data needed for an approach. Each step is specified with `name`, `description` (optional), `stage: collection`, `type`, and `value`.

Example (from [Q1001](https://github.com/google/dfiq/blob/main/dfiq/data/questions/Q1001.yaml#L185-L190)):

```yaml
steps:
  - name: Collect ForensicArtifact data
    description: Collect local browser history artifacts. These are often in the form
      of SQLite databases and JSON files in multiple directories.
    stage: collection
    type: ForensicArtifact
    value: BrowserHistory
```

Below are the current values of `type` for `stage: collection` steps, along with the `value`s set for each.


#### CrowdStrike

For `type: CrowdStrike`, current entries for `value`:

- DnsRequest
- PlatformEvents
- ProcessRollup

#### ForensicArtifact
**Description**: This corresponds to the name of a ForensicArtifact, an existing repository of machine-readable digital forensic artifacts (https://github.com/ForensicArtifacts/artifacts). Using this type is preferred when the data is a host-based file/artifact, but other methods are available as well (if there isn't an existing relevant ForensicArtifact).

For `type: ForensicArtifact`, current entries for `value`:

- BrowserHistory
- NTFSUSNJournal
- SantaLogs
- WindowsEventLogs
- WindowsPrefetchFiles
- WindowsXMLEventLogSysmon


## Processing Steps

A processor (`stage: processing`) takes the collected data and processes it in some way to produce structured data an investigator
reviews (for example: Plaso, Hindsight, or Splunk).

Example (from [Q1001](https://github.com/google/dfiq/blob/main/dfiq/data/questions/Q1001.yaml#L191-L195)):

```yaml
steps:
  - name: Process data with Plaso
    description:
    stage: processing
    type: command
    value: Plaso
```

Below are the currently-defined processing step types and values:

#### `type: command`

- Crowdstrike Investigate (UI) [🔎](https://github.com/google/dfiq/search?q="value:%20Crowdstrike%20Investigate%20%28UI%29"+language%3AYAML)
- Hindsight [🔎](https://github.com/google/dfiq/search?q="value:%20Hindsight"+language%3AYAML)
- Plaso [🔎](https://github.com/google/dfiq/search?q="value:%20Plaso"+language%3AYAML)
- Splunk [🔎](https://github.com/google/dfiq/search?q="value:%20Splunk"+language%3AYAML)

## Analysis Steps

Steps with `stage: analysis` describe how to refine, filter, or query the processed data to answer the Question.
If there are multiple analysis steps, they describe the sequence or alternative analysis queries (such as OpenSearch queries, Splunk queries, or Pandas expressions) used to analyze the data.

Example (from [Q1001](https://github.com/google/dfiq/blob/main/dfiq/data/questions/Q1001.yaml#L196-L205)):

```yaml
steps:
  - name: Filter the results to just file downloads
    description:
    stage: analysis
    type: opensearch-query
    value: data_type:("chrome:history:file_downloaded" OR "safari:downloads:entry")
  - name: Filter the results to just file downloads
    description:
    stage: analysis
    type: pandas
    value: query('data_type in ("chrome:history:file_downloaded", "safari:downloads:entry")')
```

#### `type`

The contents of the `name`, `description`, and `value` fields will vary depending on what the
analysis step is doing, but the step `type` should be one of a few common values.

Below are the currently-defined values of `type` for `stage: analysis` steps:

- GUI [🔎](https://github.com/google/dfiq/search?q="type:%20GUI"+language%3AYAML)
- manual [🔎](https://github.com/google/dfiq/search?q="type:%20manual"+language%3AYAML)
- opensearch-query [🔎](https://github.com/google/dfiq/search?q="type:%20opensearch-query"+language%3AYAML)
- pandas [🔎](https://github.com/google/dfiq/search?q="type:%20pandas"+language%3AYAML)
- splunk-query [🔎](https://github.com/google/dfiq/search?q="type:%20splunk-query"+language%3AYAML)

#### Variable Substitution in step `value`

The step's `value` may benefit from using a specific term to make the step more precise. Common examples of this
include adding time bounds and filtering down to a specific identifier (user name, host, FQDN, or PID, for example).

DFIQ's convention for denoting a variable to be substituted when used is to wrap the term in **{ }**.

==More standardization is needed here to define common variables (such as timestamps in a particular format).==

Below are the currently-used variables in steps:

- {file_reference value} [🔎](https://github.com/google/dfiq/search?q="%7Bfile_reference%20value%7D"+language%3AYAML)
- {hostname} [🔎](https://github.com/google/dfiq/search?q="%7Bhostname%7D"+language%3AYAML)
