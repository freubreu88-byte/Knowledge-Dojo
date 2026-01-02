# 🥋 Vibe-Dojo Dashboard

## 📊 Quick Stats
- **Rank:** Beginner 👶
- **Mastery:** 4 notes verified
- **Streak:** 1 days 🔥
- **Total Drills:** 7

---

## 📅 Due for Practice
```dataview
TABLE 
    status as Status, 
    next_review as "Next Review",
    topics as Topics
FROM "01_Drills"
WHERE next_review <= date(today) 
  AND status != "passed"
  AND status != "bullshit"
  AND status != "outdated"
SORT next_review ASC, status ASC
```

## 🧠 Knowledge Topics
```dataview
TABLE 
    pass_rate as "Mastery %",
    length(file.outlinks) as "Mastery Notes"
FROM "11_Topics"
SORT pass_rate DESC
```

## 🕒 Recent Activity
```dataview
LIST
FROM "02_Practice_Logs"
SORT file.ctime DESC
LIMIT 10
```

---
*Dashboard updated: 2026-01-02 13:15:13*
