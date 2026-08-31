# The Foundation Comes Before the Answers

**Mission-driven ontology and knowledge graphs for existing collections — so that AI works for your institution instead of speaking on its behalf**

Executive summary for museum and library directors
Neo Gens Co., Ltd. · Modern Knowledge Management · August 2026

---

## 1. The sector has already asked the question. The answer is not yet built.

In 2026, UNESCO and ICOM launched the first global survey of how museums are actually using artificial intelligence. It closed on 21 July, and the findings will be published as a joint report intended to identify emerging trends and, in their words, **critical support needs**. The framing matters: the sector's two leading bodies did not ask whether museums should use AI. They asked what museums need in order to use it responsibly.

Independent research from the same year suggests what that report is likely to find. Roughly **46% of surveyed institutions already use AI in some form, 11% do not know whether their own staff are using it, and only 8% have a formal AI charter.** Adoption has outrun governance.

Meanwhile, the public has taken a position. The American Alliance of Museums' Annual Survey of Museum-Goers, published in March 2026, found that **70% of the general public want museums to use no AI at all in developing exhibitions**, and 43% felt museums should not use it even for emails or website text.

Read together, these three findings describe a single predicament. Museums are adopting a technology faster than they can govern it, in front of an audience that has not granted permission — and whose trust is the institution's principal asset. The way through is not to use less AI. It is to be able to **show what the AI was standing on**.

---

## 2. The problem now has an official name

In February 2026, the Library of Congress published *Content Authenticity and Provenance in the Age of Artificial Intelligence: A Call-to-Action for the LAMs Community*, authored by Kate Murray of the Library of Congress and the independent scholar Joshua Sternfeld, as a product of the C2PA for G+LAM Community of Practice.

Its argument is uncomfortable and correct.

Provenance is not a new idea that AI has forced on the sector. Libraries and museums invented the practice. A catalogue record has long carried which agency created it, who modified it, and when. An object in a museum register carries the chain of hands it passed through. Ask how we know, and someone can walk you back.

All of it rests on a single assumption: a person was accountable at every step. The name on the record belonged to someone who had looked at the object.

AI has not replaced that process. It has entered it one step at a time, and it is already inside.

- **Description.** At the Nasher Museum of Art, a chatbot produced catalogue prose that was grammatically flawless and called works on paper sculptures.
- **Enrichment.** The US National Archives used AI to pull names out of census records so the public could find their own families. A name extracted wrongly becomes exactly as searchable as one extracted correctly.
- **Discovery.** Research generating web-archive metadata with GPT-4o found the output usable in parts, and too uneven to release without human review.
- **Cataloguing machine-made works.** The Library of Congress has had to publish guidance on cataloguing resources generated using AI software, last updated May 2026.

What these four share is what makes them hard. The record that comes out looks exactly like the records that came before it. The field naming the responsible agency still names your institution. What that name used to guarantee is no longer guaranteed.

When a library of that standing has to sit down and write rules for describing machine-made works, the question has left the conference programme and arrived at the cataloguing desk.

Hence the sentence every director should read: **no single standard, tool, or institution can resolve this alone.** The reasoning is plain. A standard like C2PA can tell you what happened to a file; it cannot tell you which piece of evidence a sentence in the record came from. A tool is only as good as the material the institution hands it. And an institution cannot be its own witness — authenticity needs a second pair of hands.

OCLC's Research Library Partnership working group on AI in metadata workflows documented the same problem from the practitioner's side, and named three specific failure modes:

- **hallucinations that introduce false information directly into catalogue records**
- **inconsistent outputs from identical inputs**, which undermines reliability
- **confidence scores that do not reflect the actual quality of the output**

These are not teething problems that a better model will fix. They are structural properties of systems that generate language from statistical likelihood. The correct response is not to wait for better models. It is to give the model a substrate that can be checked.

### The three routes directors reach for

**The standard.** Adopting C2PA and Content Credentials is worth doing, and an institution that has done it stands on firmer ground than one that has not. But a standard secures a file. What the public questions is a sentence. Ask which piece of evidence supports the third clause of a catalogue description and file-level provenance has nothing to say: the container is signed, the claim inside it is not. Standards were built to survive transmission, not to carry an argument.

**The tool.** Every vendor now offers AI-assisted description, reconciliation or enrichment, and the better ones are genuinely capable. But a tool inherits the quality of the material the institution hands it. Where two accession records disagree, the model cannot know which one your curators treat as authoritative, because nobody has written that down anywhere a machine can read. It does not fail loudly at that point. It answers from whatever it found, in your institution's voice.

