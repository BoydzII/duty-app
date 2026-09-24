import codecs

def rewrite_report_page(path):
    new_content = """"use client";

import { useState, useRef, useEffect } from "react";
import { Camera, Save, ArrowLeft, Users, Calendar } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function ReportPage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Student Info
  const [internName, setInternName] = useState("");
  const [studentId, setStudentId] = useState("");
  const [grade, setGrade] = useState("");
  const [studentNumber, setStudentNumber] = useState("");
  const [assignedDutyDay, setAssignedDutyDay] = useState("");

  // Report Info
  const [date, setDate] = useState(new Date().toISOString().split("T")[0]);
  const [dutyDay, setDutyDay] = useState("");
  const [photo, setPhoto] = useState<string | null>(null);
  
  // Friends present
  const [friendsPresent, setFriendsPresent] = useState<string[]>([]);

  // Database
  const [studentsDb, setStudentsDb] = useState<any[]>([]);
  const [isLoadingDb, setIsLoadingDb] = useState(true);

  useEffect(() => {
    fetch("/api/students")
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setStudentsDb(data.students);
        }
      })
      .catch(err => console.error("Error fetching students:", err))
      .finally(() => setIsLoadingDb(false));
  }, []);

  const handleStudentIdChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setStudentId(val);
    
    // Auto lookup when length is 5
    if (val.length === 5) {
      const found = studentsDb.find(s => String(s.studentId) === val);
      if (found) {
        setInternName(found.name);
        setGrade(found.grade);
        setStudentNumber(found.studentNumber);
        setAssignedDutyDay(found.dutyDay || "");
        if (!dutyDay && found.dutyDay) {
          setDutyDay(found.dutyDay);
        }
      }
    }
  };

  const handleToggleFriend = (friendId: string) => {
    setFriendsPresent(prev => 
      prev.includes(friendId) ? prev.filter(id => id !== friendId) : [...prev, friendId]
    );
  };

  const handleToggleSelectAllFriends = (classmates: any[]) => {
    // Select all classmates EXCEPT the reporter themselves
    const classmateIds = classmates.filter(s => String(s.studentId) !== String(studentId)).map(s => String(s.studentId));
    if (friendsPresent.length === classmateIds.length) {
      setFriendsPresent([]); // Deselect all
    } else {
      setFriendsPresent(classmateIds); // Select all
    }
  };

  const handlePhotoCapture = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
         alert("ไฟล์รูปภาพใหญ่เกินไป กรุณาเลือกไฟล์ที่มีขนาดไม่เกิน 5MB");
         return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhoto(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!internName || !studentId || !date || !dutyDay) {
      alert("กรุณากรอกข้อมูลให้ครบถ้วน");
      return;
    }
    if (!photo) {
      alert("กรุณาถ่ายรูปการทำเวร");
      return;
    }

    const newReport = {
      id: Date.now().toString(),
      date,
      dutyDay,
      reporter: {
        firstName: internName,
        studentId,
        grade,
        studentNumber,
      },
      friendsPresent, // array of studentIds
      image: photo,
      status: "pending" // Will be processed in /sync
    };

    const existingReports = JSON.parse(localStorage.getItem("dutyReports") || "[]");
    
    // Check local duplicate
    const isDuplicate = existingReports.some((r: any) => 
      r.reporter.studentId === studentId && r.date === date
    );

    if (isDuplicate) {
      alert("คุณได้บันทึกการทำเวรของวันนี้ไว้ในเครื่องแล้ว");
      return;
    }

    existingReports.push(newReport);
    localStorage.setItem("dutyReports", JSON.stringify(existingReports));
    
    alert("บันทึกข้อมูลลงเครื่องสำเร็จ! อย่าลืมไปที่เมนู 'รายการรอส่ง' เพื่อส่งข้อมูลขึ้นระบบ");
    router.push("/");
  };

  // Get classmates (same grade)
  const classmates = studentsDb
    .filter(s => s.grade === grade && String(s.studentId) !== String(studentId))
    .sort((a, b) => (parseInt(a.studentNumber) || 0) - (parseInt(b.studentNumber) || 0));

  return (
    <div className="max-w-xl mx-auto p-4 md:p-6 pb-24">
      <div className="flex items-center gap-3 mb-6">
        <Link href="/" className="bg-gray-100 hover:bg-gray-200 p-2 rounded-full transition-colors text-gray-700">
          <ArrowLeft size={20} />
        </Link>
        <h1 className="text-xl font-bold text-gray-800">บันทึกการทำเวร</h1>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* ข้อมูลผู้บันทึก Section */}
        <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 space-y-4">
          <h3 className="font-bold text-gray-800 flex items-center gap-2 pb-2 border-b">
            <span className="bg-indigo-100 text-indigo-600 p-1.5 rounded-lg"><Users size={18} /></span>
            ข้อมูลผู้รายงาน (หัวหน้าเวร/ตัวแทน)
          </h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">เลขประจำตัวนักเรียน</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={studentId}
                  onChange={handleStudentIdChange}
                  className="flex-1 w-full bg-gray-50 text-gray-900 border border-gray-200 rounded-xl p-3 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
                  placeholder="เช่น 12345"
                  required
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">ชื่อ-นามสกุล</label>
              <input
                type="text"
                value={internName}
                onChange={(e) => setInternName(e.target.value)}
                className="w-full bg-gray-50 text-gray-900 border border-gray-200 rounded-xl p-3 focus:bg-white focus:ring-2 focus:ring-indigo-500 outline-none"
                placeholder="ชื่อ-นามสกุล"
                required
              />
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">ระดับชั้น</label>
              <input
                type="text"
                value={grade}
                onChange={(e) => setGrade(e.target.value)}
                className="w-full bg-gray-50 text-gray-900 border border-gray-200 rounded-xl p-3 focus:bg-white focus:ring-2 focus:ring-indigo-500 outline-none"
                placeholder="ม.5/1"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">เลขที่</label>
              <input
                type="text"
                value={studentNumber}
                onChange={(e) => setStudentNumber(e.target.value)}
                className="w-full bg-gray-50 text-gray-900 border border-gray-200 rounded-xl p-3 focus:bg-white focus:ring-2 focus:ring-indigo-500 outline-none"
                placeholder="12"
                required
              />
            </div>
          </div>
        </div>

        {/* ข้อมูลการทำเวร Section */}
        <div className="bg-indigo-50/50 p-5 rounded-2xl border border-indigo-100 space-y-5">
          <h3 className="font-bold text-indigo-900 flex items-center gap-2 pb-2 border-b border-indigo-100">
            <span className="bg-indigo-100 text-indigo-600 p-1.5 rounded-lg"><Calendar size={18} /></span>
            ข้อมูลการทำเวร
          </h3>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-indigo-900 mb-1">วันทำเวรประจำสัปดาห์</label>
              <select
                value={dutyDay}
                onChange={(e) => setDutyDay(e.target.value)}
                className="w-full bg-white text-gray-900 border border-indigo-200 rounded-xl p-3 focus:ring-2 focus:ring-indigo-500 outline-none font-medium text-indigo-800"
                required
              >
                <option value="">-- เลือกวัน --</option>
                <option value="จันทร์">วันจันทร์</option>
                <option value="อังคาร">วันอังคาร</option>
                <option value="พุธ">วันพุธ</option>
                <option value="พฤหัสบดี">วันพฤหัสบดี</option>
                <option value="ศุกร์">วันศุกร์</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-indigo-900 mb-1">วันที่รายงาน</label>
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="w-full bg-white text-gray-900 border border-indigo-200 rounded-xl p-3 focus:ring-2 focus:ring-indigo-500 outline-none"
                required
              />
            </div>
          </div>

          {/* เลือกเพื่อน Section */}
          {grade && (
            <div className="pt-2">
              <div className="flex justify-between items-end mb-2">
                <label className="block text-sm font-bold text-indigo-900">เช็คชื่อเพื่อนร่วมเวร (ที่มาทำเวรด้วยกัน)</label>
                <button
                  type="button"
                  onClick={() => handleToggleSelectAllFriends(classmates)}
                  className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 px-2 py-1 bg-white rounded border border-indigo-200 shadow-sm"
                >
                  {friendsPresent.length === classmates.length ? "ยกเลิกทั้งหมด" : "เลือกทุกคนในห้อง"}
                </button>
              </div>
              
              {classmates.length > 0 ? (
                <div className="bg-white p-3 rounded-xl border border-indigo-100 shadow-sm">
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 max-h-60 overflow-y-auto pr-1">
                    {classmates.map(s => (
                      <label 
                        key={s.id} 
                        className={`flex items-start gap-2 p-2 rounded-lg border cursor-pointer transition-colors ${
                          friendsPresent.includes(String(s.studentId)) 
                            ? "bg-indigo-50 border-indigo-300 shadow-sm" 
                            : "bg-gray-50 border-gray-200 hover:bg-gray-100"
                        }`}
                      >
                        <input 
                          type="checkbox" 
                          checked={friendsPresent.includes(String(s.studentId))}
                          onChange={() => handleToggleFriend(String(s.studentId))}
                          className="mt-0.5 w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                        />
                        <div className="flex flex-col">
                          <span className="text-xs font-bold text-gray-800 line-clamp-1">{s.name}</span>
                          <span className="text-[10px] text-gray-500">เลขที่ {s.studentNumber}</span>
                        </div>
                      </label>
                    ))}
                  </div>
                  <div className="mt-3 text-sm text-indigo-700 bg-indigo-50 p-2 rounded-lg font-medium text-center">
                    เลือกเพื่อนแล้ว {friendsPresent.length} คน
                  </div>
                </div>
              ) : (
                <p className="text-sm text-gray-500 italic bg-white p-3 rounded-lg border border-dashed border-gray-300">
                  กำลังโหลดรายชื่อเพื่อน หรือไม่พบเพื่อนในห้องนี้
                </p>
              )}
            </div>
          )}
        </div>

        {/* รูปถ่าย Section */}
        <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100">
          <label className="block text-sm font-bold text-gray-800 mb-3">รูปถ่ายยืนยันการทำเวร (1 รูป)</label>
          
          {photo ? (
            <div className="relative group">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={photo} alt="Captured" className="w-full h-64 object-cover rounded-xl border-2 border-gray-200 shadow-sm" />
              <button
                type="button"
                onClick={() => setPhoto(null)}
                className="absolute top-3 right-3 bg-red-500 hover:bg-red-600 text-white rounded-full py-1.5 px-4 text-sm font-medium shadow-md transition-all"
              >
                ลบ / ถ่ายใหม่
              </button>
            </div>
          ) : (
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="w-full border-2 border-dashed border-indigo-300 rounded-xl p-12 flex flex-col items-center justify-center text-indigo-600 hover:border-indigo-500 hover:bg-indigo-50 transition-all bg-gray-50/50"
            >
              <div className="bg-indigo-100 p-4 rounded-full mb-3 shadow-sm">
                <Camera size={36} />
              </div>
              <span className="font-bold text-lg">แตะเพื่อถ่ายรูป / เลือกรูป</span>
              <span className="text-sm text-gray-500 mt-2">ถ่ายรูปหน้างานหลังทำความสะอาดเสร็จ</span>
            </button>
          )}
          <input
            type="file"
            accept="image/*"
            capture="environment"
            ref={fileInputRef}
            onChange={handlePhotoCapture}
            className="hidden"
          />
        </div>

        <button
          type="submit"
          className="w-full flex justify-center items-center gap-2 bg-indigo-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-indigo-700 active:bg-indigo-800 shadow-lg shadow-indigo-200 transition-all mt-8"
        >
          <Save size={22} />
          บันทึกลงเครื่อง (รอส่ง)
        </button>
      </form>
    </div>
  );
}
"""
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(new_content)

rewrite_report_page('d:/งานมด/duty-app/src/app/report/page.tsx')
print("Report page rewritten!")
