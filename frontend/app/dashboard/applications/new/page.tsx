"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, Globe, FileText, ArrowRight, ArrowLeft } from "lucide-react";

export default function NewApplicationFlow() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [countries, setCountries] = useState<any[]>([]);
  const [visaTypes, setVisaTypes] = useState<any[]>([]);
  const [selectedCountry, setSelectedCountry] = useState<number | null>(null);
  const [selectedVisaType, setSelectedVisaType] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchCountries();
  }, []);

  const fetchCountries = async () => {
    setIsLoading(true);
    try {
      const response: any = await api.get("/visas/countries/");
      if (response.success) {
        setCountries(response.data); // Assuming pagination might not be active, or we handle it if needed
      }
    } catch (err) {
      setError("Failed to load countries");
    } finally {
      setIsLoading(false);
    }
  };

  const fetchVisaTypes = async (countryId: number) => {
    setIsLoading(true);
    try {
      const response: any = await api.get(`/visas/?country=${countryId}`);
      if (response.success) {
        setVisaTypes(response.data);
      }
    } catch (err) {
      setError("Failed to load visa types");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCountrySelect = (id: number) => {
    setSelectedCountry(id);
    setSelectedVisaType(null);
    fetchVisaTypes(id);
    setStep(2);
  };

  const handleSubmit = async () => {
    if (!selectedVisaType) return;
    setIsSubmitting(true);
    setError("");
    try {
      const response: any = await api.post("/checklists/user-checklists/", {
        visa_type: selectedVisaType,
      });
      if (response.success) {
        router.push(`/dashboard/applications/${response.data.id}`);
      }
    } catch (err: any) {
      setError(err.message || "Failed to create application");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Start New Application</h1>
        <div className="flex items-center gap-2 text-sm font-medium text-gray-500">
          <span className={step >= 1 ? "text-[var(--color-primary)]" : ""}>Country</span>
          <span className="mx-2">/</span>
          <span className={step >= 2 ? "text-[var(--color-primary)]" : ""}>Visa Type</span>
        </div>
      </div>

      {error && (
        <div className="rounded-md bg-red-50 p-4 text-sm text-red-500 border border-red-200">
          {error}
        </div>
      )}

      {step === 1 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Globe className="h-5 w-5 text-[var(--color-primary)]" />
              Select Destination
            </CardTitle>
            <CardDescription>Where are you planning to travel?</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex justify-center p-8">
                <Loader2 className="h-8 w-8 animate-spin text-[var(--color-primary)]" />
              </div>
            ) : (
              <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3">
                {countries.length > 0 ? (
                  countries.map((c) => (
                    <button
                      key={c.id}
                      onClick={() => handleCountrySelect(c.id)}
                      className="flex flex-col items-center justify-center p-6 rounded-xl border-2 border-transparent bg-white shadow-sm hover:border-[var(--color-primary)] hover:shadow-md transition-all duration-200"
                    >
                      <span className="text-4xl mb-3">{c.flag_emoji || "🌎"}</span>
                      <span className="font-semibold text-gray-900">{c.name}</span>
                    </button>
                  ))
                ) : (
                  <p className="text-sm text-gray-500 col-span-full text-center p-4">No countries available.</p>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {step === 2 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-[var(--color-primary)]" />
              Select Visa Type
            </CardTitle>
            <CardDescription>What kind of visa are you applying for?</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex justify-center p-8">
                <Loader2 className="h-8 w-8 animate-spin text-[var(--color-primary)]" />
              </div>
            ) : (
              <div className="grid gap-4 sm:grid-cols-2">
                {visaTypes.length > 0 ? (
                  visaTypes.map((v) => (
                    <div
                      key={v.id}
                      onClick={() => setSelectedVisaType(v.id)}
                      className={`cursor-pointer rounded-xl border-2 p-4 transition-all duration-200 ${
                        selectedVisaType === v.id
                          ? "border-[var(--color-primary)] bg-[var(--color-primary-light)]"
                          : "border-[var(--color-border-custom)] hover:border-gray-300 bg-white shadow-sm"
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="font-semibold text-gray-900">{v.name}</h3>
                          <p className="text-sm text-gray-500 mt-1 line-clamp-2">{v.description}</p>
                        </div>
                        <div className={`h-5 w-5 rounded-full border flex items-center justify-center ${
                          selectedVisaType === v.id ? "border-[var(--color-primary)] bg-[var(--color-primary)]" : "border-gray-300"
                        }`}>
                          {selectedVisaType === v.id && <div className="h-2 w-2 rounded-full bg-white" />}
                        </div>
                      </div>
                      <div className="mt-3 flex items-center gap-2 text-xs font-medium text-gray-500">
                        <span className="bg-gray-100 px-2 py-1 rounded">Validity: {v.validity_period}</span>
                        <span className="bg-gray-100 px-2 py-1 rounded">Processing: {v.processing_time}</span>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-gray-500 col-span-full text-center p-8 bg-gray-50 rounded-lg">No visa types available for this country.</p>
                )}
              </div>
            )}
          </CardContent>
          <CardFooter className="flex justify-between border-t p-6">
            <Button variant="outline" onClick={() => setStep(1)} className="gap-2">
              <ArrowLeft className="h-4 w-4" /> Back to Countries
            </Button>
            <Button
              onClick={handleSubmit}
              disabled={!selectedVisaType || isSubmitting}
              isLoading={isSubmitting}
              className="gap-2"
            >
              Start Checklist <ArrowRight className="h-4 w-4" />
            </Button>
          </CardFooter>
        </Card>
      )}
    </div>
  );
}
