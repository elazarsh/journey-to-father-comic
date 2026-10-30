"""Write handoffs/claude/v08-image-requests.md for Codex from layout-plan.json and new-panels.json.
    python revisions/book1-v08/make_requests.py"""
import json
from pathlib import Path

V = Path(__file__).resolve().parent
B = V.parents[1]
plan = json.loads((V / 'layout-plan.json').read_text(encoding='utf-8'))
newp = json.loads((V / 'new-panels.json').read_text(encoding='utf-8'))
style = json.loads((B / 'revisions/book1-v07/production/manifest.json').read_text(encoding='utf-8'))['style']
made = {a['id'] for a in json.loads((B / 'art/book1-v07/progress.json').read_text(encoding='utf-8'))['assets']}
insets = {p['inset'] for p in plan['pages'] if p.get('inset')}

L = ['# בקשות תמונה מ־Claude לגרסה 0.8 (ל־Codex)', '',
     'נוצר אוטומטית מ־`revisions/book1-v08/layout-plan.json`. הסקיצה (`revisions/book1-v08/sketch.html`, דרך `python3 -m http.server` מתיקיית הספר) קוראת את `art/book1-v07/progress.json` בכל טעינה, כך שכל תמונה חדשה שנרשמת שם מופיעה מיד בפריסה.', '',
     'אותם כללים: סצנה אחת, בלי טקסט, בלי בועות, בלי מסגרות, מרווח לחיתוך, מקום שקט לכיתוב.', '',
     '## 1. משבצות חדשות', '']
for n in newp:
    circle = n['id'] in insets
    shape = 'עיגול תקריב, 1024x1024' if circle else 'פאנל רגיל, 1536x1024 (לרוחב)'
    L += [f"### {n['id']} (עמוד {n['page']}, {shape})", '', f"מה רואים: {n['shows']}", '', f"ביומן: \"{n['memoir']}\"", '', 'Prompt:', '```', style,
          'ONE scene, ONE image; ' + ('circular close-up composition centered (it will be masked to a circle); ' if circle else 'wide composition with calm space at the top for lettering; ') + 'no lettering, no frames.',
          'Action: ' + n['shows'], '```', '']
L += ['## 2. משבצות שלא לייצר (הוסרו מהפריסה)', '']
for p in plan['pages']:
    for r in p.get('removed', []):
        L.append(f"- {r['id']}: {r.get('why', '')}" + (' (יש תמונה; נשמרת בארכיון, לא בשימוש)' if r['id'] in made else ''))
L += ['', '## 3. שינוי בהוראות הציור', '']
for p in plan['pages']:
    for k, v in p.get('shows_override', {}).items():
        L.append(f"- {k}: {v}" + (' (כבר נוצרה: לבדוק אם צריך מחדש)' if k in made else ''))
L += ['- B01V07-P04-02: ילדים לא מזוהים ישנים בחנות ליד התנור, איטשע ביניהם.',
      '- B01V07-P04-04: ארוחת ערב רגילה (לא שבת), כולם מחכים שאמא תשב.',
      '- B01V07-P12-03, P12-04: הדירה הורחבה (הפילו קיר), ולא "עברו דירה".',
      '- B01V07-P19-04: האב והבן בבית, בלי חפץ שלא מוזכר ביומן.',
      '- B01V07-P23-04: מאיר גיטלר רושם רשימת סחורה בחנות; חיים לידו.',
      '- B01V07-P41-02: המשפחה בחדר, הילדה חולה ושוכבת.', '']
L += ['## 3א. תמונות לצייר אחרת (כדי שכל תמונה תוסיף משהו)', '',
      'לכל תמונה תפקיד: מה היא מוסיפה לרגש, לאווירה או למידע. תמונות סמוכות בעמוד שונות לפחות בשניים: גודל צילום, זווית, אור וצבע, מספר דמויות, מקום.', '']
for p in plan['pages']:
    for pid in p['order']:
        u = p.get('purpose', {}).get(pid, {})
        if u.get('verdict') == 'redirect':
            L.append(f"- {pid} (עמוד {p['page']}){' · קיימת: לייצר מחדש' if pid in made else ''}: {u.get('new_shows_he', '')} | צילום: {u.get('shot', '')} | זווית: {u.get('angle', '')} | אור: {u.get('light', '')} | למה: {u.get('purpose_he', '')}")
L += ['',
      '## 4. משבצות עם בועת דיבור או מחשבה (להשאיר מקום שקט מעל הדובר)', '',
      'משבצת עם בועה מקבלת בפריסה מקום גדול יותר. בציור: הדובר לא צמוד לקצה העליון, ויש שמיים או קיר שקט מעליו.', '']
for p in plan['pages']:
    for pid in p['order']:
        b = [t for t in p['texts'].get(pid, []) if t['type'] in ('speech', 'thought', 'whisper', 'shout') and t.get('he')]
        if b and pid not in made:
            L.append(f"- {pid}: " + '; '.join(f"{t['speaker']} ({t.get('mouth', '')})" for t in b))
L += ['', '## 5. עיגולים', '', 'לפי בקשת המשתמש עיגול תקריב מופיע רק פעם או פעמיים בספר: ' + ', '.join(sorted(insets)) + '. לא להציע עיגולים נוספים.', '']
(B / 'handoffs/claude/v08-image-requests.md').write_text('\n'.join(L), encoding='utf-8')
print(len(newp), 'new panels;', len(L), 'lines')
