import codecs
import re

path = 'd:/งานมด/duty-app/src/app/admin/page.tsx'

with codecs.open(path, 'r', 'utf-8') as f:
    c = f.read()

c = re.sub(r'const \[isAuthenticated, setIsAuthenticated\] = useState\(false\);\s*', '', c)
c = re.sub(r'const \[pin, setPin\] = useState\(""\);\s*', '', c)
c = re.sub(r'const \[pinError, setPinError\] = useState\(false\);\s*', '', c)

old_useEffect = """  useEffect(() => {
    const authStatus = localStorage.getItem("adminAuth");
    if (authStatus === "true") {
      setIsAuthenticated(true);
      fetchData();
    }
  }, []);"""
new_useEffect = """  useEffect(() => {
    fetchData();
  }, []);"""
c = c.replace(old_useEffect, new_useEffect)

c = re.sub(r'  const handleLogin = async.*?};\n\n', '', c, flags=re.DOTALL)
c = re.sub(r'  const handleLogout =.*?};\n\n', '', c, flags=re.DOTALL)
c = re.sub(r'<button onClick={handleLogout}.*?</button>', '', c, flags=re.DOTALL)
c = re.sub(r'  if \(!isAuthenticated\) \{.*?return \(.*?\);\n  }\n\n', '', c, flags=re.DOTALL)

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(c)

print("Removed redundant login!")
