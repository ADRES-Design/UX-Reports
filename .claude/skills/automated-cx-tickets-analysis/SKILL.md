---
name: automated-cx-tickets-analysis
description: "Runs the monthly CX ticket analysis for ADREC's DARI platform end-to-end and fully autonomously — no confirmation, review, or approval checkpoints — turning a Freshdesk ticket export into validated codes, themes, a month-over-month HTML dashboard, and an updated codebook. Reads and writes fixed paths inside the repository (data/, Template/, previous-codebook/, dashboards/, updated-codebook/), so it works unattended inside a scheduled Claude Code routine as well as in chat. Use this skill whenever the user mentions DARI tickets, Freshdesk exports, CX analysis, support ticket analysis, pain points, issue categories, critical issues, service analysis, MoM comparison, a codebook, or a CX insight dashboard — even if they do not name the skill, and even if they only say something like 'run July's analysis' or 'the monthly dashboard'."
---

Role: You are a Senior Qualitative UX Research Lead. Your goal is to conduct a rigorous analysis of this month’s DARI support tickets to identify the following:
Objective: Identify recurring user pain points, operational issues, and service-level patterns to support product improvements and decision-making.

AUTONOMY CONTRACT (read first — governs every state below)
* Execute STATE 1 → STATE 7 in a single uninterrupted run. Never pause for confirmation, review, sign-off, or clarification.
* Never ask the user a question mid-pipeline. If an input is missing or ambiguous, apply the FIXED CONTEXT and REPOSITORY PATHS rules below, proceed, and log the assumption in the Self-Audit Appendix.
* All exit criteria are self-verified against the deterministic checks defined per state. A failed check triggers at most 2 internal correction cycles, then the pipeline proceeds with the best available version and records the residual gap in the Self-Audit Appendix.
* Deliver the finished HTML dashboard and updated codebook to the paths in REPOSITORY PATHS without asking whether to produce them.
* Never ask which product, client, month, template, or codebook to use. All five are resolved by the sections below.
* Autonomy never licenses invention. Anti-fabrication rule: never create a ticket ID, quote, count, or service name that is not present in the supplied dataset. Missing data is reported as missing, not estimated.

FIXED CONTEXT (never ask, never infer)
* Client — ADREC (Abu Dhabi Real Estate Centre). Always.
* Product — DARI. Always. This skill covers DARI and nothing else. Never ask which product is being analysed.
* Scope of the export — every dataset given to this skill is DARI data by definition. There is no product column and none is expected. Analyse every row.
* Never drop, filter, or exclude rows on product grounds. Do not try to infer product from service names, group names, or subject text: DARI's own service names include Valuation, Broker Services, and Tenancy Contract, so any such inference would silently discard genuine DARI tickets. Silently shrinking the dataset is the most damaging error this skill can make.
* Rows are only ever removed for the two mechanical reasons in DATASET INGESTION: duplicate ticket IDs, and rows that are structurally empty. Both are counted and reported.

RESOLVING THE ANALYSIS MONTH
Everything below depends on two values. Resolve them first, print them, and use them consistently.
* `MONTH` — the lowercase English name of the month whose data is being analysed (`january` … `december`).
* `PERIOD` — that same month as `YYYYMM`.
* `PRIOR_PERIOD` — the calendar month immediately before it, as `YYYYMM`.

Resolve them in this order:
1. If the user names a month, use it. "analyse July's data" → `MONTH=july`.
2. Otherwise use the previous calendar month relative to today. This is the unattended default: a run on 2026-08-04 analyses July 2026.
3. Derive the year from context (the data folder present, the user's message, or today's date). Never guess a year that contradicts the folder that actually holds data.

Worked example — analysing July 2026:
`MONTH=july`, `PERIOD=202607`, `PRIOR_PERIOD=202606`

REPOSITORY PATHS (the only locations this skill reads from or writes to)
All paths are relative to the repository root. Never write to `/mnt/user-data/outputs/` — that folder does not exist in a routine run.

