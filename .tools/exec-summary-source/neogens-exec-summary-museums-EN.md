# AI or Not AI Is Not the Question. Whether It Can Be Trusted Is.

**Mission-driven ontology and knowledge graphs over the collection you already have — so that AI works on the confidence of your institution and the trust of the public**

Neo Gens · 12 min read

---

## 1. This year UNESCO asked every museum in the world the same question

In 2026 UNESCO and ICOM opened a global survey of how museums are actually using artificial intelligence. It closed on 21 July, and the findings will be published as a joint report setting out what the sector needs in order to be supported.

Look at how the question was framed. The two largest bodies in the field did not ask whether museums should use AI. They asked what has to be in place first, before a museum can use it responsibly.

There is already research that indicates what that report will find. The Museums & AI Survey run by MuseumWeek and the Culture For Causes Network — 180 institutions across 35 countries, fielded between 17 September and 14 November 2025 — reports that 52% of institutions have adopted AI tools, 11% do not know whether their own staff are using them, 9% have a formal AI charter or written policy, and 26% have had any formal AI training.

Adoption has outrun governance, and training trails both.

[[FIGURE:survey]]

Museum visitors have an answer of their own. In January 2026 the American Alliance of Museums put questions about AI in museums to a sample of more than 2,000 US adults, and published the results that March. What stands out: over 70% want no AI at all in developing exhibitions, while 43% want human beings to write every piece of museum content, emails and website text included, and 45% want to be told every time AI is used in a museum's work.

[[FIGURE:public]]

Put those three numbers together and they describe the present situation. Museums are taking the technology on faster than they can set the rules for it, in front of an audience that has not granted permission, and what is staked on the outcome is trust — the largest asset a museum holds.

Because what an AI puts out in the institution's name is not the status of a label on a gallery wall. It is something the museum has published to the public.

The way through is therefore not to use less AI. It is to have a foundation strong enough to carry it — one that lets AI open new possibilities in how knowledge is managed, resting on the confidence of the institution and the trust the public places in it.

---

## 2. The Library of Congress has given the problem its name

In February 2026 the Library of Congress published *Content Authenticity and Provenance in the Age of Artificial Intelligence: A Call-to-Action for the LAMs Community*, written by Kate Murray and Joshua Sternfeld for the C2PA for G+LAM Community of Practice.

The argument is uncomfortable reading, and it lands on target.

Provenance and the authenticity of evidence are not new ideas that AI has forced on the sector. This is work the field has done for a very long time. A catalogue record notes which agency created it, who amended it, and when. An object in a museum register carries the chain of hands it passed through. Ask how we know, and someone can walk you back.

All of it rests on a single assumption: a person was accountable at every step. The name on the record belonged to someone who had looked at the object, not someone writing from nowhere.

AI has not replaced the whole process. It has entered particular steps of it, and it is already inside real work.

- **Description.** At the Nasher Museum of Art, a chatbot wrote catalogue prose that was grammatically flawless in every sentence, and called works of art on paper sculptures.
- **Enrichment.** The US National Archives used AI to pull names out of census records so the public could find their own ancestors. A name extracted wrongly becomes exactly as searchable as one extracted correctly.
- **Discovery.** Research generating web-archive metadata with GPT-4o found the output usable in parts, and too uneven in quality to release without a person checking it.
- **Cataloguing machine-made works.** The Library of Congress has had to publish guidance on cataloguing resources generated using AI software, last updated May 2026.

What these four share is this. The record that comes out looks exactly like the records that came before it. The field naming the responsible agency still names your institution. What that name used to guarantee is no longer guaranteed.

When a library of that standing has to sit down and write rules for describing machine-made works, the question has entered the workflow. It is no longer a conference topic.

The paper's conclusion is the sentence every director should read: no single standard, tool, or institution can resolve this alone. The reasoning is plain. A standard like C2PA can tell you what edits a file has been through; it cannot tell you which piece of evidence a sentence in the record came from. A tool is only as good as the material the institution prepares for it. And an institution cannot verify itself — authenticity needs a witness the public accepts.

Practitioners see the same symptoms. OCLC's working group on AI in metadata workflows named three:

- AI invents false information, and it ends up sitting in a real catalogue record
- feed AI the same input and the output comes back different
- the confidence score the system reports does not reflect the quality of the work it produced

These three are not the growing pains of something not yet full-grown. They are properties of an AI that generates language from likelihood. Waiting for the next version release will not clear them. What is needed is a structure that lets AI work on ground you can trace back through.

---

## 3. A wrong label and a right one look the same

Two documented experiments make the argument better than any case for it.

At the Nasher Museum of Art a chatbot was set to work as a curator. What came back was fluent, confident catalogue language, correct in every sentence — and it called works of art on paper sculptures, renamed objects to fit an exhibition theme, and wrote descriptions a long way from the actual works.

Nothing in the output signalled that anything was wrong.

At the Mariners' Museum in 2025, curators tested three AI models on visual analysis. All three failed at the points where specialist expertise was required, and all three became useful the moment a curator was directing them. The lesson was not that AI is unusable. The lesson is that AI with nothing directing it produces work in which only a specialist can separate what was invented from genuine scholarship.

The whole risk sits in one sentence: a right answer and an answer that merely sounds right look exactly the same. The visitor cannot tell them apart. Nor can the researcher. Nor can the search engine.

---

## 4. Yale spent five years, and left the lesson behind

Between 2018 and 2023 Yale University built LUX, a cross-collection discovery platform bringing together the Yale University Art Gallery, the Yale Center for British Art, the Peabody Museum and the university library — more than 41 million records, reconciled and enriched from over a dozen external sources, built on Linked Art and IIIF, and released as open source for others to build on.

LUX is the strongest evidence that this can be done, and the strongest warning, at the same time.

