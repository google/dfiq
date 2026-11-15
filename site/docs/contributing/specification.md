# DFIQ Specification
**Version: 1.1.0**

## Introduction
The DFIQ (Digital Forensics Investigative Questions) Specification defines a standard, language-agnostic interface for
digital forensic investigations. This means that it can be used with any type of data, regardless of the tool or 
platform it is stored in. This allows both humans and machines to work together on digital forensic investigations. 
Machines can be used to automate tasks, such as data collection and processing, while humans can use their expertise 
to interpret the data and identify potential evidence. The DFIQ Specification also helps to ensure that digital 
forensic investigations are conducted in a consistent and reliable manner.

## Versions
The DFIQ Specification is versioned using a major.minor.patch scheme (semantic versioning). The `major.minor` portion
designates the feature set. Patch versions address errors or provide clarifications.

Tooling which supports version 1.1 SHOULD be compatible with all 1.1.* versions. The patch version SHOULD NOT be 
considered by tooling, making no distinction between 3.1.0 and 3.1.1 for example.

A DFIQ document must include a _dfiq_version_ field with the version.

## Format
A DFIQ document that conforms to the DFIQ Specification is represented in YAML.

## Identifiers
Every DFIQ component (`Scenario`, `Facet`, or `Question`) is canonically identified by a Universally Unique Identifier (`uuid`), which never changes throughout the object's lifecycle. UUIDs should be randomly generated (UUIDv4) by the tools used to create or process DFIQ objects.

