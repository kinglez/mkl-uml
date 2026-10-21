<!-- English-edition adaptation: Copyright 2026 kingle.zhuang. See NOTICE for upstream attribution. -->
# Robustness diagram anti-patterns

Use this catalog when reviewing, refactoring, and auditing (gate layer 4). Most entries originate in the worked robustness-analysis exercises and Preliminary Design Review guidelines in Rosenberg and Stephens; others come from the case study in *Agile Development [abbreviated title]*. Each entry identifies **symptom → significance → correction**.

## Hard-rule violations

### 1. Noun-to-noun connection

**Symptom:** direct boundary↔boundary, boundary↔entity, or entity↔entity connection.
**Significance:** under MKL robustness rules this suggests a **missing control**. Check the actual behavior before asserting it is absent from the text; UML generally allows object-to-object communication.
**Correction:** discover and name the missing function as an intervening control. In the classic example, an edge labeled “display” between two pages becomes a specifically named presentation control. Merely deleting the edge leaves the analysis incomplete.

### 2. Actor shortcut

**Symptom:** an actor connects directly to a control or entity.
**Significance:** actors interact through a visible system interface.
**Correction:** represent the actual interaction boundary: screen/form, API, webhook, message ingress, or device adapter. A machine interface is a valid boundary and does not require an invented screen.

## Stereotype confusion

### 3. Widget used as a boundary

**Symptom:** boundaries named for individual widgets such as “OK Button” or “Search Field.” A named “Main Menu” page can be a legitimate whole-interface boundary.
**Significance:** widgets are below the intended screen-level granularity; including one tends to require all of them.
**Correction:** for GUI interactions use the **whole screen or page** as the boundary and treat the widget as an action leading to a control. For machine interactions use the named interface at the same analysis level.

### 4. Verb disguised as a boundary

**Symptom:** a boundary called “Select Address” or “Validate Data.”
**Significance:** these are actions; boundaries are nouns.
**Correction:** model the action as a control and identify its actual originating human or machine interface.

### 5. Generic or technology-specific boundary name

**Symptom:** “web page,” “screen,” “form,” “ReservationServlet,” or “checkout.jsp.”
**Significance:** generic names hide unresolved interface identity; concrete implementation-class names may add premature detail.
**Correction:** establish the actual human or machine interface name at analysis level. A named Payment API or Sensor Ingress is valid; it does not require a GUI screen.

### 6. Rogue control

**Symptom:** a control lacks behavioral support in the use case or other supplied requirements evidence. A control is not required to be a domain-model noun.
**Significance:** behavior has been invented while drawing without requirements support.
**Correction:** justify it through a proposed text change, recorded as a disambiguation finding, or remove it. Aligning its name with existing vocabulary often clarifies the choice.

### 7. Generic presentation controls

**Symptom:** several controls called only “Show,” “Display,” “Manage,” or “Process.”
**Significance:** ambiguous names conceal potentially nontrivial initialization behavior.
**Correction:** use specific names such as “Show Book Details” or “Initialize Payment Page.” The control may be needed; identify what it displays.

## Scope and abstraction errors

### 8. Missing alternative courses

**Symptom:** the diagram shows only the happy path.
**Significance:** this is the most frequent and serious omission. Completeness checking requires the basic course **and all alternatives in the same diagram**.
**Correction:** walk every textual alternative and add its branch. Subordinate alternatives indicate a need to **split the use case**.

### 9. Validation without a failure path

**Symptom:** validation controls have no corresponding failure behavior; this is the first issue highlighted by the course's worked exercises.
**Significance:** half the behavior remains unspecified and will be omitted from design.
**Correction:** apply the canonical pattern from the corrected exercise for each validation:

```text
C_ValidateX -- C_MessageX : FA-0n <failure condition>
C_MessageX -- B_Window   : FA-0n return to window
```

Name the message control explicitly, for example **“Show 'Blank fields' message”**, rather than “Show,” and **color it** because it is exclusive to the alternative course. The success branch continues to the next control. This resolves missing failure behavior, vague naming, and flow distinction together.

### 9-bis. Textual alternative without a triggering validation

