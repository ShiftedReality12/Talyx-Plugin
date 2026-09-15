# Setup questions for the free Talyx plugin

<!-- Generated from build/config-schema.json. -->

Use these question IDs and their conditions. Ask only unresolved questions that affect
the requested setup; this is not a checklist to ask every client. Keep wording as written
except to insert evidenced task, output, person or source names and conflicting values. For a gap in
another existing field, use Q_FIELD below. Never invent a new config field.

## Q_WORK

**Ask:** What recurring task would you like help with, and what should it produce?

- **Fields:** Context for question routing only; no stored config key.
- **Ask when:** The task or desired result is unclear and is needed to identify material setup gaps. Skip when the user already named the task, is changing a known setting, or only wants company-wide preferences. Do not impose a workflow menu.
- **Choices:** Free text, or concrete tasks the user already named. Use the answer to target questions; do not invent a workflow-name or outcome config field.

## Q_CONTEXT

**Ask:** What company and role should Talyx use as context?

- **Fields:** `org_name`, `org_description`, `people`
- **Ask when:** Reusable company or role context is relevant and the material does not establish it. Keep unneeded context absent; a self-contained task does not require a company profile.
- **Choices:** Free text. Extract company, role and responsibilities only when stated.

## Q_INPUT

**Ask:** Which files or sources should Talyx use for this work?

- **Fields:** `inputs`, `sources`
- **Ask when:** Reusable inputs or permitted sources are needed and remain unclear. One-off files, subjects and dates belong to the workflow run, not shared setup.
- **Choices:** Offer named supplied material, a chosen working folder, or a connection the host actually exposes. If access is unavailable, offer an export/upload without claiming it is connected.

## Q_DESTINATION

**Ask:** Where should Talyx save the results?

- **Fields:** `destination`
- **Ask when:** The requested destination is unclear or differs from the documented local talyx-output folder. Otherwise apply the existing destination or report the default without asking.
- **Choices:** The local output folder or another user-named permitted destination. An external destination is a preference, not permission to send.

## Q_REVIEW

**Ask:** Who should review the results before they are used or shared?

- **Fields:** `reviewers`, `review_required`
- **Ask when:** A reviewer is material to this client's workflow and has not been identified. Review stays required by default; never invent a reviewer.
- **Choices:** Me, or someone else (ask for their name and what they review). Map Me only when the person's identity is supplied; otherwise retain the unresolved identity.

## Q_HUMAN

**Ask:** Which decisions must always stay with you or another person?

- **Fields:** `never_decide`
- **Ask when:** The client describes judgments needing a person but the boundary is ambiguous. Do not require a generic risk questionnaire when no material gap exists.
- **Choices:** Use the client's wording; examples may come only from their stated workflow.

## Q_EXCLUDE

**Ask:** What information must never appear in the output?

- **Fields:** `confidential`, `never_produce`
- **Ask when:** A stated confidentiality or forbidden-output requirement needs clarification.
- **Choices:** Free text. Record exclusions verbatim; naming a requirement does not prove it is technically enforced.

## Q_PRESERVE

**Ask:** What wording must stay exactly as written?

- **Fields:** `protected`, `terminology`
- **Ask when:** Provided material requires exact wording or terminology but does not specify it clearly.
- **Choices:** Free text or exact passages from supplied material.

## Q_CONFLICT

**Ask:** I found two different values for {field}: {existing} and {proposed}. Which should I keep?

- **Fields:** The identified existing field; no new key.
- **Ask when:** A material conflict or ambiguous replacement remains. Show both evidence sources. An explicit user instruction supplying the replacement already resolves it.
- **Choices:** Keep existing; use proposed; or supply the correct value. Silence is unresolved.

## Q_FIELD

**Ask:** For {stated_requirement}, what should {missing_detail} be?

- **Fields:** The identified existing field; no new key.
- **Ask when:** A client-stated requirement maps to another existing schema field but lacks a required detail. Name that requirement, the exact field and its missing detail. Do not introduce requirements or ask about every optional field.
- **Choices:** Use only evidence-backed choices allowed by that field's schema, otherwise free text.
