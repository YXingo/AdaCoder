# AdaCoder: Adaptive Planning Framework for Multi-Agent Code Generation

## Overview

![](img/workflow.png)

AdaCoder is a multi-agent framework that achieves adaptive planning through two strategies: 1) applying the planning mechanism only after the initial non-planning generation fails; 2) generating tailored plans based on specific error feedback from each iteration. The framework consists of four agents—Programming Assistant, Code Evaluator, Debug Specialist, and Prompt Engineer—that collaborate to handle code generation tasks. 

The process begins with Phase-1, where the Programming Assistant generates code without planning, leveraging the LLM's native capabilities by using a plan-free prompt. Simultaneously, the script-based Code Evaluator assesses the correctness of the generated code using benchmark-provided sample test cases (e.g., HumanEval), avoiding the noise and cost associated with LLM-based test case generation as in AgentCoder. This phase identifies errors beyond the LLM's capabilities or those hindering execution, and the detected error information is passed to Phase-2.

In Phase-2, the framework iteratively addresses both superficial and in-depth errors through adaptive error fixing and adaptive planning. The Debug Specialist resolves three common superficial errors using a rule-based method derived from prior work, replacing costly LLM-based bug localization and debugging. Subsequently, the Prompt Engineer generates a step-by-step plan to address deeper logical issues. For instance, if the code incorrectly returns the smallest prime factor instead of the largest, the plan explains the logical flaw and outlines the correct steps to resolve it. This enables the Programming Assistant to regenerate the code based on the new plan, ultimately ensuring the code passes all tests. 

This iterative process continues for up to $t$ iterations or until the code successfully meets all requirements, with diverse planning prompts triggered by different errors in each iteration.

## Installation

1. **Clone the Repository**  
   Begin by cloning the AdaCoder repository to your local machine using the following commands:
   
   ```bash
   git clone https://github.com/YXingo/AdaCoder.git
   cd AdaCoder
   ```
   
2. **Install Dependencies**  
   Install the required Python dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Model Settings**  
   - For **closed-source models**, set your `api_key` in the configuration file or environment variables.  
   - For **open-source models**, specify the `model_path` to point to the local model directory.

4. **Run the Project**  
   Once the setup is complete, execute the project with the following command:
   ```bash
   python src/execute.py
   ```

