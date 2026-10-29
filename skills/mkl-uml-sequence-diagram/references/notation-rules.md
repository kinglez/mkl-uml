<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Sequence notation and output contract

Apply UML semantics and the chosen MKL presentation profile separately. This original guidance is informed by Fowler, *UML Distilled* (3rd ed.), chapter 4; Rosenberg & Stephens (2007), chapter 8; and the course materials identified in [sources-and-methods.md](sources-and-methods.md).

## Activation style and balance

Omit activation bars by default for readability under this profile. Include them when requested and validate their balance on every represented execution path. Presence alone is a style choice, not a UML conformance error. The practitioner sources differ in preference; no universal mandatory/optional `ExecutionSpecification` rule is established here.

For an `alt`, check each operand separately: only one executes. Nested activation levels each need closure; totals across mutually exclusive operands can invent leaks. Under `autoactivate on`, use the tool's automatic convention; after `autoactivate off`, validate the subsequent manual region rather than assuming automatic mode covers the entire file. `--con-activaciones` suppresses the style warning, not structural balance checks.

Historical PlantUML activation issues are recorded in source research, not a claim about the current tool version. Rendering and the validator check different aspects of the artifact.

## Classify messages before allocating operations

The authority for message semantics is [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF), §17.4.3 and §17.12.18.

| Intent/sort | Modeling consequence |
|---|---|
| `synchCall` (`->` in this profile) | Sender waits for an Operation on the receiving classifier. Map arguments to its input/inout parameters. |
| `asynchCall` (`->>` with declared intent) | Invoke a receiving-class Operation without waiting. Any later completion is a separately classified callback call or Signal. |
| `reply` (`-->` with declared intent) | Return outputs of an earlier synchronous call **to its original caller**. A returned value does not create an operation on the reply receiver. |
| `asynchSignal` | Name the Signal and applicable reception/handling contract rather than inventing an Operation. |
| `createMessage` / `deleteMessage` | Trace instance creation/destruction and lifecycle evidence. |
| Unknown/ambiguous | Record the unresolved sort, signature or receiver. A dashed/open arrow alone may not establish intent. |

Use an explicit synchronous reply when the value matters to subsequent visible behavior or distinguishes a meaningful result/error. Omit uninformative replies where the interaction remains understandable. For asynchronous completion, use the appropriate new call or Signal, never a UML reply to an asynchronous call.

Self-calls follow the same sort/signature rule. `MessageKind` (`complete`, `lost`, `found`, `unknown`) concerns known message ends and differs from `MessageSort`. Provenance requirements apply to the selected scope; UML does not require every class operation to appear in one interaction.

## Fragments and labels

Use `alt` for exclusive outcomes, `opt` for optional behavior, `loop` for repetition and `break` for a terminating alternative as appropriate. Include executable/model behavior inside each branch. Label specified flows with their local IDs, such as `alt FA-01 no capacity`, and retain their owning CU identity. Prose mentioning an undesigned branch cannot establish coverage.

Declare the scenario outcomes needed to explain collaboration rather than every possible implementation condition. Deep nesting is a readability/review candidate; split or link interactions when that clarifies scope. Numeric size/nesting warnings are local heuristics.

## Participants and names

| PlantUML role | Use | Preferred prefix |
|---|---|---|
| `actor` | External human/system participation. | `ACT_` |
| `boundary` | Screen/form, API, webhook, message ingress or device adapter. | `B_` |
| `control` | A justified software coordinator/controller. | `C_` |
| `entity` | A domain concept. | `E_` |
| `participant`, `database`, `queue` | Technical collaboration or storage. | `INF_` |

Keep names aligned with supplied evidence and record aliases/changes. Label Operation calls with a concrete action, replies with returned information, Signals with events and lifecycle messages with lifecycle intent. Show enough signature detail to resolve ambiguity. Avoid duplicating a PlantUML role icon through the same stereotype text inside the label.

## PlantUML contract

```plantuml
@startuml
' DS-XX - Sequence for CU-XX <name>
skinparam style strictuml
skinparam shadowing false
skinparam responseMessageBelowArrow true

<participants>
<basic-course messages>
alt FA-01 <condition>
  <implementing messages>
else basic course
  <continuation>
end
@enduml
```

Preserve the established filename `caso_NN_secuencia.puml` when applicable. Use phase dividers when useful. A Note may summarize scenario text, but the external specification remains the source for cross-artifact checks and Note content cannot masquerade as actual participants/messages.

## Choose the artifact for the question

A sequence explains selected object collaboration. Consider a state model for one object's lifecycle across scenarios and an activity model for broader workflow/concurrency questions. Record precise interface or behavioral constraints separately when a diagram alone cannot define them.
