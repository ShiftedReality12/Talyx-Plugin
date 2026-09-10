---
name: esdp-agent-builder
description: "CSOP-003: Autonomous Agent Foundry — KB + team roster to ESDP v1.0 agent specs. 5x multiplier. 7 phases, 20 config modes, AFQS quality composite."
related_skills:
  - {skill: ce-vertical-launch-engine, relation: composed_by}
  - {skill: knowledge-architecture-factory, relation: sibling}
  - {skill: decision-machinery-forge, relation: sibling}
  - {skill: composite-intelligence-weaver, relation: informs}
  - {skill: architecture-validator, relation: informs}
retire_when: "cm-011 cross-reference resolver consumes related_skills in production AND 16-of-20 cm-006 cross-walks populated"
---

<objective>
Transform a knowledge base and team roster into ESDP v1.0-compliant agent specifications with inter-agent data flows, automatically calibrated to team size, role distribution, and decision bandwidth. Each agent embeds 50+ decision rules, 7 processing modules, 20 configuration modes. 5x specification velocity vs pioneering builds.
</objective>

<orchestration_trio>
| Component | Type | Role |
|-----------|------|------|
| K1 | Extractive | Primary engine — KB mining for assertions, quantitative thresholds, qualitative heuristics |
| K2 | Generative | Synthesis engine — agent spec generation with full ESDP dimensional framework |
| K3 | Adaptive | Fit engine — team topology calibration, decision bandwidth estimation, solo-vs-team scaling |
</orchestration_trio>

<csop_compliance>
| # | Condition | Evidence |
|---|-----------|---------|
| C1 | Architectural Asymmetry | AFQS >=85 vs <55 for manual agent specification writing |
| C2 | Orchestration Precision >90% | Phase sequence validated on HOG (9 agents) and TC (3 agents); <5% corrections |
| C3 | Execution Compounding | Each Foundry run's manifest feeds P2 assertion mining patterns + P5 test scenarios |
| C4 | Throughput >=4x | 5x: ~45 min per vertical with pattern vs ~4 hrs pioneering build |
| C5 | Vertical-Agnostic | Assertion types are universal; only domain vocabulary changes |
| C6 | Graceful Degradation | Skip P4 -> agents work without inter-agent flows. Skip P5 -> specs exist without tests |
| C7 | Quality Observability | AFQS composite + per-phase scores + ESDP compliance checks |
</csop_compliance>

<quick_start>
Invoke: `/esdp-agent-builder {client} --agents 3 --reference HOG|TC`

Optional flags:
- `--phase N` — Resume from phase N
- `--orientation O1-O5` — Sensemaking, Execution, Advantage, Choice, Learning
- `--horizon T0-T3` — Immediate (single agent), Tactical (full suite), Mid-Term (update), Strategic (cross-vertical)
</quick_start>

<essential_principles>
1. THE AGENT IS THE KB: Each agent spec embeds 50+ knowledge assertions. The spec itself is a self-contained knowledge artifact.
2. CONTENT DENSITY OVER STRUCTURE: A 37-line stub with correct headers has ~5% capability. A 200-line spec with embedded rules has ~85%.
3. SERIAL SYNTHESIS: Taxonomy extraction -> keyword-to-dimension mapping -> dimension-to-rule transformation -> canonical benchmarking -> consumer calibration.
4. TRIO KNOWLEDGE TYPES: Every agent must integrate K1 (domain expertise) + K2 (procedural methodology) + K3 (conditional decision rules).
5. 7 ESDP CONDITIONS ARE NON-NEGOTIABLE: Trio types, leverage >=3x, 7 modules, 20 modes, 50+ embedded knowledge, validation criteria, closed-loop learning.
6. CONSUMER CALIBRATION IS NOT OPTIONAL: Output format must match the principal's cognitive processing style.
</essential_principles>

<phase_modules>

## P1: Team Topology Analysis

**Input Contract:**
- REQUIRED: Team roster (names, titles, decision domains)
- OPTIONAL: Strategy transcripts mentioning team members, org chart
- SUBSTITUTABLE: Client principal profile (solo operator mode)

**Processing:**
1. Map each team member to V-domains where they make decisions
2. Estimate decision bandwidth: decisions/week x time/decision x consequence level
3. Identify overlap (multiple members in same domain) and gaps (domains with no owner)
4. Determine agent count: 3 per full-time team member, 1-2 for part-time/advisory
5. Solo operator rule: cap at 3 agents focused on highest-leverage decisions

