import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import {
  listCases,
  createCase,
  updateCase,
  deleteCase,
  type Case,
} from "@/api/cases";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import {
  FolderPlus,
  Search,
  Loader2,
  Pencil,
  Trash2,
  ExternalLink,
  X,
  AlertTriangle,
  CheckCircle2,
  FolderOpen,
} from "lucide-react";

// ─── Types ────────────────────────────────────────────────────────────────────

type Priority = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
type Status = "OPEN" | "IN_PROGRESS" | "PENDING" | "CLOSED";

interface CaseFormState {
  title: string;
  description: string;
  priority: Priority;
  status: Status;
  tags: string;
}

const DEFAULT_FORM: CaseFormState = {
  title: "",
  description: "",
  priority: "MEDIUM",
  status: "OPEN",
  tags: "",
};

// ─── Helpers ──────────────────────────────────────────────────────────────────

function priorityColor(p: Priority) {
  const map: Record<Priority, string> = {
    LOW: "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
    MEDIUM: "bg-amber-500/15 text-amber-400 border-amber-500/30",
    HIGH: "bg-orange-500/15 text-orange-400 border-orange-500/30",
    CRITICAL: "bg-red-500/15 text-red-400 border-red-500/30",
  };
  return map[p] ?? map.MEDIUM;
}

function statusColor(s: Status) {
  const map: Record<Status, string> = {
    OPEN: "bg-blue-500/15 text-blue-400 border-blue-500/30",
    IN_PROGRESS: "bg-violet-500/15 text-violet-400 border-violet-500/30",
    PENDING: "bg-amber-500/15 text-amber-400 border-amber-500/30",
    CLOSED: "bg-slate-500/15 text-slate-400 border-slate-500/30",
  };
  return map[s] ?? map.OPEN;
}

// ─── Modal ────────────────────────────────────────────────────────────────────