**The institution's own hand.** An AI charter, a review step, a rule that no machine-written record is published without a curator's sign-off — this is the strongest of the three, and the only one most institutions can begin this quarter. It is still incomplete, for a reason that has nothing to do with rigour: an institution cannot be its own witness. The people reviewing the output are the people whose earlier records supply its context, and a closed loop can be perfectly disciplined and still confirm its own mistakes. Authenticity has always needed a second pair of hands: VIAF, ORCID, a peer's citation, a source community's own account of itself.

All three are necessary. What none of them supplies is a place to put the answer to *how do we know this?* where a person can read it and a machine can reach it. That is what section 5 proposes to build.

---

## 3. What this looks like when it goes wrong

Two documented experiments are worth more than any argument.

At the **Nasher Museum of Art**, a curatorial chatbot experiment produced confident, fluent, well-formed catalogue language that called works on paper sculptures, renamed objects so they would fit an exhibition theme, and wrote descriptions that differed substantially from the actual artworks. Nothing in the output signalled that anything was wrong.

At the **Mariners' Museum**, a 2025 curator-led test of three AI models on visual analysis found that all three made specialist errors — and that all three became genuinely useful the moment a curator was in the loop directing them. The lesson was not that AI failed. It was that AI without an authority to check against produces work that only an expert can distinguish from scholarship.

This is the risk in one sentence: **a wrong catalogue record and a right one look exactly the same**, and the visitor, the researcher, and increasingly the search engine cannot tell them apart from the text alone.

---

## 4. The precedent: what Yale already paid to learn

Between 2018 and 2023, Yale University built **LUX**, a cross-collection discovery platform unifying the Yale University Art Gallery, the Yale Center for British Art, the Peabody Museum and the Yale University Library — **more than 41 million records**, reconciled and enriched from over a dozen external sources, built on Linked Open Usable Data, Linked Art and IIIF, and released as open-source software.

LUX is the strongest existing proof that a cross-domain cultural heritage knowledge graph is achievable. It is also the strongest available warning. The Oxford e-Research Centre summarised the project's central lesson under the heading **"Semantic Completeness vs Data Usability"** — the trade-off between the purity of the abstract model and the usability of the resulting data.

That trade-off is the whole of it. A five-year modelling effort that is theoretically complete but does not serve what the institution is actually for is a very expensive way to produce a diagram. **Which is why the ontology has to begin with the mission, not with the standard.** The question "what is this institution for, and what must it be able to say with authority?" is one only a director and their curators can answer. No vendor can answer it for you, and no model can infer it from your data.

The point is reinforced from an unexpected direction. Erin Canning's work on an ontology for museum critical cataloguing terminology — colonial, outdated and harmful language in existing records, and the principle that source communities define how they are named — demonstrates that the choice of knowledge structure is never neutral. Delegating that choice to a statistical model is delegating the institution's interpretive authority. That is a mission decision wearing technical clothing.

---

## 5. What we propose

We propose to work with your team to design and build a **mission-driven ontology and knowledge graph over the collection you already have** — not a replacement for your collections management system, but the layer that makes it defensible to put AI in front of it.

We build on five principles from our Modern Knowledge Management practice. Each is grounded in an established standard, and each answers one of the failure modes above.

**① Every statement is a claim until a witness confirms it.**
Nothing enters the graph as a free-floating fact. Each assertion carries who said it, on what evidence, and at what status. A claim is promoted only when independent sources converge. Provenance at the file level is handled by **C2PA / Content Credentials** — the standard the Library of Congress paper is built around; provenance at the *statement* level is the layer we add above it. Recent computer science work is converging on the same idea: *From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents* (arXiv, 2026) argues, in a different field, exactly what your registrars have always argued.

**② Identity must be decided, not left blurred.**
"Are these two the same?" is the question statistics can dodge and a knowledge system cannot — because an identity error propagates down every link built on top of it. This is **authority control**, the discipline libraries have practised for a century: unique identifiers, never reused, with a clear issuing authority, reconciled against VIAF, Wikidata and ORCID. Our operating rule: *a name can refute a match; it can never confirm one.*

**③ Internal consistency is not truth.**
A record that validates perfectly can still be wrong, and a sentence with flawless grammar can still be false. We build an explicit evidence hierarchy — what the institution directly holds and observed, then independent corroboration, then internal consistency as a filter only, and AI output entering as a claim that **cannot promote itself**.

