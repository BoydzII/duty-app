export const dynamic = 'force-dynamic';
import { NextResponse } from 'next/server';
import fs from 'fs/promises';
import path from 'path';

const dataFilePath = path.join(process.cwd(), 'data', 'duty_reports.json');
const GAS_URL = process.env.GAS_URL || process.env.NEXT_PUBLIC_GAS_URL;

async function getReportsData() {
  try {
    const data = await fs.readFile(dataFilePath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    return [];
  }
}

async function saveReportsData(data: any) {
  await fs.mkdir(path.join(process.cwd(), 'data'), { recursive: true });
  await fs.writeFile(dataFilePath, JSON.stringify(data, null, 2), 'utf8');
}

export async function POST(request: Request) {
  try {
    const data = await request.json();

    // If Google Apps Script is configured, send data there
    if (GAS_URL) {
      // Provide GAS action name (mapped to GAS add_report)
      const payload = {
        action: 'add_report',
        date: data.date,
        reporterStudentId: data.reporter.studentId,
        dutyDay: data.dutyDay,
        friendsPresent: data.friendsPresent,
        imageUrl: data.image
      };
      
      const res = await fetch(GAS_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      return NextResponse.json(await res.json());
    }

    // Otherwise use Local JSON
    const reports = await getReportsData();
    const newReport = {
      id: Date.now().toString(),
      reporter: data.reporter,
      date: data.date,
      dutyDay: data.dutyDay,
      friendsPresent: data.friendsPresent,
      imageUrl: data.image,
      createdAt: new Date().toISOString()
    };
    reports.push(newReport);
    await saveReportsData(reports);
    return NextResponse.json({ success: true, report: newReport });
  } catch (error: any) {
    console.error("API Error:", error);
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function GET() {
  try {
    if (GAS_URL) {
      const res = await fetch(`${GAS_URL}?action=get_reports`, { cache: 'no-store', next: { revalidate: 0 } });
      const result = await res.json();
      if (result.reports) {
        result.reports.sort((a: any, b: any) => new Date(b.date).getTime() - new Date(a.date).getTime());
      }
      return NextResponse.json(result);
    }

    const reports = await getReportsData();
    reports.sort((a: any, b: any) => new Date(b.date).getTime() - new Date(a.date).getTime());
    return NextResponse.json({ success: true, reports });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function DELETE(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');
    if (!id) return NextResponse.json({ success: false, error: 'Missing report id' }, { status: 400 });

    if (GAS_URL) {
      const res = await fetch(GAS_URL, {
        method: 'POST',
        body: JSON.stringify({ action: 'delete_report', id }),
      });
      const result = await res.json();
      return NextResponse.json(result);
    }

    const reports = await getReportsData();
    const filtered = reports.filter((r: any) => r.id !== id);
    await saveReportsData(filtered);
    return NextResponse.json({ success: true, reports: filtered });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