READ:
* Dataset — `data/<PERIOD>/` — use every `.xlsx` file in that folder. If the folder is missing or holds no `.xlsx`, stop and report that the export has not arrived. Do not fabricate a dataset and do not substitute another month's data.
* Dashboard template — `Template/` — use the `.html` file in that folder exactly: same layout, same colours, same section order. If the folder is empty or absent, fall back to the canonical Output Structure below and log the fallback.
* Previous codebook — `previous-codebook/<PRIOR_PERIOD>/codebook.docx` — for July 2026 that is `previous-codebook/202606/codebook.docx`. Read `.docx` with `python-docx`; `pip install python-docx` if it is not available. If the file is absent, bootstrap a new codebook from the STATE 1 seeds plus the full dataset, label it `v1 — bootstrapped`, and log it.
* Previous dashboard — `dashboards/` — the most recent `*-dashboard.html` other than the current month's, used for the MoM layer. If none exists, set MoM to "No prior baseline available — first cycle" and populate current-month figures only. Never back-fill or estimate prior-month numbers.

WRITE:
* Dashboard — `dashboards/<MONTH>-dashboard.html` → e.g. `dashboards/july-dashboard.html`
* Updated codebook — `updated-codebook/<MONTH>-codebook.docx` → e.g. `updated-codebook/july-codebook.docx`
* Codebook carry-forward — also write the same codebook to `previous-codebook/<PERIOD>/codebook.docx` → e.g. `previous-codebook/202607/codebook.docx`. This is what makes next month's run self-sufficient: next month resolves `PRIOR_PERIOD=202607` and finds the file already there, with no human copying anything. Create the folder if needed.

Create any missing output folder rather than failing. Overwrite an existing output file for the same month only if the user explicitly asked for a re-run; otherwise stop and report that the month is already complete.

DATASET INGESTION
Load the dataset in full, in one pass. Every row is in scope. There is no 50/50 split and no holdout. If the export arrives as multiple files, merge them, de-duplicate on ticket ID, sort by created date (fallback: ticket ID ascending), and treat the result as one single set. Count rows read, duplicates removed, and rows analysed, and report all three in the Self-Audit Appendix. Chunking may be used internally for context management only; it must never change the codebook mid-dataset.

Analysis Requirements:
1. Pain Points
* Identify the main user pain points across all tickets.
* Focus on friction, confusion, blockers, failures, delays, or usability concerns.
* Include example Ticket IDs for each identified pain point to support verification.
2. Issue Categories
* Categorize tickets into clear issue groups (e.g., technical issue, UX issue, integration issue, business/process issue, data issue, payment issue, access issue, etc.).
* Ensure categories are consistently applied.
* Include representative Ticket IDs for each category.
3. Repeated Issues
* Identify the most frequently recurring issues and patterns.
* Highlight trends or recurring root causes.
* Include example Ticket IDs for each repeated issue pattern.
4. Top 10 Critical Issues
* Identify the top 10 most critical issues based on:
    * frequency,
    * business impact,
    * user impact,
    * operational risk,
    * or service disruption severity.
* Explain why each issue is considered critical.
* Include supporting Ticket IDs for validation.
5. Top 5 Services with Highest Issue Count For the top 5 affected services:
* Calculate issue count per service.
* Identify the most repeated issue types within each service.
* Highlight service-specific patterns.
* Include example Ticket IDs for the reported findings.
6. Service Distribution
* Provide distribution of tickets across related services.
* Show which services receive the highest concentration of support tickets.
* Include sample Ticket IDs where relevant.

Analysis Instructions:
* Focus on actionable insights, not only summaries.
* Group similar issues when appropriate.
* Avoid duplicate findings.
* Prioritize clarity, structure, and evidence-backed observations.
* Surface both operational and UX-related implications where relevant.
* Every major finding must include at least 1–3 supporting Ticket IDs for traceability and verification.

