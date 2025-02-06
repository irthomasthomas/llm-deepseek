M	llm_deepseek.py
A	merge_branches.md
## Files changed:
M	llm_deepseek.py
A	merge_branches.md

## Summary of changes:
1d67f2b docs: Add merge process documentation
f54d7bd adding build_kwargs as a required prompt

## Detailed changes:
diff --git a/llm_deepseek.py b/llm_deepseek.py
index 980429c..a4da0e3 100644
--- a/llm_deepseek.py
+++ b/llm_deepseek.py
@@ -60,7 +60,7 @@ class DeepSeekChat(Chat):
     def execute(self, prompt, stream, response, conversation):
         messages = self._build_messages(conversation, prompt)
         response._prompt_json = {"messages": messages}
-        kwargs = self.build_kwargs(prompt)
+        kwargs = self.build_kwargs(prompt, stream)
 
         max_tokens = kwargs.pop('max_tokens', 8192)
         if prompt.options.response_format:
@@ -150,7 +150,7 @@ class DeepSeekCompletion(Completion):
     def execute(self, prompt, stream, response, conversation):
         full_prompt = self._build_full_prompt(conversation, prompt)
         response._prompt_json = {"prompt": full_prompt}
-        kwargs = self.build_kwargs(prompt)
+        kwargs = self.build_kwargs(prompt, stream)
 
         max_tokens = kwargs.pop('max_tokens', 4096)
         if prompt.options.echo:
diff --git a/merge_branches.md b/merge_branches.md
new file mode 100644
index 0000000..fb1a6a8
--- /dev/null
+++ b/merge_branches.md
@@ -0,0 +1,49 @@
+# Merging fix-kwargs and main into logprobs branch
+
+## Steps:
+1. Check current branch and status
+2. Fetch latest changes
+3. Create and switch to new logprobs branch
+4. Merge fix-kwargs branch
+5. Merge main branch
+6. Push new logprobs branch
+7. Verify the merge
+
+## Progress:
+### 1. Check current branch and status
+* fix-kwargs
+  main
+
+   * fix-kwargs
+
+### 2. Fetch latest changes
+Fetched latest changes from all remotes.
+
+### 3. Create and switch to new logprobs branch
+Created and switched to new branch 'logprobs'.
+
+### 4. Merge fix-kwargs branch
+Merged fix-kwargs branch into logprobs.
+
+### 5. Merge main branch
+Merged main branch into logprobs.
+
+### 6. Push new logprobs branch
+Pushed logprobs branch to remote repository.
+
+### 7. Verify the merge
+#### Current branch status:
+On branch logprobs
+Your branch is up to date with 'origin/logprobs'.
+
+Untracked files:
+  (use "git add <file>..." to include in what will be committed)
+	merge_branches.md
+
+nothing added to commit but untracked files present (use "git add" to track)
+#### Recent commit history:
+6743469 Merge branch 'main' into logprobs
+e7b1a3e feat(DeepSeek): Add support for logprobs and top_logprobs
+f54d7bd adding build_kwargs as a required prompt
+6ecc645 new endpoints, with reason
+898dbac changed name to llm-deepseek-xtreme avoiding naming conflicts
