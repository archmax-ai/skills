---
type: Playbook
title: Security incident
description: First hour after a suspected breach of studio or client data.
tags: [security, operations]
status: stable
generated: { by: human:r.novak, at: 2026-03-02T14:00:00Z }
verified:
  - { by: human:r.novak, at: 2026-03-02T14:00:00Z }
  - { by: process:controls-audit, at: 2026-09-01T02:00:00Z }
stale_after: 2027-03-01T00:00:00Z
---

# Trigger

Any of: a device lost or stolen, credentials in a place they should not be, a client reporting
data of theirs somewhere unexpected, or an email that someone acted on and then doubted.

# First hour

1. Tell Operations. Do not wait until you are sure — a false alarm costs an hour, a silent
   hour costs the client relationship.
2. Write down what you know with timestamps, in a single document, as you go. Reconstructing
   it afterwards is where incidents go wrong.
3. Revoke the credential or isolate the device. Do not delete anything: deleted evidence
   cannot be used to work out what happened.
4. Operations decides who is told and when, including whether the client is notified.

# Afterwards

Within a week, write what happened and what changed as a result. If nothing changed, say that
too, and say why. The `process:controls-audit` entry in this document's frontmatter records
only that the steps still match the studio's stated controls — it is not a substitute for a
person reading the page.
