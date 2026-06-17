"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuthStore } from "@/store/useAuthStore";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuthStore();
  
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    nationality: "",
    phone: "",
    password: "",
    password2: "",
  });
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      await register(formData);
      router.push("/login");
    } catch (err: any) {
      if (err.errors) {
        // Handle validation errors from backend
        let messages = "";
        if (typeof err.errors === "object") {
           messages = Object.entries(err.errors).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(" ") : v}`).join(" | ");
        } else {
           messages = err.errors.toString();
        }
        setError(messages || "Failed to register.");
      } else {
        setError(err.message || "An unexpected error occurred.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 p-4 py-12">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-2 text-center">
          <CardTitle className="text-2xl font-bold text-gray-900">Create an Account</CardTitle>
          <CardDescription>Join us to track your visa applications easily</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="rounded-md bg-red-50 p-3 text-sm text-red-500 border border-red-200">
                {error}
              </div>
            )}
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Username"
                name="username"
                placeholder="johndoe"
                value={formData.username}
                onChange={handleChange}
                required
              />
              <Input
                label="Nationality"
                name="nationality"
                placeholder="US"
                value={formData.nationality}
                onChange={handleChange}
                required
              />
            </div>
            <Input
              label="Phone Number"
              name="phone"
              placeholder="+1234567890"
              value={formData.phone}
              onChange={handleChange}
            />
            <Input
              label="Email"
              name="email"
              type="email"
              placeholder="you@example.com"
              value={formData.email}
              onChange={handleChange}
              required
            />
            <Input
              label="Password"
              name="password"
              type="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={handleChange}
              required
            />
            <Input
              label="Confirm Password"
              name="password2"
              type="password"
              placeholder="••••••••"
              value={formData.password2}
              onChange={handleChange}
              required
            />
            <Button type="submit" className="w-full" isLoading={isLoading}>
              Sign Up
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center text-sm text-gray-500">
          Already have an account?{" "}
          <Link href="/login" className="ml-1 text-[var(--color-primary)] font-medium hover:underline">
            Log in
          </Link>
        </CardFooter>
      </Card>
    </div>
  );
}
