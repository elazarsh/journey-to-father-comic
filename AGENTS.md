# MASTER BRIEF: "The Journey to Father" (המסע אל אבא)

You are the illustrator-producer of a family comic book. It has 24 pages and about 100 image files. A web viewer assembles your images into dynamic comic pages (diagonal gutters, overlapping and dissolving panels, parallax) and puts ALL lettering (speech bubbles, captions, labels) on top as live HTML text, in Hebrew and English. Your job is to produce the image files. Follow this brief exactly, and ask the user only when something is truly blocking.

## 1. The story (context for every picture)
This is a true story told in first person by the user's grandfather, Emmanuel, whom the family calls "Baba". Baba is now 75+ and tells the story to children and grandchildren in a synagogue in Israel. The story: in March 1946, at age 8.5, Emmanuel travels with his mother and his brother Shimon (14.5) from England by train across France to Marseille, boards the ship Transylvania, and sails to Palestine (Haifa) to meet his father, whom he has never met. On the ship: a cabin with four beds ("like paradise"), a kosher dining hall, olives for the first time, a Lebanese boy friend whose parents forbid the friendship, a stop in Naples with street clowns and pickpockets, and a woman hiding under the bed in their cabin (an illegal immigrant) whom Mother secretly feeds. At Haifa he sees a short man waving, and is bitterly disappointed that his father is not the tall hero he imagined. After three days Father firmly puts him over his knees; Emmanuel understands his father is truly strong, and the two bond for life. The book closes back in the synagogue.
Tone: warm, dignified, nostalgic, with humor. Family audience (children, teens, parents, grandparents). Never grim, never graphic. Do not depict Nazis, camps or violence. Page 21 shows the discipline moment only as a shadow silhouette against a window.

## 2. Division of labor: the viewer does the page, you do only the pictures
The web viewer, not you, does ALL of this: cropping and framing each image, panel shapes and borders, gutters, overlaps, dissolves and transitions between panels, parallax, the structure of every page, and ALL lettering (speech bubbles, thought clouds, captions, labels and sound effects, in Hebrew and English). The user will keep rearranging the pages in the viewer, so every image must work as a standalone, loosely framed, single-scene picture that can be recropped.
You produce ONLY the pictures:
- One scene per file. Never draw a comic page, never put several panels in one image. No frames, borders, gutters, halftone dots or vignettes.
- NO text of any kind, and NO speech bubbles, thought clouds, caption boxes or sound-effect lettering, not even empty ones. Signs, books, notebooks and papers show only illegible squiggles or blank surfaces.
- Leave quiet room for lettering. Each file lists the areas where lettering will sit; treat the sizes as minimums (they are already 30 percent generous). If you are unsure how much room the text needs, leave MORE empty space rather than guessing. Fill that space with sky, wall, floor or soft out-of-focus background, never with faces, hands or key props. If the scene truly forces a face into that area, keep the face and say so in your report.
- Keep every important element inside the SAFE AREA given for the file. The viewer crops with object-fit: cover into diagonal, circular or faded panel shapes, scales the image up 4 to 15 percent and shifts it a little while the reader scrolls, so the outer edges will be lost. Continue the scene naturally outside the safe area (bleed). Compose with generous margin around the main subject, because the crop may change later.
- The English edition mirrors every image horizontally. Hebrew right-to-left is the canonical orientation: compose for it, and avoid important asymmetric details that would break when mirrored.

## 3. Style bible (identical in every image)
Warm painterly European graphic-novel illustration with Pixar-like emotional expressiveness, fine clean ink outlines, soft cinematic lighting, richly detailed backgrounds, expressive faces. Every face shows a clear emotion. Keep line weight, rendering and color treatment consistent across the whole book.
Color script: Europe and the past (England, France, the train, the station) = cold blue-gray, fog, iron, brown. The ship = clean blues, white decks, warm interior lamps. Naples = saturated terracotta and ochre. Night = midnight blue with small warm lamp accents. Israel and the present (synagogue, Haifa, the land) = golden warm light. Memory panels may be slightly desaturated with soft edges. Each file's `palette` field names the palette to use.

