import codecs
import re

def fix_admin_students(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        c = f.read()

    c = re.sub(r'startDate\?: string;\s*endDate\?: string;', 'dutyDay?: string;', c)
    c = re.sub(r'const \[periodStart, setPeriodStart\] = useState\(""\);\s*const \[periodEnd, setPeriodEnd\] = useState\(""\);', 'const [dutyDay, setDutyDay] = useState("");', c)
    
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(c)
        
fix_admin_students('d:/งานมด/duty-app/src/app/admin/students/page.tsx')
print("Fixed!")
