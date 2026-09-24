"use client";

import { useEffect, useState } from "react";
import { Lock, LogOut, KeyRound, X, CheckCircle2 } from "lucide-react";

const DEFAULT_PIN = "1234";

export default function AdminGuard({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [pin, setPin] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  // State สำหรับ Modal เปลี่ยนรหัสผ่าน
  const [showChangeModal, setShowChangeModal] = useState(false);
  const [currentPin, setCurrentPin] = useState("");
  const [newPin, setNewPin] = useState("");
  const [confirmPin, setConfirmPin] = useState("");
  const [changeError, setChangeError] = useState("");
  const [changeSuccess, setChangeSuccess] = useState("");
  const [isSubmittingChange, setIsSubmittingChange] = useState(false);

  useEffect(() => {
    const auth = sessionStorage.getItem("admin_auth");
    if (auth === "true") {
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const envPin = process.env.NEXT_PUBLIC_ADMIN_PIN;
    const localPin = typeof window !== "undefined" ? localStorage.getItem("admin_pin_override") : null;

    // ตรวจสอบความถูกต้องโดยตรง (รับทั้งรหัสที่ตั้งใน Vercel, รหัสที่เปลี่ยนในเครื่อง, หรือ 1234)
    if (
      (localPin && pin === localPin) ||
      (envPin && pin === envPin) ||
      pin === DEFAULT_PIN
    ) {
      sessionStorage.setItem("admin_auth", "true");
      setIsAuthenticated(true);
      setError("");
      return;
    }

    // ตรวจสอบผ่าน Server API เพิ่มเติม (กรณีตั้งค่า ADMIN_PIN เป็นแบบ Server-side ใน Vercel)
    try {
      const res = await fetch("/api/admin/pin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "verify", pin }),
      });
      const data = await res.json();

      if (data.success) {
        sessionStorage.setItem("admin_auth", "true");
        setIsAuthenticated(true);
        setError("");
        return;
      }
    } catch {
      // Ignored
    }

    setError("รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง");
    setPin("");
  };

  const handleLogout = () => {
    sessionStorage.removeItem("admin_auth");
    setIsAuthenticated(false);
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setChangeError("");
    setChangeSuccess("");

    const envPin = process.env.NEXT_PUBLIC_ADMIN_PIN;
    const localPin = typeof window !== "undefined" ? localStorage.getItem("admin_pin_override") : null;
    const validCurrentPin = localPin || envPin || DEFAULT_PIN;

    if (currentPin !== validCurrentPin && currentPin !== DEFAULT_PIN && currentPin !== envPin) {
      setChangeError("รหัสผ่านเดิมไม่ถูกต้อง");
      return;
    }

    if (newPin !== confirmPin) {
      setChangeError("รหัสผ่านใหม่กับยืนยันรหัสผ่านไม่ตรงกัน");
      return;
    }

    if (newPin.length < 4) {
      setChangeError("รหัสผ่านใหม่ต้องมีความยาวอย่างน้อย 4 ตัวอักษร");
      return;
    }

    setIsSubmittingChange(true);

    try {
      localStorage.setItem("admin_pin_override", newPin);
      
      // ส่งแจ้ง API ด้วย
      fetch("/api/admin/pin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "change", currentPin, newPin }),
      }).catch(() => {});

      setChangeSuccess("เปลี่ยนรหัสผ่านสำเร็จเรียบร้อยแล้ว!");
      setCurrentPin("");
      setNewPin("");
      setConfirmPin("");
      setTimeout(() => {
        setShowChangeModal(false);
        setChangeSuccess("");
      }, 1500);
    } catch {
      setChangeError("เกิดข้อผิดพลาดในการบันทึกรหัสผ่าน");
    } finally {
      setIsSubmittingChange(false);
    }
  };

  if (isLoading) {
    return <div className="text-center py-20 text-gray-400">กำลังตรวจสอบสิทธิ์...</div>;
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white p-8 rounded-2xl shadow-lg border border-gray-100 text-center">
          <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 border border-blue-100">
            <Lock size={32} />
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">เข้าสู่ระบบอาจารย์ / แอดมิน</h2>
          <p className="text-gray-500 text-sm mb-6">พื้นที่นี้สำหรับอาจารย์ผู้ดูแลเท่านั้น กรุณากรอกรหัสผ่าน</p>
          
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <input
                type="password"
                value={pin}
                onChange={(e) => setPin(e.target.value)}
                placeholder="กรอกรหัสผ่าน (PIN)"
                className="w-full text-center text-xl tracking-widest bg-white text-gray-900 border border-gray-300 rounded-xl p-3 focus:ring-2 focus:ring-blue-500 outline-none transition"
                autoFocus
                required
              />
            </div>
            {error && <p className="text-red-600 text-sm font-medium">{error}</p>}
            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-xl transition shadow-md active:scale-95"
            >
              เข้าสู่ระบบ
            </button>
          </form>
          <p className="text-xs text-gray-400 mt-4">รหัสเริ่มต้น: <span className="font-mono font-bold text-gray-600">1234</span> (หรือรหัสที่ตั้งไว้ในระบบ)</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Top Admin Bar */}
      <div className="print:hidden flex justify-end items-center gap-2 mb-3">
        <button
          onClick={() => {
            setShowChangeModal(true);
            setChangeError("");
            setChangeSuccess("");
          }}
          className="text-xs text-blue-700 hover:text-blue-900 flex items-center gap-1.5 bg-blue-50 border border-blue-200 px-3 py-1.5 rounded-lg shadow-sm transition hover:bg-blue-100 font-medium"
        >
          <KeyRound size={14} />
          <span>เปลี่ยนรหัสผ่านแอดมิน</span>
        </button>

        <button
          onClick={handleLogout}
          className="text-xs text-gray-600 hover:text-red-600 flex items-center gap-1.5 bg-white border border-gray-200 px-3 py-1.5 rounded-lg shadow-sm transition hover:bg-red-50 font-medium"
        >
          <LogOut size={14} />
          <span>ออกจากระบบ</span>
        </button>
      </div>

      {/* Modal เปลี่ยนรหัสผ่าน */}
      {showChangeModal && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl shadow-xl border border-gray-100 max-w-md w-full p-6 relative animate-in fade-in zoom-in-95 duration-150">
            <button
              onClick={() => setShowChangeModal(false)}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 p-1 rounded-full hover:bg-gray-100 transition"
            >
              <X size={20} />
            </button>

            <div className="flex items-center gap-3 mb-5 border-b pb-3">
              <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">
                <KeyRound size={20} />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-800">เปลี่ยนรหัสผ่านแอดมิน</h3>
                <p className="text-xs text-gray-500">กำหนดรหัสผ่านใหม่เพื่อความปลอดภัย</p>
              </div>
            </div>

            {changeSuccess ? (
              <div className="bg-green-50 border border-green-200 text-green-700 p-4 rounded-xl flex items-center gap-3 text-sm my-4">
                <CheckCircle2 size={20} className="text-green-600 shrink-0" />
                <span>{changeSuccess}</span>
              </div>
            ) : (
              <form onSubmit={handleChangePassword} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">รหัสผ่านเดิม</label>
                  <input
                    type="password"
                    value={currentPin}
                    onChange={(e) => setCurrentPin(e.target.value)}
                    placeholder="รหัสผ่านปัจจุบัน (เช่น 1234)"
                    className="w-full bg-white text-gray-900 border border-gray-300 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">รหัสผ่านใหม่ (อย่างน้อย 4 ตัวอักษร)</label>
                  <input
                    type="password"
                    value={newPin}
                    onChange={(e) => setNewPin(e.target.value)}
                    placeholder="กรอกรหัสผ่านใหม่"
                    className="w-full bg-white text-gray-900 border border-gray-300 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">ยืนยันรหัสผ่านใหม่</label>
                  <input
                    type="password"
                    value={confirmPin}
                    onChange={(e) => setConfirmPin(e.target.value)}
                    placeholder="กรอกรหัสผ่านใหม่อีกครั้ง"
                    className="w-full bg-white text-gray-900 border border-gray-300 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                    required
                  />
                </div>

                {changeError && (
                  <p className="text-red-600 text-xs font-medium bg-red-50 p-2.5 rounded-lg border border-red-100">
                    {changeError}
                  </p>
                )}

                <div className="flex gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowChangeModal(false)}
                    className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2.5 rounded-xl transition text-sm"
                  >
                    ยกเลิก
                  </button>
                  <button
                    type="submit"
                    disabled={isSubmittingChange}
                    className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-medium py-2.5 rounded-xl transition text-sm shadow-sm"
                  >
                    {isSubmittingChange ? "กำลังบันทึก..." : "บันทึกรหัสใหม่"}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}

      {children}
    </div>
  );
}
