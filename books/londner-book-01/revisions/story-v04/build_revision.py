from pathlib import Path
import copy, json, re, html, base64, hashlib

V=Path(__file__).resolve().parent
B=V.parents[1]
old=json.loads((B/'revisions/story-v03/book.json').read_text())
book=copy.deepcopy(old)
original={t['id']:t for p in old['pages'] for q in p['panels'] for t in q['texts']}
src={p['id']:p['text'] for p in json.loads((B/'research/pages.json').read_text())}

def Q(id): return {'quote':id}
def T(he,en,**kw): return dict(he=he,en=en,**kw)

# Empty lists are intentional silent panels, not missing copy.
COPY={
'p01-1':[T('1971.','1971.',status='editorial'),Q('p01-1-t1')],
'p01-2':[Q('p01-2-t1')],
'p02-1':[T('נולדתי ביונדזיוב שבפולין בשנת 1900.','I was born in Jędrzejów, Poland, in 1900.'),T('שמי יצחק מאיר לונדנר. בבית קראו לי איטשע.','My name is Yitzhak Meir Londner. At home, they called me Itshe.')],
'p03-1':[T('בבית שלנו הייתה חנות עורות, ושמונה ילדים.','Our home had a leather shop, and eight children.')],
'p03-2':[],
'p03-3':[T('כשנרדמנו, אמא עוד תיקנה את הבגדים שלנו למחר.','Once we were asleep, Mother still mended our clothes for the next day.')],
'p04-1':[T('שכבתי במיטה בגלל הרגליים. אחי חיים עזר לי ללמוד לכתוב.','I was in bed because of my feet. My brother Chaim helped me learn to write.')],
'p04-2':[Q('p04-2-t1')],
'p04-3':[T('אפילו נייר שעטף סחורה הפך אצלי לחומר קריאה.','Even newspapers used to wrap goods became something I could read.')],
'p05-1':[T('מוורשה חזרתי בלי להחלים לגמרי. אז אבא לקח אותי לטיפול בווינה.','I came home from Warsaw before I had fully healed. Then Father took me to Vienna for treatment.')],
'p05-2':[T('כשאבא חזר הביתה, נשארתי בבית החולים לבדי.','When Father went home, I stayed in the hospital on my own.')],
'p05-3':[],
'p05-4':[Q('p05-4-t1')],
'p06-1':[T('כעבור שנים איבדתי את אמא, ואחר כך את אבא.','Years later, I lost Mother, and then Father.')],
'p06-2':[T('לא יכולנו להישאר כולנו יחד. חלקנו עברו לגור אצל קרובים.','We could not all stay together. Some of us went to live with relatives.')],
'p06-3':[T('1914. באירופה פרצה מלחמת העולם הראשונה.','1914. The First World War broke out in Europe.',status='editorial')],
'p07-1':[T('חזרתי לעיר שלנו. ניסינו להרוויח מספיק לאוכל.','I returned to our town. We tried to earn enough for food.')],
'p07-2':[T('חיילים לקחו אותנו לתקן דרכים. לא נתנו לנו ללכת.','Soldiers took us to repair roads. We were not free to leave.')],
'p07-3':[T('אחר כך חיפשו דוברי גרמנית. ידעתי את השפה, והתחלתי לעבוד עם מודדי דרכים.','Later, they needed German speakers. I knew the language and began working with road surveyors.')],
'p08-1':[T('בכפרים ראיתי אנשים מגדלים את האוכל שלהם.','In the villages, I saw people growing their own food.'),Q('p08-1-t1')],
'p08-2':[T('רציתי להיות חקלאי בארץ ישראל. אבל לא קיבלתי דרכון.','I wanted to be a farmer in the Land of Israel. But I could not get a passport.')],
'p09-1':[T('במקום לעלות לארץ, נקראתי לצבא הפולני. ב־1920 השתחררתי.','Instead of moving to the Land of Israel, I was called into the Polish army. I was released in 1920.')],
'p09-2':[T('ב־1922 התחתנתי עם חוה. עכשיו היינו משפחה.','In 1922, I married Chava. Now we were a family.')],
'p09-3':[T('עבדנו בחנות. שוב נקראתי לצבא, ושוב חזרתי. החלום נשאר.','We worked in a shop. I was called into the army again, and came home again. The dream stayed with me.')],
'p10-1':[T('ביקשתי אישור לעלות. אנשים שהכירו אותי כתבו מכתבים כדי לעזור.','I applied for permission to immigrate. People who knew me wrote letters to help.')],
'p10-2':[],
'p10-3':[T('1925. אחרי כל ההמתנה, הגיע האישור.','1925. After all that waiting, permission finally came.')],
'p11-1':[],
'p11-2':[T('חוה, בתנו הקטנה חנהצ׳ילה ואני יצאנו לדרך.','Chava, our little daughter Chanatshile, and I set off.')],
'p11-3':[T('ברכבת לקונסטנצה שברומניה. משם נפליג לארץ ישראל.','By train to Constanța, in Romania. From there, we would sail to the Land of Israel.')],
'p12-1':[T('בערב סוכות עלינו על האונייה ״אסיה״.','On the eve of Sukkot, we boarded the Asia.')],
'p12-2':[Q('p12-2-t1'),T('בחול המועד סוכות הגענו לארץ ישראל.','During the festival of Sukkot, we reached the Land of Israel.')],
'p13-1':[T('עוד לא הייתה מדינת ישראל. בארץ שאליה הגענו שלטו הבריטים.','There was no State of Israel yet. The country we had reached was under British rule.',status='editorial')],
'p13-2':[T('חשבתי שנותנים לנו אטריות...','I thought they were serving us noodles...')],
'p13-3':[T('זו הייתה חלבה! בארץ החדשה היו לי עוד הרבה דברים ללמוד.','It was halva! I still had plenty to learn in this new country.')],
'p14-1':[T('אבל קודם היינו צריכים חדר ועבודה. קרוב משפחה עזר לנו לחפש.','But first, we needed a room and work. A relative helped us look.')],
'p14-2':[Q('p14-2-t1')],
'p14-3':[T('זה היה אליהו, בן משפחה שלי. הוא עזר לי למצוא עבודה במחסן עצים.','It was Eliyahu, a relative of mine. He helped me find work at a timber yard.')],
'p15-1':[T('אחרינו הגיעו גם אחותה של חוה ובעלה שמעון.','Chava’s sister and her husband Shimon arrived after us.')],
'p15-2':[T('לקחתי את שמעון למחסן. עכשיו חיפשנו עבודה יחד.','I took Shimon to the yard. Now we looked for work together.')],
'p15-3':[T('כאן נולדה בתם אסתר, האחיינית של חוה.','Their daughter Esther was born here. She was Chava’s niece.')],
'p16-1':[T('1928. חנהצ׳ילה שלנו חלתה ונפטרה. לא הצלחנו להציל אותה.','1928. Our Chanatshile became ill and died. We could not save her.')],
'p16-2':[T('בשנים שאחר כך נולדו חיה ומנחם.','In the years that followed, Chaya and Menachem were born.')],
'p16-3':[T('בנינו חדר משלנו. ועדיין רציתי לעבוד באדמה.','We built a room of our own. And I still wanted to work the land.')],
'p17-1':[T('עזרתי לאחי ראובן להגיע. אחר כך פעלתי להביא גם את משפחתו.','I helped my brother Reuven come here. Then I worked to bring his family too.')],
'p17-2':[],
'p17-3':[T('אבל לא כולם נשארו. אסתר והוריה חזרו לאירופה.','But not everyone stayed. Esther and her parents returned to Europe.')],
'p18-1':[T('גם הרשל, הבן של אחי חיים, רצה לבוא לארץ.','Hershel, my brother Chaim’s son, wanted to come here too.')],
'p18-2':[T('אספנו כסף כדי לעזור לו להגיע.','We raised money to help him come.')],
'p18-3':[T('1939. מלחמת העולם השנייה פרצה.','1939. The Second World War broke out.',status='editorial')],
'p18-4':[Q('p18-4-t1'),T('לא ידעתי אם הכסף הגיע אליו.','I did not know whether the money had reached him.')],
'p19-1':[T('1943. המלחמה נמשכה. אני עבדתי במחסן.','1943. The war continued. I was working in a warehouse.')],
'p19-2':[T('ואז הודיעו לי שאני מפוטר.','Then I was told I had lost my job.')],
'p19-3':[T('חשבתי שהגיע הזמן לנסות את מה שחלמתי עליו כנער.','I thought it was time to try what I had dreamed of as a boy.')],
'p20-1':[T('דרשתי פיצויים על שנות העבודה. אחרי מאבק, הגענו להסכמה.','I asked to be paid for my years of work. After a struggle, we reached an agreement.')],
'p20-2':[T('חיה ואני חיפשנו משק בעמק יזרעאל.','Chaya and I looked for a farm in the Jezreel Valley.')],
'p20-3':[T('מכרתי רכוש ולוויתי כסף. סוף סוף קנינו משק בכפר ברוך.','I sold property and borrowed money. At last, we bought a farm in Kfar Baruch.')],
'p21-1':[Q('p21-1-t1')],
'p21-2':[],
'p21-3':[Q('p21-3-t1')],
'p21-4':[T('חיה למדה אצל השכנים, ולימדה אותנו לקטוף תירס.','Chaya learned from the neighbors and taught us how to harvest corn.')],
'p22-1':[T('מהחיטה שהשגנו יצא לחם מר. זה היה הלחם שהיה לנו.','The wheat we got made bitter bread. It was the bread we had.')],
'p22-2':[],
'p22-3':[T('עבדנו גם אצל השכנים. הם עזרו לנו, ואנחנו עזרנו להם.','We worked for our neighbors too. They helped us, and we helped them.')],
'p23-1':[T('עד שגנבו לנו את הסוסים.','Then our horses were stolen.')],
'p23-2':[Q('p23-2-t1')],
'p23-3':[T('עכשיו אנחנו היינו צריכים עזרה. כתבתי לקרובים בחוץ לארץ.','Now we needed help. I wrote to relatives overseas.')],
'p24-1':[T('אחרי מלחמת העולם השנייה, שהסתיימה באירופה ב־1945.','After the Second World War, which ended in Europe in 1945.',status='editorial'),T('בשואה איבדנו בני משפחה.','We lost family members in the Holocaust.')],
'p24-2':[T('אסתר נשארה בחיים. הגיע ממנה מכתב מגרמניה.','Esther had survived. A letter from her arrived from Germany.')],
'p24-3':[T('היא ביקשה עזרה לצאת משם. התחלתי לפעול כדי להביא אותה אלינו.','She asked for help to leave. I began working to bring her here.')],
'p25-1':[T('הבאתי מתל אביב את תעודת הלידה שלה. אסתר הרי נולדה כאן!','I brought her birth certificate from Tel Aviv. Esther had been born here!')],
'p25-2':[T('אבל תעודה אחת לא הספיקה. שאלו אם אוכל לדאוג לה.','But one document was not enough. They asked whether I could provide for her.')],
'p25-3':[],
'p26-1':[T('הקרובים שלחו עזרה. איך אחלק את הכסף, למשק או למשפחה בגרמניה?','Our relatives sent help. How should I divide the money, between the farm and the family in Germany?')],
'p26-2':[T('לקנות סוסים או לעזור לאסתר?','Buy horses, or help Esther?',status='editorial')],
'p27-1':[T('הדוד כתב לי:','My uncle wrote to me:'),Q('p27-1-t1')],
'p27-2':[T('חזרנו לעבוד עם סוסים. כך יכולתי להמשיך לעזור.','We worked with horses again. That meant I could keep helping.')],
'p27-3':[T('גם הניירות לאסתר היו מוכנים. שלחתי אותם לגרמניה.','Esther’s papers were ready too. I sent them to Germany.')],
'p28-1':[T('ואז הגיע מברק. אסתר בדרך!','Then a telegram arrived. Esther was on her way!')],
'p28-2':[],
'p28-3':[T('בנמל חיפה יצאתי בסירה אל האונייה.','At Haifa harbor, I went out to the ship in a boat.'),T('וינגרטן','Weingarten!',status='quote',source='S08-memoir-112',role='speech',speaker='יצחק')],
'p29-1':[T('היא הכירה אותי מהתמונה.','She recognized me from the photograph.')],
'p29-2':[Q('p29-2-t1')],
'p30-1':[T('הבאתי אותה לכפר. גם שם הייתה שמחה גדולה.','I brought her to the village. There was great joy there too.')],
'p30-2':[T('המשפחה עזרה לה להתחיל מחדש. בהמשך אסתר ויחזקאל התחתנו.','The family helped her start again. Later, Esther and Yehezkel married.')],
'p30-3':[T('לחגיגה הבאתי מהמשק שלנו יין וירקות.','I brought wine and vegetables from our farm for the celebration.')],
'p31-1':[T('לא תמיד היה לי זמן להיות עם הנכדים.','I did not always have time to be with my grandchildren.'),Q('p31-1-t1')],
'p31-2':[T('מה אקח איתי?','What will I take with me?',status='editorial'),T('ללמוד, גם ממי שקטן ממני.','Learn, even from someone younger than me.',status='editorial'),T('לבקש עזרה כשאני צריך.','Ask for help when I need it.',status='editorial'),T('ולעזור כשאני יכול.','And help when I can.',status='editorial')],
'p32-1':[T('בספר הבא','In the next book',status='editorial'),T('הילדים גדלים. טרקטורים מגיעים לשדות. ומה יהיה על המשק?','The children are growing up. Tractors are coming to the fields. What will happen to the farm?',status='editorial'),T('המשך יבוא.','To be continued.',status='editorial')]
}

