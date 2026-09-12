# Frontmatter reference

Every field the format defines, in the order you would write them. Only `type` is required;
everything else is optional and its absence is meaningful rather than an error. Producers may
add their own keys, and consumers must not reject a document for keys they do not recognise —
so add a plain key rather than inventing a parallel scheme.

This describes format version 0.2. A bundle may declare the version it targets with
`okf_version: "0.2"` in the frontmatter of its **root** `index.md` — the only place an
`index.md` may carry frontmatter at all.

## Identity

| Key | Required | Value |
|-----|----------|-------|
| `type` | **yes** | Short string naming the kind of concept: `Metric`, `Playbook`, `Policy`, `Reference`, `API Endpoint`, `Attested Computation`. Not registered anywhere — reuse what the bundle already uses. |
| `title` | recommended | Display name. Consumers fall back to the file name without it. |
| `description` | recommended | **One sentence.** Copied verbatim into `index.md` entries and search snippets. |
| `resource` | when applicable | URI of the underlying asset the concept describes. Omit for abstract concepts. |
| `tags` | recommended | YAML list of short strings, for the groupings that cut across directories. |

## Provenance: `sources`

The materials the concept derives from, external or internal.

```yaml
sources:
  - id: export-schema                    # stable key; required if the body cites it
    resource: https://docs.example/analytics/export-schema
    title: Analytics export schema       # human-readable label
    author: team:analytics-docs          # who produced the source (authority)
    usage_count: 5000                    # how often it was exercised (adoption, liveness)
    last_modified: 2026-05-30T00:00:00Z  # when the source itself last changed (recency)
usage_window: { from: 2026-06-01T00:00:00Z, to: 2026-06-30T00:00:00Z }
```

- `resource` is required within an entry. It is either something a consumer can follow (an
  absolute URL, a bundle-relative path, a path into `references/`) or a scope descriptor it
  cannot, such as `all queries in project X`.
- `author`, `usage_count` and `last_modified` are *credibility signals*, not a score: the
  format records the facts and leaves the judgement to the consumer. `usage_count` is coarse —
  read it as alive-versus-dead and order of magnitude, not as a ranking.
- `usage_window` is written once as a sibling of `sources` and frames every `usage_count`; a
  single entry may carry its own to override it.
- Lineage needs no field: when a `resource` points at another concept in the bundle, the
  derivation edge is already in the graph.

**Per-claim attribution** uses a markdown footnote whose label is a `sources[].id`:

```markdown
The events table is sharded daily as `events_YYYYMMDD`.[^export-schema]

[^export-schema]: Analytics export schema
```

The label is the join key into `sources`. Labels, not positions, because these documents get
rewritten constantly and a positional reference misattributes silently once the list is
reordered. Do not write a `# Citations` section — that was the previous version's mechanism
and is retired.

## Trust: `generated` and `verified`

```yaml
generated: { by: enrichment_agent/2.1, at: 2026-06-20T22:53:05Z }
verified:
  - { by: human:ahormati, at: 2026-06-25T09:00:00Z }
  - { by: process:finance-nightly, at: 2026-06-26T02:00:00Z }
```

- `generated.by` is required within `generated`; `generated.at` marks the last meaningful
  content change.
- `verified` is a list of confirmation events. A single verifier may be written as one bare
  `{ by, at }` mapping, and a consumer must treat that as a one-element list.
- The two are deliberately independent: content can change without re-confirmation, and facts
  can be re-confirmed without regeneration. That is why you leave old `verified` entries in
  place when you edit a concept.

**Trust tiers**, which consumers derive from `verified` alone:

| `verified` | Tier |
|------------|------|
| absent | unverified |
| non-`human:` actors only | machine-confirmed |
| any `human:<id>` actor | human-reviewed |

**Actor convention**, used by every `by` field:

| Form | For | Example |
|------|-----|---------|
| `<producer>/<version>` | an agent or tool | `enrichment_agent/2.1` |
| `human:<id>` | a person | `human:ahormati` |
| `process:<id>` | an automated process | `process:finance-nightly` |

Consumers key trust off the `human:` prefix, so it must never appear on content a person did
not write or confirm. Bundles also use `team:<id>` for a `sources[].author`.

## Lifecycle: `status` and `stale_after`

```yaml
status: stable                      # draft | stable | deprecated; absent means stable
stale_after: 2026-09-23T00:00:00Z   # the content is stale once now >= this instant
```

`stale_after` is an absolute instant rather than a relative lifetime, so staleness is a plain
comparison that does not depend on when the concept was read.

## Timestamps and paths