**Output:** `agents/team_topology.json` — member-to-domain mapping, bandwidth estimates, agent count
**Quality Score:** domain_coverage (domains_with_agent_owner / total_domains x 100)
**Gate:** domain_coverage >= 80%
**Immune Response:** Team roster with >10 members -> cap at top 5, recommend prioritization criteria

---

## P2: Knowledge Assertion Mining

**Input Contract:**
- REQUIRED: KB entries (from CSOP-001), P1 team topology
- OPTIONAL: Decision rules (from CSOP-002) — dramatically accelerates mining
- SUBSTITUTABLE: Strategy transcripts -> assertion extraction (when KB is thin)

**Processing:**
1. Scan KB entries for assertion types: quantitative thresholds, qualitative heuristics, process sequences, conditional logic, domain expertise signals
2. Tag each assertion with: source KB entry, V-domain, confidence level, team member relevance
3. Cluster assertions by team member domain overlap
4. Score assertions by leverage potential: (frequency x consequence x automation_feasibility)
5. Select top assertions per agent (15-25 per agent for high-density specs)

**Output:** `agents/knowledge_assertions.json` — tagged, scored, clustered assertions
**Quality Score:** assertion_density (assertions / KB_entries x 100)
**Gate:** assertion_density >= 8% AND each planned agent has >=10 assertions

---

## P3: Agent Specification Synthesis

**Input Contract:**
- REQUIRED: P1 topology, P2 assertions
- OPTIONAL: Scoring engines (from CSOP-002) — enables engine-integrated agents
- SUBSTITUTABLE: None

**Processing:**
1. For each agent: select Knowledge Type Trio (Analytical + Strategic + Evaluative/Diagnostic/Predictive)
2. Define operational definition: what the agent does, for whom, producing what
3. Calculate leverage mechanism: current throughput x agent multiplier (must be >=3x)
4. Design 7 processing modules (M1-M7): each with defined input, processing logic, output
5. Define input requirements (5 specific inputs per agent)
6. Define output schema (4-5 output components in JSON)
7. Define validation criteria (4 criteria with quantified thresholds)
8. Generate 5 orientation modifiers (O1-O5) specific to agent's domain
9. Generate 4 time horizon modifiers (T0-T3) specific to agent's decision cycle
10. Verify ESDP 7-condition compliance
11. Define inter-agent data flows (which agent outputs feed which agent inputs)

**Output:** `agents/{CLIENT}_EXCEPTIONAL_AGENTS.md` — full spec file
**Quality Score:** esdp_compliance (agents_passing_all_7 / total x 100), assertion_utilization (embedded / mined x 100)
**Gate:** esdp_compliance = 100% AND assertion_utilization >= 60%
**Immune Response:** Agent leverage <3x -> re-analyze domain, identify higher-leverage opportunities or merge

---

## P4: Inter-Agent Architecture

**Input Contract:**
- REQUIRED: P3 agent specs
- OPTIONAL: Chain/fusion definitions (from CSOP-004)
- SUBSTITUTABLE: None

**Processing:**
1. Map data flows between agents: which agent's output is another agent's input
2. Identify circular dependencies (break with priority ordering)
3. Design agent invocation sequences for common workflows
4. Define shared data contracts (standardized JSON schemas for inter-agent communication)
5. Generate architecture diagram (ASCII)

**Output:** `agents/INTER_AGENT_ARCHITECTURE.md` — data flow diagram, invocation sequences, shared contracts
**Quality Score:** flow_completeness (agents_with_defined_flows / total_agents x 100)

---

## P5: Agent Validation Framework

**Input Contract:**
- REQUIRED: P3 specs, P4 architecture
- OPTIONAL: Historical data for calibration testing
- SUBSTITUTABLE: Synthetic scenarios

**Processing:**
1. Generate test scenarios per agent (3 scenarios: best case, typical case, edge case)
2. Define expected outputs for each scenario
3. Generate validation script that tests: module I/O, scoring accuracy, recommendation consistency
4. Run validation against synthetic data

**Output:** `agents/agent_validation.py` — test suite
**Quality Score:** scenario_pass_rate (passing / total x 100)

---

## P6: Implementation Blueprint

**Input Contract:**
- REQUIRED: P3 specs, P5 validation
- OPTIONAL: Scoring engines (from CSOP-002)
- SUBSTITUTABLE: None

**Processing:**
1. For each agent: generate implementation plan (which modules become which Python methods)
2. Map module dependencies to existing engines/functions
3. Define CLI entry point structure
4. Estimate implementation effort per agent

**Output:** `agents/IMPLEMENTATION_BLUEPRINT.md` — per-agent implementation plan
**Quality Score:** engine_integration (modules_with_engine_mapping / total_modules x 100)

