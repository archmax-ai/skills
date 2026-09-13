---
type: Playbook
title: Invoice a client
description: Turning booked studio days and pass-through costs into an invoice.
tags: [finance, clients]
status: stable
generated: { by: wiki_agent/1.4, at: 2026-07-14T11:25:00Z }
verified: { by: human:l.brandt, at: 2026-07-16T08:05:00Z }
sources:
  - id: finance-handbook
    resource: https://intranet.example/finance/handbook
    title: Finance handbook, 2026 edition
    author: team:operations
    last_modified: 2026-07-01T00:00:00Z
---

# Trigger

The invoicing date agreed at [kickoff](client-kickoff.md) — for most projects the last working
day of the month, for retainers the first.

# Steps

1. Read the booked studio days from the schedule. Days are billed as booked, not as worked;
   a day the client cancelled inside 48 hours is still billed.[^finance-handbook]
2. Add pass-through costs at cost, each as its own line: billable travel under
   [travel](../policies/travel.md), and any licence bought for the project under
   [expenses](../policies/expenses.md).
3. Put the purchase-order number on the invoice when the client uses one. An invoice without
   it is not rejected, it is simply never paid.
4. Send it to the billing contact named at kickoff, copying the decision-maker.

# When an invoice is queried

Answer from the written kickoff summary and the schedule, not from memory, and copy Operations
on the reply.

[^finance-handbook]: Finance handbook, 2026 edition
