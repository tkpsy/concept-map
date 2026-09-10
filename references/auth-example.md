# Authentication: finding an intermediate concept and writing its files

This example uses a fictional task management app. Its behavior, implementation status, open questions, and code paths are illustrative. For a real project, derive concepts from its own documentation and implementation.

## How Authentication emerges

Start by explaining concrete concepts and their behavior:

- **Login:** Verify the user and start an authenticated session.
- **Logout:** End the session on the current device.
- **Password Reset:** Help a user regain access after forgetting a password. Not implemented in this example.

Together, these answer: "How do users access their accounts and end that access?" A shared explanation is "Verify users and manage access to their accounts." Give this explanation the name **Authentication**. An established term works when it fits the explanation.

```text
Task App
└── Authentication
    ├── Login
    ├── Logout
    └── Password Reset
```

Now check whether someone looking for Login would open Authentication. The parent's name suggests where to look, and its description explains why these three children belong together.

## The resulting files

This complete five-file example covers only the authentication branch. Put all five files directly under `docs/map/`.

### Task App.md

```markdown
# Task App

An app where users create tasks and manage their assignees and deadlines.
This map covers the specifications for accessing an account.

- [[Authentication]]
```

### Authentication.md

```markdown
# Authentication

Verify users and manage access to their accounts.
Login and Logout are implemented. Password Reset is not implemented.

- [[Login]]
- [[Logout]]
- [[Password Reset]]
```

### Login.md

```markdown
# Login

Verify the user's email address and password, then start a Session.
Show the task list after a successful login.

src/auth/login/

## Rationale

Display names are editable, so they are not used as login identifiers.
Changing a display name should not change how the user signs in.
```

### Logout.md

```markdown
# Logout

End the Session on the current device and return to the login screen.
Sessions on other devices remain active.

src/auth/logout/
```

### Password Reset.md

```markdown
# Password Reset

Not implemented. Intended to help users regain access after forgetting their password.

## Open questions

Should users receive reset instructions through Email Delivery, or request help from an administrator?
Decide based on the required scope of self-service recovery and administrator availability.

example/task-app#22
```

A planned concept still has a file, making the plan visible and keeping the link valid. Session and Email Delivery appear as plain names because these mentions explain behavior and relationships. In a broader map, place their files under the branches where readers would look for them.

## Apply the same process to Notifications

Start with another set of concrete concepts:

- **Deadline Reminders:** Tell assignees when their tasks are approaching a deadline.
- **Assignment Changes:** Tell the people involved when a task's assignee changes.

The shared explanation is "Inform users about changes that need their attention." Name it **Notifications**.

```text
Task App
└── Notifications
    ├── Deadline Reminders
    └── Assignment Changes
```

Concrete behavior can reveal a shared purpose or responsibility before you choose a name. Choose a perspective that makes each part of the map understandable; different branches can use different perspectives.

## When several parents seem plausible

Password Reset relates to Authentication and to the Email Delivery used to send instructions. In this map, place it under Authentication, where readers would look for the recovery procedure. Explain delivery details under Email Delivery and mention that name in the body.

When maintaining an existing tree, consider the entry points readers already use. Another parent might also be defensible. Check that the chosen path helps readers find the specification.