# Editorial connections belong in the working script, never in a reader foreword.
BRIDGES=[
('אדם משאיר זיכרון למשפחתו','מן העט עוברים לילד שהיה'),
('שם ופנים לפני תארים ומסרים','הקורא נכנס לבית שבו גדל'),
('הדאגה בבית נראית במעשים','הילד עצמו נזקק לעזרה'),
('אפשר ללמוד גם כשהרגליים אינן מאפשרות לצאת','עזרה בלימודים אינה מרפאה את הרגל'),
('עזרה מאפשרת לחזור הביתה','כעבור שנים הבית משתנה כשמאבדים את ההורים'),
('אובדן ופיזור בין קרובים','המלחמה מחייבת לחפש דרך להתקיים'),
('ידיעת שפה פותחת אפשרות עבודה','העבודה מביאה אותו לכפרים'),
('נולד רצון ברור: חקלאות בארץ ישראל','היעדר דרכון והשירות דוחים את היציאה'),
('שנים עוברות ונבנית משפחה, אבל היעד נשמר','ניסיון נוסף להשיג את האישורים'),
('המתנה שנענית סוף סוף','המסמכים הופכים לתנועה ולאריזה'),
('משפחה יוצאת עם מה שתוכל לשאת','הרכבת מביאה אל ההפלגה'),
('הגעה ממשית אל היעד הגאוגרפי','עכשיו מתחיל הצורך ללמוד לחיות כאן'),
('הומור מתוך פער אמיתי בין מוכר לחדש','לצד הארוחה יש צורך בחדר ובעבודה'),
('אדם מזהה אותו ועוזר לו להתחיל','גם הוא יכול לצרף אדם נוסף לחיפוש עבודה'),
('מעבירים עזרה הלאה; מכירים את אסתר כחלק מהמשפחה','באותו בית יש גם אובדן וגם המשכיות'),
('אובדן נשמר כאובדן; נולדים ילדים ונבנה חדר','בית משלך מעורר דאגה גם למשפחת האח'),
('חלק מהמשפחה באה וחלקה חוזרת לאירופה','ניסיון נוסף להביא בן משפחה עומד להיקטע'),
('המלחמה עוצרת דרך ממשית ולא קטע מידע כללי','בינתיים ממשיכים להתפרנס בארץ'),
('אובדן העבודה מחזיר אל החלום שנולד בכפרים','כדי לנסות צריך כסף ומשק מתאים'),
('משיגים משק במחיר ממשי של רכוש והלוואה','הגעה למקום אינה ידיעה כיצד לעבוד בו'),
('הילד שהיה תלמיד הוא אב שלומד גם מילדיו','הלמידה נמשכת באוכל, בדרך ובעבודה'),
('מתחילים להתקיים בעבודה ובעזרה הדדית','גניבת הסוסים פוגעת ביכולת הזאת'),
('גם המבוגר המסייע צריך לבקש עזרה','לצד בעיית המשק מתברר הצורך של אסתר'),
('אסתר מן החלק הראשון חוזרת כאדם שאפשר לעזור לו','הכוונה צריכה להפוך לניירות ולאחריות מעשית'),
('תעודת הלידה מקדמת, אבל אינה מספיקה','הקושי לדאוג לה נפגש עם מצוקת המשק'),
('שתי משימות נראות מתחרות על אותו כסף','עצת הדוד מגלה קשר שלא היה ברור'),
('יכולת לעבוד מאפשרת להמשיך לעזור','הניירות הופכים להפלגה אמיתית'),
('מברק, מסע לנמל וקריאה אל הסיפון','הקורא מחכה לתשובה אנושית, לא להודעה מנהלית'),
('ההכרה היא התשובה; נותנים מקום לשמחה','המפגש מאפשר התחלה חדשה'),
('התוצרת מהמשק מגיעה לשמחה משפחתית','המעשים מסבירים מי האיש שכתב את המחברת'),
('אדם עסוק, לא מושלם, שאהב; שלוש אפשרויות קצרות לקורא','הבית נבנה, אך חייו אינם מסתיימים כאן'),
('שאלה חדשה, נפרדת מסיום העלילה','ספר 2 בלי גילוי תוצאותיו')
]