The Oxford e-Research Centre summarised the project's central lesson under the heading *Semantic Completeness vs Data Usability* — the trade-off between the completeness of the abstract model and the real-world usability of the data.

Here is what matters. Five years of modelling that is theoretically perfect but does not serve the museum's mission is a very expensive academic success that cannot be put to use.

Designing the ontology therefore has to begin with the mission, not with the standard. Begin with the question of what this museum exists to do, and what it must be able to speak to. Only a director and their curators can answer that. No software vendor can answer it for you, and no AI model can infer it from data that sits outside your walls.

---

## 5. What we propose

We propose to work with your team to design and build an ontology and knowledge graph over the collection you already have, starting from the mission of the institution.

This does not replace the collections management system you use. It is the layer that makes putting AI in front of the collection something you can account for.

The work rests on five principles from our Modern Knowledge Management practice. Each is tied to a standard that already exists, and each answers one of the symptoms above.

**① Every statement is a claim until a witness confirms it.** Nothing enters the graph as a free-floating fact. Each assertion carries who said it, on what evidence, and at what status. A claim is promoted only when independent sources converge. Provenance at the file level uses C2PA and Content Credentials, the standard the Library of Congress paper is built around; provenance at the *statement* level is the layer we add above it. Computer science has arrived at the same point: *From Fluent to Verifiable: Claim-Level Auditability for Deep Research Agents* (2026) argues what your registrars have argued all along.

**② Identity must be decided, not left blurred.** Are these two the same? That is the question statistics can dodge and a knowledge system cannot. Decide it wrongly and the error flows down every link built on top of it. This is authority control, the discipline libraries have practised for a century: identifiers that are never duplicated, never reused, with a clear issuing authority, reconciled against VIAF, Wikidata and ORCID. Our working rule: a name can refute a match; it can never confirm one.

**③ Internal consistency is not truth.** A record that passes every validation rule can still be wrong, and a sentence with flawless grammar can still be false. So we set out an explicit hierarchy of evidence: first what the institution holds and observed itself, then independent sources that agree, then internal consistency, which filters rubbish and nothing more — and AI output enters as a claim that cannot promote itself.

**④ Silence is the enemy — the system must fail loudly.** The most dangerous failure is not the system that breaks. It is the system that gives up quietly and returns a plausible result: reporting that a search found nothing when it never ran, saying a record was written when nothing was saved. Every step is therefore instrumented to say when it did not do its job. This is the direct answer to OCLC's finding on confidence scores that do not mean anything.

**⑤ The map must admit its holes.** Guidance on making collections AI-ready is explicit that known gaps, deliberate exclusions and incompleteness belong in the metadata, not in a footnote. What the collection does not cover, what was never digitised, what is known to be wrong and not yet corrected — all of it is recorded as a first-class fact. An institution that can state its gaps precisely is more trustworthy than one that cannot: to researchers, to funders, and to every AI that will work on this material.

### Why a graph, and why now

MuseKG, presented at SIGIR in Melbourne in July 2026, shows the working pattern. It is a property graph over museum collections in which provenance is the first category of relationship. When a question arrives in human language, the system anchors it to entities in the graph, then pulls a compact set of surrounding evidence to assemble an answer from. The AI still speaks. But it speaks from something you can open, inspect and correct.

The vocabulary for this work already exists and is settled. CIDOC CRM, or ISO 21127 in its 2023 edition, is the common language of the cultural heritage field, used by museums such as the British Museum and the Museo del Prado, with Linked Art as the pared-down profile that works in practice for art collections. We do not invent an ontology where a standard already does the job. We extend the standard only where your mission needs a distinction the standard does not make, and we record every extension along with the reason it has to exist.

But tools alone are not enough. An ontology that works in practice comes from sitting down with the museum director, the curators, the conservators and the registrars. It does not come from software, or from any AI.

---

## 6. What we do not do

- This is not a digitisation programme and not a data cleaning service. If the underlying records are thin, the graph will make that thinness visible rather than hide it — which is worth knowing in advance.
- This work does not make AI more accurate. It makes AI's answers checkable, and traceable back to where the answer came from. That difference is the entire value of the work.
- The first engagement should be small. Take one part of the collection, take the set of questions the institution must be able to answer, and deliver a graph you can actually interrogate, before any decision about extending to other collections. Yale took five years across four collections. Nobody should sign up to that before seeing the method work on their own material.

---

## In three sentences

1. The sector's own institutions have stated the problem themselves. UNESCO, ICOM, the Library of Congress and OCLC all say the same thing: AI is entering collection workflows faster than provenance practice can adapt.
2. The answer is not less AI, but a knowledge layer that records both what is known and how it is known, so that every answer an AI produces can be traced back to institutional evidence, or is flagged as a claim still awaiting proof.
3. Neo Gens designs and builds that knowledge layer alongside your team, starting from the mission rather than from a schema — because the question of what knowledge structure your institution's mission and future require is one no model can answer for you.

---

**References**

- Murray, K. & Sternfeld, J., *Content Authenticity and Provenance in the Age of Artificial Intelligence: A Call-to-Action for the LAMs Community*, C2PA for G+LAM Community of Practice, February 2026 — Library of Congress
- UNESCO & ICOM, Global Survey on the Use of Artificial Intelligence in Museums, 2026
- MuseumWeek & Culture For Causes Network, *Museums & AI Survey*, fieldwork 17 September – 14 November 2025, 180 institutions in 35 countries; figures taken from the report card published in *MuseumWeek 2026: The Story of a Week*, 27 July 2026
- American Alliance of Museums, *AI in Museums and Community Trust: A 2025 Annual Survey of Museum-Goers Data Story*, 30 March 2026, including a January 2026 follow-up survey of more than 2,000 US adults
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
