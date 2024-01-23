from dfiq import DFIQ

dfiq_instance = DFIQ(markdown_output_path=f"site/docs")

for scenario in dfiq_instance.scenarios():
    dfiq_instance.generate_scenario_md(scenario.id)

for question in dfiq_instance.questions():
    dfiq_instance.generate_question_md(question.id)

dfiq_instance.generate_question_index_md()