Every timestamp is an ISO 8601 datetime with an explicit UTC offset: `2026-06-30T14:00:00Z`.
A bare date is not valid. Quote a timestamp if your writer would otherwise emit it unquoted in
a way a YAML parser turns into a native date — either form parses, but keep one style per
bundle.

Path-valued fields (`resource`, `sources[].resource`, `computation`, `executor.resource`,
`attester.resource`) each accept an absolute URL, a bundle-relative path beginning with `/`,
or a relative path.

## Attested computations

`type: Attested Computation` is a standalone concept carrying a sanctioned way to compute a
value, so a consumer can confirm the value came from running it and not from an agent's
improvisation. Provenance answers "where did this claim come from"; attestation answers "was
this number produced the way we said it must be".

Each figure is its own concept because trust state is per computation: revenue can be fresh
while margin is past its `stale_after`, and each attests on its own run. A narrative concept
links to one computation per figure rather than embedding them.

| Key | Required | Value |
|-----|----------|-------|
| `runtime` | **yes, for this type** | The engine that runs the computation, and therefore what `parameters` mean — a warehouse, a transformation tool, `python`. It tells the executor and attester how to read everything else. |
| `parameters` | recommended | The typed, named holes an agent may fill: `{ name, type, required }` entries. |
| `computation` | either/or | Path to a file holding the computation. Omit it to put the computation inline instead. |
| `executor` | recommended | `resource` names run instructions or code; `receipt` lists the fields a run must return as evidence. |
| `attester` | recommended | `resource` names deterministic, no-LLM code that inspects a receipt and returns a verdict. |

```markdown
---
type: Attested Computation
title: Revenue for fiscal year
description: Recognized revenue for a fiscal year, per Finance's definition.
tags: [finance, revenue]
status: stable
runtime: warehouse-sql
parameters:
  - { name: year, type: integer, required: true }
executor:
  resource: references/executors/run-on-warehouse.md
  receipt: [job_id, executed_sql, result]
attester:
  resource: references/attesters/revenue.py
generated: { by: enrichment_agent/2.1, at: 2026-06-20T22:53:05Z }
verified: { by: human:ahormati, at: 2026-06-25T09:00:00Z }
stale_after: 2026-09-23T00:00:00Z
sources:
  - id: rev-policy
    resource: https://wiki.acme/finance/revenue-recognition
    title: Revenue recognition policy
---

# Computation

    SELECT SUM(amount) AS revenue
    FROM finance.recognized_revenue
    WHERE fiscal_year = @year

The computation binds only the declared `parameters`, per the recognition policy.[^rev-policy]

[^rev-policy]: Revenue recognition policy
```

Give the computation exactly one way: a single fenced block under a `# Computation` heading
(best when it is short enough to review beside the contract), or a `computation:` path with no
body fence (best when it is long, generated, or already a real file shared with other
tooling).

**The rule that matters when consuming one:** supply values for the declared parameters and
nothing else. Binding the computation with those values is the consumer's job, and the
attester independently re-derives the same binding to compare against what actually ran —
which is why a rewritten query, a swapped computation file or a mutated dependency fails the
check. Editing the computation turns a mechanical comparison into a judgement call, which is
the one thing the type exists to prevent.

A consumer's sequence, for context: discover by `type`, load the contract and computation,
parameterise, execute via the executor to get a receipt, run the attester over the receipt,
then refuse to display a failing attestation and warn past `stale_after`. Receipts and
verdicts are runtime artifacts — never write them into the bundle.

`verified` and attestation are different things and both exist: `verified` confirms the
*definition* still matches policy and is recorded in the bundle; attestation confirms a single
*run* produced the value the sanctioned way and is not.

## Conformance

A bundle conforms when every non-reserved `.md` file has parseable YAML frontmatter
containing a non-empty `type`, and `index.md` / `log.md` follow their structures. Consumers
must not reject a bundle for missing optional fields, unknown `type` values, unknown extra
keys, broken cross-links, or missing `index.md` files.

That permissiveness is why `scripts/check_bundle.py` also reports warnings and notes: the
things it flags are all legal, and all still mistakes.

## Reading an older bundle

Two fields from version 0.1 still appear in the wild:

- `timestamp` — superseded by `generated: { by, at }`. Treat it as the last content change.
- a body `# Citations` list — superseded by the `sources` frontmatter.

When you edit such a file, migrate it: move citations into `sources` with stable `id`s, and
replace `timestamp` with a `generated` mapping naming yourself and the current time.

---

Based on the Open Knowledge Format specification v0.2:
https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
