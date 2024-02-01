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

from dfiq import DFIQ

dfiq_instance = DFIQ(markdown_output_path=f"site/docs")

for scenario in dfiq_instance.scenarios():
    dfiq_instance.generate_scenario_md(scenario.id)

for question in dfiq_instance.questions():
    dfiq_instance.generate_question_md(question.id)

dfiq_instance.generate_question_index_md()
