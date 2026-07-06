# ChoreQuest Benchmark

Kaggle-style evaluation benchmark for multi-agent task coordination.

## How to Run

```bash
# Make sure Msty is running with granite4 loaded
py benchmark/run_benchmark.py
```

## Scenarios

| ID | Query | Difficulty |
|----|-------|------------|
| 1 | list all pending tasks | easy |
| 2 | how many tasks does emma have | easy |
| 3 | assign task_1 to john | easy |
| 4 | what is emma's completion rate | easy |
| 5 | suggest a reward for john | easy |
| 6 | assign all pending tasks | medium |
| 7 | check who is overloaded | medium |
| 8 | who needs encouragement | medium |
| 9 | assign tasks fairly | hard |
| 10 | analyze engagement + rewards | hard |

## Metrics

- **Tool Selection Accuracy**: Did agent call correct tools?
- **Argument Accuracy**: Did agent pass correct arguments?
- **Completion Rate**: Did scenario complete successfully?
- **Efficiency**: How many tool calls needed?

## Results

Results saved to `benchmark/results.json` after each run.