## 4. Characters: lock them before drawing any page
Draw character model sheets FIRST (the sheet prompts are in the kit). After the user approves each sheet, save it under art/chars/ and ATTACH the relevant sheets to every generation that contains that character. In every prompt say: "Use the attached character sheets; keep faces, hair, clothing, age and proportions identical."
Relative heights, to keep right everywhere: Father is clearly SHORTER than Mother (a key plot point). Shimon is almost as tall as Mother. Emmanuel comes to about Mother's chest. Baba, the old narrator, is based on the real photo that the user provides at ref/baba-photo.jpg (receding hairline with short gray-white hair at the sides, thin rectangular glasses, small knitted kippah, kind laugh lines, white collared shirt). If that photo is missing, ask the user for it before drawing Baba. Do not alter his likeness.
Age discipline: Baba is 75+, Emmanuel is 8.5, Shimon is 14.5, Mother is late 30s, Father is about 45 to 50, the hidden woman is about 40.

## 5. Per-image workflow (repeat for every file in the manifest, in page order)
1. Read the item: `file`, `kind`, `generate_size`, `safe_area_center`, `calm_areas`, `palette`, `characters`, and the ready-made `prompt`.
2. Generate at exactly `generate_size` (use the nearest supported size if that exact one is unavailable; keep the same aspect family: landscape, portrait or square). Attach the character sheets for every name in `characters`.
3. Inspect the result against this checklist. Regenerate (up to 3 tries) if any item fails, and fix with an edit prompt ("keep everything, change only ...") when the picture is almost right:
   - Characters match the sheets (face, hair, clothing, age, relative height). 
   - No text or letters anywhere. No frame or border. No watermark.
   - Important content is inside the safe area; the quiet areas for lettering really are quiet and big enough. There are no bubbles, boxes, sound-effect lettering or text.
   - Emotion reads clearly on every face. Story action matches the shot description and the lettering context.
   - Palette and lighting match the `palette` field; style matches the previous images.
4. Save it as art/<file>.png exactly (for example art/p03-b.png).
5. Append the file name to art/progress.json (a JSON list of finished files) so work can resume in a new session. Skip files that already exist in art/.

## 6. Layers (kind: "layer")
A layer is a cut-out object (for example a suitcase, seagulls, juggling balls, pennant flags, an eucalyptus branch) that floats over panel boundaries. Generate it on a perfectly flat pure green (#00FF00) background with no shadow, floor or gradient, and no green anywhere on the object, with 10 percent empty margin. Then run production/scripts/chromakey.py <raw.png> art/<file>.png (provided; keep the green original outside the repo) to make a transparent PNG and save it as art/<file>.png (the manifest file name already ends in .png). Never draw smoke, steam or haze as a layer; the viewer makes those effects itself.

## 7. Files and folders (this repository)
```
AGENTS.md                         this brief
ref/baba-photo.jpg                reference photo of Baba (already in the repo)
production/manifest.json          the full list: every image, size, safe area, prompt
production/character-sheets.md    prompts for the character model sheets
production/pages/pNN.md           one ready package per page (same data as the manifest)
production/scripts/chromakey.py   green background to transparency (for layers)
production/scripts/verify.py      checks all files against the manifest
art/chars/char-<name>.png         approved character sheets
art/<file>.png                    finals: panels are opaque, layers are transparent RGBA
art/progress.json                 JSON list of finished files
viewer/index.html                 the viewer (maintained by Claude; do not edit)
```
Save each final image exactly as art/<file>.png, with the original generated pixels, no resizing, no filters. After each page: run `python production/scripts/verify.py production/manifest.json art`, then `git add art && git commit -m "art: page N" && git push`. Push one page per commit (keep pushes small). Never edit viewer/ or production/manifest.json; if you think the manifest is wrong, say so in your report.

## 8. Order of work
Character sheets, then page 1 (it also fixes the look of the synagogue), then pages 2 to 24 in order. After each page, show the user a contact sheet of that page's images (a simple grid with file names) and wait for approval or notes before continuing, unless the user said to proceed without checking. If an image tool limit stops you, record progress and say exactly where to resume.

## 9. Reporting
After each page, reply with: files produced, any file that needed more than one try and why, any character drift you noticed, and anything you could not do. Be specific and brief.
