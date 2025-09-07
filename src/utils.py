import re
import signal
import modules_db


def raise_timeout(signum, frame):
    raise TimeoutError


def find_non_negative_l(code, substring):
    result = code.find(substring)
    return result if result != -1 else len(code)


def find_non_negative_r(code, substring):
    result = code.rfind(substring)
    return result if result != -1 else len(code)


def execute_test(code):
    global_namespace = {}

    try:
        signal.signal(signal.SIGALRM, raise_timeout)
        signal.alarm(1)

        exec(code, global_namespace)

        signal.alarm(0)

        return True, None
    except Exception as e:
        signal.alarm(0)
        return False, e


def preprocess(code):
    def ffilter(code_block):
        code_block.replace("    ", "\t").replace("   ", "\t").replace("  ", "\t").replace("\t", "    ")
        code_block = code_block.split('if __name__ == "__main__":')[0]
        code_block = code_block.split("if __name__ == '__main__':")[0]
        lines = code_block.split('\n')
        new_lines = []
        for line in lines:
            if not (line.strip().startswith('print') or line.strip().startswith(
                    'input') or line.strip().startswith(
                'assert') or line.strip().startswith('unittest')):
                new_lines.append(line)
        code_block = '\n'.join(new_lines)

        return code_block

    code_blocks = []

    if '```' in code:
        split_list = find_all_occurrences(code, '```')

        if code.find('def ') < split_list[0]:
            code_block = code[code.index('def '):code.index('```')].strip()
            code_block = ffilter(code_block)

            judge = False
            while not judge:
                try:
                    compile(source=code_block, filename='', mode='exec')
                    judge = True
                except Exception as e:
                    code_block = remove_last_row(code_block)
                    judge = False

            code_blocks.append(code_block)

            rest_code = code[split_list[0]:].split('\n')
            if len(rest_code) < 1 or rest_code[1].startswith('def'):
                pass
            else:
                split_list.pop(0)

        for i in range(len(split_list) // 2):
            code_block = code[split_list[2 * i]: split_list[2 * i + 1]].strip()
            code_block = '\n'.join(code_block.split('\n')[1:])
            code_block = ffilter(code_block)
            code_blocks.append(code_block)

        if len(split_list) % 2 != 0:
            code_block = code[split_list[-1]:].strip()
            code_block = '\n'.join(code_block.split('\n')[1:])
            code_block = ffilter(code_block)
            code_blocks.append(code_block)

        code = '\n\n'.join(code_blocks)

    return code


def remove_last_row(code):
    return '\n'.join(code.split('\n')[:-1])


def get_missing_name(exception_message):
    match = re.search(r"name '(.+?)' is not defined", exception_message)
    if match:
        return match.group(1)
    else:
        return None


def add_import_statement(missing_name, code):
    module_name, fc_name, import_statement = None, None, ""

    if missing_name in modules_db.modules:
        import_statement = f"import {missing_name}\n\n"
    elif missing_name in modules_db.fcs:
        import_statement = f"from {modules_db.fcs[missing_name]} import {missing_name}\n\n"

    if missing_name == 'np':
        import_statement = "import numpy as np\n\n"
    elif missing_name == 'pd':
        import_statement = "import pandas as pd\n\n"

    return import_statement + code


def could_be_fixed(judge, e_type):
    if not judge and e_type == "NameError" or (e_type == "SyntaxError" or e_type == "IndentationError"):
        return True
    else:
        return False
