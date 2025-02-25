from flow import flow

ds = []
with open('datasets/HumanEval.jsonl', 'r') as file:
    for line in file:
        ds.append(json.loads(line))

flow.file = "your file path"
flow.ds = data
flow.LLM = ChatGPT.ChatGPT()
flow.k_value = 5

if __name__ == '__main__':
    for i in range(len(ds)):
        code, judge, error = flow(i)
        print(code, judge, error)
