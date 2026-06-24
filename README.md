# Task Coordination Agent

An intelligent multi-agent system for coordinating tasks and motivation 
in both family (ChoreQuest) and organizational (PTO Connect) contexts.

## Problem

Task coordination is hard whether you're managing family chores or 
organizing PTO volunteers. This agent system automates assignment, 
tracking, and motivation across both use cases.

## Solution

A unified AI agent framework with four specialized agents

### mcp-task-coordination

Reads/writes tasks to Prisma (home) or Supabase (org)
Handles task reassignment logic
Surfaces "conflict detection" (overloaded user, deadline clash)


### mcp-engagement

- Point ledger
- Reward catalog
- Incentive burn analysis


### mcp-communication

- Wraps Twilio (SMS), SendGrid (email)
- Tracks delivery/open rates
L- earns optimal send times per user


### mcp-insights

- Aggregates participation data
- Generates trend reports
- Flags anomalies ("Why did engagement drop 40%?")
