propose_prompt = '''
We are given a nxn partially solved board and have to solve it according to the following rules:
- We need to replace the 0s with numbers from 1-n
- Each number from 1-n must appear exactly once in each column and row in the solved board
Given a board, decide which cell to fill in next and the number to fill it with, each possible next step is seperated by a new line.
If the board is fully filled or no valid next step exists output only 'END'.
Sample Input-1: 
1 0 3
2 0 0
0 1 2
Possible next steps for Sample Input-1:
1 2 3
2 0 0
0 1 2

1 0 3
2 0 0
3 1 2

1 0 3
2 3 0
0 1 2

Sample Input-2: 
1 2 3
2 3 1
3 1 2
Possible next steps for Sample Input-2:
END

Input: 
{input}
Possible next steps for Input:
'''

value_prompt = '''
We are given a nxn partially solved board.
- We need to replace the 0s with numbers from 1-n
- Each number from 1-n must appear exactly once in each column and row in the solved board
Given a partially filled board, evaluate how likely it is to reach a valid solution (sure/likely/impossible)
Sample-Input-1:
0 0 0
0 0 0
0 0 0
Board is empty, hence it is always possible to get to a solution.
Sure

Sample-Input-2:
1 0 3
2 0 0
0 1 2
No constraint is violated till now and it is likely to get to a solution.
Likely

Sample-Input-3:
1 1 3
2 0 0
0 1 2
Constraint violated in first row.
Impossible

Input:
{input}
'''