Output Structure (HTML Dashboard):
1. Executive Summary
2. Key Pain Points
3. Issue Categories Breakdown
4. Repeated Issues & Patterns
5. Top 10 Critical Issues
6. Top 5 Services Analysis
7. Service Distribution
8. Month-over-Month (MoM) Comparison
9. Strategic Recommendations
10. Self-Audit Appendix (see below)
Maintain a concise, professional, and research-oriented tone.

OPERATIONAL RULES
VERACITY PROTOCOL:
1. Never paraphrase user quotes — use verbatim text only.
2. Every quote must include ticket ID.
3. If missing, use User 1 / User 2 or transcript filename.

PROJECT CONTEXT:
Client: ADREC (Abu Dhabi Real Estate Centre)
Product: DARI — the public-facing real estate services platform for the Emirate of Abu Dhabi
Goal: Identify user pain points and issues to reveal opportunities for enhancements and recommend solutions.

AMBIGUITY PROTOCOL (non-blocking):
1. Do not guess unclear meaning.
2. Mark unclear segments as [QUERY_FOR_HUMAN] — this is a label for later reading, never a stop condition.
3. Code the ticket to its best-fit existing code with confidence = Low, or to `UNCODABLE` when no code fits at all.
4. Record every flagged item in the Self-Audit Appendix with ticket ID and the reason for ambiguity.
5. If flagged items exceed 10% of the dataset, still complete the run and state the flag rate in the Executive Summary as a confidence caveat.

SELF-AUDIT APPENDIX (replaces human audit)
Appended as the final dashboard section, collapsible, containing:
* Resolved `MONTH`, `PERIOD`, and `PRIOR_PERIOD`, plus every input path actually read and every output path written.
* Inputs used and every default/inference applied (codebook version, ticket count ingested, template source, whether the template was found in `Template/` or fell back to the canonical structure).
* Row reconciliation: rows read from the export, duplicates removed, structurally empty rows removed, rows analysed. These must add up. If rows analysed is lower than rows read for any other reason, say so explicitly and name the reason — never let the dataset shrink unexplained.
* Coverage: tickets in, tickets coded, % coded, UNCODABLE count, [QUERY_FOR_HUMAN] count and rate.
* Codebook delta vs previous version: codes added / merged / split / renamed / deprecated, each with a rationale line and a mapping from the old code.
* Consistency result from STATE 3 (pass-1 vs pass-2 agreement rate, resolved disagreements) and the number of internal correction cycles run.
* Bias and negative-case findings from STATE 6.
* Residual gaps: any check that did not pass, stated plainly.
* Confidence rating (High / Medium / Low) with the reason.

STATE DEFINITIONS

STATE 1 — Interpretive Alignment
Goal: Ensure shared understanding of interpretation logic using fixed seeds.
Input:
* Client / Product — fixed as ADREC / DARI (see FIXED CONTEXT)
* Existing codebook — read from `previous-codebook/<PRIOR_PERIOD>/codebook.docx` (see REPOSITORY PATHS)
* seed1:

Input:“ user request to us: email 1: Dear Team
Please update the investor’s information accordingly
Best regards
email 2: Dear Sir or Madame,
Please update my e-mail address in the DARI.AE system into the correct one: [email address].
I am enclosing my pre-registration certificate and my passport details to identify verification. Also I confirm my phone number: [phone number].
Thank you in advance.
Best regards,
[Customer name]

our team response:
email: Dear RE Initial Registry Follow-up Team Thank you for reaching out to ADREC Customer Support Team. With reference to your request, we would like to inform you that the required action has been completed. Kindly review and let us know if you have any further inquiries. Sincerely, ADREC-Support Team ”

Output:
insight: users are forced to contact our support team to update their information like email and phone number
Pain Points:
- unable to update user information on our system, instead users ask our support team to update information.
Recommendations:
- Add a modify information feature inside the platform.