function CaseModal({
  open,
  onClose,
  onSave,
  saving,
  initial,
  mode,
}: {
  open: boolean;
  onClose: () => void;
  onSave: (form: CaseFormState) => void;
  saving: boolean;
  initial: CaseFormState;
  mode: "create" | "edit";
}) {
  const [form, setForm] = useState<CaseFormState>(initial);
  const firstRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (open) {
      setForm(initial);
      setTimeout(() => firstRef.current?.focus(), 50);
    }
  }, [open, initial]);

  if (!open) return null;

  const handle = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ background: "rgba(0,0,0,0.65)", backdropFilter: "blur(6px)" }}
    >
      <div
        className="relative w-full max-w-lg rounded-2xl border shadow-2xl"
        style={{
          background: "linear-gradient(145deg, #1a1f2e 0%, #111520 100%)",
          borderColor: "rgba(99,102,241,0.25)",
          animation: "modalIn .18s cubic-bezier(.22,1,.36,1)",
        }}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 pt-6 pb-4 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div
              className="flex h-9 w-9 items-center justify-center rounded-xl"
              style={{ background: "rgba(99,102,241,0.2)" }}
            >
              {mode === "create" ? (
                <FolderPlus size={16} className="text-indigo-400" />
              ) : (
                <Pencil size={16} className="text-indigo-400" />
              )}
            </div>
            <h2 className="text-lg font-semibold text-white">
              {mode === "create" ? "New Case" : "Edit Case"}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X size={16} />
          </button>
        </div>

        {/* Body */}
        <div className="px-6 py-5 space-y-4">
          {/* Title */}
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              Case Title <span className="text-red-400">*</span>
            </label>
            <input
              ref={firstRef}
              name="title"
              value={form.title}
              onChange={handle}
              placeholder="e.g. Phishing Campaign Investigation"
              className="w-full rounded-lg border px-3 py-2 text-sm text-white placeholder-slate-500 outline-none transition-all focus:ring-2 focus:ring-indigo-500/50"
              style={{
                background: "rgba(255,255,255,0.05)",
                borderColor: "rgba(255,255,255,0.12)",
              }}
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              Description
            </label>
            <textarea
              name="description"
              value={form.description}
              onChange={handle}
              rows={3}
              placeholder="Brief summary of the case..."
              className="w-full rounded-lg border px-3 py-2 text-sm text-white placeholder-slate-500 outline-none resize-none transition-all focus:ring-2 focus:ring-indigo-500/50"
              style={{
                background: "rgba(255,255,255,0.05)",
                borderColor: "rgba(255,255,255,0.12)",
              }}
            />
          </div>

          {/* Priority & Status */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1.5">
                Priority
              </label>
              <select
                name="priority"
                value={form.priority}
                onChange={handle}
                className="w-full rounded-lg border px-3 py-2 text-sm text-white outline-none transition-all focus:ring-2 focus:ring-indigo-500/50"
                style={{
                  background: "#1a1f2e",
                  borderColor: "rgba(255,255,255,0.12)",
                }}
              >
                {(["LOW", "MEDIUM", "HIGH", "CRITICAL"] as Priority[]).map(
                  (p) => (
                    <option key={p} value={p}>
                      {p}
                    </option>
                  )
                )}
              </select>
            </div>

            {mode === "edit" && (
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1.5">
                  Status
                </label>
                <select
                  name="status"
                  value={form.status}
                  onChange={handle}
                  className="w-full rounded-lg border px-3 py-2 text-sm text-white outline-none transition-all focus:ring-2 focus:ring-indigo-500/50"
                  style={{
                    background: "#1a1f2e",
                    borderColor: "rgba(255,255,255,0.12)",
                  }}
                >
                  {(
                    ["OPEN", "IN_PROGRESS", "PENDING", "CLOSED"] as Status[]
                  ).map((s) => (
                    <option key={s} value={s}>
                      {s.replace("_", " ")}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          {/* Tags */}
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              Tags{" "}
              <span className="text-slate-600 font-normal">(comma-separated)</span>
            </label>
            <input
              name="tags"
              value={form.tags}
              onChange={handle}
              placeholder="phishing, ransomware, critical"
              className="w-full rounded-lg border px-3 py-2 text-sm text-white placeholder-slate-500 outline-none transition-all focus:ring-2 focus:ring-indigo-500/50"
              style={{
                background: "rgba(255,255,255,0.05)",
                borderColor: "rgba(255,255,255,0.12)",
              }}
            />
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 px-6 pb-6">
          <button
            onClick={onClose}
            className="rounded-lg px-4 py-2 text-sm font-medium text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            Cancel
          </button>
          <button
            disabled={saving || !form.title.trim()}
            onClick={() => onSave(form)}
            className="flex items-center gap-2 rounded-lg px-5 py-2 text-sm font-semibold text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            style={{
              background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
              boxShadow: saving ? "none" : "0 0 20px rgba(99,102,241,0.4)",
            }}
          >
            {saving && <Loader2 size={14} className="animate-spin" />}
            {mode === "create" ? "Create Case" : "Save Changes"}
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Delete Confirm ───────────────────────────────────────────────────────────

function DeleteConfirm({
  caseItem,
  onClose,
  onConfirm,
  deleting,
}: {
  caseItem: Case;
  onClose: () => void;
  onConfirm: () => void;
  deleting: boolean;
}) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ background: "rgba(0,0,0,0.65)", backdropFilter: "blur(6px)" }}
    >
      <div
        className="w-full max-w-md rounded-2xl border p-6 shadow-2xl"
        style={{
          background: "linear-gradient(145deg, #1a1f2e 0%, #111520 100%)",
          borderColor: "rgba(239,68,68,0.3)",
          animation: "modalIn .18s cubic-bezier(.22,1,.36,1)",
        }}
      >
        <div className="flex items-start gap-4">
          <div
            className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl"
            style={{ background: "rgba(239,68,68,0.15)" }}
          >
            <AlertTriangle size={18} className="text-red-400" />
          </div>
          <div className="flex-1">
            <h3 className="text-base font-semibold text-white mb-1">
              Delete Case?
            </h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              This will permanently delete{" "}
              <span className="font-medium text-white">
                &ldquo;{caseItem.title}&rdquo;
              </span>{" "}
              and all associated tasks, timeline events, and decisions. This
              action cannot be undone.
            </p>
          </div>
        </div>
        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={onClose}
            className="rounded-lg px-4 py-2 text-sm font-medium text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            Cancel
          </button>
          <button
            disabled={deleting}
            onClick={onConfirm}
            className="flex items-center gap-2 rounded-lg px-5 py-2 text-sm font-semibold text-white transition-all disabled:opacity-50"
            style={{ background: "linear-gradient(135deg, #ef4444, #dc2626)" }}
          >
            {deleting && <Loader2 size={14} className="animate-spin" />}
            Delete Case
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Toast ────────────────────────────────────────────────────────────────────

function Toast({ message, type }: { message: string; type: "success" | "error" }) {
  return (
    <div
      className="fixed bottom-6 right-6 z-[100] flex items-center gap-3 rounded-xl border px-4 py-3 shadow-2xl text-sm font-medium"
      style={{
        background:
          type === "success"
            ? "linear-gradient(135deg,#064e3b,#065f46)"
            : "linear-gradient(135deg,#7f1d1d,#991b1b)",
        borderColor:
          type === "success"
            ? "rgba(52,211,153,0.3)"
            : "rgba(248,113,113,0.3)",
        color: type === "success" ? "#6ee7b7" : "#fca5a5",
        animation: "toastIn .25s cubic-bezier(.22,1,.36,1)",
      }}
    >
      {type === "success" ? (
        <CheckCircle2 size={16} />
      ) : (
        <AlertTriangle size={16} />
      )}
      {message}
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

export function CaseList() {
  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");

  // Modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<"create" | "edit">("create");
  const [modalInitial, setModalInitial] = useState<CaseFormState>(DEFAULT_FORM);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  // Delete state
  const [deleteTarget, setDeleteTarget] = useState<Case | null>(null);
  const [deleting, setDeleting] = useState(false);

  // Toast
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);

  const showToast = (message: string, type: "success" | "error" = "success") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3500);
  };

  // ── Data Loading ──────────────────────────────────────────────────────────

  const loadCases = async () => {
    try {
      const data = await listCases();
      setCases(data);
    } catch {
      showToast("Failed to load cases.", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCases();
  }, []);

  // ── Filtered list ─────────────────────────────────────────────────────────

  const filtered = cases.filter((c) => {
    const q = query.toLowerCase();
    if (!q) return true;
    return (
      c.title.toLowerCase().includes(q) ||
      c.id.toLowerCase().includes(q) ||
      (c.tags ?? []).some((t) => t.toLowerCase().includes(q))
    );
  });

  // ── CRUD handlers ─────────────────────────────────────────────────────────

  const openCreate = () => {
    setModalMode("create");
    setModalInitial(DEFAULT_FORM);
    setEditingId(null);
    setModalOpen(true);
  };

  const openEdit = (c: Case) => {
    setModalMode("edit");
    setModalInitial({
      title: c.title,
      description: c.description ?? "",
      priority: c.priority as Priority,
      status: c.status as Status,
      tags: (c.tags ?? []).join(", "),
    });
    setEditingId(c.id);
    setModalOpen(true);
  };

  const handleSave = async (form: CaseFormState) => {
    setSaving(true);
    try {
      const tags = form.tags
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean);

      if (modalMode === "create") {
        await createCase({
          title: form.title,
          description: form.description || undefined,
          priority: form.priority,
          tags,
        });
        showToast("Case created successfully!");
      } else if (editingId) {
        await updateCase(editingId, {
          title: form.title,
          description: form.description || undefined,
          priority: form.priority,
          status: form.status,
          tags,
        });
        showToast("Case updated successfully!");
      }
      setModalOpen(false);
      await loadCases();
    } catch {
      showToast("Operation failed. Please try again.", "error");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteTarget) return;
    setDeleting(true);
    try {
      await deleteCase(deleteTarget.id);
      showToast("Case deleted.");
      setDeleteTarget(null);
      setCases((prev) => prev.filter((c) => c.id !== deleteTarget.id));
    } catch {
      showToast("Delete failed. Please try again.", "error");
    } finally {
      setDeleting(false);
    }
  };

  // ─── Render ───────────────────────────────────────────────────────────────

  return (
    <>
      <style>{`
        @keyframes modalIn {
          from { opacity: 0; transform: scale(0.94) translateY(8px); }
          to   { opacity: 1; transform: scale(1)   translateY(0);    }
        }
        @keyframes toastIn {
          from { opacity: 0; transform: translateY(12px); }
          to   { opacity: 1; transform: translateY(0);    }
        }
        @keyframes rowFadeIn {
          from { opacity: 0; transform: translateY(4px); }
          to   { opacity: 1; transform: translateY(0);   }
        }
      `}</style>

      {/* Modals */}
      <CaseModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSave={handleSave}
        saving={saving}
        initial={modalInitial}
        mode={modalMode}
      />
      {deleteTarget && (
        <DeleteConfirm
          caseItem={deleteTarget}
          onClose={() => setDeleteTarget(null)}
          onConfirm={handleDelete}
          deleting={deleting}
        />
      )}
      {toast && <Toast {...toast} />}

      {/* Page */}
      <div className="min-h-screen p-6 sm:p-10" style={{ background: "var(--color-background, #0d1117)" }}>
        <div className="max-w-7xl mx-auto space-y-6">

          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-white">
                Cases
              </h1>
              <p className="text-slate-400 mt-1 text-sm">
                Manage all investigations and incidents in one place.
              </p>
            </div>
            <button
              id="new-case-btn"
              onClick={openCreate}
              className="flex items-center gap-2 rounded-xl px-5 py-2.5 text-sm font-semibold text-white transition-all hover:brightness-110 active:scale-95 self-start sm:self-auto"
              style={{
                background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
                boxShadow: "0 0 24px rgba(99,102,241,0.35)",
              }}
            >
              <FolderPlus size={16} />
              New Case
            </button>
          </div>

          {/* Search */}
          <div className="relative max-w-md">
            <Search
              size={15}
              className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none"
            />
            <input
              id="case-search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search cases by title, ID, or tags..."
              className="w-full rounded-xl border pl-10 pr-4 py-2.5 text-sm text-white placeholder-slate-500 outline-none transition-all focus:ring-2 focus:ring-indigo-500/50"
              style={{
                background: "rgba(255,255,255,0.04)",
                borderColor: "rgba(255,255,255,0.1)",
              }}
            />
          </div>

          {/* Table */}
          <div
            className="rounded-2xl border overflow-hidden shadow-xl"
            style={{
              borderColor: "rgba(255,255,255,0.08)",
              background: "rgba(255,255,255,0.02)",
            }}
          >
            {loading ? (
              <div className="flex items-center justify-center py-24">
                <Loader2
                  size={32}
                  className="animate-spin"
                  style={{ color: "#6366f1" }}
                />
              </div>
            ) : (
              <table className="w-full text-sm text-left">
                <thead>
                  <tr
                    style={{
                      background: "rgba(255,255,255,0.04)",
                      borderBottom: "1px solid rgba(255,255,255,0.07)",
                    }}
                  >
                    {["Case ID", "Title", "Status", "Priority", "Created", "Actions"].map(
                      (h, i) => (
                        <th
                          key={h}
                          className="px-5 py-3.5 text-xs font-semibold uppercase tracking-wider text-slate-500"
                          style={{ textAlign: i === 5 ? "right" : "left" }}
                        >
                          {h}
                        </th>
                      )
                    )}
                  </tr>
                </thead>
                <tbody>
                  {filtered.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="py-20 text-center">
                        <div className="flex flex-col items-center gap-3">
                          <FolderOpen size={36} className="text-slate-600" />
                          <p className="text-slate-500 text-sm">
                            {query
                              ? `No cases match "${query}"`
                              : "No cases yet. Create one to get started."}
                          </p>
                          {!query && (
                            <button
                              onClick={openCreate}
                              className="mt-1 rounded-lg px-4 py-1.5 text-xs font-semibold text-indigo-400 border border-indigo-500/30 hover:bg-indigo-500/10 transition-colors"
                            >
                              + New Case
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ) : (
                    filtered.map((c, idx) => (
                      <tr
                        key={c.id}
                        id={`case-row-${c.id.substring(0, 8)}`}
                        className="group transition-colors"
                        style={{
                          borderBottom: "1px solid rgba(255,255,255,0.05)",
                          animation: `rowFadeIn 0.25s ease both`,
                          animationDelay: `${idx * 40}ms`,
                        }}
                        onMouseEnter={(e) =>
                          ((e.currentTarget as HTMLElement).style.background =
                            "rgba(99,102,241,0.06)")
                        }
                        onMouseLeave={(e) =>
                          ((e.currentTarget as HTMLElement).style.background =
                            "transparent")
                        }
                      >
                        {/* Case ID */}
                        <td className="px-5 py-4">
                          <span className="font-mono text-xs px-2 py-1 rounded-md text-slate-400" style={{ background: "rgba(255,255,255,0.05)" }}>
                            {c.id.substring(0, 8)}
                          </span>
                        </td>

                        {/* Title */}
                        <td className="px-5 py-4 font-medium text-white max-w-xs truncate">
                          {c.title}
                        </td>

                        {/* Status */}
                        <td className="px-5 py-4">
                          <span
                            className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold ${statusColor(c.status as Status)}`}
                          >
                            {c.status.replace("_", " ")}
                          </span>
                        </td>

                        {/* Priority */}
                        <td className="px-5 py-4">
                          <span
                            className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold ${priorityColor(c.priority as Priority)}`}
                          >
                            {c.priority}
                          </span>
                        </td>

                        {/* Created */}
                        <td className="px-5 py-4 text-slate-500 text-xs">
                          {new Date(c.created_at).toLocaleDateString("en-GB", {
                            day: "numeric",
                            month: "short",
                            year: "numeric",
                          })}
                        </td>

                        {/* Actions */}
                        <td className="px-5 py-4">
                          <div className="flex items-center justify-end gap-1">
                            {/* Open */}
                            <Link
                              to={`/cases/${c.id}`}
                              id={`open-case-${c.id.substring(0, 8)}`}
                              title="Open case workspace"
                              className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 hover:text-indigo-400 hover:bg-indigo-500/10 transition-colors"
                            >
                              <ExternalLink size={14} />
                            </Link>

                            {/* Edit */}
                            <button
                              id={`edit-case-${c.id.substring(0, 8)}`}
                              title="Edit case"
                              onClick={() => openEdit(c)}
                              className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 hover:text-amber-400 hover:bg-amber-500/10 transition-colors"
                            >
                              <Pencil size={14} />
                            </button>

                            {/* Delete */}
                            <button
                              id={`delete-case-${c.id.substring(0, 8)}`}
                              title="Delete case"
                              onClick={() => setDeleteTarget(c)}
                              className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-500 hover:text-red-400 hover:bg-red-500/10 transition-colors"
                            >
                              <Trash2 size={14} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            )}
          </div>

          {/* Footer count */}
          {!loading && cases.length > 0 && (
            <p className="text-xs text-slate-600 text-right">
              Showing {filtered.length} of {cases.length} case
              {cases.length !== 1 ? "s" : ""}
            </p>
          )}
        </div>
      </div>
    </>
  );
}