---

## P7: Execution Manifest

**Input Contract:**
- REQUIRED: All phase quality scores
- OPTIONAL: Prior Foundry manifests (cross-vertical comparison)
- SUBSTITUTABLE: None

**Processing:**
1. Compute Agent Foundry Quality Score (AFQS)
2. Record: agents designed, assertions mined/embedded, compliance status, inter-agent flows
3. Identify calibration opportunities
4. Write manifest

**Output:** `EXECUTION_MANIFEST.json` + AFQS: 0-100

</phase_modules>

<quality_composite>
## Agent Foundry Quality Score (AFQS)

```
AFQS = (domain_coverage x 0.15) + (assertion_density x 0.15)
     + (esdp_compliance x 0.25) + (assertion_utilization x 0.15)
     + (flow_completeness x 0.10) + (scenario_pass_rate x 0.15)
     + (engine_integration x 0.05)
```

| AFQS Range | Rating | Action |
|-----------|--------|--------|
| 90-100 | EXCEPTIONAL | Deploy agents with confidence |
| 80-89 | STRONG | Deploy, note thin assertions for enrichment |
| 70-79 | ADEQUATE | Deploy with caveats, schedule assertion mining phase 2 |
| 60-69 | MARGINAL | Do not deploy — assertion density insufficient |
| <60 | INSUFFICIENT | KB too thin for agent construction — enrich KB first |
</quality_composite>

<orientation_matrix>
## 5O x 4T Configuration Matrix (20 Modes)

| | T0-Immediate | T1-Tactical | T2-Mid-Term | T3-Strategic |
|---|---|---|---|---|
| **O1-Sensemaking** | Single high-leverage agent from ambiguous role data | Full agent suite with extensive KB mining | Refine agent specs after production observation | Cross-vertical agent pattern library |
| **O2-Execution** | Rapid spec from clear team + clear KB | Standard full pipeline | Incremental agent updates for team changes | Agent template standardization |
| **O3-Advantage** | Competitive differentiation — unique agent capabilities | Full suite with proprietary advantage emphasis | Agent capability expansion for market shifts | Multi-client agent benchmarking |
| **O4-Choice** | Quick comparison: 3 agents vs 5 agents trade-off | Full trade-off: depth vs breadth per agent | A/B agent configuration testing | Optimal agent topology research |
| **O5-Learning** | Post-deployment agent accuracy audit | Full calibration against team member feedback | Continuous agent drift monitoring | Meta-analysis: which agent designs produce best outcomes |
</orientation_matrix>

<10x_multiplier_pipeline>
## 10x Multiplier Pipeline (Sub-Process within P2-P3)

When invoked with `--10x` or as part of standard P3 synthesis:

1. **Stage 1: Extract** — Pull 550+ keywords from taxonomy
2. **Stage 2: Map** — Keywords to 30-50 decision dimensions
3. **Stage 3: Synthesize** — Dimensions to 150-300 if/then rules
4. **Stage 4: Distribute** — 50+ rules per agent
5. **Stage 5: Inject** — 25-50 canonical benchmarks as heuristic anchors
</10x_multiplier_pipeline>

<integration_map>
**Upstream:**
- CSOP-001 Genesis Engine — KB entries (P4), taxonomy (P2), deployed commands
- CSOP-002 Decision Machinery Forge — scoring engines (optional, accelerates P3)
- Client config JSON — team roster, pools, focus areas

**Internal Skill Invocations:**
- `/content-multiplier` — keyword-to-rule transformation in 10x pipeline
- `/esdp-exceptional-skills` — ESDP v1.0 compliance verification

**Downstream Consumers:**
- CSOP-004 Composite Intelligence Weaver — agent specs inform chain design
- CSOP-005 Architecture Integrity Sentinel — agent compliance testing
- `/{prefix}-chain-*` — chains invoke agent capabilities
- `/{prefix}-fusion-*` — fusions synthesize cross-agent intelligence
</integration_map>

<success_criteria>
- 3+ agents written with full ESDP compliance (7/7 conditions each)
- 150+ total decision rules embedded across agents
- 7 processing modules per agent with domain-specific content
- 20 configuration modes per agent (5O x 4T)
- Inter-agent data flow architecture documented
- Consumer calibration specified per output type
- AFQS >= 80
- Execution manifest written
</success_criteria>
## Ecosystem Cross-References

| Skill | Role | Trigger Condition |
|---|---|---|
| `/pre-call-prep` | Pre-call intelligence preparation — produces call scripts and Force Multiplier reports | When ESDP agents consume PCP behavioral scoring output as training input |
