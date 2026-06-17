"use client";

import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

export default function SettingsPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
  });

  const [passwords, setPasswords] = useState({
    current: "",
    new: "",
    confirm: "",
  });

  const [profileMessage, setProfileMessage] = useState({ type: "", text: "" });
  const [passwordMessage, setPasswordMessage] = useState({ type: "", text: "" });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response: any = await api.get("/accounts/profile/");
        if (response.success && response.data) {
          setForm({
            first_name: response.data.first_name || "",
            last_name: response.data.last_name || "",
            email: response.data.email || "",
          });
        }
      } catch (error) {
        console.error("Failed to fetch profile", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleSaveProfile = async () => {
    setIsSaving(true);
    setProfileMessage({ type: "", text: "" });
    try {
      const response: any = await api.patch("/accounts/profile/", {
        first_name: form.first_name,
        last_name: form.last_name,
      });
      if (response.success) {
        setProfileMessage({ type: "success", text: "Profile updated successfully." });
      }
    } catch (error: any) {
      setProfileMessage({ type: "error", text: error.message || "Failed to update profile." });
    } finally {
      setIsSaving(false);
    }
  };

  const handleChangePassword = async () => {
    setIsChangingPassword(true);
    setPasswordMessage({ type: "", text: "" });
    
    if (passwords.new !== passwords.confirm) {
      setPasswordMessage({ type: "error", text: "New passwords do not match." });
      setIsChangingPassword(false);
      return;
    }

    try {
      const response: any = await api.post("/accounts/change-password/", {
        current_password: passwords.current,
        new_password: passwords.new,
        confirm_password: passwords.confirm,
      });
      if (response.success) {
        setPasswordMessage({ type: "success", text: "Password updated successfully!" });
        setPasswords({ current: "", new: "", confirm: "" });
      }
    } catch (error: any) {
      const errorMsg = error.response?.data?.message || error.message || "Failed to update password.";
      setPasswordMessage({ type: "error", text: errorMsg });
    } finally {
      setIsChangingPassword(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-[var(--color-primary)]" />
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900">Settings</h1>
        <p className="text-gray-500">Manage your profile and account settings.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Profile Information</CardTitle>
          <CardDescription>Update your personal details here.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium text-gray-700">First Name</label>
              <input
                value={form.first_name}
                onChange={e => setForm({...form, first_name: e.target.value})}
                className="w-full border rounded-md px-3 py-2 mt-1 focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]"
                placeholder="First Name"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Last Name</label>
              <input
                value={form.last_name}
                onChange={e => setForm({...form, last_name: e.target.value})}
                className="w-full border rounded-md px-3 py-2 mt-1 focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]"
                placeholder="Last Name"
              />
            </div>
            <div className="col-span-2">
              <label className="text-sm font-medium text-gray-700">Email (read-only)</label>
              <input 
                value={form.email} 
                disabled 
                className="w-full border rounded-md px-3 py-2 mt-1 bg-gray-50 text-gray-500 cursor-not-allowed" 
              />
            </div>
          </div>
          
          {profileMessage.text && (
            <p className={`mt-3 text-sm ${profileMessage.type === 'success' ? 'text-green-600' : 'text-red-500'}`}>
              {profileMessage.text}
            </p>
          )}

          <Button 
            onClick={handleSaveProfile} 
            disabled={isSaving}
            className="mt-6"
          >
            {isSaving ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
            Save Changes
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Change Password</CardTitle>
          <CardDescription>Ensure your account is using a long, random password to stay secure.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 max-w-md">
            <div>
              <label className="text-sm font-medium text-gray-700">Current Password</label>
              <input 
                type="password" 
                value={passwords.current} 
                onChange={e => setPasswords({...passwords, current: e.target.value})} 
                className="w-full border rounded-md px-3 py-2 mt-1 focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]" 
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">New Password</label>
              <input 
                type="password" 
                value={passwords.new} 
                onChange={e => setPasswords({...passwords, new: e.target.value})} 
                className="w-full border rounded-md px-3 py-2 mt-1 focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]" 
              />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700">Confirm New Password</label>
              <input 
                type="password" 
                value={passwords.confirm} 
                onChange={e => setPasswords({...passwords, confirm: e.target.value})} 
                className="w-full border rounded-md px-3 py-2 mt-1 focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]" 
              />
            </div>

            {passwordMessage.text && (
              <p className={`text-sm ${passwordMessage.type === 'success' ? 'text-green-600' : 'text-red-500'}`}>
                {passwordMessage.text}
              </p>
            )}

            <Button 
              onClick={handleChangePassword} 
              disabled={isChangingPassword || !passwords.current || !passwords.new || !passwords.confirm}
              className="mt-2"
            >
              {isChangingPassword ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
              Update Password
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
