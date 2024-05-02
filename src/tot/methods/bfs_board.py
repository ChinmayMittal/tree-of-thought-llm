import re
import itertools
import numpy as np
from functools import partial
from tot.models import gpt


def split_on_empty_lines(input_string):
    # Using a regular expression to split on one or more empty lines
    segments = re.split(r'\n\s*\n+', input_string.strip())
    return segments


def get_proposals(task, node): 
    propose_prompt = task.propose_prompt_wrap(node)
    proposals = gpt(propose_prompt, n=1, stop=None)[0]
    return split_on_empty_lines(proposals)

def get_value(task, node, n_evaluate_sample, cache_value=True):
    if cache_value and node in task.value_cache:
        return task.value_cache[node]
    value_prompt = task.value_prompt_wrap(node)
    value_outputs = gpt(value_prompt, n=n_evaluate_sample, stop=None)
    value = task.value_outputs_unwrap(value_outputs)
    if cache_value:
        task.value_cache[node] = value
    return value

def solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    x = task.get_input(idx)  # input instance for this task, settup in tot/tasks
    frontier = [x] ## frontier for the BFS tree
    max_depth = task.get_max_depth(x)
    print("Max Depth: ", max_depth)
    for depth in range(max_depth):
        print(f"Frontier at Depth: {depth}->", frontier)
        print()

        ### generation
        next_frontier = []
        if args.method_generate == 'sample':
            raise NotImplementedError()
        elif args.method_generate == 'propose':
            for node in frontier:
                new_nodes = get_proposals(task, node)
                for new_node in new_nodes:
                    next_frontier.append((new_node, node))
                    
        print(f"Next Frontier Length at depth: {depth}-->", len(next_frontier))
        print()
        
        # evaluation
        if args.method_evaluate == 'vote':
            raise NotImplementedError()
        elif args.method_evaluate == 'value':
            values = []
            for (node, parent) in next_frontier:
                terminal = (node.upper() == 'END')
                if not terminal:
                    value = get_value(task, node, args.n_evaluate_sample)
                else:
                    value = get_value(task, parent, args.n_evaluate_sample)
                values.append((node if not terminal else parent, value, terminal)) ## node, value, terminal
        
        # selection
        if args.method_select == 'sample':
            raise NotImplementedError()
        elif args.method_select == 'greedy':
            values.sort(key=lambda x: x[1], reverse=True)

        print(f"Values at Depth: {depth}->", values)
        print()
        
        selected_nodes = values[:args.n_select_sample]
        frontier = []
        for (node, value, terminal) in selected_nodes:
            if terminal:
                return node
            frontier.append(node)
    return frontier[0]


                
        
        
            
        
