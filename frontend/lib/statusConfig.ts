export const statusConfig: Record<string, { label: string; className: string }> = {
  in_progress: { label: 'In Progress', className: 'bg-orange-100 text-orange-700 border border-orange-200' },
  completed:   { label: 'Completed',   className: 'bg-green-100 text-green-700 border border-green-200' },
  submitted:   { label: 'Submitted',   className: 'bg-blue-100 text-blue-700 border border-blue-200' },
  approved:    { label: 'Approved',    className: 'bg-emerald-100 text-emerald-700 border border-emerald-200' },
};