VISUALS={
'p03-1':'הבית והחנות באותה סצנה. בדים ועורות, לא ייצור נעליים. צפיפות משפחתית חמה, ללא המצאת מראה מזוהה של האחים.',
'p03-2':'פאנל ללא כיתוב: בסיום יום הופך שטח החנות למקום שינה. המיטות והמלאי צריכים להיראות יחד כדי שהילד יבין את ההחלפה.',
'p04-1':'איטשע במיטה, חיים מציע דף. זהו קושי מוחשי, לא דיוקן של ילד שמודגם בו מסר. אין פצע גלוי.',
'p04-3':'העיתון עדיין כולל קיפול של עטיפת סחורה. רואים שהוא יכול לקרוא במיטה. אין כותרת מזויפת או תאריך שלא נבדק.',
'p05-1':'מפה בשכבת HTML/SVG: יונדזיוב, ורשה, חזרה הביתה, ואז וינה. אין לתאר זאת כנסיעה רצופה אחת בין שני בתי חולים.',
'p05-3':'פאנל ללא כיתוב: אישה מסיעה בעגלת חולים את הילד אל בית הכנסת בבית החולים. הפעולה צריכה להיראות כעזרה, בלי בועה או תואר מקצועי מומצא.',
'p06-1':'זמן עבר מפורש. שני המקומות של ההורים ריקים. לא להוסיף תיאור מוות או דמות ליד מיטת מוות.',
'p07-3':'הנער מתווך בין מודד אוסטרי לחקלאי פולני. כלי המדידה נראים בבירור. אין לקשור את ידיעת הגרמנית לאשפוז בלי מקור.',
'p10-2':'פאנל ללא כיתוב: תיק בקשות אצל פקיד. אין חותמת סירוב, מספר ניסיונות, שעון קופץ או דחייה שלא תועדו.',
'p11-1':'פאנל ללא כיתוב: נארזים מזון יבש, פרימוס ושמיכות. הפרטים מוסרים את היקף ההכנה בלי רשימת ציוד בקריינות.',
'p13-2':'תקריב תגובתו למאכל הלבן. עדיין לא לחשוף את ההסבר. זו אינה תמונת אטריות אמיתיות.',
'p13-3':'תיקון שוט: נשארים באותה ארוחה, ורואים את החלבה בצלחת. אין לצייר כאן את המשפחה מול מגורים כפי שהוצע בגרסה הקודמת. הגילוי והכיתוב מגיעים יחד.',
'p15-1':'אחותה של חוה ובעלה מגיעים עם צרורות. ללא המצאת דיוקנאות מזוהים. אין מסר או רמז על גורלם העתידי.',
'p15-2':'תיקון שוט: יצחק ושמעון ליד מחסן העצים, מחפשים אפשרות לעבוד. הפעולה מבוססת על דף 64, ומחליפה את תמונת התינוקת הקודמת.',
'p15-3':'תרשים משפחתי קטן ב־HTML/SVG או דימוי משפחה לא מתועד: חוה, אחותה ומשפחתה, ובתם אסתר. זהו זיהוי קשר, לא תצלום קבוצתי היסטורי.',
'p16-1':'להשאיר מרחב שקט סביב חנהצ׳ילה. לא לעבור בתוך אותו פאנל אל התינוקות החדשים ולא להציג לידה כמחיקת האובדן.',
'p17-2':'פאנל ללא כיתוב: פעולת סידור ניירות ועבודה למען משפחת ראובן. אין להראות את בואה כאירוע מאומת אם המקור הוא בקשה בלבד.',
'p17-3':'מפה גרפית של החזרה לאירופה. מעבר רגיל בשנות השלושים, ללא חיזוי גרפי של המלחמה הבאה או תאריך מומצא.',
'p20-3':'משק צנוע עם אדמה, רפת וכרם ברקע לפי התיאור. אין להציג את הפיצויים כמקור הכסף היחיד לקנייה.',
'p21-1':'אבא, שחלם שנים על חקלאות, אינו יודע לפתוח את המחרשה. ההפתעה גלויה עכשיו ולא מוקדמת בכיתוב העמוד הקודם.',
'p21-2':'פאנל ללא כיתוב: מנחם משחק בידית המחרשה. מסמנים בתנועה את הידית שקפצה. אין להוסיף דיבור או להציג אותו כמדריך מקצועי.',
'p21-3':'אותו מנגנון נפתח, והאב רואה את המעשה. הציטוט הקצר מספיק; אין להוסיף מוסר על לימוד מהילדים.',
'p22-2':'פאנל ללא כיתוב: איסוף אבנים ודרך הנבנית בחצר הבוצית. רואים את הבוץ ואת הדרך, בלי להוסיף נפילה או סכנה מומצאת.',
'p23-1':'הקורא מגלה מקום ריק של סוסים. ללא ציור גנבים, לילה מסוים או סיבת גניבה שלא תועדה.',
'p24-1':'רכיב גרפי של רקע היסטורי אחרי המלחמה. 1945 מתארת את סוף המלחמה באירופה בלבד. אין להציג שנה זו כתאריך המכתב או הגעת אסתר.',
'p24-3':'יצחק מתחיל לפעול, עם כתובות ופניות כלליות. אין להראות שכבר מצא תעודת לידה בביתו; המקור אומר שהביא אותה מתל אביב.',
'p25-3':'פאנל ללא כיתוב: המשך איסוף והגשת ניירות. התהליך מתקדם, אך עדיין אין אישור בידי יצחק. בלי טקסט או חותמות מומצאות בתוך האיור.',
'p26-2':'שאלה קצרה לקורא מעל דימוי סוסים ועזרה לאסתר. אין לכתוב את הפתרון, אין סכומי כסף מומצאים ואין שתי ערימות כסף היסטוריות.',
'p27-2':'העבודה עם הסוסים מתחדשת. אין ציור העברת כסף מסוימת לאסתר: אין תיעוד לחלוקה מדויקת של אותו סכום.',
'p28-2':'פאנל ללא כיתוב: יציאה לכיוון הנמל. לשמור מעבר גאוגרפי ברור, בלי לקבוע אמצעי תחבורה יבשתית שלא נזכר.',
'p28-3':'יצחק בסירה מול סיפון האונייה. הקריאה בשם המשפחה בשכבת טקסט חיה סמוכה לדובר. אין עדיין תשובה של אסתר או פרטי אונייה שלא זוהו.',
'p29-1':'נותנים לגילוי זמן: אסתר מזהה אותו. אין להמחיז הבאת צילום מסוים בכיס או ביד; ידוע רק שהכירה אותו לפי תמונה.',
'p30-3':'יין וירקות מן המשק מובאים לחתונה. הכרם והיבול שכבר נראו חוזרים עכשיו בשמחת המשפחה. אין לכתוב מעליהם מסר מופשט.',
'p31-1':'חזרה ליד המבוגרת ולמחברת של 1971. אין נכדים יושבים סביבו במפגש שלא תועד. הכיתוב מראה גם את קוצר הזמן, לא סבא מושלם.',
'p32-1':'הזמנה עריכתית לספר הבא: משק מוכר, ילדים שגדלו וטרקטור מרוחק. אין אירוע איום, מכירה או תוצאת הסיפור הבא.'
}

