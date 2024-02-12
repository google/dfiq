# Copyright 2024 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import jinja2
import logging
import networkx as nx
import os
import re
import yamale
import yaml

logging.basicConfig(
    level=logging.DEBUG, format="%(filename)s | %(levelname)s | %(message)s"
)


class Component(object):
    """Base class for DFIQ components.

    Components are the building blocks of DFIQ. They represent different logical
    entities: Scenarios, Facets, Questions, and Approaches. This base class
    defines the attributes that all components share.

    Attributes:
        id (str): The unique ID of the component, as described at dfiq.org/spec.
        name (str): The name of the component, often in the form of a question.
        description (str, optional): A few sentence description of the component.
        type (str, optional): The type of component.
        tags (set[str], optional): A set of tags associated with the component.
        parent_ids (set[str], optional): A set of IDs of the component's parents.
        child_ids (set[str], optional): A set of IDs of the component's children.
        is_internal (bool): Whether the component is private and for internal use only.

    Methods:
        set_children(child_ids: set[str]): Sets the component's children.
    """

    def __init__(
        self,
        dfiq_id: str,
        name: str,
        description: str | None = None,
        tags: set[str] | None = None,
        parent_ids: set[str] | None = None,
    ) -> None:
        self.id = dfiq_id
        self.name = name.rstrip()
        self.description = description
        self.type = None
        self.tags = tags
        self.parent_ids = parent_ids
        self.child_ids = None
        self.is_internal = False

        if not self.tags:
            self.tags = set()

        self.all_tags = set(self.tags)

        if not self.parent_ids:
            self.parent_ids = set()

        if description:
            if isinstance(description, str):
                self.description = description.rstrip()

        if self.id[1] == "0":
            self.is_internal = True

    def set_children(self, child_ids: list) -> None:
        """Set the component's `child_ids` attribute to a list of its children."""
        self.child_ids = child_ids


class Approach(Component):
    """An Approach in DFIQ.

    Approaches are detailed explanations of how to answer a Question using a specific
    method, including the required data, processing, and analysis steps. As there
    is often more than one way to answer a question, there can be multiple Approaches
    that answer a given Question using different techniques.

    Attributes:
        view (dict): A concise representation of how to perform this investigative approach.
        type (str): The type of component, which is always "approach".
    """

    def __init__(
        self,
        dfiq_id: str,
        name: str,
        description: str,
        tags: set[str] | None,
        view: dict,
    ) -> None:
        super().__init__(
            dfiq_id, name, description, tags, parent_ids={dfiq_id.split(".")[0]}
        )
        self.view = view
        self.type = "approach"

        if self.id[6] == "0":
            self.is_internal = True


class Question(Component):
    """A Question in DFIQ.

    Questions are the fundamental "building blocks" of DFIQ. All other DFIQ
    components are relative to Questions: Approaches describe how to answer the
    Questions, and Scenarios and Facets organize the Questions logically.

    Attributes:
        type (str): The type of component, which is always "question".
    """

    def __init__(
        self,
        dfiq_id: str,
        name: str,
        description: str | None,
        tags: set[str] | None,
        parent_ids: set[str],
    ) -> None:
        super().__init__(dfiq_id, name, description, tags, parent_ids)
        self.type = "question"

    @property
    def approaches(self) -> set[str]:
        """All Approaches associated with a given Question."""
        return self.child_ids


class Facet(Component):
    """A Facet in DFIQ.

    Facets are used for intermediate-level grouping in DFIQ. A particular Facet can
    be part of multiple different Scenarios and will contain multiple Questions. A
    Facet breaks the larger Scenario into smaller logical pieces, but a Facet is
    still too broad to answer directly; it must also be broken down (into Questions).

    Attributes:
        type (str): The type of component, which is always "facet".
    """

    def __init__(
        self,
        dfiq_id: str,
        name: str,
        description: str | None,
        tags: set[str] | None,
        parent_ids: set[str],
    ) -> None:
        super().__init__(dfiq_id, name, description, tags, parent_ids)
        self.type = "facet"

    @property
    def questions(self) -> set[str]:
        """All Questions associated with a given Facet."""
        return self.child_ids


class Scenario(Component):
    """A Scenario in DFIQ.

    A Scenario is the highest-level grouping in DFIQ. A Scenario is made of one or
    more Facets (different "sides" of an investigation), which in turn are made up of
    investigative Questions.

    Attributes:
        type (str): The type of component, which is always "scenario".
    """

    def __init__(
        self, dfiq_id: str, name: str, description: str, tags: set[str] | None
    ):
        super().__init__(dfiq_id, name, description, tags)
        self.type = "scenario"

    @property
    def facets(self) -> set[str]:
        """All Facets associated with a given Scenario."""
        return self.child_ids


