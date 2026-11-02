# Book 1 v0.8: source integrity and static visual QA

Report created 2026-10-31T15:25:09.585869+00:00. Audit snapshot 2026-10-31T15:20:47.547557+00:00. Production is still adding sources, so counts and proofs are snapshots, not the final completion count.

## Scope and limits

Read-only QA of book1 art under the authoritative 48-page v08 layout. No art, production scene data, global progress, receipts or master pixels were changed. All reports, programs and proof images are in this QA directory. No book2 or GitHub work was performed.

These are **source review and static crop proofs**, not browser screenshots or final lettering approval. Browser checks were not performed in this QA pass; the existing handoff records Chromium blocked by setsockopt. No browser test is claimed. Local Python has Pillow and NumPy but no cv2, dlib, torch or onnxruntime. No detector was installed or downloaded and no credentials were read. Therefore face detection was not refreshed. Font metrics, Hebrew/English bubbles, tails, caption collisions, 1280/820/390px layout and print still require actual renderer checks.

## Integrity snapshot

- 112 of 170 active panel sources are registered; 58 remain absent at the audit time.
- 88 active PNG masters were available locally, decoded successfully, had expected dimensions and matched both progress and individual receipt SHA-256 values.
- 24 active masters are inherited remote PNGs represented here by local WebPs. Their recorded master hashes are retained, but this pass did **not** fetch or independently rehash those remote PNGs. A preview is not a replacement master.
- No local master/receipt hash mismatch was found. No v08 review record carrying a source_web_sha256 disagreed with its current preview at this snapshot.
- 95 local PNG/WebP pairs were compared by decoded, equally resampled RGB values. All except the two below had mean absolute error below 10/255, consistent with corresponding lossy previews. This is a correspondence screen, not a proof of identical bytes.

### Two confirmed stale reader previews

| ID | Current verified PNG | WebP loaded by sketch | Action |
|---|---|---|---|
| B01V07-P08-04 | Eye-level child in bed, both bandaged feet | Old bird's-eye bed/floor composition, same aspect | Rebuild WebP from current verified PNG; record its new WebP hash |
| B01V07-P09-04 | 1536×1024 boy practicing writing in bed | 1024×1024 blue night rooftop/window scene | Rebuild WebP from current verified PNG; record its new WebP hash |

The static crop proofs prefer locally available verified PNGs. Until these previews are repaired, the reader will show different art from the corresponding QA crop proofs.

## Face and protection provenance

faces.json has 62 active registered assets with entries and 50 without entries at this snapshot. Entries contain only bare coordinates, without sourceSHA, detector model/version or detection time. **All existing boxes are unbound candidates.** Missing or empty face entries never establish that a source is safe for text.

Confirmed stale examples: P26-04 now shows hands and swatches; P27-01 now shows a hand carrying a sample case; both retain large old face boxes. P36-01's current head/cap lies approximately at [41,43,11,16]% of the source, while the old face box is [51.5,25.9,19.6,13]%. These old boxes can move the crop and protect the wrong area. In addition, faces alone never protect key hands, feet, books, the collecting box or crates.

[manual-protection-candidates.json](manual-protection-candidates.json) binds seven manually inspected protection records to both the declared master SHA and the SHA of the actual PNG/WebP reviewed. Coordinates are conservative manual estimates, not detector output. Do not copy them into production without reviewing the exact current hash.

## Concrete crop fixes for Claude

The full source art is valid for these scenes. The problem is the current slot/fit. No redraw is requested by this QA report.

| ID | Visible current-mask problem | Renderer candidate |
|---|---|---|
| P01-02 | Narrow vertical panel cuts both writing hands sideways | contain, fx=.5, fy=.5, zoom=.92; keep hands and pen clear of diagonals; applies to phone too |
| P05-01 | Bottom diagonal cuts mother's/child's feet | cover, fx=.5, fy=1.0, zoom=1.00; inspected comparison preserves feet |
| P08-01 | Very short top strip removes the swollen/limping foot, the reason for the scene | Increase panel height; contain/.92 is a temporary safe treatment |
| P21-01 | Father is cropped from nose down; crate/hands cannot fit the tiny strip | Reallocate substantially more height. Contain technically preserves pixels but makes the scene unreadably small; no object-position-only fix |
| P28-04 | Speaker's upper face/head cut off | contain, fx=.5, fy=.5, zoom=.92 or taller slot. A tested fy=0/zoom=1 cover crop still grazes the hair at the slanted edge |
| P38-02 | Welcoming Henich's face is cut vertically at the left | contain/.92 or widen slot; also visible on phone |
| P38-03 | Both actual male speakers are cut at opposite sides; daughters remain centered | contain/.92 or wider scene slot. Full source contains six people, including four daughters. Contain creates quiet top/bottom renderer room for the two bubbles; applies to phone too |

