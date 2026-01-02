Teach yourself how to create good Claude Code skills by reading everything in @docs, take your time, Our goal will be to improve existing skill further.
Understand very well how to create Claude Code skills:
[create_new_skill-process.md](docs/create_new_skill-process.md)
[anthropic-skill-docs](docs/knowledge/anthropic-skill-docs)

Also note [important.md](important.md) and make sure to follow what it says.

- The skill we're improving is [approval-tests](output_skills/approval-tests) for all three languages.

Once you're ready, you can analyze what's currently in the skill and make yourself a plan of how to improve it further (you can use todo tool you have you create a temporary todo file in the root), taking into account best practices of creating Claude Code skills and important considerations from context management as a guidance.

You can teach yourself more about each version of approvaltests by using resources in links.md

Once you have an imporvement plan, work through it and implement until you see no more things to improve. Take your time, we're not rushing, the goal is to make it really really good.

Commit every improvement as a separate commit.

I want you to focus on thinking about what the user needs to know about this - the user is Claude Code!

Once you finished learning about what's needed, use the following process:
1. Invoke the refinement-loop skill
2. After reading it, make these adjustments for this session:
   - Instead of writing iterations to playground/{tag}-N.md files, use commits
   - Instead of temporary files, edit the real skill files directly
   - Each commit = one iteration
3. Apply this adjusted process to improve the target skill

I want you to target on cross-checking what is in SkillMD while keeping focus on best practices still, but maybe things like what is Reporters or what is Combinations or what is Inline or what is Discoverers or the fact that there's options and so on. Maybe some of them can be in the main one, because right now I see what the skill contains and I don't know that it brings a lot of value, does it? Because I think people then have to read further in depth to look into things. 

So take your time and think deeply about what's there vs what the AI needs to know as it reads through it. 