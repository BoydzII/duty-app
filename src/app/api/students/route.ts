export const dynamic = 'force-dynamic';
import { NextResponse } from 'next/server';

const GAS_URL = process.env.GAS_URL || process.env.NEXT_PUBLIC_GAS_URL;

export async function GET() {
  try {
    if (GAS_URL) {
      const res = await fetch(`${GAS_URL}?action=get_students`, { cache: 'no-store', next: { revalidate: 0 } });
      const result = await res.json();
      return NextResponse.json(result);
    }
    return NextResponse.json({ success: true, students: [] });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const data = await request.json();
    if (GAS_URL) {
      const res = await fetch(GAS_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      return NextResponse.json(await res.json());
    }
    return NextResponse.json({ success: true });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
