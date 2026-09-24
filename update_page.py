import codecs
import re

path = 'd:/งานมด/duty-app/src/app/page.tsx'

with codecs.open(path, 'r', 'utf-8') as f:
    c = f.read()

# Remove SMTE logo and gap class
c = c.replace('gap-6', '')
# Regex to remove the SMTE logo line and the comment above it
c = re.sub(r'\{\/\* eslint-disable-next-line @next\/next\/no-img-element \*\/\}\s*<img src="/smte-pakchong-logo\.png".*?/>', '', c, flags=re.DOTALL)

# Replace the text block
old_text = """        <div className="text-center mt-3">
          <p className="text-lg md:text-xl font-extrabold text-blue-900 tracking-wide">
            โครงการห้องเรียนพิเศษวิทยาศาสตร์ คณิตศาสตร์ เทคโนโลยี และสิ่งแวดล้อม (SMTE)
          </p>
          <p className="text-base md:text-lg font-bold text-blue-800 mt-1">ระดับมัธยมศึกษาตอนปลาย</p>
        </div>"""

new_text = """        <div className="text-center mt-3">
          <p className="text-2xl md:text-3xl font-extrabold text-blue-900 tracking-wide">
            โรงเรียนปากช่อง
          </p>
          <p className="text-lg md:text-xl font-bold text-blue-800 mt-2">จังหวัดนครราชสีมา</p>
        </div>"""

c = c.replace(old_text, new_text)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(c)

print("Updated page.tsx!")
