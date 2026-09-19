---
schema_version: "1.1"
name: new-long-task-workspace
description: A multi-week task should get one durable entry point another agent can resume.
tags: [create, core]
max_turns: 16
allowed_tools: [Read, Glob, Grep, Skill, Bash, Write, Edit]
---
I'm starting a research project that will take a few weeks: compare three note-taking apps (Obsidian, Notion, Apple Notes) for my 6-person team and recommend one. Set it up under ./team-notes-research in this directory so that I, or another AI agent later, can pick it up cold, and draft the plan. Don't do the research yet.