class DFIQ:
    """A DFIQ knowledge base.

    An instance of a DFIQ knowledge base. Upon initialization, it reads DFIQ YAML files from
    yaml_data_path, converts them to Python objects, and builds a graph of the components'
    relationships.

    Attributes:
        yaml_data_path (str): The path to the directory containing the DFIQ YAML files.
        markdown_output_path (str, optional): The path to the directory where the
            generated Markdown files should be saved.
        plural_map (dict): A dictionary mapping from DFIQ component types to their
            plural forms.
        components (dict): A dictionary mapping from DFIQ component IDs to their
            corresponding components.
        graph (nx.DiGraph, optional): A directed graph representing the relationships
            between DFIQ components.
        jinja_env (jinja2.Environment): A Jinja2 environment used to generate Markdown
            files.
    """

    def __init__(
        self,
        yaml_data_path: str = "data",
        markdown_output_path: str | None = None,
        templates_path: str = "templates",
    ) -> None:
        self.yaml_data_path = yaml_data_path
        self.markdown_output_path = markdown_output_path
        self.plural_map = {
            "Scenario": "scenarios",
            "Facet": "facets",
            "Question": "questions",
            "Approach": "approaches",
        }
        self.components = {}
        self.graph = None
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_path), trim_blocks=True
        )
        self.schemas = {
            "Scenario": None,
            "Facet": None,
            "Question": None,
            "Approach": None,
        }

        logging.info(f'"yaml_data_path" set to "{self.yaml_data_path}"')

        self._load_dfiq_schema()
        self.load_dfiq_items_from_yaml()
        self.build_graph()
        self.add_child_ids()
        self.add_child_tags()

    def scenarios(self) -> list[Scenario]:
        """Returns a list of all Scenarios in the DFIQ knowledge base."""
        return sorted(
            [c for c in self.components.values() if isinstance(c, Scenario)],
            key=lambda x: x.id,
        )

    def facets(self) -> list[Facet]:
        """Returns a list of all Facets in the DFIQ knowledge base."""
        return sorted(
            [c for c in self.components.values() if isinstance(c, Facet)],
            key=lambda x: x.id,
        )

    def questions(self) -> list[Question]:
        """Returns a list of all Questions in the DFIQ knowledge base."""
        return sorted(
            [c for c in self.components.values() if isinstance(c, Question)],
            key=lambda x: x.id,
        )

    def approaches(self) -> list[Approach]:
        """Returns a list of all Approaches in the DFIQ knowledge base."""
        return sorted(
            [c for c in self.components.values() if isinstance(c, Approach)],
            key=lambda x: x.id,
        )

    def add_child_ids(self) -> None:
        """Adds the list of their child IDs to a component's `child_ids` attribute.

        This is necessary due to how DFIQ components are designed. Instead of specifying a component's
        children in it directly (allowing a "top-down" view of the DFIQ hierarchy), only the component's
        parent(s) are. This enables filtering out "internal" components without leaking references to
        those components. Because of this, DFIQ takes a "bottom-up" approach to construct the hierarchy
        at the time of initialization (using a networkx DiGraph).
        """
        if not self.graph:
            raise ValueError("DFIQ Graph needed before adding children.")

        for dfiq_id, component in self.components.items():
            children = sorted(list(nx.DiGraph.successors(self.graph, dfiq_id)))
            self.components[dfiq_id].set_children(children)

    def add_child_tags(self) -> None:
        """Adds tags from a Question's Approaches to that Question's `all_tags attribute."""
        if not self.graph:
            raise ValueError("DFIQ Graph needed before adding children.")

        for dfiq_id, component in self.components.items():
            parents = sorted(list(nx.DiGraph.predecessors(self.graph, dfiq_id)))
            if self.components[dfiq_id].type == "approach":
                for parent in parents:
                    self.components[parent].all_tags = self.components[
                        parent
                    ].all_tags.union(self.components[dfiq_id].tags)

    @staticmethod
    def convert_yaml_object_to_dfiq_component(
        yaml_object: dict,
    ) -> Scenario | Facet | Question | Approach | None:
        """Takes a dict, loaded from a DFIQ YAML file, and converts to the appropriate dfiq.Component object."""

        assert yaml_object["type"] in (
            "scenario",
            "facet",
            "question",
            "approach",
        ), "Object must be of known DFIQ type"

        if yaml_object["type"] == "scenario":
            return Scenario(
                yaml_object["id"],
                yaml_object["display_name"],
                yaml_object.get("description"),
                yaml_object.get("tags"),
            )

        elif yaml_object["type"] == "facet":
            return Facet(
                yaml_object["id"],
                yaml_object["display_name"],
                yaml_object.get("description"),
                yaml_object.get("tags"),
                yaml_object.get("parent_ids"),
            )

        elif yaml_object["type"] == "question":
            return Question(
                yaml_object["id"],
                yaml_object["display_name"],
                yaml_object.get("description"),
                yaml_object.get("tags"),
                yaml_object.get("parent_ids"),
            )

        elif yaml_object["type"] == "approach":
            return Approach(
                yaml_object["id"],
                yaml_object["display_name"],
                yaml_object.get("description"),
                yaml_object.get("tags"),
                yaml_object.get("view"),
            )

        else:
            return None

    def load_yaml_files_by_type(
        self, dfiq_type: str, yaml_data_path: str | None = None
    ) -> dict:
        """Load all DFIQ YAML files of a given type from the appropriate path.

        Given the yaml_data_path, locate the correct sub-directory for that
        dfiq_type, validate any YAML files there, and load them into a dict.

        Args:
            dfiq_type (str): The component type (Scenario, Facet, Question, or Approach).
            yaml_data_path (str, optional): The base path holding the YAML files.

        """
        if not yaml_data_path:
            yaml_data_path = self.yaml_data_path
        component_dict = {}
        dfiq_files = os.listdir(
            os.path.join(yaml_data_path, self.plural_map.get(dfiq_type))
        )
        for dfiq_file in dfiq_files:
            if dfiq_file.endswith(("-template.yaml", "-blank.yaml")):
                continue
            file_to_open = os.path.join(
                yaml_data_path, self.plural_map.get(dfiq_type), dfiq_file
            )

            if not self.validate_yaml_file(file_to_open):
                continue

            if not self.validate_dfiq_schema(file_to_open, dfiq_type):
                continue

            with open(file_to_open, mode="r") as file:
                component_from_yaml = yaml.safe_load(file)
                converted = self.convert_yaml_object_to_dfiq_component(
                    component_from_yaml
                )

                if converted:
                    component_dict[component_from_yaml["id"]] = converted
        return component_dict

    @staticmethod
    def validate_yaml_file(yaml_file_path: str) -> bool:
        """Validate that a YAML file can be parsed by pyYAML."""
        with open(yaml_file_path, mode="r") as file:
            try:
                _ = yaml.safe_load(file)
            except (yaml.parser.ParserError, yaml.scanner.ScannerError) as e:
                logging.warning(f"error parsing {yaml_file_path}:\n{e}")
                return False
            return True

    def _load_dfiq_schema(self) -> None:
        """Load Yamale 'spec' files to use for validation."""
        self.schemas["Scenario"] = yamale.make_schema("utils/scenario_spec.yaml")
        self.schemas["Facet"] = yamale.make_schema("utils/facet_spec.yaml")
        self.schemas["Question"] = yamale.make_schema("utils/question_spec.yaml")
        self.schemas["Approach"] = yamale.make_schema("utils/approach_spec.yaml")

    def validate_dfiq_schema(self, yaml_file_path: str, component_type: str) -> bool:
        """Validate that a YAML file adheres to the appropriate DFIQ Schema."""
        try:
            yaml_to_validate = yamale.make_data(yaml_file_path)
            yamale.validate(self.schemas[component_type], yaml_to_validate)
        except yamale.YamaleError as e:
            logging.warning(e)
            return False
        return True

    def load_dfiq_items_from_yaml(self, yaml_data_path: str | None = None) -> None:
        """Load all four types of DFIQ components from a base path."""
        if not yaml_data_path:
            yaml_data_path = self.yaml_data_path

        self.components = {}
        for dfiq_component in ["Scenario", "Facet", "Question", "Approach"]:
            self.components.update(
                self.load_yaml_files_by_type(dfiq_component, yaml_data_path)
            )

    def build_graph(self) -> None:
        """Create a nx.DiGraph linking all loaded DFIQ components."""
        self.graph = nx.DiGraph()
        for dfiq_id, content in self.components.items():
            self.graph.add_node(dfiq_id)
            logging.debug(f"added node: {dfiq_id}")

        for dfiq_id, content in self.components.items():
            if content.parent_ids:
                for parent_id in content.parent_ids:
                    self.graph.add_edge(parent_id, dfiq_id)
                    logging.debug(f"added edge: {parent_id} -> {dfiq_id}")

    def display_graph(self) -> None:
        """Display the DFIQ graph."""
        nx.draw(self.graph, with_labels=True, font_weight="bold")

    def generate_scenario_md(
        self, scenario_id: str, allow_internal: bool = False
    ) -> None:
        """Generates Markdown for a Scenario page.

        Args:
            scenario_id (str): The ID of the scenario to generate the page for.
            allow_internal (bool): Check if generating internal items is allowed.
        """
        if not self.markdown_output_path:
            raise ValueError("Markdown output path not specified")

        scenario = self.components.get(scenario_id)

        if not scenario:
            raise Exception(f"Unable to find {scenario_id} in components dictionary")

        if scenario.is_internal and not allow_internal:
            logging.warning(
                f"Will not generate Scenario page for internal Scenario {scenario_id}"
            )
            return

        template = self.jinja_env.get_template("scenario.jinja2")
        context = {
            "scenario": scenario,
            "components": self.components,
            "allow_internal": allow_internal,
        }
        content = template.render(context)
        with open(
            os.path.join(self.markdown_output_path, "scenarios", f"{scenario_id}.md"),
            mode="w",
        ) as file:
            file.write(content)

    def generate_question_md(
        self,
        question_id: str,
        skip_if_no_approaches: bool = True,
        allow_internal: bool = False,
    ) -> None:
        """Generates Markdown for a Question page.

        Args:
           question_id (str): The ID of the Question to generate the page for.
           skip_if_no_approaches (bool, optional): Whether to skip generating the page
               if the Question has no associated Approaches. Defaults to True.
           allow_internal (bool): Check if generating internal items is allowed.
        """
        if not self.markdown_output_path:
            raise ValueError("Markdown output path not specified")

        question = self.components.get(question_id)

        if not question:
            raise Exception(f"Unable to find {question_id} in components dictionary")

        if question.is_internal and not allow_internal:
            logging.warning(
                f"Will not generate Question page for internal Question {question_id}"
            )
            return

        if skip_if_no_approaches and not question.approaches:
            logging.debug(
                f"Skipped writing Markdown for {question_id}; it had no Approaches"
            )
            return

        template = self.jinja_env.get_template("question_with_approaches.jinja2")
        context = {
            "question": question,
            "components": self.components,
            "allow_internal": allow_internal,
        }
        content = template.render(context)
        output_path = os.path.join(
            self.markdown_output_path, "questions", f"{question_id}.md"
        )
        with open(output_path, mode="w") as file:
            file.write(content)

        logging.info(f"Wrote Markdown for Question {question_id} to {output_path}")

    def generate_question_index_md(self, allow_internal: bool = False) -> None:
        """Generates Markdown for the index page listing all Questions.

        Args:
            allow_internal (bool): Check if generating internal items is allowed.
        """

        if not self.markdown_output_path:
            raise ValueError("Markdown output path not specified")

        template = self.jinja_env.get_template("questions_index.jinja2")
        context = {"components": self.components, "allow_internal": allow_internal}
        content = template.render(context)
        with open(
            os.path.join(self.markdown_output_path, "questions", "index.md"), mode="w"
        ) as file:
            file.write(content)

    def generate_approach_glossary_md(self, allow_internal: bool = False) -> None:
        """Generates Markdown for the Approach Glossary page, listing common items in Approaches.

        Args:
            allow_internal (bool): Check if generating from internal items is allowed.
        """
        data_type_and_value = {}
        processor_and_analysis_names = {}
        analysis_step_types = set()
        step_variables = set()
        for dfiq_id, component in self.components.items():
            if not isinstance(component, Approach):
                continue

            if not allow_internal and component.is_internal:
                continue

            for d in component.view.get("data"):
                if not data_type_and_value.get(d["type"]):
                    data_type_and_value[d["type"]] = set()
                data_type_and_value[d["type"]].add(d["value"])

            for p in component.view.get("processors"):
                if not processor_and_analysis_names.get(p["name"]):
                    processor_and_analysis_names[p["name"]] = set()

                for analysis in p["analysis"]:
                    processor_and_analysis_names[p["name"]].add(analysis["name"])

                    for step in analysis["steps"]:
                        analysis_step_types.add(step["type"])
                        m = re.findall(r"\{.*?\}", step["value"])
                        if m:
                            step_variables.update(m)

        if not self.markdown_output_path:
            raise ValueError("Markdown output path not specified")

        descriptions = {
            "ForensicArtifact": "This corresponds to the name of a ForensicArtifact, an existing repository of "
            "machine-readable digital forensic artifacts ("
            "https://github.com/ForensicArtifacts/artifacts). Using this type is preferred when "
            "the data is a host-based file/artifact, but other methods are available as well (if "
            "there isn't an existing relevant ForensicArtifact).",
            "description": "Text description of the data type. `description` is often using in conjunction with "
            "another data type to provide more context. It can also be used alone, either as a "
            "placeholder or when more robust, programmatic data types do not fit.",
        }

        template = self.jinja_env.get_template("approach_glossary.jinja2")
        context = {
            "data_type_and_value": data_type_and_value,
            "processor_and_analysis_names": processor_and_analysis_names,
            "analysis_step_types": analysis_step_types,
            "step_variables": step_variables,
            "descriptions": descriptions,
            "components": self.components,
        }
        content = template.render(context)
        with open(
            os.path.join(
                self.markdown_output_path, "contributing", "approach_glossary.md"
            ),
            mode="w",
        ) as file:
            file.write(content)