from revision_changes import apply_revision
apply_revision(COPY,VISUALS,BRIDGES,T,Q,book)
registry=[]; panels=[]
for p in book['pages']:
    focus,bridge=BRIDGES[p['number']-1]
    p['action']=focus;p['turn_hook']=bridge
    p['story_function']=focus;p['connection_to_next_page']=bridge
    p['review_notes']=(p.get('review_notes','')+' גרסה 0.4: נוסח מעובד חדש לעיון המשפחה. שתיקה בפאנל היא הוראה לאיור, לא טקסט חסר.').strip()
    for q in p['panels']:
        q['previous_texts']=copy.deepcopy(q['texts'])
        texts=[]
        for i,s in enumerate(COPY[q['id']],1):
            if 'quote' in s:
                t=copy.deepcopy(original[s['quote']]);t['preserved_from']=s['quote']
                if t['id']=='p14-2-t1':t.update(role='speech',speaker='אליהו')
                if t['id']=='p01-1-t1':t.update(role='inscription')
            else:
                t=dict(id=f"{q['id']}-v04-t{i}",he=s['he'],en=s['en'],status=s.get('status','adapted'),role=s.get('role','caption'),speaker=s.get('speaker','יצחק' if s.get('status','adapted')!='editorial' else 'מסגרת עריכתית'),source=s.get('source',p['sources'][0]),sources=p['sources'],review_required=s.get('status','adapted')!='quote',wording_origin='new editorial draft 0.4, not a verbatim historical statement')
                if t['status']!='quote':registry.append(dict(panel=q['id'],**t))
            if t['status']=='quote':
                # Whitespace is insignificant; punctuation may frame an excerpt.
                needle=' '.join(t['he'].strip(' .!?,:;').split())
                hay=' '.join(src[t['source']].split())
                assert needle in hay,(t['id'],needle)
            assert not re.search('[—–]',t['he'])
            texts.append(t)
        q['texts']=texts
        q['silent']=not texts
        q['visual']=VISUALS.get(q['id'],q['visual'])
        q['image_only_information']=q['visual'] if not texts else 'התנועה, המבט והפרטים החזותיים אינם מתוארים שוב בקריינות.'
        panels.append(q)

