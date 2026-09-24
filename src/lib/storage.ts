import localforage from 'localforage';

export interface DraftReport {
  id: string; // unique local id (e.g., timestamp)
  internId: string;
  internName: string;
  studentId: string;
  grade: string;
  studentNumber: string;
  department: string;
  date: string;
  photoBase64: string;
}

const DRAFTS_KEY = 'internship_drafts';

export async function saveDraftReport(report: Omit<DraftReport, 'id'>) {
  const drafts = await getDraftReports();
  const newDraft: DraftReport = {
    ...report,
    id: Date.now().toString(),
  };
  drafts.push(newDraft);
  await localforage.setItem(DRAFTS_KEY, drafts);
  return newDraft;
}

export async function getDraftReports(): Promise<DraftReport[]> {
  const drafts = await localforage.getItem<DraftReport[]>(DRAFTS_KEY);
  return drafts || [];
}

export async function clearDraftReport(id: string) {
  const drafts = await getDraftReports();
  const updatedDrafts = drafts.filter(draft => draft.id !== id);
  await localforage.setItem(DRAFTS_KEY, updatedDrafts);
}

export async function clearAllDrafts() {
  await localforage.removeItem(DRAFTS_KEY);
}
