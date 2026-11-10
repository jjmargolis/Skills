---
name: "political-spectrum-heatmap"
description: "Build a political spectrum heatmap: a sourced chart of where voter guides agree and disagree on every contest on a specific ballot, as an interactive page plus a one-page PDF and PNG."
---

# Political spectrum heatmap

Use when the user asks for a political spectrum heatmap, a "where the voter guides disagree" sheet, a voter-guide comparison, or an endorsement matrix for a ballot. Ask only for what is missing: the address or district, and the election (default: the next general election). Stay neutral: report the guides' positions and give no recommendation of your own.

Create a task list: ballot, guides, positions, build, verify.

## 1. Pin down the ballot
- List every contest on the user's ballot: federal, statewide, legislative, local, judicial, and every ballot proposal. Prefer the official sample ballot or certified candidate list.
- Name the nominees and which party lines they appear on, including fusion lines where those exist.
- Flag district lines that split the user's area (congressional, state senate, etc.). Say which rows depend on the exact block.
- Search for every fact here; do not rely on memory. Primaries and nominees change.

## 2. Pick the guides
- Find 12–20 guides that actually published positions for THIS election. Cover the spectrum: party organizations, editorial boards, good-government and civic groups, fiscal watchdogs, issue groups (housing, transit, preservation, environment), local political clubs, labor, and progressive or left groups.
- Group them right to left into 5–7 honestly named camps.
- A guide with no slate found for this election is left off and listed under "not found." Never fill a column from past positions or reputation.

## 3. Collect positions (academic rigor)
- Every cell comes from a source read this session, with a URL and date. Prefer the guide's own site. Mark positions taken from news coverage as secondhand.
- Keep three states distinct: took a position (Y/N or a candidate), explicitly declined to take one, and no position found.
- Flag stale positions, such as a summer "TBD" that may have changed.
- Don't infer a position from a party line, except where the party's own nomination is the position. Note it when you do.
- Run searches in parallel. Ballot-proposal explainers from local outlets often list several groups' positions at once.

## 4. Score and sort
- For a candidate race, the Y side is the most-endorsed candidate.
- Split = share of guides on the losing side, among guides that took a position. Declines are excluded.
- Sort contests from most split to most agreed, in bands: Most split (40% or more), Contested (20–39%), Mostly agreed (under 20%).
- Write a one-sentence takeaway saying where the real fights are and which camps break apart. Don't restate the table.

## 5. Build
Load the artifact-design skill before writing the page.
- **Layout:** contests down the left (name plus a one-line plain-English summary), then a split bar with the W–L count, then guide columns with rotated names under camp headers.
- **Chips:** solid blue = Y or most-endorsed; peach = N or rival; dashed outline = declined; dot = no position. Put candidate initials inside the chips.
- **Interactive artifact:** tapping a chip shows guide, contest, position and a source link. Store all sources in one JS object keyed by short ids. Works at phone width, with the table scrolling horizontally inside its own container and a sticky contest column. Light and dark themes.
- **One-page portrait Letter PDF:** use a print copy of the page with forced light theme. Include the chart, legend, a one-line definition of "split," candidate full names, the district caveat, and an abbreviated source list (org + date) with the "not found" guides. No long explanations. Render with Playwright Chromium (`page.pdf`, `prefer_css_page_size`, `print_background`, `@page{size:Letter portrait;margin:.35in}`). Use CSS `zoom` on the table container to fit one page.
- **PNG:** `pdftoppm -r 220 -png -singlefile` from the PDF.

## 6. Verify, then deliver
- Re-check every cell against its source and recompute every split.
- Render the PDF to a low-res PNG and look at it once. Fix overflow or a second page, then re-render.
- Publish the artifact and send the PDF and PNG with SendUserFile.
- In the reply: the key finding in 2–3 lines; bullets for anything secondhand, stale, district-dependent, or missing; then a Sources list of markdown links.