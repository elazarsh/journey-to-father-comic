> **ענף העבודה המשותף עודכן:** `claude/londner-script-review` כולל כעת 170 מקורות איור. [מפתח חזותי של כל התמונות](revisions/book1-v08/qa/art-inventory.html). נוספה [עטיפה ייעודית לעיון](art/book1-v08-cover/cover-v01.png). קובצי ה־PDF הישנים טרם הופקו מחדש. [פירוט תיקון המסירה](handoffs/codex/BOOK1-V08-ART-COMPLETION.md).

> **ספר 1: כל 170 מקורות האיור הושלמו.** [תצוגת עבודה](revisions/book1-v08/sketch.html), [מסירה לקלוד והערות השילוב](handoffs/codex/BOOK1-V08-ART-COMPLETION.md). זו אינה בדיקת עימוד סופית.

> Current image production follows Claude v0.8: [layout and lettering](revisions/book1-v08/layout-plan.json), [image requests](handoffs/claude/v08-image-requests.md), [live sketch](revisions/book1-v08/sketch.html). Book2 belongs to Claude; Codex is producing book1 images only.

> **גרסה 0.8 (עימוד קומיקס, Claude):** [הסקיצה](revisions/book1-v08/sketch.html), [התסריט 0.8](revisions/book1-v08/script-v08-he.md), [בקשות תמונה](handoffs/claude/v08-image-requests.md). בתסריט 0.7 הוחלפו שורות שהומצאו במילים מהיומן ([מה שונה](revisions/book1-v07/claude-review/changes-applied-he.md)).

> העלילה ודמות יצחק אושרו. גרסה 0.7 מוסיפה פתיחה ברורה, דיבור ומחשבה ופריסות מגוונות. [תור התמונות הפעיל](revisions/book1-v07/production/manifest.json). הסגנון: דרמטי ופסטורלי.

> גרסה פעילה לעיון: [ספר 1, גרסה 0.7](revisions/book1-v07/README.md), [קריאת הסקיצה](revisions/book1-v07/book1-reader.html). לפי הבהרת המשפחה: שלושה ספרים, ו־48 עמודי ספר 1 עד היציאה באונייה, לפני ההגעה. הנחיות המשפחה והגילים: [רציפות הדמויות](revisions/book1-v07/family-continuity.md). תיאור ההפקה בן 32 העמודים להלן נשמר לארכיון ואינו רשימת האיורים הפעילה.

# הדרך של איטשע · ספר 1

חבילת הפקה פרטית לספר על יצחק מאיר לונדנר, לילדים מגיל 10 ולמבוגרים. גרסה 0.2, סקיצה להמשך עבודה.

## נקודות כניסה

- [מפת הספר והחיתוכים](production/structure.html): כל 32 עמודי הסיפור ו־89 המשבצות, כולל מידע עלילתי מלא לצוות ההפקה.
- [תצוגת קריאה](viewer/index.html): פתיחה קצרה ללא תקציר עלילתי. הסקיצה אינה ספר מאויר גמור.
- [הנחיות לכל תמונה](production/manifest.json), [מידות וצורות](production/geometry.json), [טקסט חי בעברית ובאנגלית](production/text.json).
- [מצב האיורים](art/progress.json), [תיעוד יצירה ופסילות](production/generation-receipts.json), [המשך העבודה](HANDOFF.md).
- [נוסח חדש לבדיקה](production/new-wording-review.md). השורות החדשות אינן ציטוטים של יצחק.

התמונות המקוריות נשמרות ב־art; קובצי WebP ב־art/web הם עותקי תצוגה. קובצי art/drafts הם סקיצות מהסבב הקודם, ואינם התאמה מאושרת למסגרות החדשות. art/rejected מכיל ניסיונות שנפסלו, ואין לשלבם בספר.

לפתיחה בדפדפן אפשר לפתוח את קובצי HTML ישירות, או להריץ `python -m http.server 8000` מתוך התיקייה ולגלוש ל־`http://localhost:8000/production/structure.html`.

לרענון ה־HTML לאחר עדכון איורים: `python tools/render.py`. נדרשת ספריית Pillow. לבדיקה: `python tools/verify.py`.

יעד המסירה הוא המאגר הפרטי elazarsh/journey-to-father-comic, בענף codex/londner-book-01-v07-art ובתיקייה books/londner-book-01. תיעוד אימות ההעלאה נשמר בקובץ handoffs/codex/state.json כשאימות מרחוק הושלם. אין לפרסם חומר משפחתי או תצלומי מקור באתר ציבורי.
