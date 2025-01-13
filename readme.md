
# Self-Validating AI Agent for Customer Feedback Summarization

## Overview

This project builds an AI agent that autonomously validates and improves summaries generated from customer feedback. It ensures accuracy, relevance, and consistency by checking the alignment between feedback and the generated summary.

## Key Features

1. Generate Summaries: Uses GPT-3.5 to create summaries from feedback.
2. Validate Output: Compares the summary with the feedback using cosine similarity.
3. Iterative Refinement: If the summary is inaccurate, the agent refines it through multiple iterations.

## How It Works

1. Generate a Summary from customer feedback using GPT-3.5.
2. Validate the Summary using cosine similarity to check if it aligns with the feedback.
3. Refine the Summary if similarity is low, repeating until an acceptable level is reached.

## Requirements

- Python 3.x
- Install dependencies: `pip install -r requirements.txt`
- Set up OpenAI API key in `.env`:  
  `OPENAI_API_KEY=your_openai_api_key_here`

## How to Run
1. Run the script: python main.py


---------------------------------------------------------------------------------------------------

## Future Approach to solve this issue to use RLHL:

## Step 1: Summarize Feedback (Using GPT):

Continue generating summaries from feedback using your existing GPT-based model.

## Step 2: Collect Human Feedback:

After generating the summary, ask for feedback from humans (via thumbs-up/thumbs-down or ratings).

## Step 3: Reward Model Training:

Use the feedback to train a simple regression model or neural network that predicts the quality of a summary based on human ratings.

## Step 4: Reinforcement Learning Loop:

Use the rewards from the feedback to guide the reinforcement learning loop.

The model will get adjusted based on positive and negative rewards, learning how to create better summaries.

## Simplified Workflow:
AI Agent: Generates output (e.g., a summary).
Human Feedback: Humans provide feedback on the output (e.g., thumbs-up or thumbs-down).
Reward Model: Feedback is used to train a model that scores the output.
Reinforcement Learning: The agent learns to optimize its behavior based on the feedback and rewards it receives.
Continuous Learning: The process repeats, and the agent gets better with each iteration.

By continuously integrating human feedback into the AI model’s learning process, the system becomes more reliable, reduces hallucinations, and can autonomously validate its own outputs over time.