book.update(version='0.4-editorial-draft',status='rewritten for family review; not final script or approved new art',source_previous_version='../story-v03/book.json',editorial_principle='A child follows a person pursuing a goal, facing setbacks, learning and helping. Images carry actions; narration supplies context, changes and causal connections. No invented incident for suspense.',story_pages=32)
book['revision_limits']={'max_he_words_per_text_block':18,'max_he_words_per_page':55,'max_exposition_pages':2,'planned_exposition_pages':0,'silent_panels_intentional':True}
assert set(COPY)=={q['id'] for q in panels}
oldwords=sum(len(t['he'].split()) for p in old['pages'] for q in p['panels'] for t in q['texts'])
newwords=sum(len(t['he'].split()) for q in panels for t in q['texts'])
stats=[]
for p in book['pages']:
    ts=[t for q in p['panels'] for t in q['texts']]
    words=sum(len(t['he'].split()) for t in ts)
    assert words<=55,(p['number'],words)
    assert max([len(t['he'].split()) for t in ts] or [0])<=18
    stats.append({'page':p['number'],'he_words':words,'en_words':sum(len(t['en'].split()) for t in ts),'silent_panels':[q['id'] for q in p['panels'] if q['silent']]})
quotes=[t for q in panels for t in q['texts'] if t['status']=='quote']
oldquotes=[t['id'] for t in original.values() if t['status']=='quote']
assert set(oldquotes).issubset({t.get('preserved_from') for t in quotes})
report={'version':book['version'],'pages':len(book['pages']),'panels':len(panels),'previous_he_words':oldwords,'revised_he_words':newwords,'text_blocks':sum(len(q['texts']) for q in panels),'silent_panels':[q['id'] for q in panels if q['silent']],'preserved_quotes':len(oldquotes),'verified_quotes_in_this_version':len(quotes),'new_nonquote_text_blocks':len(registry),'reading_context_review':'All 32 pages reviewed for first introduction, cause before result, and warmth supported by primary sources','max_he_words_per_page':max(x['he_words'] for x in stats),'max_he_words_per_text_block':max(len(t['he'].split()) for q in panels for t in q['texts']),'planned_dense_exposition_pages':0,'page_word_counts':stats,'checks':{'quote_text_matches_primary_transcript':True,'all_previous_literal_quotes_preserved':True,'no_long_dashes_in_hebrew':True,'all_89_panel_ids_preserved':True,'visual_changes_documented':True},'limitations':['New adapted narration and all new translations require editorial/family review.','No visual browser approval is claimed.','Some historical dates and supporting faces remain unresolved.','This review draft does not overwrite or approve the production branch.']}

