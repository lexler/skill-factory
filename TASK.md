
Teach yourself how to create good Claude Code skills by reading everything in @docs, take your time, Our goal will be to improve existing skill further.
Understand very well how to create Claude Code skills:
[create_new_skill-process.md](docs/create_new_skill-process.md)
[anthropic-skill-docs](docs/knowledge/anthropic-skill-docs)

Also note [important.md](important.md) and make sure to follow what it says.

- The skill we're improving is [approval-tests](output_skills/approval-tests) for python.

Once you're ready, you can analyze what's currently in the skill and make yourself a plan of how to improve it further (you can use todo tool you have you create a temporary todo file in the root), taking into account best practices of creating Claude Code skills and important considerations from context management as a guidance.

You can teach yourself more about python approvaltests by using resources in [links.md](output_skills/approval-tests/links.md)

Once you have an imporvement plan, work through it and implement until you see no more things to improve. Take your time, we're not rushing, the goal is to make it really really good.

Commit every improvement as a separate commit.

I want you to focus on thinking about what the user needs to know about this - the user is Claude Code!
I currently see shit like:
```
### Supported Python versions

3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14
```
Claude Code can search by itself and this is good for something that's a comprehensive doc. But the point of the skill is not to build a comprehensive doc, it is to teach CC to be effective in this and provide gradual exposure of information. Shit like the above is in no way helping us. If we need to look at what python version this lib supports, we can look online.

This needs to be hand picked information that is distilled and is amazing for making Claude Code really efficient in writing approval tests, specifically in python right now.