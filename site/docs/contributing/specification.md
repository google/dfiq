# DFIQ Specification
**Version: 1.0.0**

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
```
 Q1024.12
 └──┼───┼── First character indicates type (Scenario, Facet, or Question)
    └───┼── 4-digit number*, unique per type 
        └── [optional] 2-digit number* indicates this is an Approach, 
            specific to the Question
```
Both the 4- and 2-digit numbers start with a 1 (or higher) for components appropriate for external use. Numbers 
starting with a 0 are reserved for internal use (think of it like private IP address space). Users of DFIQ can use 
these IDs for their internal components without worrying about collisions with public components. 
[DFIQ on GitHub](https://github.com/google/dfiq) will serve as the definitive central repository to manage
public DFIQ components (and their IDs).

## Schema
Below are the schemas for the different DFIQ components: [Scenario](#scenario), [Facet](#facet), [Question](#question),
and [Approach](#approach). Each DFIQ component is typically saved as its own YAML file, named after its DFIQ ID 
(example: `S1001.yaml`).

If a field is not explicitly OPTIONAL, it can be considered REQUIRED.

### Scenario
A Scenario is the highest-level grouping in DFIQ. A Scenario is made of one or more [Facets](#facet) (different 
"sides" of an investigation), which in turn are made up of investigative [Questions](#question).

| Field name     | Type       | Description                                                                              |
|----------------|------------|------------------------------------------------------------------------------------------|
| `display_name` | `string`   | A human readable name for the scenario.                                                  |
| `description`  | `string`   | A description of the scenario. Markdown syntax MAY be used for rich text representation. |
| `dfiq_version` | `string`   | A semantic version format major.minor.patch scheme.                                      |
| `type`         | `string`   | Represent the type of DFIQ object. Should be `scenario` for scenarios.                   |
| `id`           | `string`   | Identifier using the format defined in [identifiers](#identifiers).                      |
| `tags`         | `[string]` | Optional. List of tags.                                                                  |
| `contributors` | `[Object]` | Optional. List of people who contributed to this component.                              |

Example ([source](https://github.com/google/dfiq/blob/main/data/scenarios/S1001.yaml)):
```yaml
display_name: Data Exfiltration
type: scenario
description: >
  An employee is suspected of unauthorized copying of sensitive data (code,
  trade secrets, etc) from internal systems to those outside of the company's
  control.
id: S1001
dfiq_version: 1.0.0
tags:
  - Insider
```

### Facet
Facets are used for intermediate-level grouping in DFIQ. A particular Facet can be part of multiple different
[Scenarios](#scenario) and will contain multiple [Questions](#question). A Facet breaks the larger Scenario into 
smaller logical pieces, but a Facet is still too broad to answer directly; it must also be broken down (into Questions).

| Field name     | Type       | Description                                                                                     |
|----------------|------------|-------------------------------------------------------------------------------------------------|
| `display_name` | `string`   | A human readable name for the facet.                                                            |
| `description`  | `string`   | Optional. A description of the facet. Markdown syntax MAY be used for rich text representation. |
| `dfiq_version` | `string`   | A semantic version format major.minor.patch scheme.                                             |
| `type`         | `string`   | Represent the type of DFIQ object. Should be `facet` for facets.                                |
| `id`           | `string`   | Identifier using the format defined in [identifiers](#identifiers).                             |
| `tags`         | `[string]` | Optional. List of tags.                                                                         |
| `contributors` | `[string]` | Optional. List of people who contributed to this component.                                     |
| `parent_ids`   | `[string]` | List of DFIQ scenario IDs that this facet belongs to.                                           |

Example ([source](https://github.com/google/dfiq/blob/main/data/facets/F1008.yaml)):
```yaml
display_name: Are there signs of staging data for future exfiltration?
type: facet
description: >
  "Staging" refers to the collection of data of interest onto a local system,
  as a precursor step for future exfiltration of that data. When reviewing
  data from Questions in this Facet, look for unusual volumes of results
  (number or size of files downloaded or sent, for example).
id: F1008
dfiq_version: 1.0.0
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
can be, it likely should be multiple Questions). A single Question can be reused in multiple different Facets.

| Field name     | Type       | Description                                                                                        |
|----------------|------------|----------------------------------------------------------------------------------------------------|
| `display_name` | `string`   | A human readable name for the question.                                                            |
| `description`  | `string`   | Optional. A description of the question. Markdown syntax MAY be used for rich text representation. |
| `dfiq_version` | `string`   | A semantic version format major.minor.patch scheme.                                                |
| `type`         | `string`   | Represent the type of DFIQ object. Should be `question` for questions.                             |
| `id`           | `string`   | Identifier using the format defined in [identifiers](#identifiers).                                |
| `tags`         | `[string]` | Optional. List of tags.                                                                            |
| `contributors` | `[string]` | Optional. List of people who contributed to this component.                                        |
| `parent_ids`   | `[string]` | List of DFIQ facet IDs that this question belongs to.                                              |

Example ([source](https://github.com/google/dfiq/blob/main/data/questions/Q1001.yaml)):
```yaml
display_name: What files were downloaded using a web browser?
type: question
description: Downloading files via a web browser is a common way to introduce
  files to a computer. Determining what files were downloaded can be helpful 
  in variety of scenarios, ranging from malware investigations to insider cases. 
id: Q1001
dfiq_version: 1.0.0
tags:
 - Web Browser
parent_ids:
 - F1008
 - F1002
```

### Approach

Approaches are detailed explanations of how to answer a [Question](#question) using a specific method, including the 
required data, processing, and analysis steps. As there is often more than one way to answer a question, there can be
multiple Approaches that answer a given Question using different techniques. 

Approaches are tightly linked to their Question. Whereas a Question can be a part of multiple Facets, and a Facet can
be part of multiple Scenario, an Approach can only apply to a single specific Question.

| Field name     | Type       | Description                                                                                                                                                                                                            |
|----------------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `display_name` | `string`   | A human readable name for the approach.                                                                                                                                                                                |
| `description`  | `Object`   | See Approach Description schema.                                                                                                                                                                                       |
| `type`         | `string`   | Represent the type of DFIQ object. Should be `approach` for approaches.                                                                                                                                                |
| `dfiq_version` | `string`   | A semantic version format major.minor.patch scheme.                                                                                                                                                                    |
| `id`           | `string`   | Identifier using the format defined in [identifiers](#identifiers). An Approach identifier will share the first five characters with the Question it relates to, and end with a two-digit suffix. Example: `Q1024.12`. |
| `tags`         | `[string]` | Optional. List of tags.                                                                                                                                                                                                |
| `contributors` | `[string]` | Optional. List of people who contributed to this component.                                                                                                                                                            |
| `view`         | `Object`   | The view aims to be a concise representation of how to perform this investigative approach. See the [View schema](#view).                                                                                              |

#### Description 
The `description` is a bit that goes before the details on how to implement the approach. It can introduce important
concepts and terms. If reasonable, long form explanations of forensic concepts should be added to the
ForensicsWiki, and then a link to that page added in `references` to avoid duplication.

| Field name            | Type       | Description                                                                                                              |
|-----------------------|------------|--------------------------------------------------------------------------------------------------------------------------|
| `summary`             | `string`   | A human readable summary for the approach.                                                                               |
| `details`             | `string`   | A description of the approach. Markdown syntax MAY be used for rich text representation.                                 |
| `references`          | `[string]` | Optional. List of URLs of public references to this approach. Markdown syntax MAY be used for rich text representation.  |
| `references_internal` | `[string]` | Optional. List of URLs of private references to this approach. Markdown syntax MAY be used for rich text representation. |

Example ([source](https://github.com/google/dfiq/blob/main/data/approaches/Q1001.10.yaml#L26;L37)):
```yaml
description:
  summary: Parse download records from web browsers' own databases.
  details: >
    Most web browsers track file downloads (at least in non-Incognito/private
    sessions) in local artifacts on the system. We can collect and review
    these records. This approach is useful when you have remote access to a
    system (via GRR for example) or a disk image.
  references:
    - "[Chrome](https://forensics.wiki/google_chrome/#downloadsstart_time),
      [Firefox](https://forensics.wiki/mozilla_firefox/#downloads), and
      [Safari](https://forensics.wiki/apple_safari/#downloads) downloads on
      ForensicsWiki"
```

#### View
The `view` aims to be a concise representation of how to perform this investigative approach, with some omissions.
The `data` section describes the data that will need to be collected, but _not_ how to collect it. Similarly,
each object in `processors` may provide configuration or filtering information, but doesn't explain how to run the processor.

| Field name   | Type       | Description                                                                              |
|--------------|------------|------------------------------------------------------------------------------------------|
| `data`       | `[Object]` | The data required to answer the question via this approach.                              |
| `notes`      | `Object`   | A description of the approach. Markdown syntax MAY be used for rich text representation. |
| `processors` | `[Object]` | Optional. List of Processor objects.                                                     |

##### Data
This section (`view.data`) can have multiple ways describing the data needed for
this approach. They should be thought of as complementary or as alternates
to each other (they can be "OR"d together, they do not need to be "AND"d).
Each is specified by a pair of `type` and `value`. Current `type`s are
`artifact` and `description`, but more can be added as needs arise.

* `artifact` corresponds to the name of a [ForensicArtifact](https://github.com/ForensicArtifacts/artifacts), an existing
repository of machine-readable digital forensic artifacts.
Specifying a value for `artifact` is preferred when the data is a host-based
file/artifact, but other methods are available as well.
* `description` is a string describing the data that's needed. This can be used
alone to describe the data, if an `artifact` isn't available or appropriate, or
in conjunction with an `artifact` to better describe it.

| Field name | Type     | Description                                                                          |
|------------|----------|--------------------------------------------------------------------------------------|
| `type`     | `string` | The type of the data. Example: `artifact` for ForensicArtifact definition.           |
| `value`    | `string` | The value of the type. Example: `BrowserHistory` (the name of the ForensicArtifact). |

Example ([source](https://github.com/google/dfiq/blob/main/data/approaches/Q1001.10.yaml#L40;L45)):
```yaml
data:
  - type: artifact
    value: BrowserHistory
  - type: description
    value: Collect local browser history artifacts. These are often in the
      form of SQLite databases and JSON files in multiple directories.
```

##### Notes
The data specified often comes with certain caveats; these can often be tacit knowledge or assumed that "everyone
knows that". This can lead to incorrect assumptions and analysis. Explicitly stating them reduces ambiguity.

| Field name    | Type       | Description                                                                               |
|---------------|------------|-------------------------------------------------------------------------------------------|
| `covered`     | `[string]` | List of strings describing what this data is covering in the context of the approach.     |
| `not_covered` | `[string]` | List of strings describing what this data is NOT covering in the context of the approach. |

Example ([source](https://github.com/google/dfiq/blob/main/data/approaches/Q1001.10.yaml#L46;L57)):
```yaml
notes:
  covered:
    - Chrome downloads. Beyond "stable" Chrome, this also includes
      Chromium, Chrome Canary, Chrome Beta, and other Chromium-based browsers
      (Microsoft Edge, Brave, and Opera) on Windows, macOS, and Linux
    - Safari downloads
    - Includes downloads from all Chrome profiles
  not_covered:
    - Browsers installed in non-standard paths
    - Downloads made during Incognito sessions
```

#### Processors
A processor is what takes the data collected and processes it in some way to produce structured data an investigator
reviews. Multiple processors can be defined, as there are often multiple programs capable of doing similar processing
(example: log2timeline, Magnet Axiom, and Hindsight can all process browser history artifacts and deliver similar results).

| Field name | Type       | Description                                        |
|------------|------------|----------------------------------------------------|
| `name`     | `string`   | Name of the processor.                             |
| `options`  | `[Object]` | Optional. Configuration options for the processor. |
| `analysis` | `Object`   | Optional. Analysis methods and steps.              |

##### Options
The named processor may benefit from some configuration options.

| Field name | Type     | Description                                                 |
|------------|----------|-------------------------------------------------------------|
| `type`     | `string` | Type of option. This is dependent on the type of processor. |
| `value`    | `string` | Value of the option.                                        |

Example ([source](https://github.com/google/dfiq/blob/main/data/approaches/Q1001.10.yaml#L60;L62)):
```yaml
options:
  - type: parsers
    value: webhist
```

##### Analysis
After running the processor against the `data` (possibly using the `options`),
we may want to take further analysis steps to refine that information.
This could take the form of filtering the data, sorting or otherwise
manipulating it, or something specific to a given analysis platform (for
example, Timesketch may produce a graph).

Each object in `analysis` is an analysis method, consisting of its `name`
and the analysis `steps`. Broadly speaking, each analysis method should produce
similar output; the user can choose whichever method is available to them and
get similar results. This will not always be the case (a Timesketch graph is
different from a pandas DataFrame), but it is the intent.

| Field name | Type       | Description                       |
|------------|------------|-----------------------------------|
| `name`     | `string`   | Name of the analysis method.      |
| `steps`    | `[Object]` | The steps of the analysis method. |

###### Steps
Under each analysis method will be a sequence of one or more maps with
keys `description`, `type`, and `value`. If there is more than one map,
they should be processed in sequence in the analysis method (if applicable).
In this way, we can describe multiple chained steps of
analysis (with the `description` being a way to communicate to the user
what exactly each "step" is doing, enabling a "show-your-work"-type capability).

| Field name    | Type     | Description                                      |
|---------------|----------|--------------------------------------------------|
| `description` | `string` | Human readable description of the analysis step. |
| `type`        | `string` | The type of the analysis step.                   |
| `value`       | `string` | The value of the analysis step.                  |

Example ([source](https://github.com/google/dfiq/blob/main/data/approaches/Q1001.10.yaml#L63;L73)):
```yaml
analysis:
  - name: OpenSearch
    steps:
      - description: Filter the results to just file downloads
        type: opensearch-query
        value: data_type:("chrome:history:file_downloaded" OR "safari:downloads:entry")
  - name: Python Notebook
    steps:
      - description: Filter the results to just file downloads
        type: pandas
        value: query('data_type in ("chrome:history:file_downloaded", "safari:downloads:entry")')
      - description: Not necessary, but wanted to show two steps
        type: pandas
        value: sort_values(by='timestamp').head(5)
```

Python notebooks (Jupyter, Colab, etc) have become powerful tools for
security analysts. Recording the analysis steps in a way that would work
in a notebook makes the analysis more accessible and easier to demonstrate.

`type: pandas` refers to pandas [DataFrame](https://pandas.pydata.org/docs/reference/frame.html)
methods. They allow chaining, which is very powerful and flexible.
One would apply the operation in `value` by assuming the
data from the previous step (either the results from `data`
or the prior analysis step) was saved into a Pandas DataFrame (`df`),
then applying the operation to it. For example, the
first `pandas` step in the example is equivalent to:
`df.query('data_type in ("chrome:history:file_downloaded", "safari:downloads:entry")')`.