(V/'book.json').write_text(json.dumps(book,ensure_ascii=False,indent=2))
(V/'wording-review.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2))
(V/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))

lines=['# הדרך של איטשע · ספר 1 · שכתוב 0.4','טיוטה לעיון המשפחה. הנוסח המעובד הוא חדש, לא ציטוט מפי יצחק. ציטוטים מסומנים ונבדקו מול התמלול.','## חוט הסיפור','ילד שנאלץ לקבל עזרה ממשיך ללמוד. כנער נולד בו רצון לעבוד את האדמה בארץ ישראל. כשהוא סוף סוף משיג משק, הוא מגלה שעליו ללמוד גם מילדיו ולבקש עזרה שוב. מה שהוא בונה נעשה גם דרך לעזור לבני משפחתו. החיבור הזה נשאר כאן בדף העבודה, ואינו תקציר שמופיע בתחילת הספר.']
for p in book['pages']:
    lines += [f"## עמוד {p['number']}: {p['title']}",f"זמן לצוות: {p['time']}",f"תפקיד בסיפור: {p['action']}",f"החיבור להמשך: {p['connection_to_next_page']}"]
    for q in p['panels']:
        lines += [f"### {q['id']}",'כיתוב לקורא:']
        lines += [t['he']+(' [ציטוט מקורי]' if t['status']=='quote' else '') for t in q['texts']] if q['texts'] else ['ללא כיתוב. הפעולה נמסרת בציור.']
        lines += ['מה הציור מוסר: '+q['visual']]
    lines += ['מקורות: '+', '.join(p['sources'])]
