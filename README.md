# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr helps users search for thrifted clothing items based on a description, size, and maximum price. It searches through available listings and selects a matching item. It then uses the user's wardrobe to suggest one or two outfits that pair with the selected item. Finally, it creates a short fit card caption describing the item and outfit.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings data for items that match the user's description, size, and maximum price.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None)
- **Returns:** A list of matching listing dictionaries, each containing `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.
- **When it has nothing:** Returns an empty list `[]`.

#### `suggest_outfit`

- **What it does:** Suggests one or two outfits using the new item and the user's wardrobe.
- **Inputs:** `new_item` (dict), `wardrobe` (dict)
- **Returns:** A non-empty string containing one or two outfit suggestions using the new item and, when available, specific items from the user's wardrobe.
- **When it has nothing:** If the wardrobe has no items, returns a non-empty string with general styling ideas for the new item instead.

### `create_fit_card`

- **What it does:** Creates a short caption someone would actually post about the new item and outfit.
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** A two-to-four sentence caption that mentions the item, its price and platform, and describes the outfit's vibe.
- **When it has nothing:** If `outfit` is empty or contains only whitespace, returns a descriptive message instead of raising an error.

### Branch Rule

If `search_listings` returns an empty list, put a message in the session state saying that no matching listings were found and stop the loop. Otherwise, take the first matching listing and pass it to `suggest_outfit`.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a helpful message in `session["error"]` telling the user to change the description, size, or maximum price, and stop. Otherwise, select the first search result and continue to `suggest_outfit`, then `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** The query is parsed using regular expressions and string cleanup to extract the maximum price and size and use the remaining words as the item description.

**What moves through the session:** The parsed query is stored in `session["parsed"]`, followed by the search results in `session["search_results"]`. The first result becomes `session["selected_item"]`, which is read back from the session and passed to `suggest_outfit`. The outfit is stored in `session["outfit_suggestion"]`, then passed with the selected item to `create_fit_card`, whose result is stored in `session["fit_card"]`.
---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

Found: Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit: Here are two cute outfit ideas using the Y2K Butterfly Baby Tee and pieces you already own:

**Outfit 1: Casual Y2K Streetwear**
* **Top:** Y2K Butterfly Baby Tee
* **Bottoms:** Baggy straight-leg jeans (dark wash)
* **Outerwear:** Black cropped zip hoodie (worn open or layered over your shoulders)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag
* **Why it works:** The fitted, cropped silhouette of the baby tee balances out the volume of your baggy dark-wash jeans for that quintessential early 2000s streetwear proportion.

**Outfit 2: Effortless Contrast (Soft & Edgy)**
* **Top:** Y2K Butterfly Baby Tee
* **Bottoms:** Wide-leg khaki trousers
* **Outerwear:** Vintage black denim jacket
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt
* **Why it works:** This plays on the contrast between the girly, pastel butterfly print and the utilitarian, grunge feel of your black denim jacket and combat boots, anchored nicely by neutral khaki trousers.

Fit card: Obsessed with this Y2K butterfly baby tee I just listed on Depop for $18! It's giving major early 2000s streetwear vibes when you style it with baggy dark-wash jeans and chunky sneakers. Grab it before it’s gone and let your inner brat-pack era shine! 🦋✨

0 model calls this session, 2 served from cache

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

```
Here are two outfit ideas using the vintage Levi's 501s and pieces already in your wardrobe:

### Outfit 1: Casual Streetwear Vibe
* **Top:** Oversized grey crewneck sweatshirt
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag
* **Why it works:** The straight-leg fit of the Levi's 501s creates a great balanced silhouette when paired with an oversized crewneck. Throw on the chunky white sneakers and crossbody bag for an effortless, comfortable, everyday streetwear look.

### Outfit 2: Classic Edgy Contrast
* **Top:** White ribbed tank top
* **Outerwear:** Vintage black denim jacket
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt
* **Why it works:** Pairing the medium-wash denim with a fitted white tank and black combat boots leans into a classic, slightly grunge aesthetic. Adding the vintage black denim jacket on top creates a cool denim-on-denim contrast, pulled together nicely with the brown leather belt.

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

```
Nothing beats the effortless vibe of a classic vintage fit. These dreamy vintage Levi's 501 jeans in a perfect medium wash are giving off major off-duty supermodel energy. Just pair them with your favorite fresh white sneakers for that ultimate, timeless weekend look. Grab them on my Depop for just $38 before someone else snags them!

