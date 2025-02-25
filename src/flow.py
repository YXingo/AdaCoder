from agents import *

file = ""
ds = None
LLM = None
k_value = None


def flow(id):
    sample = ds[id]

    code = programming_assistant(sample, "")
    judge, error = code_evaluator(code, sample)
    if judge:
        return code, judge, error
    judge, error = execute_test(f"{code}\n\n{sample['sample_test_cases']}\n\ncheck({sample['entry_point']})")

    if could_be_fixed(judge, type(error).__name__):
        code = debug_specialist(sample, code, type(error).__name__, str(error))

        judge, error = execute_test(f"{code}\n\n{sample['sample_test_cases']}\n\ncheck({sample['entry_point']})")

        if could_be_fixed(judge, type(error).__name__):
            code = debug_specialist(sample, code, type(error).__name__, str(error))

    judge, error = code_evaluator(code, sample)

    if judge:
        return code, judge, error

    for i in range(k_value):
        plan = prompt_engineer(sample, error)
        code = programming_assistant(sample, plan)

        judge, error = code_evaluator(code, sample)

        if judge:
            return code, judge, error
        judge, error = execute_test(f"{code}\n\n{sample['sample_test_cases']}\n\ncheck({sample['entry_point']})")

        if could_be_fixed(judge, type(error).__name__):
            code = debug_specialist(sample, code, type(error).__name__, str(error))

            judge, error = execute_test(f"{code}\n\n{sample['sample_test_cases']}\n\ncheck({sample['entry_point']})")

            if could_be_fixed(judge, type(error).__name__):
                code = debug_specialist(sample, code, type(error).__name__, str(error))

        judge, error = code_evaluator(code, sample)

        if judge:
            return code, judge, error

    return code, judge, error


