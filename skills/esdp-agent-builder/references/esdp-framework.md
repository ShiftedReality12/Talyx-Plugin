# ESDP v1.0 Framework Reference

## 7 Mandatory Conditions

| # | Condition | Threshold | Evidence Required |
|---|-----------|-----------|-------------------|
| 1 | Trio Knowledge Types | K1 + K2 + K3 | Each type named and role described |
| 2 | Leverage Mechanism | >= 3x | Quantified multiplier with justification |
| 3 | 7 Processing Modules | M1-M7 | Each module named with domain-specific content |
| 4 | 20 Configuration Modes | 5O x 4T | Each mode defined with unique modifier |
| 5 | Embedded Knowledge | >= 50 assertions | Decision rules with WHEN/THEN/THRESHOLD |
| 6 | Validation Criteria | Quantified | 4+ criteria with numeric thresholds |
| 7 | Closed-Loop Learning | O5 mode | Learning capture architecture specified |

## Agent Spec Schema

```
AGENT-{INITIALS}-{NNN}: {Name}

Trio: K1 ({type}) + K2 ({type}) + K3 ({type})
Leverage: {N}x — {justification}
Domains: V-{CODE}, V-{CODE}, ...
Consumer: {Name} ({style})

## Operational Definition
{2-3 paragraphs}

## Leverage Mechanism
{Quantified: what takes X hours manually -> Y minutes with agent}

## Knowledge Type Classification
| Component | Type | Role |
| K1 | {type} | Primary analytical engine |
| K2 | {type} | Strategic/directional framework |
| K3 | {type} | Synthesis/quality layer |

## Processing Modules
M1: {Name} — {description with domain content}
M2-M7: ...

## Configuration Modes (5x4 = 20)
{Orientation x Time Horizon matrix}

## Embedded Knowledge (50+)
{Numbered decision rules with WHEN/THEN/THRESHOLD}

## Validation Criteria
{4+ quantified criteria}

## ESDP Compliance
{7-row table with PASS/evidence}
```

## Standard Agent Roles (3 per principal)

| Role | Primary Function | Typical Domains |
|------|-----------------|-----------------|
| Deal/Flow Radar | Screening, scoring, triage | V-DEAL, V-FINX, V-{asset} |
| Counterparty Intel | Behavioral profiling, competitive | V-PSYA, V-COMP, V-MKTX |
| Portfolio/Allocation | Risk, regime, rebalancing | V-PORT, V-FINX, V-ALTS |

## Actuarial Intelligence Agents

Three actuarial agents wire the 3,083-entry KB into the ESDP pipeline. Each satisfies all 7 mandatory conditions.

| Agent ID | Name | Domains | Archetype Trigger | KB Entries |
|----------|------|---------|-------------------|------------|
| ACT-001 | Actuarial Enrichment Orchestrator | V-PPLI, V-LOSS, V-RISK, V-PENS, V-INVX | Any actuarial archetype fires | 579 (HQ, mda >= 0.70) |
| ACT-002 | PPLI Qualification Analyzer | V-PPLI | ppli-specialist archetype | 701 (V-PPLI domain) |
| ACT-003 | Actuarial Provenance Tracer | All 9 V-domains | Any actuarial output generated | 3,083 (full KB) |

### ACT-001: Actuarial Enrichment Orchestrator

Trio: K1 (Actuarial KB — 3,083 entries, 9 domains) + K2 (Archetype triggers — 4 YAMLs) + K3 (IRC quality gate — 13-section whitelist)
Leverage: 8x — manual actuarial research per prospect takes ~4 hours; agent delivers in ~30 seconds
Domains: V-PPLI, V-LOSS, V-RISK, V-PENS, V-INVX, V-MORT, V-EMRG, V-HLTH, V-PROP
Consumer: Pre-Call Prep (Phase 0.9), ROB (M8), 9010 (Step 3.3)

Processing Modules:
- M1: Archetype Gate — evaluate prospect against 4 archetype trigger configs
- M2: Domain Selector — map archetype to relevant actuarial domains
- M3: KB Query — Cypher query against ActuarialEntry nodes (mda_composite >= threshold)
- M4: Epoch Tagger — attach temporal epoch labels to each entry
- M5: Provenance Assembler — build provenance block with KB version, source count, coverage
- M6: IRC Validator — validate all IRC citations against 13-section whitelist
- M7: Output Formatter — structure actuarial intel card for downstream consumption

Configuration Modes (5O x 4T):
- O1-Compliance x T1-Immediate: IRC-gated output for same-day call prep
- O2-Structuring x T2-Weekly: PPLI structuring depth for weekly advisor review
- O3-Risk x T3-Monthly: Loss/risk methodology overlay for monthly portfolio review
- O4-Pension x T4-Quarterly: DB plan de-risking intelligence for quarterly plan reviews
- O5-Learning x T1-Immediate: Capture which actuarial entries produce advisor engagement

### ACT-002: PPLI Qualification Analyzer

Trio: K1 (V-PPLI KB — 701 entries, 15 PPLI dimensions) + K2 (IRC statutes — 267 entries) + K3 (Epoch currency — 6 epochs)
Leverage: 12x — manual PPLI qualification analysis takes ~6 hours; agent delivers in ~30 seconds
Domains: V-PPLI
Consumer: ROB M8 (PPLI-specialist archetype), Cortex synthesis, advisor deliverables

Processing Modules:
- M1: Section 7702 Qualification Check — corridor test, guideline premium, cash value accumulation
- M2: Section 817(h) Diversification Test — investor control doctrine analysis
- M3: COI Benchmarking — cost of insurance comparison across carrier structures
- M4: Estate Planning Integration — GRAT/CLAT/dynasty trust PPLI overlay
- M5: Epoch Currency Validator — flag pre-TCJA assumptions, prioritize POST_CAA_2021
- M6: Competitive Contrast Generator — provenance-backed vs carrier illustration positioning
- M7: Compliance Gate — IRC whitelist + state DOI regulatory check

### ACT-003: Actuarial Provenance Tracer

Trio: K1 (Full KB — 3,083 entries) + K2 (342 ActuarialSource nodes) + K3 (12 Assumption nodes with traceability)
Leverage: 20x — manual provenance tracing across 342 sources takes ~10 hours; agent delivers in ~30 seconds
Domains: All 9 V-domains
Consumer: Any product generating actuarial output (PCP, ROB, 9010, Cortex)

Processing Modules:
- M1: Claim Extractor — identify actuarial claims in generated output
- M2: Entry Resolver — match claims to ActuarialEntry nodes via content similarity
- M3: Source Tracer — follow DERIVED_FROM to ActuarialSource nodes
- M4: Epoch Resolver — follow GOVERNED_BY to ActuarialEpoch nodes
- M5: Assumption Mapper — trace to Assumption nodes via AFFECTS/FEEDS
- M6: Provenance Block Builder — assemble full provenance metadata
- M7: Audit Trail Logger — write provenance chain to transfer audit log

## Reference Implementations

| Architecture | Agents | Total Rules | Lines |
|-------------|--------|-------------|-------|
| HOG Resources | 9 (MH-001 through MH-009) | 277+ | ~1,350 |
| Terrace Capital | 3 (TH-001, TH-002, AH-001) | 157 | 728 |
| Actuarial Intelligence | 3 (ACT-001, ACT-002, ACT-003) | 150+ | ~450 |
