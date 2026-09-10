---
name: concept-map
description: Reduce comprehension debt in AI-built projects by creating and maintaining a concept map in docs/map/. Use when a project works but the user cannot explain it, specifications or decisions are hard to find, or design documents are too large. Organize concepts, current behavior, rationale, and open questions into a tree of Markdown files that can be explored in Obsidian.
---

# Concept map (`docs/map/`)

Create **one Markdown file per concept**, connected by **parent-to-child `[[links]]` forming a tree**. Readers should be able to find a concept in the map, open its file, and understand its role, behavior, and unresolved questions.

The goal is to help users explain a project and make informed changes, especially when AI implementation has outpaced their understanding. Ground the map in the project's documentation and implementation.

Use the user's or project's language for names and content. The English examples in this skill do not determine the output language.

## Basic structure

1. **Use parent-child relationships as a reading path.** Choose one root named after the product, and one parent for every other concept. Place a concept under the topic where readers would look for its details.
2. **Describe dependencies in plain text.** Write "Password Reset uses Email Delivery." Reserve `[[links]]` for parent-to-child navigation so dependency edges do not obscure the reading path.
3. **Keep concept files directly under `docs/map/`.** Links carry the hierarchy. `[[Login]]` points to `Login.md`. Names may use any language. For a name containing a path separator, such as `/login`, use `login.md` and keep the official name in its heading.

## Find intermediate concepts

**Write a sentence that explains several concrete concepts together, then name that sentence.** A new name is useful when it communicates their shared experience, purpose, or responsibility.

1. **Explain each concrete concept briefly.** Include what it does: Login starts an authenticated session, Logout ends it, and Password Reset helps a user regain access after forgetting a password.
2. **Group concepts that make sense to explain together.** Summarize them in one sentence: "Verify users and manage access to their accounts." This becomes the parent's description.
3. **Give the description a short name.** Here, "Authentication" works. Use an established term when it fits. If a label such as "Mechanisms" tells readers little, name what those mechanisms accomplish.
4. **Check the reading path.** Would someone looking for Login open Authentication? Does the parent's description explain why those children belong together? Adjust the name or grouping if needed. Concepts without a useful grouping can stay directly under their current parent.

Choose the perspective that makes sense at that point in the map. Authentication groups an access-related purpose; Notifications groups the responsibility of informing users about changes. Familiar screens, processes, and services can also provide useful groupings. Sharing a directory or technology alone does not determine a parent.

When several parents seem plausible, choose **the entry point readers would use to find the specification**. Mention other relationships in the body. For example, the password recovery procedure belongs under Authentication, while email delivery details can be explained elsewhere.

When creating a first map or choosing an intermediate concept, read the [worked authentication example](references/auth-example.md). It shows the reasoning and the resulting files.

## Write a concept file

Start with the concept's name as a heading, followed by a short explanation of **its role and current behavior**. For an intermediate concept, explain what its children have in common.

Check existing documents against the implementation or current specification. Mark contradictions and unverified details explicitly. Give planned concepts their own files, starting with "Not implemented. Intended to..." so readers can distinguish current behavior from plans.

Add sections only when they have useful content:

- **Rationale:** Decisions whose reasons prevent misunderstanding or an ill-informed change. Include relevant history when outdated documents remain misleading or an unusual design has a reason worth preserving.
- **Open questions:** What still needs a decision, the known options, and the information needed to choose. Once resolved, update the current specification and keep rationale only where useful.
- **Pitfalls:** Behavior that can fail silently or surprise someone making a change.

Mark a gap in your investigation as "Unverified." A decision already made by the project does not become an open question just because the reader has not learned about it yet.

Keep decisions and questions with the living concepts they concern. When one approach replaces another, preserve necessary rationale with the replacement concept.

Use these reference forms; code paths are relative to the target project's root:

```text
[[Name]]              Parent-to-child link to Name.md
Plain concept name    Dependencies and related topics: uses Email Delivery
Plain path            Implementation location: src/auth/ or src/email/
owner/repo#n          Issue: example/task-app#27
```

## Create a map

1. **Establish the scope and evidence.** Read any existing map, product description, design documents, `CLAUDE.md` / `AGENTS.md`, and relevant implementation. Identify the product or area being mapped.
2. **Explain the product in a short paragraph.** Start with roughly three to five sentences. Extract concrete concepts and their roles, then return to the evidence to fill important gaps.
3. **Find intermediate concepts and choose parents.** Apply the process above to build a reading path from the product to its details. Let the content determine the number of nodes and the depth.
4. **Write the files.** Establish each concept's opening explanation, then move relevant specifications, cautions, and rationale from existing documents. Create files for planned concepts too. Record known open decisions with their concepts and mark conflicting evidence as unverified.
5. **Check structure and findability.** Follow the completion checks below. If Obsidian is available, explore the map in graph view as well.
6. **Connect the documentation entry points.** Point existing guides and `CLAUDE.md` / `AGENTS.md` to `docs/map/`. Consolidate duplicate specifications after checking their destinations, while keeping working instructions in the instruction files.

## Maintain a map

- **Add a concept:** Explain its role and link to it from the parent readers would try first. Reference relevant issues in its body.
- **Change a parent:** Move the link from the old parent to the new one, then check that both descriptions still fit their children.
- **Rename or merge:** Update incoming links and plain-text mentions. Preserve necessary rationale with the surviving concept.
- **Change behavior or finish implementation:** Update the opening description and any implementation-status or open-question notes.
- **Improve a crowded branch:** Look for children that share a useful explanation. Child count alone does not establish the need for another intermediate concept.

Issue scope and concept scope can differ. One issue may be referenced by several concepts.

## Check completion

Read the concept files and their links to check the structure:

- All concept files are directly under `docs/map/`, and every `[[Name]]` resolves to a file there.
- There is one root with no parent; every other concept has exactly one parent.
- Following child links from the root reaches every concept, without cycles.

Count repeated mentions of the same parent-child relationship as one edge, and ignore link syntax inside code examples. A tree with `N` nodes has `N-1` edges, but that count alone does not prove the structure is a tree.

Then choose a few concrete specifications a reader might seek and follow the path from the root. Check that parent names suggest where to go, and the destination explains the concept's role, behavior, and any uncertainty. Compare those statements with the evidence used to write them.

For a request focused on understanding, provide a short tour of the main branches and point out where unresolved questions live.

This approach targets one product with a few dozen concepts, maintained by an individual or small team. If exhaustive dependency tracing or a large classification system is the main goal, choose a representation suited to that purpose.
