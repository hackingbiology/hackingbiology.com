# Response to the ChatGPT critique of biohack.it — proposal, not yet actioned

Source: https://chatgpt.com/share/6a84d52d-d614-83eb-956c-93261224aa50 ("Analisi di Biohack It").
Written 2026-08-19, for review with Fabio before anything is implemented. Nothing in this note
has been applied to biohack.it or hackingbiology.com — it is a proposal.

## How to read the source critique

It's a solid outside read — better calibrated than most AI critique, and it says so itself
("ChatGPT is AI and can make mistakes"). Treat it as one informed opinion, not a verdict. Its
numeric scorecard (Idea 9/10, Scope discipline 5/10, etc.) is a gut-check, not a grade to chase.

## Accept as-is

- **The homepage undersells the project relative to the spec.** True, cheap to fix, zero risk —
  pure copy work.
- **The old Hacking Biology blog reads as "garage biohacker"; BIOHACK.IT needs an infrastructural
  voice.** This *confirms* a separation already built into the 2026-08-18 hackingbiology.com
  rebuild (blog = personal notebook, explicitly becoming purely personal; Foundation = accountable
  institutional voice). Not a gap — a validation.
- **"Community is the quality control" is too hacker-register for medicine.** ChatGPT's rewrite —
  *"Community review + deterministic validation + expert oversight"* — is good and worth adopting
  verbatim or close to it.
- **The real asset is standardization, not AI/biohacking/longevity.** Strong unifying line for both
  sites: the Foundation guarantees the standard stays open; biohack.it makes it usable day to day.
- **Claim-language discipline**: "Among qualifying users exposed to X, the observed change was Y"
  instead of "X causes Y". Cheap, should become an editorial rule everywhere a number is shown.
- **Negative results as a cultural value** ("I tried X. Nothing happened.") — free, high-authenticity,
  worth adding to copy immediately.
- **MVP is too wide (144 requirements).** Accept the discipline; don't accept "delete the vision" —
  the spec can stay ambitious, what needs discipline is *sequencing*, not scope of the document.

## Where I'd push back or calibrate

**"Distributed trial" should become "distributed observational research network".**
Disagree with the blanket rename — Fabio explicitly wants to keep leaning on "distributed trial",
and there's a real middle path: keep it for *narrative register* (tagline, deck, "From one person
to a distributed trial") and use more precise language only where a *specific data claim* is being
made (data pages, API responses, individual result displays). That gets the punch of the phrase
without the risk ChatGPT is flagging — the risk is claim-by-claim, not the vision statement.

**Scientific Advisory Board + Clinical Safety Board are "almost mandatory".**
Agree on direction, disagree on urgency — these are real people to recruit, not a copy change.
Belongs on the roadmap as a governance milestone, with honest "in formation" framing on the
Foundation page in the meantime. Never claim a board that doesn't exist yet.

**Genomics public-by-default is "aggressive".**
This is the one point I'd flag as genuinely serious — but it's a product/data-architecture decision
on biohack.it, not something fixed by editing a website. Surfacing it for Fabio's decision, not
deciding it here and not burying it.

**The numeric scorecard.**
Directional colour from one AI reading public specs, not a rigorous multi-expert review. Don't
chase the numbers up; chase the underlying issues if they're real problems on their own merits.

## What to bring into copy now (zero engineering risk)

1. Secondary tagline on biohack.it, under "An open laboratory for longevity":
   **"Turn self-experimentation into evidence."**
2. Reposition from "platform for biohackers" to
   **"Open infrastructure for structured human self-experimentation."**
   Slots naturally next to the existing Foundation language ("open infrastructure for longevity
   research") — a refinement, not a rewrite.
3. The **GitHub equivalence table** (Protocol=repository, Fork=protocol copy, Commit=dose change,
   CI=safety monitoring, Issues=disputed claim, Release=protocol version, Telemetry=biomarkers,
   README=doctor sheet, Dataset=research output) — full version as a deck slide (it's a perfect
   explainer visual) and on biohack.it's homepage or a "How it works" section (product mechanics,
   biohack.it's territory). On hackingbiology.com, at most one callback line, not the full table —
   it belongs to the product site, not the Foundation site.
4. Two new rows in the Foundation's existing "What could go wrong" table (the right home for this —
   the table already primes readers for self-criticism): statistical methodology still immature;
   genomics-public-by-default handled with deliberate caution.
5. A line on negative results as a cultural value, in biohack.it's About or guarantees.
6. Keep **"From one person to a distributed trial"** as the strongest narrative anchor — ChatGPT
   itself calls it the most important phrase in the spec — paired with the calibration above.

## Structural additions (more effort, still mostly writing)

- A **"Scientific Method" / "How evidence works here"** page on biohack.it: what can and cannot be
  inferred from the data, N-of-1 vs RCT, confounding/bias named explicitly. Directly answers the
  researcher persona's strongest objection.
- Extend the Foundation's governance section to name Scientific Advisory Board + Clinical Safety
  Board as planned structures — "in formation", not pretend-populated.

## Proposed MVP roadmap

Adopting ChatGPT's MVP cut close to as-is — it's sound product discipline — sequenced in phases:

**Phase 0 — Positioning (days, copy only).** Everything above. Ships without touching the product.

**Phase 1 — MVP core.**
1. Protocol data model (Substance → SafetyRule → Biomarker → Measurement) — already spec'd, build it.
2. Blood/biomarker layer: LOINC/UCUM, one working lab-import path.
3. Safety gate: baseline + risk acknowledgement required before activating a protocol — the spec
   already requires this; **verify it's actually enforced in the build, not just documented.**
4. Doctor protocol sheet — single-page clinician-readable export. High credibility, low novel risk.

Explicitly deferred out of MVP: procurement, advanced nutrition, social features/leaderboards,
genomics public-by-default.

**Phase 2 — Evidence & trust.**
5. Three flagship protocols with real demonstration data: rapamycin monitoring, a metabolic
   intervention, exercise/VO₂max.
6. "Evidence Confidence" annotations (value + uncertainty + provenance + evidence level) on key
   numbers.
7. First publication — not "rapamycin works", but a methods paper/preprint: *"An open data model
   for structured longitudinal self-experimentation in longevity."*

**Phase 3 — Governance & scale.**
8. Recruit Scientific Advisory Board + Clinical Safety Board (3–4 credible names each, to start).
9. Decide and implement the genomics privacy policy (opt-in publication, not public-by-default).
10. Research API — cohort/intervention/biomarker queries on de-identified, annotated data.

**Definition of "MVP done"** — adopt ChatGPT's numbers as a literal scoreboard rather than another
feature list: 100 users · 10,000 lab reports · 20 protocols · 3 cohort analyses · 1 published
dataset · 1 paper/preprint.

## What I would not do

- Not renaming "distributed trial" away from the narrative.
- Not treating the 12-point critique as a mechanical checklist to clear all at once — several items
  are institution-building work (boards, publications) that takes months and shouldn't gate the
  copy/MVP work.
- Not chasing the numeric scorecard as a target.
- Not doing ChatGPT's offered "second pass" (30–50 requirement-level red-team objections) yet —
  useful once there's a working system to red-team against; premature before Phase 1 ships.
