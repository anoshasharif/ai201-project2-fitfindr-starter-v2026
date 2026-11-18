# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
I chose 4 of 5 because the search uses keyword matching, so some valid queries may be phrased differently from the listing data and fail to find a match.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
I chose 5 of 5 because an empty search result is a clear condition the planning loop can check. The agent should never continue to `suggest_outfit` when no listing was found.

---

## 3. Something about state

Given a query that finds at least one listing, the `id` of the listing selected by `search_listings` is the same `id` of the `new_item` received by `suggest_outfit` — in 5 of 5 tries.

**Why this target:**
I chose 5 of 5 because session state should reliably pass the selected item between tools. Unlike model-generated text, carrying an item from one tool to the next should not vary between runs.

---

## 4. Something about the fit card

Given a successful outfit suggestion, the fit card mentions the selected item's title or identifying item type, price, and platform, and is between two and four sentences — in at least 4 of 5 tries.

**Why this target:**
I chose 4 of 5 because the fit card is model-generated, so its exact wording can vary between runs. The important details and length should still be correct in most runs even when the wording changes.

---

## 5. Price ceiling 

Given a query with a maximum price, every listing returned by `search_listings` has a price less than or equal to that maximum — in 5 of 5 tries.

**Why this target:**
I chose 5 of 5 because the maximum price is a numeric filter, so the search should consistently exclude listings that cost more than the user's stated budget.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->


## Unit 9 Capstone Acceptance Criteria

**1. MCP Search Failure Handling (Extension)**

When the MCP search service raises an MCPError, FitFindr must return a clear error message in all 3 of 3 test runs without crashing.

**Target:** 100% of simulated MCP failures produce a readable error.

**Reason:** An unavailable search service should not terminate the entire application. A lower success rate would leave some users with unexplained failures.

**2. Preventing Outfit Generation After MCP Failure (Extension)**

When an MCP search failure occurs, FitFindr must leave both `outfit_suggestion` and `fit_card` as `None` in all 3 of 3 test runs.

**Target:** Zero outfit suggestions or fit cards generated after a search failure.

**Reason:** Generating recommendations without valid search results could produce misleading clothing suggestions.

**3. Structured Failure Logging (Extension)**

For 3 simulated failed HTTP requests, FitFindr must write 3 separate JSON records to `results/capstone_runs.jsonl`. Every record must contain `timestamp`, `input`, `output`, `duration_seconds`, and `status`, with `status` equal to `failed`.

**Target:** 3 of 3 failed requests logged with all five required fields.

**Reason:** Missing failure records make debugging difficult. Complete logging is necessary to identify and investigate failures.

**4. Successful Clothing Recommendations**

For 3 runs of the query `vintage graphic tee under $30`, FitFindr must return at least one matching listing, a nonempty outfit suggestion, and a nonempty fit card without reporting an error.

**Target:** 3 of 3 runs satisfy all four conditions.

**Reason:** Failure handling should not interfere with the system's original recommendation functionality.

**5. Empty Search Result Handling**

For 3 runs of `designer ballgown size XXS under $5`, FitFindr must return an error containing `No matching listings`, leave `fit_card` as `None`, and return an empty `search_results` list.

**Target:** 3 of 3 runs meet all three conditions.

**Reason:** An empty search should produce a helpful response instead of fabricated recommendations. Any fabricated result would undermine user trust.

