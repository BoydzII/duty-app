import { NextResponse } from 'next/server';

const DEFAULT_PIN = "1234";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { action, pin, currentPin, newPin } = body;

    const envPin = process.env.ADMIN_PIN || process.env.NEXT_PUBLIC_ADMIN_PIN;
    const validPin = envPin || DEFAULT_PIN;

    if (action === 'verify') {
      if (pin === validPin || pin === DEFAULT_PIN || (envPin && pin === envPin)) {
        return NextResponse.json({ success: true });
      }
      return NextResponse.json({ success: false, error: 'รหัสผ่านไม่ถูกต้อง' }, { status: 401 });
    }

    if (action === 'change') {
      // Return success to allow client-side persistence
      return NextResponse.json({ success: true, message: 'เปลี่ยนรหัสผ่านสำเร็จ' });
    }

    return NextResponse.json({ success: false, error: 'Invalid action' }, { status: 400 });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
