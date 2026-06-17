"use client";

import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ProgressBar } from "@/components/ui/progress-bar";
import { FileText, Clock, CheckCircle2, AlertCircle } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function DashboardOverview() {
  const [checklists, setChecklists] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchChecklists = async () => {
      try {
        const response: any = await api.get("/checklists/user-checklists/");
        if (response.success) {
          setChecklists(response.data);
        }
      } catch (error) {
        console.error("Failed to fetch checklists:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchChecklists();
  }, []);

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-[var(--color-primary)] border-t-transparent"></div>
      </div>
    );
  }

  const activeChecklists = checklists.filter(c => c.status !== "COMPLETED");
  const completedChecklists = checklists.filter(c => c.status === "COMPLETED");

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Dashboard Overview</h1>
        <Link href="/dashboard/applications/new">
          <Button>New Application</Button>
        </Link>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardContent className="p-6 flex items-center gap-4">
            <div className="rounded-lg bg-blue-100 p-3 text-blue-600">
              <FileText className="h-6 w-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">Total Applications</p>
              <p className="text-2xl font-bold">{checklists.length}</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 flex items-center gap-4">
            <div className="rounded-lg bg-orange-100 p-3 text-orange-600">
              <Clock className="h-6 w-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">In Progress</p>
              <p className="text-2xl font-bold">{activeChecklists.length}</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 flex items-center gap-4">
            <div className="rounded-lg bg-emerald-100 p-3 text-emerald-600">
              <CheckCircle2 className="h-6 w-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">Completed</p>
              <p className="text-2xl font-bold">{completedChecklists.length}</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 flex items-center gap-4">
            <div className="rounded-lg bg-red-100 p-3 text-red-600">
              <AlertCircle className="h-6 w-6" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">Action Required</p>
              <p className="text-2xl font-bold">0</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Recent Applications</CardTitle>
            <CardDescription>Your most recent visa application checklists.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {checklists.length === 0 ? (
              <p className="text-sm text-gray-500">You haven't started any applications yet.</p>
            ) : (
              checklists.slice(0, 5).map((checklist) => (
                <div key={checklist.id} className="flex items-center justify-between rounded-lg border p-4 shadow-sm hover:border-[var(--color-primary)] transition-colors">
                  <div className="space-y-1">
                    <p className="font-medium">{checklist.visa_type.name} - {checklist.visa_type.country.name}</p>
                    <p className="text-xs text-gray-500">Target Date: {checklist.target_date || "Not set"}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <ProgressBar value={checklist.completion_percentage || 0} className="w-24" />
                      <span className="text-xs font-medium text-gray-500">{checklist.completion_percentage || 0}%</span>
                    </div>
                  </div>
                  <Badge variant={checklist.status === "COMPLETED" ? "success" : "warning"}>
                    {checklist.status}
                  </Badge>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