Components may also include an optional human-readable `id` field:
```
 Q1024
 └──┼──── First character indicates type (Scenario, Facet, or Question)
    └──── 4-digit number, unique per type
```
The `id` field is optional and is only required when a component is merged into the official [DFIQ repository on GitHub](https://github.com/google/dfiq), which serves as the definitive central repository to manage public DFIQ IDs. To ensure backwards compatibility, existing DFIQ users may continue using internal IDs (where the 4-digit number starts with `0`), or use the optional `internal` boolean field to designate private components.

Components that link to parent objects via `parent_ids` may reference parents using either their `uuid` or their legacy DFIQ `id`.

## Schema
Below are the schemas for the different DFIQ components: [Scenario](#scenario), [Facet](#facet), and [Question](#question) (which contains [Approaches](#approach)). Each top-level DFIQ component (`Scenario`, `Facet`, `Question`) is typically saved as its own YAML file (example: `S1001.yaml`), while `Approaches` are defined inline within their parent `Question`.

If a field is not explicitly OPTIONAL, it can be considered REQUIRED.

### Scenario
A Scenario is the highest-level grouping in DFIQ. A Scenario is made of one or more [Facets](#facet) (different 
"sides" of an investigation), which in turn are made up of investigative [Questions](#question), or a Scenario may link directly to [Questions](#question) as its children.

| Field name     | Type       | Description                                                                              |
|----------------|------------|------------------------------------------------------------------------------------------|
| `name`         | `string`   | A human readable name for the scenario.                                                  |
| `description`  | `string`   | A description of the scenario. Markdown syntax MAY be used for rich text representation. |
| `dfiq_version` | `string`   | A semantic version format major.minor.patch scheme.                                      |
| `type`         | `string`   | Represents the type of DFIQ object. Should be `scenario` for scenarios.                  |
| `uuid`         | `string`   | A Universally Unique Identifier (UUIDv4) that uniquely identifies this component.        |
| `id`           | `string`   | Optional. Identifier using the format defined in [identifiers](#identifiers).            |
| `internal`     | `boolean`  | Optional. Whether the component is internal (private) or public.                         |
| `tags`         | `[string]` | Optional. List of tags.                                                                  |
| `contributors` | `[string]` | Optional. List of people who contributed to this component.                              |

Example ([source](https://github.com/google/dfiq/blob/main/dfiq/data/scenarios/S1001.yaml)):
```yaml
name: Data Exfiltration
type: scenario
description: >
  An employee is suspected of unauthorized copying of sensitive data (code, trade
  secrets, etc) from internal systems to those outside of the company's control.
uuid: aba6b02b-2ee7-49ab-9cbe-20b7259d4661
id: S1001
dfiq_version: 1.1.0
tags:
  - Insider
```

### Facet
Facets are used for optional intermediate-level grouping in DFIQ. A particular Facet can be part of multiple different
[Scenarios](#scenario) and will contain multiple [Questions](#question). A Facet breaks the larger Scenario into 
smaller logical pieces, but a Facet is still too broad to answer directly; it must also be broken down (into Questions).

| Field name     | Type       | Description                                                                                     |
|----------------|------------|-------------------------------------------------------------------------------------------------|
| `name`         | `string`   | A human readable name for the facet.                                                            |
| `description`  | `string`   | Optional. A description of the facet. Markdown syntax MAY be used for rich text representation. |
| `dfiq_version` | `string`   | A semantic version format major.minor.patch scheme.                                             |
| `type`         | `string`   | Represents the type of DFIQ object. Should be `facet` for facets.                               |
| `uuid`         | `string`   | A Universally Unique Identifier (UUIDv4) that uniquely identifies this component.               |
| `id`           | `string`   | Optional. Identifier using the format defined in [identifiers](#identifiers).                   |
| `internal`     | `boolean`  | Optional. Whether the component is internal (private) or public.                                |
| `tags`         | `[string]` | Optional. List of tags.                                                                         |
| `contributors` | `[string]` | Optional. List of people who contributed to this component.                                     |
| `parent_ids`   | `[string]` | List of DFIQ scenario UUIDs or IDs that this facet belongs to.                                  |

Example ([source](https://github.com/google/dfiq/blob/main/dfiq/data/facets/F1008.yaml)):
```yaml
name: Are there signs of staging data for future exfiltration?
type: facet
description: >
  "Staging" refers to the collection of data of interest onto a local system, as a
  precursor step for future exfiltration of that data. When reviewing data from Questions
  in this Facet, look for unusual volumes of results (number or size of files downloaded
  or sent, for example).
uuid: d95ef023-4246-41f5-b33b-73d924649986
id: F1008
dfiq_version: 1.1.0
tags:
  - TA0009
parent_ids:
  - S1001
```

### Question
Questions are the fundamental "building blocks" of DFIQ. All other DFIQ components are relative to Questions: 
[Approaches](#approach) describe how to answer the Questions, and [Scenarios](#scenario) and [Facets](#facet) organize
the Questions logically.  

A Question should be specific enough that it can be readily answered, and not easily divided into multiple parts (if it
can be, it likely should be multiple Questions). A single Question can be reused in multiple different Facets or Scenarios.

| Field name     | Type       | Description                                                                                        |
|----------------|------------|----------------------------------------------------------------------------------------------------|
| `name`         | `string`   | A human readable name for the question.                                                            |
| `description`  | `string`   | Optional. A description of the question. Markdown syntax MAY be used for rich text representation. |
| `dfiq_version` | `string`   | A semantic version format major.minor.patch scheme.                                                |
| `type`         | `string`   | Represents the type of DFIQ object. Should be `question` for questions.                            |
| `uuid`         | `string`   | A Universally Unique Identifier (UUIDv4) that uniquely identifies this component.                  |
| `id`           | `string`   | Optional. Identifier using the format defined in [identifiers](#identifiers).                      |
| `internal`     | `boolean`  | Optional. Whether the component is internal (private) or public.                                   |
| `tags`         | `[string]` | Optional. List of tags.                                                                            |
| `contributors` | `[string]` | Optional. List of people who contributed to this component.                                        |
| `parent_ids`   | `[string]` | List of DFIQ facet or scenario UUIDs or IDs that this question belongs to.                         |
| `approaches`   | `[Object]` | Optional. List of [Approach](#approach) objects describing how to answer this question.            |

Example ([source](https://github.com/google/dfiq/blob/main/dfiq/data/questions/Q1001.yaml)):
```yaml
name: What files were downloaded using a web browser?
type: question
description:
uuid: 8620a183-d67f-481e-a63c-d8b8dfa5e968
id: Q1001
dfiq_version: 1.1.0
tags:
parent_ids:
  - F1008
  - F1002
approaches:
  - name: Collect download records from local browser artifacts (Plaso)
    ...
```

### Approach

Approaches are detailed explanations of how to answer a [Question](#question) using a specific method, including the 
required data collection, processing, and analysis steps. As there is often more than one way to answer a question, there can be
multiple Approaches that answer a given Question using different techniques.

Approaches are tightly linked to their Question and are defined inline under the `approaches` field of a Question.

| Field name            | Type       | Description                                                                                                              |
|-----------------------|------------|--------------------------------------------------------------------------------------------------------------------------|
| `name`                | `string`   | A human readable name for the approach.                                                                                  |
| `description`         | `string`   | Optional. A description of the approach. Markdown syntax MAY be used for rich text representation.                       |
| `internal`            | `boolean`  | Optional. Whether the approach is internal (private) or public.                                                          |
| `tags`                | `[string]` | Optional. List of tags.                                                                                                  |
| `references`          | `[string]` | Optional. List of URLs of public references to this approach. Markdown syntax MAY be used for rich text representation.  |
| `references_internal` | `[string]` | Optional. List of URLs of private references to this approach. Markdown syntax MAY be used for rich text representation. |
| `notes`               | `Object`   | Optional. Coverage caveats for the approach. See the [Notes schema](#notes).                                             |
| `steps`               | `[Object]` | Ordered sequence of investigative steps (`collection`, `processing`, `analysis`). See the [Steps schema](#steps).        |

Example ([source](https://github.com/google/dfiq/blob/main/dfiq/data/questions/Q1001.yaml#L153-L205)):
```yaml
- name: Collect download records from local browser artifacts (Plaso)
  description: |-
    Parse download records from web browsers' own databases.

    Most web browsers track file downloads (at least in non-Incognito/private sessions)
    in local artifacts on the system. We can collect and review these records. This
    approach is useful when you have remote access to a system (via GRR for example)
    or a disk image.
  tags:
    - Web Browser
    - SQLite
    - Chrome
    - Safari
    - Edge
    - Plaso
  references:
    - '[Chrome](https://forensics.wiki/google_chrome/#downloadsstart_time), [Firefox](https://forensics.wiki/mozilla_firefox/#downloads),
      and [Safari](https://forensics.wiki/apple_safari/#downloads) downloads on ForensicsWiki'
    - '[Web Browsers on ForensicArtifacts](https://github.com/ForensicArtifacts/artifacts/blob/main/data/webbrowser.yaml)'
```

#### Notes
The approach often comes with certain caveats; these can often be tacit knowledge or assumed that "everyone
knows that". This can lead to incorrect assumptions and analysis. Explicitly stating them reduces ambiguity.

| Field name    | Type       | Description                                                                               |
|---------------|------------|-------------------------------------------------------------------------------------------|
| `covered`     | `[string]` | List of strings describing what this data is covering in the context of the approach.     |
| `not_covered` | `[string]` | List of strings describing what this data is NOT covering in the context of the approach. |

Example ([source](https://github.com/google/dfiq/blob/main/dfiq/data/questions/Q1001.yaml#L172-L183)):
```yaml
notes:
  covered:
    - Chrome downloads. Beyond "stable" Chrome, this also includes Chromium, Chrome
      Canary, Chrome Beta, and other Chromium-based browsers (Microsoft Edge, Brave,
      and Opera) on Windows, macOS, and Linux
    - Safari downloads
    - Includes downloads from all Chrome profiles
  not_covered:
    - Firefox downloads
    - Downloads on any other browsers
    - Browsers installed in non-standard paths
    - Downloads made during Incognito sessions
```

#### Steps
The `steps` list aims to be a concise, ordered representation of how to perform the investigative approach across three stages:
`collection`, `processing`, and `analysis`.

* `collection` steps describe the data that needs to be collected (for example, `type: ForensicArtifact` with `value: BrowserHistory`, corresponding to a [ForensicArtifact](https://github.com/ForensicArtifacts/artifacts) definition).
* `processing` steps describe the processor or tool used to transform raw collected data into structured data (for example, `type: command` with `value: Plaso`).
* `analysis` steps describe how to filter, query, or manipulate the processed data to answer the question (for example, `type: opensearch-query`, `type: splunk-query`, or `type: pandas`).

| Field name    | Type     | Description                                                                                        |
|---------------|----------|----------------------------------------------------------------------------------------------------|
| `name`        | `string` | Human readable summary of the step.                                                                |
| `description` | `string` | Optional. Detailed description or additional context for the step.                                 |
| `stage`       | `string` | The stage of the step: `collection`, `processing`, or `analysis`.                                  |
| `type`        | `string` | The type of the step (e.g. `ForensicArtifact`, `command`, `opensearch-query`, `pandas`).           |
| `value`       | `string` | The value of the step (e.g. `BrowserHistory`, `Plaso`, or an analysis query).                      |

Example ([source](https://github.com/google/dfiq/blob/main/dfiq/data/questions/Q1001.yaml#L184-L205)):
```yaml
steps:
  - name: Collect ForensicArtifact data
    description: Collect local browser history artifacts. These are often in the form
      of SQLite databases and JSON files in multiple directories.
    stage: collection
    type: ForensicArtifact
    value: BrowserHistory
  - name: Process data with Plaso
    description:
    stage: processing
    type: command
    value: Plaso
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

Python notebooks (Jupyter, Colab, etc) have become powerful tools for
security analysts. Recording the analysis steps in a way that would work
in a notebook makes the analysis more accessible and easier to demonstrate.

`type: pandas` refers to pandas [DataFrame](https://pandas.pydata.org/docs/reference/frame.html)
methods. They allow chaining, which is very powerful and flexible.
One would apply the operation in `value` by assuming the
data from the previous step was saved into a Pandas DataFrame (`df`),
then applying the operation to it. For example, the
`pandas` step in the example is equivalent to:
`df.query('data_type in ("chrome:history:file_downloaded", "safari:downloads:entry")')`.