* seed2:
Input:“ User: Dear DARI team,
Kindly note that the below unit/contract has been closed without any request from our side. Please rectify this issue at the earliest in order to proceed with the contract renewal.
Contract No: 454377 Unit No: BS1-602 UNT No: UNT231108
Our team response: Dear [Customer name], Thank you for reaching out to ADREC Customer Support Team. With reference to your inquiry, please be informed that contract number 454377 has expired as of 31-10-2025. According to the procedures followed in the Emirate of Abu Dhabi, the system automatically closes the contract 90 days after its expiration date. Therefore, the contract cannot be reactivated, and a new contract must be registered for the concerned unit. Kindly verify and let us know if you have any further questions. Sincerely, ADREC-Support Team”
Output:
Insights:- User not aware of the business rule that after 90 days, contract will be closed automatically if not renewed this is based on rules and regulations https://adrec.gov.ae/en/rules_and_regulations
Pain Points:
- lack of knowledge regarding the automatic closing of contract after 90 days.
Recommendations:
- include in the service card (page prior to starting any service) this business rule in a clear UI.

Action:
* Analyze how coding is applied in both seeds
* Extract interpretation patterns:
    * Insight formation logic
    * Pain point extraction logic
    * Recommendation logic
* Align reasoning approach with baseline examples
Context Rule (Important):
* Scope is fixed: ADREC / DARI. Do not ask the user which product this is, and do not branch the workflow by product.
* Both seeds above are DARI tickets, so the interpretation patterns they encode are the right ones for every run of this skill.
* All outputs (codebooks, themes, dashboards) are framed as DARI under the ADREC client context.
* Month-to-month differences are handled by the data and the carried-forward codebook, never by changing workflow logic.
Exit Criteria (automated self-check, replaces human confirmation):
* Re-derive insight / pain point / recommendation from each seed input without looking at the seed output, then compare.
* PASS when, for both seeds: the insight names the same systemic cause, the pain point is user-framed (not team-framed), and the recommendation is a concrete platform change rather than a process suggestion.
* On FAIL: adjust the interpretation rules and re-derive (max 2 cycles), then proceed and log the mismatch in the Self-Audit Appendix.
* Alignment is asserted by the pipeline, never requested from the user.

STATE 2 — Codebook Enhancement (FULL DATASET, SINGLE PASS)
Goal: Improve existing codebook using the entire dataset in one pass.
Input:
* Existing codebook — `previous-codebook/<PRIOR_PERIOD>/codebook.docx`
* The complete dataset — every ticket, no split, no sampling
Action:
* Apply current codebook across all tickets in one sweep
* Identify improvements:
    * missing codes
    * overlaps / redundancy
    * unclear definitions
    * merges / splits / renames
* Only refine existing structure (no full rebuild unless necessary)
Output:
* Enhanced codebook (auto-accepted once the exit checks pass)
Exit Criteria (automated, replaces human review):
* Coverage: ≥95% of all tickets map to a code; UNCODABLE ≤5%.
* Every code carries: definition, inclusion rule, exclusion rule, and ≥1 real example Ticket ID.
* No two codes overlap semantically; near-duplicates are merged with the merge logged.
* Every change is recorded as add / merge / split / rename / deprecate with a rationale.
* Failing checks trigger up to 2 internal revision cycles, then proceed with the best version and log residual gaps.

STATE 3 — Consistency Validation (FULL DATASET, SECOND PASS)
Goal: Validate the enhanced codebook by re-coding the same complete dataset with the codebook frozen. Rigour now comes from re-coding consistency, not from a holdout split.
Input:
* The complete dataset again (same tickets — no split, no sample)
* Enhanced codebook from State 2, frozen for the duration of this pass
Action:
* Apply the codebook without modifying it
* Compare pass-2 codes against pass-1 codes ticket by ticket
* Identify:
    * disagreements between the two passes
    * edge cases
    * ambiguous mappings
    * uncodable items
    * inconsistencies (same pattern coded differently in different places)
Output:
* Final coded matrix covering 100% of tickets
* Consistency + issues report (agreement rate, disagreement list, uncodable list)
Exit Criteria (automated):
* Consistency PASS when pass-1 vs pass-2 agreement is ≥90% and no single unresolved pattern accounts for >5% of tickets.
* Disagreements are resolved in favour of the code whose inclusion/exclusion rule matches more literally; each resolution is logged.
* On FAIL: run exactly one refinement cycle in STATE 4, then freeze the codebook regardless of outcome and log the state.

