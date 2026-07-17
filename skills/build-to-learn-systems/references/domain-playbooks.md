# Domain playbooks

This skill works for any buildable system. The **structure** never changes — phases,
ADRs, SPECs, milestones, "break it" tests. Only the **content** does.

Read the playbook for the learner's domain before writing the Roadmap. Each is short
on purpose: enough to stop you transplanting server metaphors into a game course, not
a tutorial on the domain.

> The failure mode this file exists to prevent: writing "Docker / migrations /
> brokers" sections into a Unity course because the bundled example course had them.
> **Translate, don't transplant.**

## The structural spine (identical in every domain)

| Element | The question it always answers |
|---------|-------------------------------|
| **Phase** | What is the next self-contained thing that runs? |
| **Milestone** | What can the learner *see* working at the end? |
| **ADR** | Which real choice did we make, and what did we reject? |
| **SPEC / FR** | What does it do? |
| **SPEC / NFR** | How good is it — along the axis that matters *here*? |
| **"Break it" test** | How does it fail, and what does the failure look like? |
| **Hands-on loop** | Fast feedback first; production shape later |

Every domain has all seven. The rest of this file is how each one is spelled.

---

## Game client (Unity, Godot, Bevy, custom engine)

**Phase 0 milestone:** something rendered and moving — a rotating object plus a
health-check log. Visual proof the toolchain lives.

**Typical phase arc:** environment → maths/types → game loop & state → player &
movement → data → asset generation → gameplay systems → visuals → UI → build.

**ADR topics that actually come up:** engine version pinning (match the reference!),
render pipeline (built-in vs URP/HDRP), folder structure, custom physics vs the
engine's, baking assets offline vs generating at runtime, LOD strategy, input system.

**NFR axes that matter:** frame time (not "latency"), memory/GC pressure, load time,
draw calls, frame-rate independence, determinism if networked.

**"Break it" tests:** delete a semicolon → see the compile error; unassign an
Inspector reference → `NullReferenceException`; remove `Time.deltaTime` → movement
speed changes with frame rate.

**Hands-on loop:** Editor play mode (instant) → then a real build.

**Traps:** don't teach `Rigidbody` where the reference hand-rolls motion; don't treat
scenes as "environments" in the server sense; Inspector wiring is part of the
hands-on and must be written out step by step.

**No such thing here as:** ports, migrations, brokers, deploys. Don't invent them.

---

## Game server (authoritative multiplayer, matchmaking, state sync)

**Phase 0 milestone:** a client connects, sends a packet, gets a reply — plus a
health endpoint.

**Typical phase arc:** environment → transport (TCP/UDP/WebSocket) → protocol &
serialisation → connection lifecycle → authoritative state → tick loop → client
prediction & reconciliation → matchmaking → persistence → scaling.

**ADR topics:** UDP vs TCP vs WebSocket, tick rate, snapshot vs delta vs event
sourcing, authority model, serialisation format, interest management, room sharding.

**NFR axes:** tick budget, p99 latency, bandwidth per client per second, concurrent
players per node, cheat resistance, reconnection behaviour.

**"Break it" tests:** kill the server mid-session → watch the client reconnect;
inject 200ms latency and packet loss → watch prediction fight reconciliation; send a
malformed packet → confirm it's rejected, not crashed.

**Hands-on loop:** local server + 2 clients → then containerised.

**Traps:** this is where game *and* backend vocabulary both apply — be explicit about
which side of the wire each phase is on.

---

## Web

"Web" is three different animals. Pick the right sub-playbook — the wrong one
produces advice that is subtly wrong throughout.

| Sub-domain | Examples | The thing that defines it |
|------------|----------|---------------------------|
| **(a) SPA** | React, Vue | Runs in the browser; deploy is a static host |
| **(b) Meta-framework** | Next.js, Nuxt | **Has a server**; it's a full-stack course |
| **(c) Creative / 3D** | Three.js, WebGL | **Has a render loop**; closer to a game |

