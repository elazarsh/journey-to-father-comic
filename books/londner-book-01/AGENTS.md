# Londner Book 1: scoped production instructions

These instructions apply to this book directory only. This is Yitzhak Meir Londner's story, not the Emmanuel story in the host repository template. Do not change the host repository's root viewer or root production files.

Read README.md, HANDOFF.md, production/manifest.json and method/SKILL.md. The user explicitly requested the present image batch, layout HTML and GitHub filing. Do not infer final family approval of an identity or historical detail from that authorization.

One scene per original image, no lettering, bubbles, frames, watermarks or readable documents. Keep original pixels unchanged. Apply masks and crop transforms in the renderer. The manifest defines each panel's source composition contract, target polygon, caption zone and protected region. Essential faces, hands and props must survive actual mask and zoom 1.00–1.15. Check both languages; longer English lettering must also fit.

Do not turn the leather/supplies shop into a cobbler workshop. Do not invent identifiable portraits of relatives. The family explicitly approved Yitzhak’s existing child, youth and adult likenesses in the latest message. Childhood v02 is the current approved child master; the child at the left of the three-age sheet was rejected. Keep art/rejected out of the reader. Old drafts are shown as contained sketches, never implied to have passed the new crop review.

No plot summary, moral list, chronology overview or future challenges on opening pages. Production mode contains spoilers by design. Reader mode opens with two invitation lines, then the story. Sources belong at the end.

Quoted Hebrew must remain verbatim; all newly written/adapted text requires a registry entry. Do not invent thoughts, conversations, dates or historical evidence. Preserve unresolved chronology notes, including Esther's arrival/wedding and the sequence of farm events. No public publishing or messages to others are authorized by this package.

After generation update manifest file/actual_size/sha256/status, generation-receipts, progress and handoff state. Regenerate HTML with tools/render.py, run tools/verify.py and inspect actual masks visually. Do not label unperformed browser checks as passed.

Family editorial direction on clarity and tone: read revisions/story-v04/AGENTS.md. Establish relationships, reasons and first introductions before relying on them; a short caption must remain understandable to a child meeting Yitzhak for the first time. Preserve the affectionate older narrator and source-supported happiness alongside hardship. Version 0.4 is a separate review draft, not automatic approval to replace the production script or regenerate all art.

Current structure after the family clarification: read revisions/book1-v06/AGENTS.md and README.md. Exactly THREE books, with unresolved source-based endings between volumes. The new first-book review script retains 48 pages but merges childhood and the path toward aliyah, stopping on the ship before arrival in 1925. Version 0.5's four-volume split and first-book ending at Vienna are superseded. The new IDs begin B01V06. Old 32-page and v05 manifests are archive/reuse candidates, not the active generation queue.

Family continuity applies to ALL volumes: revisions/book1-v06/family-continuity.json is the evidence/casting reference. Yitzhak's birth family has FIVE sons including him and THREE daughters; parents are additional. Raisel was born after the move to the larger home. Do not put unborn siblings in early scenes, use the same ages across decades, confuse Chava the sister and Chava the wife, or add deceased/later-born children to the 1925 traveling household. Most sibling birth years and supporting portraits are not verified. Record visual age estimates as estimates; verify actual generated groups against each scene's cast contract. Shoes use the Hebrew verb נועלים in adapted copy, while literal primary-source quotations remain unchanged.

Latest authorized production is revisions/book1-v07. The family approved book 1 plot and Yitzhak age identities, requested dramatic pastoral illustration, live speech/thought bubbles and varied quality layouts. The 48-page story remains intact. See that directory’s production/manifest.json, character-approvals.json and visual-direction.md. Upload and remotely verify the pre-art handoff first, then start the opening art batch. Adapted thought bubbles may express documented desires/uncertainty/longing; they are registered adaptations, not fabricated historical inner dialogue.

## Version 0.8: comic layout and memoir-fidelity edits (Claude, after user approval)

- The user approved replacing invented lines in the 0.7 script with the memoir's own words (see revisions/book1-v07/claude-review/). The user is the family member who approved the plot; he asked for MINIMUM invention. Do not add morals, reasons, questions to the reader or summaries that the memoir does not state. The reassuring line on page 23 stays by explicit request. Book-frame lines (the three takeaways, "המשך יבוא") are marked as frame, not Yitzhak's voice.
- revisions/book1-v08/layout-plan.json is now the source of truth for page layout and lettering. The story, the 48 pages and the B01V07 image IDs are unchanged. Five panels were removed and two circle insets added (NEW-P02-a, NEW-P36-a).
- New image work: read handoffs/claude/v08-image-requests.md. Keep registering images in art/book1-v07/progress.json as before; the sketch at revisions/book1-v08/sketch.html picks them up automatically when served over http. After adding images, run revisions/book1-v08/detect_faces.py and build_sketch.py.
- Speech bubbles only where the memoir reports speech; thought bubbles only where it states a wish, worry or plan. Leave a calm area above each speaker listed in the requests file.
