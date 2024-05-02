import argparse
from tot.methods.bfs_board import solve
from tot.tasks.latin_square import LatinSquareTask
from tot.models import gpt_usage

backend = "gpt-3.5-turbo"
args = argparse.Namespace(
    backend=backend, ## OpenAI model
    temperature=0.7, ## model temperature
    task="latin-square", ## Task
    naive_run=False,##  --naive_run: if True, run naive IO/CoT sampling instead of ToT + BFS
    prompt_sample=None, ## (choices=[standard, cot]): sampling prompt
    method_generate="propose", ## (choices=[sample, propose]): thought generator, whether to sample independent thoughts (used in Creative Writing) or propose sequential thoughts (used in Game of 24)
    method_evaluate="value", ## (choices=[value, vote]): state evaluator, whether to use the value states independently (used in Game of 24) or vote on states together (used in Creative Writing)
    method_select="greedy",## [greedy/sample] how to choose the states to keep for BFS --> greedily choose best states / sample according to votes
    n_generate_sample=1, ## number of times to prompt for thought generation
    n_evaluate_sample=3, ## number of times to prompt for state evaluation
    n_select_sample=5, ## number of states to keep from each step (i.e. b in the paper's ToT + BFS algorithm
)

task = LatinSquareTask()
print("Number of Examples:", len(task))
print("Sample Input:\n", task.get_input(0), sep='')

output = solve(args, task, 0)
print("output", output)

print(gpt_usage(backend=backend))
# ys, infos = solve(args, task, 900)
# print(ys)
# print(infos)
# print(ys[0])