```
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked AI to help me implement `search_listings` so it could search by description, size, and maximum price while following the required empty-list behavior.
- *What came back:* AI helped me build keyword matching, size matching, and price filtering. When I first tested the implementation, I got a `NameError` because the regular expression code used `re` but the module had not been imported.
- *What I changed:* I added `import re` to `tools.py` and tested the function again. I also tested an impossible size to confirm that the function returned `[]` when there were no matches.

**Moment 2**

- *What I asked for:* I asked AI to help me connect the three tools in `run_agent` and make sure the agent stopped when a search returned no results.
- *What came back:* AI suggested parsing the query with regular expressions, storing the parsed values and tool outputs in the session, and checking `search_results` before calling `suggest_outfit`.
- *What I changed:* I implemented the branch so an empty search stores an actionable message in `session["error"]` and returns immediately. I then tested both a matching query and an impossible query to confirm that the successful path reached `create_fit_card` while the empty path stopped with `fit_card` still set to `None`.


<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty search stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item in session matches item passed on | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes item details and is 2–4 sentences | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Maximum price is respected | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
Criterion 1 — Full three-tool run returns a fit card
Produced by: run_eval.py::main, using agent.py::run_agent

Query: vintage graphic tee under $30
stopped early: no
selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
search_results: 10

Trace:
[1] search_listings (via MCP)
    out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
    out: Here are two specific outfit ideas using the Y2K butterfly baby tee and pieces from your current wardrobe...
[3] create_fit_card
    out: Living out my early 2000s dreams in this Y2K butterfly baby tee, and I am obsessed! I just scored it on Depop for $18...

```
Criterion 2 — Empty search stops before tool 2
Produced by: run_eval.py::main, using agent.py::run_agent

Query: designer ballgown size XXS under $5
stopped early: yes
selected_item: None
search_results: 0

Trace:
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)

Error:
No matching listings were found. Try changing the description, choosing a different size, or increasing your maximum price.

```
Criterion 3 — Item in session matches item passed on
Produced by: run_eval.py::main, using agent.py::run_agent

Query: vintage graphic tee under $30
stopped early: no
selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
search_results: 10

Trace:
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are two outfit ideas using the Y2K butterfly baby tee and pieces already in your wardrobe...
```
Criterion 4 — Fit card includes item details and is 2–4 sentences
Produced by: run_eval.py::main, using agent.py::run_agent

Query: vintage graphic tee under $30
stopped early: no
selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)

Fit card:
Obsessed with this Y2K butterfly baby tee I just dropped on depop for $18! It gives the ultimate effortless streetwear vibe when you style it with baggy dark wash jeans and chunky sneakers. Grab it before it’s gone and get ready to live in this look all season.

```
Criterion 5 — Maximum price is respected
Produced by: run_eval.py::main, using agent.py::run_agent

Query: graphic tee under $25
stopped early: no
selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
search_results: 4

Trace:
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 4 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Mesh Long-Sleeve Top — Black … +1 more
```

---


## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools and returns a fit card | 4 of 5 | MET (5/5) | All five tries completed `search_listings`, `suggest_outfit`, and `create_fit_card` and returned a fit card. |
| 2 | Empty search stops before tool 2 | 5 of 5 | MET (5/5) | All five impossible-query tries returned zero search results and stopped before `suggest_outfit`. |
| 3 | Selected item stays consistent in session | 5 of 5 | MET (5/5) | In all five tries, the selected listing was the same item passed from the search result into `suggest_outfit`. |
| 4 | Fit card includes item details and is 2–4 sentences | 4 of 5 | MET (5/5) | All five fit cards identified the selected item, included its price and platform, and stayed within 2–4 sentences. |
| 5 | Maximum price is respected | 5 of 5 | MET (5/5) | All five tries returned search results within the query's $25 maximum price. |

**Diagnoses**

All five criteria met their original targets, so there were no missed criteria requiring a failure diagnosis. The results suggest that some of my targets may have been conservative, especially Criterion 1 and Criterion 4, which required only 4 of 5 successful tries but passed 5 of 5. If I tightened one criterion, I would raise Criterion 4 to 5 of 5 because all five fit cards successfully included the required item details and stayed within the required sentence range.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are two cute outfit ideas using the Y2K Butterfly Baby Tee and pieces you already own:  **Outfit 1: Casua…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Obsessed with this Y2K butterfly baby tee I just listed on Depop for $18! It's giving major early 2000s street…
```

**Empty search**

```
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

I moved search_listings from a direct function call to an MCP tool. I registered search_listings in mcp_server.py and changed agent.py to call it using call_tool("search_listings", ...) from mcp_client.py. The behavior did not change after the move: matching searches still returned listings, and empty searches still stopped before suggest_outfit.

---

## The Improvement

**What I changed:**

I changed the prompt in `tools.py::create_fit_card` so that it now tells the model to write exactly three complete sentences with no bullet points or headings. The prompt still requires the item, price, platform, and outfit vibe.

**Which failure it was meant to fix:**

This change was meant to make Criterion 4 more reliable. Although Criterion 4 met its original target in the before run, its 4-of-5 target allowed one failure. Since the fit card's sentence count depends on model output, I tightened the prompt to make the required 2–4 sentence format more consistent.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools and returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty search stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item stays consistent in session | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card includes item details and is 2–4 sentences | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Maximum price is respected | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:**

Yes. The after run passed Criterion 4 in all five tries. Each fit card stayed within the required 2–4 sentence range while still including the selected item, price, platform, and outfit vibe. The other four criteria also continued to pass, so the prompt change improved the consistency of the fit card without breaking the rest of the agent.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
