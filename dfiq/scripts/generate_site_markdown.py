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

import os
import re
from pathlib import Path
from dfiq import DFIQ

# This file should be called from the repository root:
# PYTHONPATH=. python dfiq/scripts/generate_site_markdown.py

file_path = os.path.abspath(__file__)
templates_dir = os.path.join(os.path.dirname(os.path.dirname(file_path)), "templates")
docs_dir = Path("site/docs")
dfiq_instance = DFIQ(templates_path=templates_dir, markdown_output_path=docs_dir)

for subdir in ("scenarios", "questions"):
    for existing_md in (docs_dir / subdir).glob("*.md"):
        if existing_md.name != "index.md":
            existing_md.unlink()

for scenario in dfiq_instance.scenarios():
    dfiq_instance.generate_scenario_md(scenario.id or scenario.uuid)

for question in dfiq_instance.questions():
    dfiq_instance.generate_question_md(question.id or question.uuid)

dfiq_instance.generate_question_index_md()
dfiq_instance.generate_approach_glossary_md()

mkdocs_path = Path("site/mkdocs.yml")
question_nav = ["      - questions/index.md"] + [
    f"      - questions/{q.id or q.uuid}.md"
    for q in dfiq_instance.questions()
    if not q.is_internal and q.visible_approaches()
]
scenario_nav = ["      - scenarios/index.md"] + [
    f"      - scenarios/{s.id or s.uuid}.md"
    for s in dfiq_instance.scenarios()
    if not s.is_internal
]
nav_block = (
    "  - Questions:\n"
    + "\n".join(question_nav)
    + "\n  - Scenarios:\n"
    + "\n".join(scenario_nav)
    + "\n"
)
mkdocs_text, count = re.subn(
    r"  - Questions:\n(?:      - .*\n)+  - Scenarios:\n(?:      - .*(?:\n|$))+",
    nav_block,
    mkdocs_path.read_text(encoding="utf-8"),
)
if count != 1:
    raise ValueError(
        "Expected to update Questions and Scenarios nav in site/mkdocs.yml"
    )
mkdocs_path.write_text(mkdocs_text, encoding="utf-8")
