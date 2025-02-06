# Merging fix-kwargs and main into logprobs branch

## Steps:
1. Check current branch and status
2. Fetch latest changes
3. Create and switch to new logprobs branch
4. Merge fix-kwargs branch
5. Merge main branch
6. Push new logprobs branch
7. Verify the merge

## Progress:
### 1. Check current branch and status
* fix-kwargs
  main

   * fix-kwargs

### 2. Fetch latest changes
Fetched latest changes from all remotes.

### 3. Create and switch to new logprobs branch
Created and switched to new branch 'logprobs'.

### 4. Merge fix-kwargs branch
Merged fix-kwargs branch into logprobs.

### 5. Merge main branch
Merged main branch into logprobs.

### 6. Push new logprobs branch
Pushed logprobs branch to remote repository.

### 7. Verify the merge
#### Current branch status:
On branch logprobs
Your branch is up to date with 'origin/logprobs'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	merge_branches.md

nothing added to commit but untracked files present (use "git add" to track)
#### Recent commit history:
6743469 Merge branch 'main' into logprobs
e7b1a3e feat(DeepSeek): Add support for logprobs and top_logprobs
f54d7bd adding build_kwargs as a required prompt
6ecc645 new endpoints, with reason
898dbac changed name to llm-deepseek-xtreme avoiding naming conflicts
