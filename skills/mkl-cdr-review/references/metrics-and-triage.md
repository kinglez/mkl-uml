<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Metrics and review triage

Apply formal metrics only when they serve the requested review. Describe each measure's input, calculation, interpretation and limits. A threshold is either a documented project criterion or an explicitly labeled local heuristic. Metric values do not replace demonstrated design findings.

## Direct attention using relative risk

Rank selected classes by operation/attribute volume, relationships and known changes. Inspect high-ranked candidates in detail, then complete the applicable structural and coverage checks across the rest. Ebert & Dumke, *Software Measurement*, §9.3.3 motivates relative prioritization of error-prone components; its discussion concerns implemented modules. Adapting it to design classes is this skill's convention.

The historical 5/20/80 allocation is a planning aid: the highest-ranked small group may merit redesign discussion and the next group detailed inspection. The groups overlap; they are not three percentages to add together. Neither membership nor class size proves a defect. Small designs may be better reviewed entirely without percentile triage.

## What a class diagram can measure

| Measure | Interpretation and limitation |
|---|---|
| Operation/attribute count | Size of modeled interface/state; no measure of method-body complexity. |
| Inheritance depth | Longest modeled generalization path; inspect substitution and framework context. |
| Direct subclasses | Breadth of a modeled hierarchy; no automatic quality verdict. |
| Incoming/outgoing relationships | A structural coupling proxy; not complete runtime coupling. |
| WMC | Requires chosen method-complexity weights; plain operation count is only an explicitly simplified proxy. |
| RFC | Needs a defined response set/call scope unavailable from many class-only inputs. |
| LCOM | Requires a specified cohesion variant and suitable usage evidence. The historical corpus extraction has a damaged formula; do not derive an implementation from it. |

CK terminology is attributed to Chidamber & Kemerer (1994), with Ebert & Dumke §10.4 as the inherited explanation source. Report only measures actually computed, with the implementation's approximation stated. Correlations reported in particular studies are context-dependent.

## Quality questions

Use maintainability vocabulary to organize questions: does a change stay local, can the design be understood, can required behavior be modified safely, and can tests observe and isolate it? ISO/IEC 25010 supplies quality-model context; these are local review prompts rather than reproduced standard definitions.

A design can justify an adapter, stateless service or richer interface. Confirm the required behavior and contracts before reporting an anti-pattern. Testability concerns should identify a concrete observability or dependency problem.

## Setting thresholds

ISO/IEC 25023:2016 §8.8.1 includes measures that depend on a project-specified complexity threshold. It does not establish a universal value for this pack. ISO/IEC/IEEE 15939:2017 informs choosing decision criteria from goals, project history and statistical evidence.

Publish the chosen criterion, origin, affected scope and resulting action. Without comparable historical data, use a declared heuristic and investigate the candidate rather than claim statistical confidence. This repository's size/coupling/readability warning thresholds are local conventions, not UML or ISO acceptance limits.

## Review effectiveness

A clean review may reflect mature material. A low or high finding count alone cannot establish review quality. Inspect actual artifact coverage, skipped checks and meaningful negative regressions. The RITME case in van Solingen & Berghout, *The Goal Question Metric Method*, Case B is a single historical context; its roughly 0.4 faults/page is not a universal expected density. See [session-budget.md](session-budget.md).

No metric supplies missing human review evidence or turns an unavailable layer into acceptance. Coverage eligibility is assessed before a formal disposition.
