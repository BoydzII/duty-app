import Link from 'next/link';
import { Camera, CloudUpload, FileText } from 'lucide-react';
import Image from 'next/image';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center py-6 space-y-6">
      
      <div className="flex flex-col items-center gap-4 w-full max-w-md px-4">
        <div className="flex items-center justify-center gap-6">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/school-logo.jpg" alt="โรงเรียนปากช่อง" className="h-24 md:h-28 object-contain mix-blend-multiply" />
          
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/smte-pakchong-logo.png" alt="SMTE Pakchong School" className="h-20 md:h-24 object-contain mix-blend-multiply" />
        </div>
        
        <div className="text-center mt-3">
          <p className="text-lg md:text-xl font-extrabold text-blue-900 tracking-wide">
            โครงการห้องเรียนพิเศษวิทยาศาสตร์ คณิตศาสตร์ เทคโนโลยี และสิ่งแวดล้อม (SMTE)
          </p>
          <p className="text-base md:text-lg font-bold text-blue-800 mt-1">ระดับมัธยมศึกษาตอนปลาย</p>
        </div>
      </div>

      <h1 className="text-2xl font-bold text-center text-blue-800 border-t pt-6 w-full max-w-lg border-gray-200">
        ระบบบันทึกเวรประจำวัน
      </h1>
      <p className="text-gray-600 text-center max-w-md">
        บันทึกการทำเวรแบบออฟไลน์ และส่งข้อมูลเมื่อเชื่อมต่ออินเทอร์เน็ต
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-lg">
        <Link href="/report" className="flex flex-col items-center justify-center p-6 bg-white border-2 border-blue-100 rounded-xl shadow-sm hover:shadow-md hover:border-blue-300 transition-all gap-4">
          <div className="bg-blue-100 p-4 rounded-full text-blue-600">
            <Camera size={40} />
          </div>
          <span className="font-semibold text-lg text-gray-800">เช็คชื่อทำเวร</span>
        </Link>
        
        <Link href="/sync" className="flex flex-col items-center justify-center p-6 bg-white border-2 border-orange-100 rounded-xl shadow-sm hover:shadow-md hover:border-orange-300 transition-all gap-4">
          <div className="bg-orange-100 p-4 rounded-full text-orange-600">
            <CloudUpload size={40} />
          </div>
          <span className="font-semibold text-lg text-gray-800">รายการรอส่ง</span>
        </Link>
      </div>

      <div className="mt-8 border-t pt-8 w-full max-w-lg">
        <Link href="/admin" className="flex items-center justify-between p-4 bg-gray-50 border rounded-lg hover:bg-gray-100">
          <div className="flex items-center gap-3 text-gray-700">
            <FileText size={24} />
            <span className="font-medium">ส่วนของอาจารย์ (Admin)</span>
          </div>
          <span className="text-sm text-gray-500">ดูรายงานทั้งหมด &rarr;</span>
        </Link>
      </div>
    </div>
  );
}
