"use client";

import { useEffect, useState } from "react";
import { DraftReport, getDraftReports, clearDraftReport } from "@/lib/storage";
import { CloudUpload, Trash2, CheckCircle } from "lucide-react";
import Link from "next/link";

export default function SyncPage() {
  const [drafts, setDrafts] = useState<DraftReport[]>([]);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncStatus, setSyncStatus] = useState<string | null>(null);

  useEffect(() => {
    loadDrafts();
  }, []);

  const loadDrafts = async () => {
    const data = await getDraftReports();
    setDrafts(data);
  };

  const handleDelete = async (id: string) => {
    if (confirm("คุณต้องการลบรายงานนี้ใช่หรือไม่?")) {
      await clearDraftReport(id);
      loadDrafts();
    }
  };

  const handleSync = async () => {
    if (drafts.length === 0) return;
    setIsSyncing(true);
    setSyncStatus("กำลังส่งข้อมูล...");

    let successCount = 0;
    
    for (const draft of drafts) {
      try {
        const response = await fetch('/api/reports', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(draft),
        });

        if (response.ok) {
          const result = await response.json();
          if (result.success) {
            await clearDraftReport(draft.id);
            successCount++;
          } else {
            console.error("GAS Error:", result.error);
            alert(`เกิดข้อผิดพลาดจากเซิร์ฟเวอร์: ${result.error}`);
          }
        } else {
          const result = await response.json();
          alert(`เกิดข้อผิดพลาดในการเชื่อมต่อ: ${result.error || response.statusText}`);
        }
      } catch (error) {
        console.error("Error syncing draft", draft.id, error);
        alert(`เกิดข้อผิดพลาดของระบบ: ${error}`);
      }
    }

    setIsSyncing(false);
    
    if (successCount === drafts.length) {
      setSyncStatus(`ส่งสำเร็จทั้งหมด ${successCount} รายการ!`);
    } else {
      setSyncStatus(`ส่งสำเร็จ ${successCount} รายการ, ล้มเหลว ${drafts.length - successCount} รายการ`);
    }
    
    loadDrafts();
  };

  return (
    <div className="max-w-xl mx-auto mt-4">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">รายการรอส่ง (Offline Drafts)</h2>
        <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm font-medium">
          {drafts.length} รายการ
        </span>
      </div>

      {syncStatus && (
        <div className={`p-4 mb-6 rounded-md ${syncStatus.includes('สำเร็จทั้งหมด') ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>
          {syncStatus}
        </div>
      )}

      {drafts.length === 0 ? (
        <div className="text-center p-12 bg-white rounded-lg border border-dashed">
          <CheckCircle className="mx-auto text-green-500 mb-2" size={48} />
          <p className="text-gray-600 text-lg">ไม่มีรายการค้างส่ง</p>
          <Link href="/report" className="text-blue-600 hover:underline mt-2 inline-block">
            + ไปถ่ายรูปรายงาน
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          <button
            onClick={handleSync}
            disabled={isSyncing}
            className="w-full bg-green-600 text-white py-3 rounded-md font-medium text-lg hover:bg-green-700 transition-colors flex items-center justify-center gap-2 disabled:bg-gray-400"
          >
            <CloudUpload size={24} />
            {isSyncing ? "กำลังส่งข้อมูล..." : "ส่งข้อมูลทั้งหมดเข้า Server"}
          </button>

          <div className="space-y-3">
            {drafts.map((draft) => (
              <div key={draft.id} className="bg-white p-4 rounded-lg border shadow-sm flex items-start gap-4">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={draft.photoBase64} alt="" className="w-20 h-20 object-cover rounded-md border" />
                <div className="flex-1">
                  <h3 className="font-bold text-gray-800">{draft.internName}</h3>
                  <div className="flex gap-2 text-sm text-gray-600">
                    <span>ชั้น: {draft.grade}</span>
                    <span>เลขที่: {draft.studentNumber}</span>
                  </div>
                  <p className="text-sm text-gray-600">สถานที่: {draft.department}</p>
                  <p className="text-sm text-gray-500">วันที่: {draft.date}</p>
                </div>
                <button 
                  onClick={() => handleDelete(draft.id)}
                  className="text-red-500 p-2 hover:bg-red-50 rounded-md"
                  disabled={isSyncing}
                >
                  <Trash2 size={20} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
