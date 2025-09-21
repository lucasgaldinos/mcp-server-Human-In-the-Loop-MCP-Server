---
description: Use web search to find relevant information.
---

#think Since the same errors are still hapenning, the prompt shall be almost the same.

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

## how to proceed

- Don't stop until you find a solution.
- Remember to recall your prompt CONSTANTLY. E.g. #think you stopped and said the test were successful and justified like it was everything working as it should, when I literally shown you it was not. just read our past conversation.
- when you need to test some changes in the inline chat, you'll prompt #runInTerminal
