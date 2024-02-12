# Approach Glossary

DFIQ's Approaches contain the important "how" to answer the Questions. Approaches are also the most complicated
part of DFIQ, due to the amount of structured information they contain. DFIQ has a detailed
[specification](https://dfiq.org/contributing/specification) that is a useful reference for
creating new Approaches. However, some parts of Approaches need user-defined values that are beyond the specification.
This page is a glossary of currently-used values, generated from the
[DFIQ YAML files](https://github.com/google/dfiq/tree/main/data).

When writing new Approaches, check this glossary first to see if there's already an existing term that fits with what
you're trying to do. If not, you are free to create a new one, but trying to reuse existing terms first will increase
consistency throughout DFIQ. These concepts (data type, processors, analysis steps) also may not be straight-forward at
first; the hope is that seeing some common values (and the linked usages) will help make them more clear.

## Data

This section (`view.data`) can have multiple ways describing the data needed for this approach. They should be thought
of as complementary or as alternates to each other (they can be "OR"d together, they do not need to be "AND"d).
Each is specified by a pair of `type` and `value`.

Example (from [Q1001.10](https://github.com/google/dfiq/blob/main/data/approaches/Q1001.10.yaml#L39)):

```
view:
  data:
    - type: ForensicArtifact
      value: BrowserHistory
```

Below are the current values of `type`, along with the `value`s set for each.


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

#### description
**Description**: Text description of the data type. `description` is often using in conjunction with another data type to provide more context. It can also be used alone, either as a placeholder or when more robust, programmatic data types do not fit.

For `type: description`, current entries for `value`:

- Collect local browser history artifacts. These are often in the form of SQLite databases and JSON files in multiple directories.
- Files used by the Windows Prefetch service.
- Santa logs stored on the local disk; they may also be centralized off-system, but this artifact does not include those.
- The NTFS $UsnJnrl file system metadata file. This ForensicArtifact definition does not include the $J alternate data stream, but many tools collect it anyway.
- Windows Event Log files


## Processors

A processor is what takes the data collected and processes it in some way to produce structured data an investigator
reviews. Multiple processors can be defined, as there are often multiple programs capable of doing similar processing
(example: log2timeline, Magnet Axiom, and Hindsight can all process browser history artifacts and deliver similar
results).

Example (from [Q1001.10](https://github.com/google/dfiq/blob/main/data/approaches/Q1001.10.yaml#L58)):

```
  processors:
    - name: Plaso
```

Below are the currently-defined processors:

- Crowdstrike Investigate (UI) [🔎](https://github.com/google/dfiq/search?q="name:%20Crowdstrike%20Investigate%20%28UI%29"+language%3AYAML)
- Hindsight [🔎](https://github.com/google/dfiq/search?q="name:%20Hindsight"+language%3AYAML)
- Plaso [🔎](https://github.com/google/dfiq/search?q="name:%20Plaso"+language%3AYAML)
- Splunk [🔎](https://github.com/google/dfiq/search?q="name:%20Splunk"+language%3AYAML)

## Analysis Steps

Under each analysis method will be a sequence of one or more maps with keys `description`, `type`, and `value`.
If there is more than one map, they should be processed in sequence in the analysis method (if applicable). In this
way, we can describe multiple chained steps of analysis (with the `description` being a way to communicate to the user
what exactly each "step" is doing, enabling a "show-your-work"-type capability).

Example (from [Q1001.10](https://github.com/google/dfiq/blob/main/data/approaches/Q1001.10.yaml#L63)):

```
      analysis:
        - name: OpenSearch
          steps:
            - description: &filter-desc Filter the results to just file downloads
              type: opensearch-query
              value: data_type:("chrome:history:file_downloaded" OR "safari:downloads:entry")
        - name: Python Notebook
          steps:
            - description: *filter-desc
              type: pandas
              value: query('data_type in ("chrome:history:file_downloaded", "safari:downloads:entry")')
```

#### `type`

The contents of the `description` and `value` fields will vary wildly with little repetition, depending on what the
analysis step is doing, but the step `type` should be one of a few common values.

Below are the currently-defined values of `type`:

- GUI [🔎](https://github.com/google/dfiq/search?q="type:%20GUI"+language%3AYAML)
- manual [🔎](https://github.com/google/dfiq/search?q="type:%20manual"+language%3AYAML)
- opensearch-query [🔎](https://github.com/google/dfiq/search?q="type:%20opensearch-query"+language%3AYAML)
- pandas [🔎](https://github.com/google/dfiq/search?q="type:%20pandas"+language%3AYAML)
- splunk-query [🔎](https://github.com/google/dfiq/search?q="type:%20splunk-query"+language%3AYAML)

#### Variable Substitution in step `value`

The step's `value` may benefit from some using a specific term to make the step more precise. Common examples of this
include adding time bounds and filtering down to a specific identifier (user name, host, FQDN, or PID, for example).

DFIQ's convention for denoting a variable to be substituted when used is to wrap the term in **{ }**.

==More standardization is needed here to define common variables (such as timestamps in a particular format).==

Below are the currently-used variables in analysis steps:

- {file_reference value} [🔎](https://github.com/google/dfiq/search?q="%7Bfile_reference%20value%7D"+language%3AYAML)
- {hostname} [🔎](https://github.com/google/dfiq/search?q="%7Bhostname%7D"+language%3AYAML)
