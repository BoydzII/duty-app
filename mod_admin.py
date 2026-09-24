import codecs

def modify_admin_students(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        content = f.read()

    # Replace Student interface
    old_student = '  startDate?: string;\n  endDate?: string;'
    new_student = '  dutyDay?: string;'
    content = content.replace(old_student, new_student)

    # Replace periodStart and periodEnd state with dutyDay
    content = content.replace('const [periodStart, setPeriodStart] = useState("");\n  const [periodEnd, setPeriodEnd] = useState("");', 'const [dutyDay, setDutyDay] = useState("");')

    # Replace body in handleSetPeriod
    old_body = 'body: JSON.stringify({ action: "update_period", ids: selectedIds, startDate: periodStart, endDate: periodEnd })'
    new_body = 'body: JSON.stringify({ action: "update_period", ids: selectedIds, dutyDay: dutyDay })'
    content = content.replace(old_body, new_body)

    # Replace periodStart/End checks
    content = content.replace('if (!periodStart || !periodEnd) return alert("กรุณาระบุวันที่เริ่มและสิ้นสุด");', 'if (!dutyDay) return alert("กรุณาระบุวันทำเวร");')

    # Replace the "Set Period" button state clear
    content = content.replace('setPeriodStart("");\n                  setPeriodEnd("");', 'setDutyDay("");')

    # Replace table column header
    content = content.replace('<th className="p-3">ช่วงเวลาฝึกงาน</th>', '<th className="p-3">วันทำเวร</th>')

    # Replace table cell
    old_cell = '''                      <td className="p-3 text-xs text-gray-600">
                        {s.startDate && s.endDate ? (
                          <div className="flex flex-col gap-0.5">
                            <span className="text-green-700 font-medium">เริ่ม: {new Date(s.startDate).toLocaleDateString('th-TH')}</span>
                            <span className="text-orange-700 font-medium">สิ้นสุด: {new Date(s.endDate).toLocaleDateString('th-TH')}</span>
                          </div>
                        ) : <span className="text-gray-400">ยังไม่กำหนด</span>}
                      </td>'''
    new_cell = '''                      <td className="p-3 text-sm font-medium text-gray-700">
                        {s.dutyDay ? (
                          <span className="px-2 py-1 bg-indigo-50 text-indigo-700 rounded-md border border-indigo-100">{s.dutyDay}</span>
                        ) : <span className="text-gray-400">ยังไม่กำหนด</span>}
                      </td>'''
    if old_cell in content:
        content = content.replace(old_cell, new_cell)
    else:
        # try replacing ignoring whitespace using regex or a simpler replace
        import re
        content = re.sub(r'<td className="p-3 text-xs text-gray-600">[\s\S]*?</td>', new_cell, content)
    
    # Replace the modal title and inputs
    old_modal_title = '<h3 className="font-bold text-lg text-gray-800">กำหนดช่วงเวลาฝึกงาน</h3>'
    old_modal_title_2 = '<h3 className="font-bold text-lg text-gray-800">กำหนดช่วงเวลาฝึกงาน (แบบกลุ่ม)</h3>'
    new_modal_title = '<h3 className="font-bold text-lg text-gray-800">กำหนดวันทำเวร (แบบกลุ่ม)</h3>'
    content = content.replace(old_modal_title_2, new_modal_title)
    content = content.replace(old_modal_title, new_modal_title)
    
    # Replace "ตั้งเวลาฝึกงาน"
    content = content.replace('ตั้งเวลาฝึกงาน', 'ตั้งวันทำเวร')
    content = content.replace('กำหนดเวลาฝึกงาน', 'กำหนดวันทำเวร')

    old_inputs = '''              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">วันที่เริ่มฝึกงาน</label>
                  <input type="date" value={periodStart} onChange={e => setPeriodStart(e.target.value)} className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-500 outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">วันที่สิ้นสุด</label>
                  <input type="date" value={periodEnd} onChange={e => setPeriodEnd(e.target.value)} className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-500 outline-none" />
                </div>
              </div>'''
    
    new_inputs = '''              <div className="grid grid-cols-1 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">วันทำเวรประจำสัปดาห์</label>
                  <select value={dutyDay} onChange={e => setDutyDay(e.target.value)} className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-indigo-500 outline-none">
                    <option value="">-- เลือกวันทำเวร --</option>
                    <option value="จันทร์">วันจันทร์</option>
                    <option value="อังคาร">วันอังคาร</option>
                    <option value="พุธ">วันพุธ</option>
                    <option value="พฤหัสบดี">วันพฤหัสบดี</option>
                    <option value="ศุกร์">วันศุกร์</option>
                  </select>
                </div>
              </div>'''
    
    if old_inputs in content:
        content = content.replace(old_inputs, new_inputs)
    else:
        # Regex replace
        content = re.sub(r'<div className="grid grid-cols-2 gap-4">[\s\S]*?</div>\s*</div>', new_inputs, content)
    
    # Change status button text from ฝึกงาน/ไม่ฝึก to ทำเวร/ไม่ทำ
    content = content.replace("{s.isInterning !== false ? 'ฝึกงาน' : 'ไม่ฝึก'}", "{s.isInterning !== false ? 'ทำเวร' : 'ไม่ทำ'}")
    
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(content)

modify_admin_students('d:/งานมด/duty-app/src/app/admin/students/page.tsx')
print('Modified admin students page!')
