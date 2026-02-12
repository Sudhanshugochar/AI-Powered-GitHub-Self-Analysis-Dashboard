# System Prompts for AI-Powered GitHub Analysis

This document outlines the prompts used by the Ollama models (Llama 3.1 & Mistral) for various analysis tasks.

## 1. Sentiment Analysis
**Task**: Determine the emotional tone of a commit message.
**Prompt Template**:
```text
Analyze the sentiment of the following commit message. Return only 'Positive', 'Neutral', or 'Negative'.

Commit Message: {commit_message}
```
**Expected Output**: `Positive`, `Neutral`, or `Negative`.

## 2. Topic Classification
**Task**: Categorize a repository based on its description.
**Prompt Template**:
```text
Classify the following repository description into one of these topics: 'Web Development', 'Data Science', 'Machine Learning', 'Mobile App', 'DevOps', 'Other'. Return only the topic name.

Description: {repo_description}
```
**Expected Output**: A single category name.

## 3. Skill Extraction
**Task**: Extract technical skills from a README file.
**Prompt Template**:
```text
Extract a list of technical skills, languages, and frameworks mentioned in the following README content. Return them as a comma-separated list.

README:
{readme_content_truncated}
```
**Expected Output**: `Python, React, Docker, Kubernetes`

## 4. Code Quality Review (Planned)
**Task**: Summarize code quality based on a snippet.
**Prompt Template**:
```text
Review the following code snippet for readability, efficiency, and potential bugs. Provide a concise summary.

Code:
{code_snippet}
```
**Expected Output**: A short paragraph describing the code quality.

## 5. Model Comparison Task
**Task**: General reasoning to benchmark latency.
**Prompt Template**:
```text
Explain the concept of recursion in programming.
```
