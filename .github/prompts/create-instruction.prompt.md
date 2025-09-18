@workspace
Analyze this codebase to generate or update `.github/copilot-instructions.md` for guiding AI coding agents.

Focus on discovering the essential knowledge that would help an AI agents be immediately productive in this codebase. Consider aspects like:

- The "big picture" architecture that requires reading multiple files to understand - major components, service boundaries, data flows, and the "why" behind structural decisions
- Critical developer workflows (builds, tests, debugging) especially commands that aren't obvious from file inspection alone
- Project-specific conventions and patterns that differ from common practices
- Integration points, external dependencies, and cross-component communication patterns
- Check the users input for what they want to focus on and emphasize those areas

Source existing AI conventions from `**/{.github/copilot-instructions.md,AGENT.md,AGENTS.md,CLAUDE.md,.cursorrules,.windsurfrules,.clinerules,.cursor/rules/**,.windsurf/rules/**,.clinerules/**,README.md}` (do one glob search).

Guidelines (read more at <https://aka.ms/vscode-instructions-docs>):

- If `.github/copilot-instructions.md` exists, merge intelligently - preserve valuable content while updating outdated sections
- Write concise, actionable instructions (~20-50 lines) using markdown structure
- Include specific examples from the codebase when describing patterns
- Avoid generic advice ("write tests", "handle errors") - focus on THIS project's specific approaches
- Document only discoverable patterns, not aspirational practices
- Reference key files/directories that exemplify important patterns

Update `.github/copilot-instructions.md` for the user, then ask for feedback on any unclear or incomplete sections to iterate.

### User input

<user-input>
This repo is currently using tkinter and does not work well with vscode's interactive window. I think it would be better if you fetched the documentation links and then implement the tool calls using inputs/options directly in chat.

Before starting the task:

1. You may #fetch:

    ```pseudo
    fetch_webpage([
    "https://code.visualstudio.com/api/extension-guides/ai/ai-extensibility-overview",
    "https://code.visualstudio.com/api/extension-guides/ai/tools",
    "https://code.visualstudio.com/api/extension-guides/ai/mcp",
    "https://code.visualstudio.com/api/extension-guides/ai/chat",
    "https://code.visualstudio.com/api/extension-guides/ai/chat-tutorial",
    "https://code.visualstudio.com/api/extension-guides/ai/language-model",
    "https://code.visualstudio.com/api/extension-guides/ai/language-model-tutorial",
    "https.code.visualstudio.com/api/extension-guides/ai/language-model-chat-provider",
    "https.code.visualstudio.com/api/extension-guides/ai/prompt-tsx"
    ], "documentation")
    ```

2. You must #search for relevant files inside [knowledge base](../knowledge_base/)

3. Summarize the fetched documentation and search results to get the context of the project and the changes needed inside a file `docs/CONTEXT.md`.

4. Everytime you're suffering from context loss, you may redo the steps above, adding new findings and solutions to `docs/CONTEXT.md` file.

Then you may start the tasks:

1. Then, you must update the `copilot-instructions.md`.

2. You must create new instructions for the user related to enforcing good workspace practices, system design, design patterns, and docs. — e.g. prefer snake_case, follow builder pattern for x reason (random ass example),  etc. —

3. You must create a `TASKS.md` with detailed tasks inside `docs/tasks/TASKS.md`

    You are currently doing:
    [TODO.md](../../TODO.md#L7-L10)

    ```md
    - [ ] | high | hitl-1  | Setup `.github/` folder.
    - [ ] | high | hitl-14 |  Improve UI/UX
      1. | high | hitl-15  | #think in a plan and immediately fix the UI/UX to be more user friendly. I think the tkinter makes things too complex.
          - Explore the authors choice. Why he chose these approach instead of others? What are the limitations from the current ones? (the vscode or any other ide built-in ones solutions).
    ```

</user-input>
