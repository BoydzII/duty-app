import codecs

def rewrite_admin_dashboard(path):
    new_content = """"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Users, FileText, CheckCircle, XCircle, RefreshCw, LogOut, Download, AlertCircle, Camera } from "lucide-react";
import { useRouter } from "next/navigation";
import * as XLSX from "xlsx";

interface Student {
  id: string;
  name: string;
  studentId: string;
  grade: string;
  studentNumber: string;
  isInterning?: boolean;
  dutyDay?: string;
}

export default function AdminDashboard() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [pin, setPin] = useState("");
  const [pinError, setPinError] = useState(false);
  
  const [reports, setReports] = useState<any[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  
  const [loading, setLoading] = useState(true);
  
  // Get today's date formatted as YYYY-MM-DD in local time
  const getTodayLocalString = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const [filterDate, setFilterDate] = useState(getTodayLocalString());

  useEffect(() => {
    const authStatus = localStorage.getItem("adminAuth");
    if (authStatus === "true") {
      setIsAuthenticated(true);
      fetchData();
    }
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/admin/pin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pin }),
      });
      const data = await res.json();
      
      if (data.success) {
        setIsAuthenticated(true);
        localStorage.setItem("adminAuth", "true");
        fetchData();
      } else {
        setPinError(true);
      }
    } catch (error) {
      setPinError(true);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("adminAuth");
    setIsAuthenticated(false);
    setPin("");
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      const [reportsRes, studentsRes] = await Promise.all([
        fetch("/api/reports"),
        fetch("/api/students")
      ]);
      const reportsData = await reportsRes.json();
      const studentsData = await studentsRes.json();

      if (reportsData.success) setReports(reportsData.reports || []);
      if (studentsData.success) setStudents(studentsData.students || []);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
    setLoading(false);
  };

  const getDayNameFromDate = (dateStr: string) => {
    const d = new Date(dateStr);
    const dayNames = ['อาทิตย์', 'จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์'];
    return dayNames[d.getDay()];
  };

  const filterDayName = getDayNameFromDate(filterDate);

  // หาว่าวันไหนมีใครบ้างที่ต้องทำเวร
  const dutyStudents = students.filter(s => s.dutyDay === filterDayName && s.isInterning !== false);
  
  // รายงานของวันนี้
  const filteredReports = reports.filter(r => {
    if (!r.date) return false;
    const rDateObj = new Date(r.date);
    const rYear = rDateObj.getFullYear();
    const rMonth = String(rDateObj.getMonth() + 1).padStart(2, '0');
    const rDay = String(rDateObj.getDate()).padStart(2, '0');
    const rDateStr = `${rYear}-${rMonth}-${rDay}`;
    return rDateStr === filterDate;
  });

  // เช็คว่าใครทำเวรแล้วบ้าง (ตัวแทนส่ง + เพื่อนที่อยู่ใน friendsPresent)
  const presentStudentIds = new Set<string>();
  filteredReports.forEach(r => {
    if (r.reporter?.studentId) presentStudentIds.add(String(r.reporter.studentId));
    if (r.friendsPresent && Array.isArray(r.friendsPresent)) {
      r.friendsPresent.forEach((id: string) => presentStudentIds.add(String(id)));
    }
  });

  // เด็กที่ไม่ได้ทำเวร = dutyStudents ที่ไม่อยู่ใน presentStudentIds
  const missingStudents = dutyStudents.filter(s => !presentStudentIds.has(String(s.studentId)));

  const handleExportExcel = () => {
    const wb = XLSX.utils.book_new();
    
    // Sheet 1: รายงานการทำเวร
    const reportData = filteredReports.map(r => {
      // Find friends names
      const friendsNames = (r.friendsPresent || []).map((id: string) => {
        const found = students.find(s => String(s.studentId) === String(id));
        return found ? found.name : id;
      }).join(", ");

      return {
        "วันที่": new Date(r.date).toLocaleDateString('th-TH'),
        "รหัสนักเรียน (ผู้รายงาน)": r.reporter?.studentId,
        "ชื่อ-นามสกุล (ผู้รายงาน)": r.reporter?.firstName,
        "ชั้น": r.reporter?.grade,
        "เลขที่": r.reporter?.studentNumber,
        "วันทำเวร": r.dutyDay,
        "เพื่อนที่ร่วมเวร": friendsNames,
        "เวลาที่ส่ง": new Date(r.createdAt || r.date).toLocaleString('th-TH')
      };
    });
    const ws1 = XLSX.utils.json_to_sheet(reportData);
    XLSX.utils.book_append_sheet(wb, ws1, "รายงานการทำเวร");

    // Sheet 2: รายชื่อผู้ขาดเวร
    const missingData = missingStudents.map(s => ({
      "รหัสนักเรียน": s.studentId,
      "ชื่อ-นามสกุล": s.name,
      "ชั้น": s.grade,
      "เลขที่": s.studentNumber,
      "วันทำเวร": s.dutyDay,
      "สถานะ": "ขาดเวร"
    }));
    const ws2 = XLSX.utils.json_to_sheet(missingData);
    XLSX.utils.book_append_sheet(wb, ws2, "รายชื่อผู้ขาดเวร");

    XLSX.writeFile(wb, `สรุปเวร_${filterDate}.xlsx`);
  };

  const handleDeleteReport = async (id: string) => {
    if (confirm('คุณต้องการลบรายงานนี้ใช่หรือไม่?')) {
      try {
        const res = await fetch(`/api/reports?id=${id}`, { method: 'DELETE' });
        if (res.ok) {
          fetchData();
        }
      } catch (error) {
        console.error("Failed to delete report:", error);
      }
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <form onSubmit={handleLogin} className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-sm">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-gray-800">ระบบจัดการเวร</h1>
            <p className="text-gray-500 mt-2">กรุณาใส่รหัสผ่านเพื่อเข้าสู่ระบบ</p>
          </div>
          <div>
            <input
              type="password"
              value={pin}
              onChange={(e) => {
                setPin(e.target.value);
                setPinError(false);
              }}
              className={`w-full border-2 rounded-xl p-4 text-center text-2xl tracking-[0.5em] focus:outline-none transition-all ${
                pinError ? 'border-red-500 bg-red-50 text-red-700' : 'border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100'
              }`}
              placeholder="••••"
              maxLength={6}
            />
            {pinError && <p className="text-red-500 text-sm text-center mt-3 font-medium">รหัสผ่านไม่ถูกต้อง</p>}
          </div>
          <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 rounded-xl mt-6 transition-all shadow-md active:scale-[0.98]">
            เข้าสู่ระบบ
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-12">
      <nav className="bg-white border-b sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center gap-4">
              <h1 className="text-xl font-bold text-gray-800">ระบบจัดการเวรทำความสะอาด</h1>
            </div>
            <div className="flex items-center gap-2">
              <Link href="/admin/students" className="text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2">
                <Users size={18} />
                <span className="hidden sm:inline">จัดการนักเรียน</span>
              </Link>
              <button onClick={handleLogout} className="text-red-500 hover:bg-red-50 p-2 rounded-lg transition-colors" title="ออกจากระบบ">
                <LogOut size={20} />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        
        {/* แถบเครื่องมือ & ค้นหา */}
        <div className="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="flex items-center gap-3 w-full md:w-auto">
            <label className="font-semibold text-gray-700 whitespace-nowrap">ประจำวันที่:</label>
            <input 
              type="date" 
              value={filterDate} 
              onChange={e => setFilterDate(e.target.value)}
              className="border-2 border-gray-200 rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none flex-1 md:flex-none text-gray-700 font-medium"
            />
            <span className="bg-indigo-50 text-indigo-700 px-3 py-1.5 rounded-lg text-sm font-semibold border border-indigo-100 hidden sm:block">
              วัน{filterDayName}
            </span>
          </div>
          <div className="flex items-center gap-2 w-full md:w-auto">
            <button 
              onClick={handleExportExcel}
              className="flex-1 md:flex-none flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium transition-colors shadow-sm"
            >
              <Download size={18} />
              <span>Export Excel</span>
            </button>
            <button 
              onClick={fetchData} 
              className="flex items-center justify-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-medium transition-colors border border-gray-200"
            >
              <RefreshCw size={18} className={loading ? "animate-spin" : ""} />
            </button>
          </div>
        </div>

        {/* สรุปสถิติ */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex items-center gap-4">
            <div className="bg-blue-100 p-3 rounded-full text-blue-600">
              <Users size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">นักเรียนที่มีเวรวันนี้</p>
              <p className="text-2xl font-bold text-gray-800">{dutyStudents.length} <span className="text-base font-normal text-gray-500">คน</span></p>
            </div>
          </div>
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex items-center gap-4">
            <div className="bg-green-100 p-3 rounded-full text-green-600">
              <CheckCircle size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">ทำเวรแล้ว (รวมเพื่อน)</p>
              <p className="text-2xl font-bold text-green-600">{presentStudentIds.size} <span className="text-base font-normal text-gray-500">คน</span></p>
            </div>
          </div>
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex items-center gap-4">
            <div className="bg-red-100 p-3 rounded-full text-red-600">
              <XCircle size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">ขาดเวร</p>
              <p className="text-2xl font-bold text-red-600">{missingStudents.length} <span className="text-base font-normal text-gray-500">คน</span></p>
            </div>
          </div>
        </div>

        {/* ผู้ยังไม่ส่งงาน */}
        {missingStudents.length > 0 && (
          <div className="bg-red-50 border border-red-200 rounded-2xl p-5">
            <h2 className="text-lg font-bold text-red-800 flex items-center gap-2 mb-4">
              <AlertCircle size={20} />
              รายชื่อนักเรียนที่ขาดเวรวันนี้ ({missingStudents.length} คน)
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
              {missingStudents.map(student => (
                <div key={student.id} className="bg-white p-3 rounded-xl border border-red-100 shadow-sm flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-red-100 text-red-600 flex items-center justify-center font-bold text-sm shrink-0">
                    {student.studentNumber || '-'}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800 text-sm line-clamp-1">{student.name}</p>
                    <p className="text-xs text-gray-500">{student.grade} | รหัส: {student.studentId}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* รายงานที่ส่งแล้ว */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-5 border-b border-gray-100 flex justify-between items-center bg-gray-50">
            <h2 className="text-lg font-bold text-gray-800 flex items-center gap-2">
              <FileText size={20} className="text-indigo-600" />
              รายงานการทำเวรวันนี้ ({filteredReports.length} รายการ)
            </h2>
          </div>
          
          {loading ? (
            <div className="p-8 text-center text-gray-500">กำลังโหลดข้อมูล...</div>
          ) : filteredReports.length === 0 ? (
            <div className="p-12 text-center flex flex-col items-center">
              <div className="bg-gray-100 p-4 rounded-full text-gray-400 mb-3">
                <FileText size={32} />
              </div>
              <p className="text-gray-500 font-medium">ยังไม่มีรายงานในวันนี้</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
              {filteredReports.map((report) => (
                <div key={report.id} className="border rounded-2xl overflow-hidden hover:shadow-md transition-shadow bg-white flex flex-col">
                  {report.imageUrl ? (
                    <div className="relative h-48 bg-gray-100 border-b">
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img src={report.imageUrl} alt="Duty Photo" className="w-full h-full object-cover" />
                    </div>
                  ) : (
                    <div className="h-48 bg-gray-100 border-b flex items-center justify-center text-gray-400 flex-col gap-2">
                      <Camera size={32} />
                      <span className="text-sm">ไม่มีรูปภาพ</span>
                    </div>
                  )}
                  
                  <div className="p-4 flex-1 flex flex-col">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="font-bold text-gray-800 text-lg">{report.reporter?.firstName}</h3>
                        <p className="text-xs text-indigo-600 font-medium bg-indigo-50 inline-block px-2 py-0.5 rounded border border-indigo-100 mt-1">
                          {report.reporter?.grade} | เลขที่ {report.reporter?.studentNumber}
                        </p>
                      </div>
                      <span className="text-xs text-gray-500">
                        {new Date(report.createdAt || report.date).toLocaleTimeString('th-TH', {hour: '2-digit', minute:'2-digit'})}
                      </span>
                    </div>
                    
                    {report.friendsPresent && report.friendsPresent.length > 0 && (
                      <div className="mt-2 pt-3 border-t border-gray-100">
                        <p className="text-xs font-semibold text-gray-500 mb-1">เพื่อนที่มาทำเวรด้วย ({report.friendsPresent.length} คน):</p>
                        <div className="flex flex-wrap gap-1">
                          {report.friendsPresent.map((friendId: string) => {
                            const friend = students.find(s => String(s.studentId) === String(friendId));
                            return (
                              <span key={friendId} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                                {friend ? friend.name.split(' ')[0] : friendId}
                              </span>
                            );
                          })}
                        </div>
                      </div>
                    )}
                    
                    <div className="mt-auto pt-4 flex justify-end">
                      <button 
                        onClick={() => handleDeleteReport(report.id)}
                        className="text-xs text-red-500 hover:text-red-700 font-medium px-2 py-1 hover:bg-red-50 rounded transition-colors"
                      >
                        ลบรายงาน
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
"""
    with codecs.open(path, 'w', 'utf-8') as f:
        f.write(new_content)

rewrite_admin_dashboard('d:/งานมด/duty-app/src/app/admin/page.tsx')
print("Admin dashboard rewritten!")
