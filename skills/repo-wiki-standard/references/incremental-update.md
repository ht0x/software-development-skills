# Incremental updates, manifest, and protected content

The wiki is a *living* artifact: after the first generation it should update in
place as the code changes, regenerating only what's affected and never trampling
human edits. Two mechanisms make this work — the **manifest** and **protected
blocks**.

## The manifest — `<output>/.wiki_manifest.json`

A machine-managed file inside the chosen output path (default `docs/wiki/`),
mapping each page to the source files it was built from, with content hashes.
Regenerate it every run. It also stores the resolved `output` path and
`languages` so later runs reuse the user's Phase 0 choices.

### Schema

```json
{
  "version": 1,
  "generatedAt": "2026-07-06T00:00:00Z",
  "output": "docs/wiki",
  "template": "architecture",
  "languages": ["en"],
  "pages": [
    {
      "path": "en/01-Architecture-Overview.md",
      "title": "Architecture Overview",
      "language": "en",
      "sources": [
        { "file": "src/app.ts", "hash": "a1b2c3d4..." },
        { "file": "src/server.ts", "hash": "e5f6a7b8..." }
      ]
    }
  ]
}
```

### Hashing

Use Git's blob hash for each source file so it's cheap and reproducible:

```bash
git hash-object <file>
```

Store the hash per source per page. Record the exact set of files a page cites,
so change detection is precise.

## Change detection (update run)

1. Load the manifest.
2. For each page, recompute `git hash-object` for every recorded source.
3. Mark a page **stale** if any source's hash changed, a cited source was deleted,
   or a newly relevant source appeared in its module/scope.
4. Regenerate only stale pages. Recompute `Home.md` only if the page *set* changed
   (page added/removed/renamed).
5. Rewrite the manifest with fresh hashes and timestamp.
6. Report to the user: pages updated / added / removed, each with the triggering
   source file(s).

If a page's Markdown was edited by a human (outside a protected block) but its
sources are unchanged, treat it as intentional and do **not** overwrite it —
report the situation and ask before touching it.

## Protected blocks — human edits that survive regeneration

Any content a person wants to keep permanently is wrapped in markers. Automatic
regeneration copies these blocks through verbatim and rebuilds only the
surrounding generated content.

```markdown
<!-- wiki:protected -->
## Team notes (hand-written)

This subsystem has an undocumented quirk: the retry queue must drain before
migrations run. Keep this here.
<!-- /wiki:protected -->
```

Rules:

- Never modify, reorder, or delete text between `<!-- wiki:protected -->` and
  `<!-- /wiki:protected -->`.
- When regenerating a page, extract its protected blocks first, generate the new
  body, then re-insert each protected block at its original anchor (match by
  nearest preceding heading; if ambiguous, append them under a "Protected notes"
  section and tell the user).
- Protected blocks let teams embed human judgment that becomes a durable knowledge
  asset — the same guarantee Qoder's Repo Wiki gives manually revised knowledge.

## Git-based sharing

The output directory (default `docs/wiki/`, or wherever the user chose) — pages
plus `wiki_plan.yaml` and `.wiki_manifest.json` — is committed and pushed like any
other source. Teammates `git pull` to get the wiki; there's no
separate store. When two people regenerate independently, the manifest + protected
blocks keep merges sane: resolve Markdown conflicts as normal, then run an update
to reconcile hashes.
