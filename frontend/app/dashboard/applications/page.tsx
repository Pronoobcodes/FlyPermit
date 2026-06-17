"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Plus, FileText } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { ProgressBar } from "@/components/ui/progress-bar";
import { statusConfig } from "@/lib/statusConfig";

export default function ApplicationsPage() {
  const [checklists, setChecklists] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchChecklists = async () => {
      try {
        const response: any = await api.get("/checklists/user-checklists/");
        if (response.success) {
          const fetchedData = response.data?.results ?? response.data ?? [];
          setChecklists(Array.isArray(fetchedData) ? fetchedData : []);
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

  const safeChecklists = Array.isArray(checklists) ? checklists : [];

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">My Applications</h1>
        <Link href="/dashboard/applications/new">
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            New Application
          </Button>
        </Link>
      </div>

      {safeChecklists.length === 0 ? (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center p-12 text-center">
            <div className="rounded-full bg-gray-100 p-4 mb-4">
              <FileText className="h-8 w-8 text-gray-400" />
            </div>
            <CardTitle className="mb-2">No applications found</CardTitle>
            <CardDescription className="mb-6 max-w-sm">
              You don't have any visa applications yet. Start a new application to generate a customized document checklist.
            </CardDescription>
            <Link href="/dashboard/applications/new">
              <Button variant="outline" className="gap-2">
                <Plus className="h-4 w-4" />
                Create your first application
              </Button>
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4">
          {safeChecklists.map((checklist) => (
            <Link href={`/dashboard/applications/${checklist.id}`} key={checklist.id}>
              <Card className="hover:border-[var(--color-primary)] transition-colors cursor-pointer">
                <CardContent className="p-6 flex items-center justify-between">
                  <div className="space-y-1">
                    <h3 className="font-semibold text-lg">{checklist.visa_type?.name ?? 'Unknown Visa'} - {checklist.visa_type?.country?.name ?? 'Unknown'}</h3>
                    <p className="text-sm text-gray-500">Started on {new Date(checklist.created_at).toLocaleDateString()}</p>
                    <div className="flex items-center gap-3 mt-3">
                      <ProgressBar value={checklist.completion_percentage || 0} className="w-32" />
                      <span className="text-sm font-medium text-gray-600">{Math.round(checklist.completion_percentage || 0)}% Complete</span>
                    </div>
                  </div>
                  {(() => {
                    const config = statusConfig[checklist.status] ?? statusConfig.in_progress;
                    return (
                      <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${config.className}`}>
                        {config.label}
                      </span>
                    );
                  })()}
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