(V/'script-he.md').write_text('\n\n'.join(lines))

review=['# נוסח חדש לבדיקה, גרסה 0.4','כל היחידות הבאות הן עיבוד או מסגרת עריכתית חדשה. הן אינן ציטוטים. האנגלית היא תרגום חדש. לא הוספו פגישה עם נכדים, אירוע סכנה או שיחה לא מתועדת.']
for t in registry:review += [f"## {t['id']}",t['he'],t['en'],'מקורות לאירוע: '+', '.join(t['sources'])]
(V/'wording-review.md').write_text('\n\n'.join(review))
changes=['# שינויי איור נדרשים לפני הפקה','אין לשלב טקסט חדש בתמונה שהפעולה בה אינה תואמת. אין לייצר את כל הספר מחדש לפני עיון בנוסח.']
for pid,v in VISUALS.items():changes += [f'## {pid}',v]
(V/'visual-handoff.md').write_text('\n\n'.join(changes))

# Reuse the actual geometric reader, but keep this revision fully separate.
assets=json.loads((B/'production/manifest.json').read_text())['images']
byq={q['id']:q for q in panels}
for a in assets:
    q=byq[a['id']];a['visual']=q['visual'];a['text_ids']=[t['id'] for t in q['texts']];a['silent']=q['silent']
    a['previous_prompt_status']='Requires comparison with revised visual direction; do not use old prompt blindly.'
    a['revision_visual_direction']=q['visual']
    a['revised_texts']=q['texts']
(V/'manifest-review.json').write_text(json.dumps({'version':book['version'],'images':assets,'notice':'Review data, not a final image-generation manifest. Use revised visual directions; retain original pixels.'},ensure_ascii=False,indent=2))
embedded={};relative={}
for p in (B/'art/web').glob('*.webp'):
    url='data:image/webp;base64,'+base64.b64encode(p.read_bytes()).decode()
    relative['art/web/'+p.name]='../../art/web/'+p.name
    embedded['art/web/'+p.name]=url
