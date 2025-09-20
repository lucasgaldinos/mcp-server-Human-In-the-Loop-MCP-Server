---
description: "Improve the documentation about the Model Context Protocol (MCP) to ensure clarity and usability for developers."
---

#think The choices didn't appear. Though, the tools now kinda work.

Some ackonowledgments and errors:

- `get_multiline_input` and `get_user_input` seems kinda the same. Maybe #fetch ing the past sources again helps you
- not all tools were tested.
- `show_info_message` does the job of the `get_user_choice` better than the `get_user_choice` itself.
- My choice for `get_user_choice` was `3. blue`, not the index `{3}`.
- `show_confirmation_dialog` was not tested.

#think I want you to:

1. Recall our conversation, specially:
   - my prompts
   - the main objective of the repo
   - your past websearches and fetches results.
   - See what is and what is not capable.
   - created files that are not used anymore and shouldn't even be here.
   - generate a summarization document at [reports](../../docs/reference/reports/) with your findings, errors found, context losses, next focus avoiding context loss, with the big picture in place.
2. #think in a solution to this problem.
   - You may #websearch and #fetch relevant results.
   - You must do MULTIPLE researches, for every bug you find along the way (e.g. you test the tool in the inline chat and it does not work as expected —if it does, I'll prompt inject the json saying it did not work.).
   - #websearch <https://modelcontextprotocol.io/> and #fetch the relevant specs from <https://modelcontextprotocol.io/specification> or any other relevant endpoint that may help you.
   - Use #deepwiki multiple times to make questions about <https://github.com/modelcontextprotocol> the url from it.
   - Do not stop searching until you find at least 3 different solutions for the problem.
   - #think Please generate a full documentation with
     - the links used (no need to reference exactly, but it would be cool).
     - It should contain proper guides and examples (for you to use as well) with code examples of using that code + expected result.
3. Create a plan of execution using #actor-critic-thinking
   - read and update the proper markdown file or files inside [docs](../../docs/):

      1. [files](../../docs/CONTEXT.md)
      1. [files](../../docs/MIGRATION_GUIDE.md)
      1. [files](../../docs/MIGRATION_STRATEGY.md)
      1. [files](../../docs/PRODUCTION_EXAMPLES.md)
      1. [files](../../docs/README.md)
      1. [files](../../docs/V2_COMPLETION_SUMMARY.md)  
   - prompt with #get_multiline_input for my changes.
4. prompt me with #show_info_message asking if you should proceed with the plan or not.
5. Do not stop until you finish
   - you may use web search in between retries to search for errors.
   - track the system outpu constntly with the #file:mcpServer.mcp.config.ws0.human-in-the-loop-v3-dev output terminal.
6. before conluding the task, #show_confirmation_dialog

## how to proceed

- Don't stop until you find a solution.
- Remember to recall your prompt CONSTANTLY. E.g. #think you stopped and said the test were successful and justified like it was everything working as it should, when I literally shown you it was not. just read our past conversation.
- when you need to test some changes in the inline chat, you'll prompt me with the #get_user_input or #get_multiline_input which are working.