**Symptom:** the specification declares an alternative such as “the code already exists,” but the basic course has no check from which it can branch.
**Significance:** unlike an unsupported drawn alternative (#10), the defect is in the **specification**: an outcome is declared without the question that produces it. Diagram construction exposes the missing attachment point.
**Correction:** propose adding the validation step to the basic course, subject to authorization for upstream edits, or remove the alternative if it does not apply.

### 9-ter. Business rule with implicit validation and no alternative

**Symptom:** a business rule requires a valid email format, a biography of at most 1,000 characters, or a price within a range, but no failure course is specified.
**Significance:** this is the counterpart to 9-bis: the question exists, but the outcome is missing. The resulting validation control lacks a failure branch, leaving error behavior unimplemented.
**Correction:** report a disambiguation finding. Every in-flow validation rule needs a supporting alternative course or an explicit statement that the interface validates it beforehand and produces no branch here.

### 10. Orphaned alternative course

**Symptom:** an error branch cannot be associated with a basic-course sentence.
**Significance:** either text is incomplete or the branch is invented.
**Correction:** attach it to a specific textual step or remove it.

### 11. Diagram/text mismatch

**Symptom:** text begins earlier or later than the diagram, entire paragraphs are unrepresented, or diagram details have no textual counterpart.
**Significance:** the two views describe the same behavior; divergence makes at least one inaccurate.
**Correction:** run the Highlighter Technique (gate layer 2). Mismatch often shows that the text was not examined sentence by sentence.

### 11-bis. Use case/wireframe inconsistency

**Symptom:** specified data differs from interface fields. An observed “Register Author” example requested first name, surname, date of birth, nationality, email, and biography, while the wireframe showed identity number, names, surnames, and mobile number.
**Significance:** boundaries derive from screens and entities from specifications. A contradiction between these sources propagates into the diagram and code. This is precisely the review concern of evaluating use cases in their GUI context.
**Correction:** report a traceability finding. The analyst must decide which source governs; do not resolve the conflict by assumption.

### 12. Misaligned vocabulary

**Symptom:** “matching entries” appears where the domain says “Book,” or “click search” replaces the specification's “press Search Now.”
**Significance:** this breaks traceability and reintroduces ambiguity.
**Correction:** align domain concepts with domain vocabulary, interfaces with interface evidence, and actors with role evidence; preserve meaning and record aliases rather than demanding every noun be a domain class.

## Premature detailed design

### 13. Operations assigned to classes

**Symptom:** entity notes contain `save(): void` or `validate(): void`.
**Significance:** operation allocation belongs to detailed design through sequences; doing it here freezes decisions prematurely.
**Correction:** remove operations. Discovered attributes may feed the domain model; operations must wait.

### 14. Inheritance and static relationships

**Symptom:** generalization or `extends` relationships appear in a robustness diagram.
**Significance:** static structure belongs in the domain or class model.
**Correction:** move the relationship to the domain model.

### 15. Design-pattern-itis

**Symptom:** `Factory`, `Strategy`, `Singleton`, DAOs, or architectural layers appear.
**Significance:** these are solution details, while robustness analysis is **conceptual preliminary design**.
**Correction:** remove them and let justified patterns emerge during detailed design.

### 16. Sequence-level detail

**Symptom:** the robustness diagram attempts the same detail as the later sequence diagram.
**Significance:** this duplicates work and anticipates decisions, contrary to review guidance.
**Correction:** keep logical flow here; reserve detailed interactions for the next artifact.

## Diagram hygiene

### 17. Orphaned elements

**Symptom:** declared objects have no relationships.
**Correction:** connect or remove them.

### 18. No controls, or too few controls

**Symptom:** nearly every element is a noun.
**Significance:** controls represent system behavior; without them the diagram conveys little.
**Correction:** return to the text and extract its verbs.

### 19. Ambiguous or misplaced labels

**Symptom:** actor→boundary labels become ambiguous when multiple actions enter a boundary, or labels diverge from the text.
**Correction:** label **boundary→control** edges using the same verbs as the specification.

### 20. Oversized diagram

**Symptom:** dozens of elements and nested alternatives make the diagram unreadable.
**Significance:** the use case probably encompasses more than one goal.
**Correction:** **split the use case**, rather than shrinking the font.