STATE 4 — Refinement & Final Codebook
Goal: Final automated optimization of the codebook (no human editing step).
Input:
* Findings from State 2 + State 3
Action:
* Refine:
    * definitions
    * boundaries
    * examples
    * exclusions
* Merge learnings from the STATE 2 and STATE 3 passes
* Ensure backward compatibility
Backward-compatibility rule (automated): never silently delete a code that exists in a previous month's codebook. Mark it `DEPRECATED` and record an explicit old-code → new-code mapping so MoM comparison stays valid.
Output:
* Final codebook, frozen and version-stamped internally as `DARI-codebook-vN-<PERIOD>` (the version stamp goes in the document header; the filename follows REPOSITORY PATHS). Freezing is automatic; no approval is sought.

STATE 5 — Thematic Construction
Goal: Build interpretive themes from final coded dataset.
Action:
* Cluster codes into 3–5 themes
* Focus on WHY behavior occurs
* Do not introduce new codes
Exit Criteria (automated): 3–5 themes; every theme maps to ≥2 codes; every code maps to exactly one theme; no theme restates a single code's label.

STATE 6 — Theme Validation
Goal: Stress-test themes for bias and edge cases.
Action:
* Identify contradictions
* Surface negative cases
* Detect overgeneralization or bias
Exit Criteria (automated): for each theme, actively search for at least one disconfirming ticket; where a theme rests on <5 tickets, label it "Emerging — low evidence" rather than dropping or inflating it. Record all findings in the Self-Audit Appendix.

STATE 7 — Insight Synthesis & Dashboard Mapping (WITH MoM COMPARISON)
Goal: Convert themes into structured insights and build dashboard output using current + previous month data.
Inputs:
* Final codebook (current month, from STATE 4)
* Current month coded dataset + themes
* Dashboard template — `Template/` (see REPOSITORY PATHS)
* Previous month dashboard — most recent `dashboards/*-dashboard.html`; may be absent
* Previous month codebook — `previous-codebook/<PRIOR_PERIOD>/codebook.docx`; may be absent

Action:
* Map insights into existing dashboard structure (NO UI redesign)
* Build Month-over-Month (MoM) comparison layer exactly as defined in template:
    * compare themes vs previous month themes
    * compare code frequency shifts
    * identify increases/decreases in key pain points
    * highlight emerging vs disappearing issues
* Ensure alignment between:
    * previous month codes + current month codes (via the STATE 4 deprecation mapping)
    * previous dashboard metrics + current outputs
* Populate MoM tab using both datasets
* Append the Self-Audit Appendix as the final section.

Constraints:
* Must follow dashboard template exactly
* Must NOT redesign layout or colors
* Must NOT invent new metrics outside codebook + provided structure
* Where a prior-month figure does not exist, print "No prior baseline" — never interpolate.

Output & Delivery (automated, no confirmation step):
* Completed dashboard including:
    * current month insights
    * MoM comparison tab
    * structured HTML dashboard-ready output (template-compatible)
    * Self-Audit Appendix

Write all three files, in this order, without asking whether to save, render, or proceed:
1. `dashboards/<MONTH>-dashboard.html`
2. `updated-codebook/<MONTH>-codebook.docx`
3. `previous-codebook/<PERIOD>/codebook.docx` — identical content to (2); this is the carry-forward copy that lets next month run unattended.

Then report a 3–5 line summary covering ticket volume, top 3 pain points, confidence rating, and the paths written. If running in chat rather than a routine, also present the dashboard file.

Verify before finishing: all three files exist and are non-empty, the dashboard opens as valid HTML with all ten sections present, and the codebook contains every code with its definition, inclusion rule, exclusion rule, and ≥1 real example Ticket ID. Report any check that fails in the Self-Audit Appendix rather than silently proceeding.