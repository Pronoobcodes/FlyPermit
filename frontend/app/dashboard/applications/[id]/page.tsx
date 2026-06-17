"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ProgressBar } from "@/components/ui/progress-bar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Loader2, ArrowLeft, CheckCircle2, Circle, Clock } from "lucide-react";
import Link from "next/link";

export default function ChecklistDetail() {
  const { id } = useParams();
  const router = useRouter();
  const [checklist, setChecklist] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchChecklist = async () => {
    try {
      const response: any = await api.get(`/checklists/user-checklists/${id}/`);
      if (response.success) {
        setChecklist(response.data);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load checklist");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchChecklist();
  }, [id]);

  const handleToggleItem = async (itemId: number, currentStatus: string) => {
    const newStatus = currentStatus === "have_it" ? "pending" : "have_it";
    
    // Optimistic update
    setChecklist((prev: any) => {
      const newItems = prev.items.map((item: any) => 
        item.id === itemId ? { ...item, status: newStatus } : item
      );
      const completedCount = newItems.filter((i: any) => i.status === "have_it").length;
      const completion_percentage = Math.round((completedCount / newItems.length) * 100);
      
      return { ...prev, items: newItems, completion_percentage };
    });

    try {
      await api.patch(`/checklists/checklist-items/${itemId}/`, {
        status: newStatus
      });
      // Optionally refetch to ensure sync
      // fetchChecklist();
    } catch (err: any) {
      // Revert on error
      fetchChecklist();
      alert("Failed to update item status");
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-[var(--color-primary)]" />
      </div>
    );
  }

  if (error || !checklist) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500 mb-4">{error || "Checklist not found"}</p>
        <Link href="/dashboard">
          <Button variant="outline">Return to Dashboard</Button>
        </Link>
      </div>
    );
  }

  const isCompleted = checklist.completion_percentage === 100;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/dashboard">
          <Button variant="ghost" size="icon" className="rounded-full">
            <ArrowLeft className="h-5 w-5" />
          </Button>
        </Link>
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">{checklist.visa_type_name}</h1>
          <p className="text-sm text-gray-500">Created on {new Date(checklist.created_at).toLocaleDateString()}</p>
        </div>
        <div className="ml-auto">
          <Badge variant={isCompleted ? "success" : "warning"} className="text-sm px-3 py-1">
            {isCompleted ? "Completed" : "In Progress"}
          </Badge>
        </div>
      </div>

      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-medium text-gray-900">Application Progress</h3>
            <span className="text-sm font-bold text-[var(--color-primary)]">{checklist.completion_percentage}%</span>
          </div>
          <ProgressBar value={checklist.completion_percentage} className="h-3" />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Required Documents</CardTitle>
          <CardDescription>Check off the documents as you collect them.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {checklist.items.map((item: any) => {
              const isDone = item.status === "have_it";
              return (
                <div 
                  key={item.id} 
                  className={`flex items-center gap-4 p-4 rounded-lg border transition-all ${
                    isDone ? "bg-emerald-50 border-emerald-200" : "bg-white border-gray-200 hover:border-gray-300"
                  }`}
                >
                  <button 
                    onClick={() => handleToggleItem(item.id, item.status)}
                    className={`flex-shrink-0 focus:outline-none transition-transform active:scale-95 ${
                      isDone ? "text-[var(--color-success)]" : "text-gray-300 hover:text-gray-400"
                    }`}
                  >
                    {isDone ? <CheckCircle2 className="h-8 w-8" /> : <Circle className="h-8 w-8" />}
                  </button>
                  
                  <div className="flex-1">
                    <h4 className={`font-semibold ${isDone ? "text-emerald-900 line-through opacity-70" : "text-gray-900"}`}>
                      {item.document_name}
                    </h4>
                    {item.user_note && (
                      <p className="text-sm text-gray-500 mt-1">{item.user_note}</p>
                    )}
                  </div>

                  {item.marked_done_at && (
                    <div className="text-xs text-gray-500 flex flex-col items-end">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" /> Done
                      </span>
                      <span>{new Date(item.marked_done_at).toLocaleDateString()}</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
