import jinja2
import logging
import networkx as nx
import os
import yaml

logging.basicConfig(
    level=logging.DEBUG, format="%(filename)s | %(levelname)s | %(message)s"
)


class Component(object):
    def __init__(self, dfiq_id, name, description=None, tags=None, parent_ids=None):
        self.id = dfiq_id
        self.name = name
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
            self.parent_ids = ()

        if name:
            self.name = name.rstrip()

        if description:
            if isinstance(description, str):
                self.description = description.rstrip()

        if self.id[1] == "0":
            self.is_internal = True

    def set_children(self, child_ids):
        self.child_ids = child_ids


class Approach(Component):
    def __init__(self, dfiq_id, name, description, tags, view):
        super().__init__(dfiq_id, name, description, tags, [dfiq_id.split(".")[0]])
        self.view = view
        self.type = "approach"

        if self.id[6] == "0":
            self.is_internal = True


class Question(Component):
    def __init__(self, dfiq_id, name, description, tags, parent_ids):
        super().__init__(dfiq_id, name, description, tags, parent_ids)
        self.type = "question"

    @property
    def approaches(self):
        return self.child_ids


class Facet(Component):
    def __init__(self, dfiq_id, name, description, tags, parent_ids):
        super().__init__(dfiq_id, name, description, tags, parent_ids)
        self.type = "facet"

    @property
    def questions(self):
        return self.child_ids


class Scenario(Component):
    def __init__(self, dfiq_id, name, description, tags):
        super().__init__(dfiq_id, name, description, tags)
        self.type = "scenario"

    @property
    def facets(self):
        return self.child_ids


class DFIQ:
    def __init__(self, yaml_data_path=None, markdown_output_path=None):
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
            loader=jinja2.FileSystemLoader("templates/"), trim_blocks=True
        )

        if not yaml_data_path:
            self.yaml_data_path = "data"
            logging.info(
                f'"yaml_data_path" not specified; set to "{self.yaml_data_path}"'
            )
            
        self.load_dfiq_items_from_yaml()
        self.build_graph()
        self.add_child_ids()
        self.add_child_tags()

    def scenarios(self):
        return sorted(
            [c for c in self.components.values() if isinstance(c, Scenario)],
            key=lambda x: x.id,
        )

    def facets(self):
        return sorted(
            [c for c in self.components.values() if isinstance(c, Facet)],
            key=lambda x: x.id,
        )

    def questions(self):
        return sorted(
            [c for c in self.components.values() if isinstance(c, Question)],
            key=lambda x: x.id,
        )

    def approaches(self):
        return sorted(
            [c for c in self.components.values() if isinstance(c, Approach)],
            key=lambda x: x.id,
        )

    def add_child_ids(self):
        if not self.graph:
            raise ValueError("DFIQ Graph needed before adding children.")

        for dfiq_id, component in self.components.items():
            children = sorted(list(nx.DiGraph.successors(self.graph, dfiq_id)))
            self.components[dfiq_id].set_children(children)

    def add_child_tags(self):
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
    def convert_yaml_object_to_dfiq_component(yaml_object):
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

    def load_yaml_files_by_type(self, dfiq_type, yaml_data_path=None):
        if not yaml_data_path:
            yaml_data_path = self.yaml_data_path
        component_dict = {}
        dfiq_files = os.listdir(
            os.path.join(yaml_data_path, self.plural_map.get(dfiq_type))
        )
        for dfiq_file in dfiq_files:
            if dfiq_file.endswith(("-template.yaml", "-blank.yaml")):
                continue
            with open(
                os.path.join(yaml_data_path, self.plural_map.get(dfiq_type), dfiq_file),
                mode="r",
            ) as file:
                component_from_yaml = yaml.safe_load(file)
                component_dict[
                    component_from_yaml["id"]
                ] = self.convert_yaml_object_to_dfiq_component(component_from_yaml)

        return component_dict

    def load_dfiq_items_from_yaml(self, yaml_data_path=None):
        if not yaml_data_path:
            yaml_data_path = self.yaml_data_path

        self.components = {}
        for dfiq_component in ["Scenario", "Facet", "Question", "Approach"]:
            self.components.update(
                self.load_yaml_files_by_type(dfiq_component, yaml_data_path)
            )

    def build_graph(self):
        self.graph = nx.DiGraph()
        for dfiq_id, content in self.components.items():
            self.graph.add_node(dfiq_id)
            logging.debug(f"added node: {dfiq_id}")

        for dfiq_id, content in self.components.items():
            if content.parent_ids:
                for parent_id in content.parent_ids:
                    self.graph.add_edge(parent_id, dfiq_id)
                    logging.debug(f"added edge: {parent_id} -> {dfiq_id}")

    def display_graph(self):
        nx.draw(self.graph, with_labels=True, font_weight="bold")

    def generate_external_scenario_md(self, scenario_id):
        if not self.markdown_output_path:
            raise ValueError("Markdown output path not specified")

        s = self.components.get(scenario_id)

        if s.is_internal:
            logging.warning(
                f"Will not generate external Scenario page for internal Scenario {scenario_id}"
            )
            return False

        template = self.jinja_env.get_template("external_scenario_md.jinja2")
        context = {"scenario": s, "components": self.components}
        content = template.render(context)
        with open(
            os.path.join(self.markdown_output_path, "scenarios", f"{scenario_id}.md"),
            mode="w",
        ) as file:
            file.write(content)

    def generate_external_question_md(self, question_id, skip_if_no_approaches=True):
        if not self.markdown_output_path:
            raise ValueError("Markdown output path not specified")

        q = self.components.get(question_id)

        if skip_if_no_approaches and not q.approaches:
            logging.debug(
                f"Skipped writing markdown for {question_id}; it had no Approaches"
            )
            return

        template = self.jinja_env.get_template(
            "external_question_with_approaches_md.jinja2"
        )
        context = {"question": q, "components": self.components}
        content = template.render(context)
        output_path = os.path.join(
            self.markdown_output_path, "questions", f"{question_id}.md"
        )
        with open(output_path, mode="w") as file:
            file.write(content)

        logging.info(f"Wrote markdown for Question {question_id} to {output_path}")

    def generate_external_question_index_md(self):
        if not self.markdown_output_path:
            raise ValueError("Markdown output path not specified")

        template = self.jinja_env.get_template("external_questions_index_md.jinja2")
        context = {"components": self.components}
        content = template.render(context)
        with open(
            os.path.join(self.markdown_output_path, "questions", "index.md"), mode="w"
        ) as file:
            file.write(content)
