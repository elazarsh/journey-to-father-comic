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

יעד המסירה הוא המאגר הפרטי elazarsh/journey-to-father-comic, בענף codex/londner-book-01-ready ובתיקייה books/londner-book-01. תיעוד אימות ההעלאה נשמר בקובץ production/github-receipt.json כשאימות מרחוק הושלם. אין לפרסם חומר משפחתי או תצלומי מקור באתר ציבורי.
