import Link from 'next/link';
import { Camera, CloudUpload, LayoutDashboard } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white p-4 shadow-md sticky top-0 z-50">
      <div className="max-w-4xl mx-auto flex justify-between items-center">
        <Link href="/" className="font-bold text-lg">
          Shared responsibility
        </Link>
        <div className="flex gap-4">
          <Link href="/report" className="flex items-center gap-1 hover:text-blue-200">
            <Camera size={20} />
            <span className="hidden sm:inline">เช็คชื่อเวร</span>
          </Link>
          <Link href="/sync" className="flex items-center gap-1 hover:text-blue-200">
            <CloudUpload size={20} />
            <span className="hidden sm:inline">รอส่ง</span>
          </Link>
          <Link href="/admin" className="flex items-center gap-1 hover:text-blue-200">
            <LayoutDashboard size={20} />
            <span className="hidden sm:inline">แอดมิน</span>
          </Link>
        </div>
      </div>
    </nav>
  );
}