for a in assets:
    if a['web_file'] in embedded:
        embedded[a['file']]=embedded[a['web_file']];relative[a['file']]=relative[a['web_file']]
    if a.get('existing_draft'):
        key='art/web/draft-'+a['id']+'.webp'
        embedded[a['existing_draft']]=embedded[key];relative[a['existing_draft']]=relative[key]
embedded['art/chars/yitzhak-child-v02.png']=embedded['art/web/child-reference.webp']
relative['art/chars/yitzhak-child-v02.png']='../../art/web/child-reference.webp'
tpl=(B/'tools/template.html').read_text()
tpl=tpl.replace('</style>','body[data-mode=reader] .caption{min-height:0!important}</style>')
tpl=tpl.replace('const bilingual=t=>bi(t.he,t.en);','const bilingual=t=>`<div class="line-${E(t.role||"caption")}">${bi(t.he,t.en)}</div>`;')
tpl=tpl.replace('</style>','.line-inscription{font-size:.8em;font-family:serif;font-style:italic;padding-top:5px}.line-label{font-size:.86em}</style>')
tpl=tpl.replace("p.panels.map(q=>{const g=byId[q.id].geometry","p.panels.filter(q=>q.texts.length).map(q=>{const g=byId[q.id].geometry")
tpl=tpl.replace('<div class="mobile-caption">${q.texts.map(bilingual).join(\'\')}</div>','${q.texts.length?`<div class="mobile-caption">${q.texts.map(bilingual).join(\'\')}</div>`:\'\'}')
tpl=tpl.replace('32 עמודי סיפור, 89 משבצות.','טיוטת שכתוב 0.4 לעיון: 32 עמודי סיפור, 89 משבצות.')
def render(mode,inline):
    fs=embedded if inline else relative
    return tpl.replace('__DEFAULT_MODE__',mode).replace('__BOOK_DATA__',json.dumps(book,ensure_ascii=False).replace('</','<\\/')).replace('__ASSET_DATA__',json.dumps(assets,ensure_ascii=False).replace('</','<\\/')).replace('__FILES_DATA__',json.dumps(fs,ensure_ascii=False)).replace('__CHAR_DATA__',json.dumps(fs['art/chars/yitzhak-child-v02.png']))
(V/'reader.html').write_text(render('reader',True))
(V/'structure.html').write_text(render('plan',False))

# A lightweight copy-first review makes unwritten panels reviewable without pretending the art is finished.
def esc(s):return html.escape(str(s))
body=[]
for p in book['pages']:
    cards=[]
    for q in p['panels']:
        tx=''.join('<p'+(' class="quote"' if t['status']=='quote' else '')+'>'+esc(t['he'])+'</p>' for t in q['texts'])
        if not tx:tx='<p class="silent">הציור ממשיך בלי כיתוב.</p>'
        prev=''.join('<p>'+esc(t['he'])+'</p>' for t in q['previous_texts'])
        cards.append('<article><small>'+esc(q['id'])+'</small><div class="copy">'+tx+'</div><details><summary>מה רואים בציור</summary><p>'+esc(q['visual'])+'</p></details><details><summary>הנוסח הקודם להשוואה</summary>'+prev+'</details></article>')
    body.append('<section><header><span>עמוד '+str(p['number'])+'</span><h2>'+esc(p['title'])+'</h2></header><div class="panels">'+''.join(cards)+'</div></section>')
out='''<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>הדרך של איטשע · עיון בנוסח 0.4</title><style>*{box-sizing:border-box}body{margin:0;background:#f0eee6;color:#243c31;font:19px/1.7 Arial,sans-serif}main{max-width:1000px;margin:auto;padding:24px}h1{font-size:32px}section{background:#fffdf6;border-radius:12px;margin:24px 0;padding:24px}header{border-bottom:1px solid #dedccf;margin-bottom:20px}header span,small{font-size:13px;color:#677868}h2{margin:3px 0 12px;font-size:23px}.panels{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}article{border:1px solid #dfdfce;padding:18px;border-radius:9px}.copy{min-height:100px;font-size:23px}.copy p{margin:12px 0}.silent{color:#7a806f;font-size:16px;font-style:italic}details{font-size:14px;border-top:1px solid #eee;padding-top:12px}summary{cursor:pointer}.note{font-size:16px;color:#526453}@media print{section{break-inside:avoid}.note,details{display:none}}</style><main><h1>הדרך של איטשע · ספר 1</h1><p class="note">עיון בנוסח החדש, גרסה 0.4. זהו דף עריכה, ולא פריסת הספר. כותרות העמודים וסימוני השתיקה מיועדים לעיון בלבד. פתחו את ״מה רואים בציור״ כדי לבדוק מה אינו נאמר במילים.</p>'''+''.join(body)+'</main></html>'
(V/'wording-review.html').write_text(out)
print(json.dumps({k:v for k,v in report.items() if k!='page_word_counts'},ensure_ascii=False,indent=2))