The .92 value is an initial 8% renderer inset to keep complete source content away from slanted corners. It is deliberately outside the default cover-only treatment; production currently has no per-ID fit override. Implement as a renderer crop setting, never by changing master pixels. Final text readability and panel sizing still need judgment. Exact hash-bound candidates and side-by-side PNGs: [crop-override-candidates.json](crop-override-candidates.json).

### Offscreen speech and quiet room

P38-04 is Chava's close-up, with Henich speaking from off-panel right/edge. Current mouthOf() parses the word right and can then snap to the nearest detected face, which would risk attributing Henich's speech to Chava after face detection is refreshed. Use an explicit offPanel=true flag, bypass nearest-face assignment, and test a mouth anchor [1.02,.38] in normalized final-panel space (English mirror [-.02,.38]). A starting bubble zone is [60,3,36,19]% in the upper-right of the final panel, pending actual Hebrew/English text measurement. The source's quiet region is documented separately in the manual protection record.

P38-03 requires its two bubbles in the calm renderer area introduced by contain or by a larger slot; current source cover crop leaves too little safe space above six heads. Preserve Claude's reading order and speaker assignment. Avoid treating mouth prose mentioning both left/right as a reliable coordinate: mouthOf() currently checks both keywords and the later left match wins, even in text describing a right-side face and a left-side bubble.

### Family scene P12-04

Visually checked the inherited preview and its current v08 mask: father + mother + five boys + three girls including baby Raisel = **10 people**. Mother holds the baby; Yitzhak's bandaged foot remains on the stool. The current mask preserves all ten heads and the foot prop. Do not redraw for count. The existing accepted minor uncertainty remains: relative ages are estimates and eldest Chaim is not dramatically older; this review does not approve invented identities or exact birth years. Two captions still need to avoid the family and the foot in the actual renderer.

## Evidence and reruns

- [source-audit.json](source-audit.json): per-ID source, preview and receipt hashes, master availability, dimensions and issues.
- [preview-correspondence.json](preview-correspondence.json): decoded source/preview correspondence screen.
- [crop-proof-metadata.json](crop-proof-metadata.json): source SHA, actual proof input SHA/path, current object-position, shape and desktop/phone aspects for each proof. Desktop includes the renderer's 1.037 page-height factor.
- [phone-proof-metadata.json](phone-proof-metadata.json): hash-bound unlettered phone crop proofs at the .72–1.45 aspect clamp.
- page-01-static.png through page-48-static.png: whole-page static crop proofs. Circle z order is respected; fade gradients, shadows and lettering are omitted. Empty panels are dark placeholders. They do not imply complete art or completed QA for all 48 pages.
- sources-*.jpg: uncropped source thumbnails with the current desktop crop beneath them.
- phone-crops-*.jpg: static phone crop contacts, no text or live height/collision checks.
- pages-01-12-contact.jpg through pages-37-48-contact.jpg: whole-book static overview.
- [index.html](index.html): local evidence gallery.

Programs in this directory write only QA outputs. Refresh after the batch finishes, in order: audit_sources.py, compare_previews.py, crop_proofs.py, override_candidates.py, phone_proofs.py, manual_protection.py, write_report.py. Regenerated contact sheets need renewed visual review; re-running scripts alone is not a pass. Original sources and production data remain untouched.


## Integration correction, 2026-11-01

P08-04 and P09-04 were cross-version selection mismatches: the local canonical PNGs were older images, while the WebPs correctly represented Claude’s selected .v2 replacements. Do not regenerate those previews from the older PNGs. source-selection.json now pins each active panel to the reviewed .v2 source SHA and file, preserving both original versions.
