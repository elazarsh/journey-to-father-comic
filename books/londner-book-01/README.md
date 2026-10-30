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
