import React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "success" | "warning" | "danger" | "outline";
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  const baseStyles = "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2";
  
  const variants = {
    default: "bg-gray-100 text-gray-900",
    success: "bg-[var(--color-success)] text-white",
    warning: "bg-[var(--color-warning)] text-white",
    danger: "bg-[var(--color-danger)] text-white",
    outline: "text-gray-900 border border-gray-200",
  };

  return (
    <div className={cn(baseStyles, variants[variant], className)} {...props} />
  );
}