### (a) SPA — React, Vue

**Phase 0 milestone:** dev server up, one component rendering, HMR confirmed working
(change text → see it without a refresh).

**Typical phase arc:** environment & tooling → component model → state → data fetching
→ routing → forms & validation → performance → accessibility → testing → build/deploy.

**ADR topics:** framework (React vs Vue), state management (local vs
context/provide-inject vs a store — Redux/Zustand/Pinia), styling (CSS Modules vs
Tailwind vs CSS-in-JS), bundler (Vite vs webpack), data-fetching strategy (TanStack
Query vs hand-rolled), TypeScript or not, component library vs bespoke.

**NFR axes:** bundle size, Core Web Vitals (LCP/INP/CLS), time-to-interactive,
accessibility (WCAG), re-render cost.

**"Break it" tests:** throttle the network to Slow 3G → watch the loading states you
wrote actually appear; navigate with the keyboard only → find the focus traps; render
a 10k-row list → watch it jank; throw inside a child → confirm the error boundary
catches it instead of blanking the app.

**Hands-on loop:** dev server with HMR (instant) → then production build + preview.

**Traps:** React and Vue have **fundamentally different reactivity models** — VDOM
diffing with explicit dependencies vs proxy-based automatic tracking. Do not write
React idioms (`useEffect` deps, memoisation) into a Vue course; Vue's equivalent
problems are different ones. "Deploy" here is a static host, not a service.

### (b) Meta-framework — Next.js, Nuxt

<!-- The important correction: this is NOT "frontend with extras". -->

> **A Next.js/Nuxt course is a full-stack course.** These frameworks run code on a
> server. Half the backend playbook applies (auth, caching, data access, deploy as a
> service). Treating it as "frontend plus some magic" is the classic way to produce a
> course that leaves the learner unable to debug their own app.

**Phase 0 milestone:** dev server up, a route rendering **on the server** — prove it
by viewing source and seeing real HTML, not an empty `<div id="root">`.

**Typical phase arc:** environment → file-based routing → rendering modes
(SSG/SSR/ISR/streaming) → server vs client component boundary → server-side data
fetching → mutations (server actions / API routes) → auth & sessions → caching &
revalidation → deploy.

**ADR topics:** rendering mode *per route* (not one global choice), where the
server/client boundary sits, data fetching location, caching + revalidation strategy,
auth model (session cookie vs JWT), where mutations live (server actions vs API
routes vs a separate backend), deployment target (managed platform vs self-hosted
Node vs static export).

**NFR axes:** TTFB, Core Web Vitals, cache hit ratio, server response time, cold-start
time, and **JS shipped to the client** (the whole point of server rendering is
shipping less).

**"Break it" tests:** disable JavaScript → confirm the page still renders (proves SSR
is real); let a cache entry go stale → confirm revalidation fires; kill the upstream
API → confirm the error boundary / fallback appears rather than a white screen; put a
client-only API (`window`) in a server component → read the error and understand why.

**Hands-on loop:** dev server → production build → deploy preview.

**Traps:** the **server/client boundary is the core concept** — get it into the
vocabulary by Phase 1–2, not Phase 8. Most beginner bugs are boundary confusion. Also:
"it works in dev" is especially unreliable here; dev and production rendering differ.

### (c) Creative / 3D — Three.js, WebGL

**Phase 0 milestone:** canvas mounted, one lit cube spinning, an fps counter visible.

**Typical phase arc:** environment → scene/camera/renderer → **the render loop** →
geometry & materials → lighting → interaction & raycasting → shaders (GLSL) →
performance (draw calls, instancing) → asset loading (glTF).

**ADR topics:** raw Three.js vs react-three-fiber, camera model, asset format &
compression (Draco/KTX2), custom shader vs stock material, physics library or none,
who owns the render loop (`requestAnimationFrame` vs the framework).

