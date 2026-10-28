# המסע אל אבא · The Journey to Father

A family comic book (book 1 of "Grandpa Emmanuel's stories"), 24 pages, true story.

## How the work is split
- **Illustration** (Codex / GPT): only standalone pictures, one scene per file. No text, no bubbles, no frames, no page layout.
- **Everything else** (Claude): cropping, panel shapes, gutters, transitions, page structure, parallax, all lettering (Hebrew and English), and publishing the live viewer.

## Layout of this repository
| Path | What it is |
| --- | --- |
| `AGENTS.md` | The full production brief for the illustrator agent |
| `production/manifest.json` | Every image: file name, size, safe area, ready prompt (105 files) |
| `production/pages/pNN.md` | One ready package per page |
| `production/character-sheets.md` | Prompts for the character model sheets |
| `production/scripts/` | `chromakey.py` (layers) and `verify.py` (checks) |
| `ref/baba-photo.jpg` | Reference photo for the Baba character |
| `art/` | The finished images (`pNN-x.png`, layers `pNN-nK.png`), `art/chars/` for sheets |
| `viewer/index.html` | The single-file interactive viewer (source) |
| `research/comic-structure.html` | Research on building a comic in live HTML |

## File naming
`p03-b.png` is panel `b` on page 3. `p01-n1.png` is a transparent layer. The viewer loads images by these exact names.

## Flow
1. Illustrator agent creates character sheets, then pages 1 to 24, one commit per page.
2. Claude pulls `art/`, converts to WebP, publishes the viewer, and the user arranges pages in the viewer's layout editor.