**④ Silence is the enemy — the system must fail loudly.**
The most dangerous failure is not the system that breaks. It is the system that gives up quietly and returns a plausible result: reporting that a search found nothing when it never ran, or that a record was written when nothing was saved. Every step is instrumented to say when it did not do its job. This is the direct answer to OCLC's finding on confidence scores that do not mean what they appear to mean.

**⑤ The map must admit its holes.**
Current guidance on making collections AI-ready is explicit that **known absences, exclusions and incompleteness belong in the metadata**, not in a footnote. What the collection does not cover, what was never digitised, and what is known to be wrong and not yet corrected are recorded as first-class facts. An institution that can state its gaps precisely is more trustworthy than one that cannot — to researchers, to funders, and to any AI system reasoning over it.

### Why a graph, and why now

**MuseKG**, presented at SIGIR '26 in Melbourne in July 2026, demonstrates the working pattern: a typed property graph over museum collections in which **provenance is the first relation category**, grounding natural-language questions to graph entities and retrieving a compact neighbourhood of *evidence* to generate an answer from. The model still speaks — but it speaks from something you can inspect and correct.

The vocabulary for this already exists and is stable. **CIDOC CRM (ISO 21127, 2023 edition)** is the sector's lingua franca for semantic interoperability, adopted by the British Museum and the Museo del Prado among others, with **Linked Art** as the pared-down profile that makes it practical for art collections. We do not invent an ontology where a standard will serve. We extend the standard where your mission requires distinctions the standard does not make — and we document every extension and why it exists.

---

## 6. What we do not claim

Honesty about limits is part of the offering, not a risk to it.

- **This is not a digitisation programme and not a metadata clean-up service.** If the underlying records are thin, the graph will make that visible rather than conceal it — which is the point, but it should be expected.
- **This does not make AI accurate.** It makes AI *checkable*. The distinction is the entire value.
- **The first engagement should be small.** A defined subset of the collection, a defined set of questions the institution needs to answer with authority, and a working graph you can interrogate — before any commitment to scale. Yale took five years across four collections; nobody should sign up for that without seeing the method work on their own material first.

---

## In three sentences

1. The sector's own institutions — UNESCO, ICOM, the Library of Congress, OCLC — have now stated the problem: AI is entering collection workflows faster than the provenance practices that made those workflows trustworthy can adapt.
2. The answer is not less AI, but a knowledge layer that records what is known *and how it is known*, so that every AI-produced answer can be traced back to institutional evidence or flagged as a claim.
3. **Neo Gens designs and builds that layer with you, starting from your mission rather than from a schema — because the question of what your institution must be able to say with authority is the one question no model can answer for you.**

---

Noppadol Weerakitti · noppadol@neogens.co · neogens.co

**References**

- Murray, K. & Sternfeld, J., *Content Authenticity and Provenance in the Age of Artificial Intelligence: A Call-to-Action for the LAMs Community*, C2PA for G+LAM Community of Practice, February 2026 — Library of Congress
- UNESCO & ICOM, Global Survey on the Use of Artificial Intelligence in Museums, 2026
- American Alliance of Museums, *AI in Museums and Community Trust*, Annual Survey of Museum-Goers, March 2026
- OCLC Research Library Partnership, Managing AI in Metadata Workflows Working Group
- Library of Congress, *Cataloging of Resources Generated Using Artificial Intelligence (AI) Software* — FAQ, updated May 2026
- US National Archives, AI-assisted name extraction in the National Archives Catalog
- *Web Archives Metadata Generation with GPT-4o: Challenges and Insights*, arXiv
- Yale University, LUX cross-collection discovery platform (2018–2023); Oxford e-Research Centre, *Semantic Completeness vs Data Usability: Lessons Learnt from LUX, Linked Art and IIIF*
- *MuseKG: An Interactive Knowledge Graph Over Museum Collections*, SIGIR '26, Melbourne, July 2026
- CIDOC CRM, ISO 21127:2023; Linked Art profile
- *From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents*, arXiv, 2026
- Canning, E., *Defining an Ontology for Museum Critical Cataloguing Terminology Guidelines*, 9th Workshop on Linked Data in Linguistics
- American Alliance of Museums, *Curatorial Chatbot: An Experiment with AI at the Nasher Museum of Art*