**NFR axes:** **frame time** (a 16.6 ms budget at 60 fps), draw calls, triangle count,
GPU memory, asset download size, time-to-first-frame.

**"Break it" tests:** drop in a 10 MB uncompressed texture → watch frame time
collapse; spawn 10k meshes without instancing → watch draw calls kill it; remove a
`dispose()` and re-create objects in a loop → watch GPU memory climb until it dies;
remove the delta-time multiply → watch speed change with frame rate.

**Hands-on loop:** dev server with HMR → then production build.

**Traps:** **the render loop is a game loop** — read the *game client* playbook above,
not the SPA one. Frame-rate independence matters exactly as it does in Unity. If using
**react-three-fiber** you have two models at once (React reconciliation *and* an
imperative render loop); that tension is real and deserves its own ADR.

### Web sub-domain not listed?

Design systems / component libraries lean on (a) but swap the NFR axes for API
ergonomics, versioning, and documentation coverage. Static-site generators (Astro)
sit between (a) and (b) — decide by asking whether there's a server at runtime.

---

## Backend / distributed (APIs, chat, queues, caches)

This is the domain the bundled example course covers — see
`references/example-evergreen-context.md`.

**Phase 0 milestone:** service starts, health endpoint answers, container runs.

**Typical phase arc:** environment → transport/protocol → data model & migrations →
auth → core domain → realtime → persistence & caching → observability → scaling.

**ADR topics:** language/runtime, sync vs async, SQL vs NoSQL, broker choice, auth
model, schema evolution, idempotency, deployment target.

**NFR axes:** throughput, p99 latency, durability, ordering guarantees, consistency,
availability, cost per unit.

**"Break it" tests:** stop the database → confirm the service reports unhealthy
rather than lying; kill a consumer mid-message → confirm redelivery; replay a
duplicate request → confirm idempotency.

**Hands-on loop:** run locally → then docker-compose → then production shape.

---

## Systems & tooling (compilers, interpreters, databases, CLIs)

**Phase 0 milestone:** the binary builds and runs; `--version` prints; one trivial
input produces one correct output end to end.

**Typical phase arc (compiler):** environment → lexer → parser → AST → semantic
analysis → IR → optimisation → codegen → runtime.

**ADR topics:** implementation language, hand-written vs generated parser, IR design,
error-reporting strategy, memory model, testing strategy (golden files? fuzzing?).

**NFR axes:** correctness first, then compile time, memory, error-message quality.

**"Break it" tests:** feed deliberately malformed input → confirm a *useful* error
with position, not a panic; fuzz it → confirm no crash.

**Hands-on loop:** REPL or single-file input → then a real test corpus.

**Traps:** correctness dominates; a "milestone" is a passing test on real input, not
something visual.

---

## Data / ML (pipelines, feature stores, RAG)

**Phase 0 milestone:** the pipeline runs end to end on 10 rows and writes an output
you can open.

**Typical phase arc:** environment → ingestion → validation → transformation →
storage → training or indexing → serving → evaluation → monitoring.

**ADR topics:** batch vs streaming, storage format, orchestration, feature
computation (offline/online), model registry, evaluation metric, drift detection.

**NFR axes:** correctness, reproducibility (same input → same output), freshness,
throughput, cost per run, training/serving skew.

**"Break it" tests:** feed a row with a null in a required column → confirm it's
quarantined, not silently averaged; re-run yesterday's job → confirm identical
output.

**Traps:** "it ran" is not "it's correct". Every phase needs a data-quality assertion,
not just a green checkmark.

---

## Domain not listed?

Derive the playbook from the spine at the top:

1. What can the learner **see working** after one sitting? → Phase 0 milestone.
2. What are the **real decisions** with defensible alternatives? → ADR topics.
3. Along which axis does "good" get measured *here*? → NFR axes.
4. How does it **fail**, and what does that look like? → "break it" tests.
5. What's the **fastest feedback loop** available? → hands-on loop.

Then write it down in the manifest so later sessions stay consistent.
