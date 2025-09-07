from utils import *


def programming_assistant(sample, plan=None):
    if plan:
        prompt = f"""Solve the following problem according to the given plan.

## Plan
{plan}

## Task Description
{sample['prompt']}"""
    else:
        prompt = f"""## Task Description
{sample['prompt']}"""

    while True:
        try:
            response = LLM(prompt, truncation=True, max_new_tokens=512, do_sample=True, temperature=0.2, top_p=0.9)[0][
                'generated_text']
            code = preprocess(response)
        except Exception as e:
            print(e)
            code = ""
        if code != "":
            break

    return code


def code_evaluator(code, sample):
    return execute_test(f"{code}\n\n{sample['test']}\n\ncheck({sample['entry_point']})")


def debug_specialist(sample, code, e_type, e_message):
    try:
        compile(source=code, filename='', mode='exec')
        judge = True
    except Exception as e:
        judge = False
    while not judge:
        try:
            compile(source=code, filename='', mode='exec')
            judge = True
        except:
            judge = False
            code = remove_last_row(code)

        if judge:
            structure['debugged_code'] = code
            print("\n\nDebug Specialist: Done!\n\n")
            return structure

    if e_type == "NameError":
        judge = False
        while True:
            fixed_code = add_import_statement(get_missing_name(e_message), code)

            if code == fixed_code or judge:
                print("\n\nDebug Specialist: Done!\n\n")
                return code
            else:
                code = fixed_code

            judge, exception = execute_test(
                f"{code}\n\n{sample['sample_test_cases']}\n\ncheck({sample['entry_point']})")
            e_message = str(exception)

    return code


def prompt_engineer(sample, error):
    description = sample["docstring"][:sample["docstring"].find('>>>')]

    prompt = f"""Develop a new plan based on the feedback from the last error.

## Task Description
{description}

## Error Feedback
Error Type: {type(error).__name__}
Error Message: {str(error)}

## Let's explore various approaches and perspectives to solve this problem.

## My Plan
- Firstly,"""

    while True:
        try:
            response = LLM(prompt, truncation=True, max_length=88, max_new_tokens=88,
                           do_sample=True, temperature=0.2, top_p=0.9)[0]['generated_text']

            plan = '- Firstly,' + response[len(prompt):]
            index = min(
                find_non_negative_l(plan, '\n\n'),
                find_non_negative_l(plan, '"""'),
                find_non_negative_l(plan, "'''"),
            )
            plan = plan[:index]
        except Exception as e:
            print(e)
            plan = ""
        if plan != "":
            break

    return plan
