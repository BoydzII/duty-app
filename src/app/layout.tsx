import type { Metadata } from "next";
import { Sarabun } from "next/font/google";
import Navbar from "@/components/Navbar";
import "./globals.css";

const sarabun = Sarabun({
  weight: ['300', '400', '500', '600', '700'],
  subsets: ['thai', 'latin'],
  variable: "--font-sarabun",
});

export const metadata: Metadata = {
  title: "Internship Report System",
  description: "Offline-first application for daily internship reporting.",
  manifest: "/manifest.json",
  other: {
    "color-scheme": "light",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="th" style={{ colorScheme: "light" }}>
      <body
        className={`${sarabun.variable} antialiased bg-gray-50 min-h-screen text-gray-800`}
      >
        <div className="print:hidden">
          <Navbar />
        </div>
        <main className="max-w-4xl mx-auto p-4 md:p-6 print:max-w-full print:p-0">
          {children}
        </main>
      </body>
    </html>
  );
}
