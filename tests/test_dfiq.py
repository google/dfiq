# Copyright 2026 Google LLC
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

from pathlib import Path
import tempfile
import unittest

from dfiq import DFIQ, Question

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "dfiq" / "templates"


class DFIQTest(unittest.TestCase):
    def test_bundled_data_loads(self) -> None:
        kb = DFIQ(templates_path=TEMPLATES_DIR)
        self.assertGreaterEqual(len(kb.scenarios()), 6)
        self.assertGreaterEqual(len(kb.facets()), 30)
        self.assertGreaterEqual(len(kb.questions()), 90)
        self.assertGreaterEqual(len(kb.approaches()), 18)
        self.assertIn("F1008", kb.components["S1001"].facets)
        self.assertIn("Q1001", kb.components["F1008"].questions)

    def test_v1_1_custom_data_and_markdown_generation(self) -> None:
        scenario_uuid = "11111111-1111-4111-8111-111111111111"
        q_mixed_uuid = "22222222-2222-4222-8222-222222222222"
        q_internal_approach_uuid = "33333333-3333-4333-8333-333333333333"

        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp) / "data"
            out_public = Path(tmp) / "out_public"
            out_internal = Path(tmp) / "out_internal"
            (data_dir / "scenarios").mkdir(parents=True)
            (data_dir / "questions").mkdir(parents=True)
            # Intentionally omit data_dir / "facets" and add a non-YAML file.
            (data_dir / "questions" / "README.txt").write_text(
                "ignore me", encoding="utf-8"
            )

            (data_dir / "scenarios" / "scenario.yaml").write_text(
                f"""---
name: Direct Question Scenario
type: scenario
description: Scenario without facets or legacy IDs.
uuid: {scenario_uuid}
dfiq_version: 1.1.0
""",
                encoding="utf-8",
            )

            (data_dir / "questions" / "q_mixed.yaml").write_text(
                f"""---
name: Mixed visibility approaches question?
type: question
uuid: {q_mixed_uuid}
dfiq_version: 1.1.0
tags:
  - PublicQuestionTag
parent_ids:
  - {scenario_uuid}
approaches:
  - name: Public SQL Approach
    description: |-
      First summary paragraph
      spanning two lines.

      Second detail paragraph.
    tags:
      - PublicApproachTag
    steps:
      - name: Run multi-line GoogleSQL
        stage: analysis
        type: googlesql-query
        value: |-
          SELECT *
          FROM events
          WHERE ok = TRUE
  - name: Internal Approach
    internal: true
    tags:
      - SecretInternalTag
    steps:
      - name: Query internal logs
        stage: collection
        type: internal-tool
        value: secret_source
""",
                encoding="utf-8",
            )

            (data_dir / "questions" / "q_only_internal_approach.yaml").write_text(
                f"""---
name: Internal-only approach question?
type: question
uuid: {q_internal_approach_uuid}
dfiq_version: 1.1.0
parent_ids:
  - {scenario_uuid}
approaches:
  - name: Private Approach
    internal: true
    tags:
      - OnlyInternalTag
    steps:
      - name: Collect private artifact
        stage: collection
        type: internal-tool
        value: private_artifact
""",
                encoding="utf-8",
            )

            kb = DFIQ(
                yaml_data_path=data_dir,
                markdown_output_path=out_public,
                templates_path=TEMPLATES_DIR,
            )
            self.assertEqual(len(kb.scenarios()), 1)
            self.assertEqual(len(kb.facets()), 0)
            self.assertEqual(len(kb.questions()), 2)

            scenario = kb.components[scenario_uuid]
            self.assertEqual(
                scenario.facets,
                sorted([q_mixed_uuid, q_internal_approach_uuid]),
            )

            q_mixed = kb.components[q_mixed_uuid]
            assert isinstance(q_mixed, Question)
            self.assertEqual(
                q_mixed.all_tags, {"PublicQuestionTag", "PublicApproachTag"}
            )
            self.assertEqual(
                q_mixed.visible_tags(allow_internal=True),
                {"PublicQuestionTag", "PublicApproachTag", "SecretInternalTag"},
            )

            kb.generate_scenario_md(scenario_uuid, allow_internal=False)
            kb.generate_question_md(q_mixed_uuid, allow_internal=False)
            kb.generate_question_md(q_internal_approach_uuid, allow_internal=False)
            kb.generate_question_index_md(allow_internal=False)

            self.assertFalse(
                (out_public / "questions" / f"{q_internal_approach_uuid}.md").exists()
            )
            scenario_md = (out_public / "scenarios" / f"{scenario_uuid}.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("## Questions", scenario_md)
            self.assertIn(f'/questions/{q_mixed_uuid}"', scenario_md)
            self.assertNotIn(f'/questions/{q_internal_approach_uuid}"', scenario_md)

            index_md = (out_public / "questions" / "index.md").read_text(
                encoding="utf-8"
            )
            self.assertNotIn("SecretInternalTag", index_md)
            self.assertNotIn("OnlyInternalTag", index_md)
            self.assertNotIn(f'/questions/{q_internal_approach_uuid}"', index_md)

            q_md = (out_public / "questions" / f"{q_mixed_uuid}.md").read_text(
                encoding="utf-8"
            )
            self.assertNotIn("SecretInternalTag", q_md)
            self.assertIn(
                "- First summary paragraph spanning two lines.",
                q_md,
            )
            self.assertIn(
                "First summary paragraph\nspanning two lines.\n\nSecond detail paragraph.",
                q_md,
            )
            self.assertIn(
                "         ```googlesql\n"
                "         SELECT *\n"
                "         FROM events\n"
                "         WHERE ok = TRUE\n"
                "         ```",
                q_md,
            )

            kb.markdown_output_path = out_internal
            kb.generate_question_md(q_mixed_uuid, allow_internal=True)
            kb.generate_question_md(q_internal_approach_uuid, allow_internal=True)
            self.assertTrue(
                (out_internal / "questions" / f"{q_internal_approach_uuid}.md").exists()
            )
            q_internal_md = (
                out_internal / "questions" / f"{q_mixed_uuid}.md"
            ).read_text(encoding="utf-8")
            self.assertIn("SecretInternalTag", q_internal_md)
            self.assertIn("## Internal Approach", q_internal_md)


if __name__ == "__main__":
    unittest.main()
