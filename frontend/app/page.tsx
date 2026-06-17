import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col bg-[var(--background)]">
      <header className="sticky top-0 z-50 w-full border-b border-[var(--color-border-custom)] bg-[var(--color-surface)]/80 backdrop-blur">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <span className="text-xl font-bold tracking-tight text-[var(--color-primary)]">
              FlyPermit
            </span>
          </div>
          <nav className="hidden md:flex gap-6">
            <Link href="#features" className="text-sm font-medium text-gray-600 hover:text-[var(--color-primary)] transition-colors">
              Features
            </Link>
            <Link href="#how-it-works" className="text-sm font-medium text-gray-600 hover:text-[var(--color-primary)] transition-colors">
              How it works
            </Link>
          </nav>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost">Log In</Button>
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden pt-24 pb-32">
          <div className="absolute inset-0 bg-gradient-to-b from-[var(--color-primary-light)] to-transparent opacity-50" />
          <div className="container mx-auto px-4 relative z-10 text-center">
            <h1 className="mx-auto max-w-4xl text-5xl font-extrabold tracking-tight sm:text-6xl text-gray-900 mb-6">
              Simplify Your <span className="text-[var(--color-primary)]">Visa Application</span> Process
            </h1>
            <p className="mx-auto max-w-2xl text-lg text-gray-600 mb-10">
              Track requirements, organize documents, and monitor your progress step-by-step.
              Never miss a critical document again.
            </p>
            <div className="flex justify-center gap-4">
              <Link href="/register">
                <Button size="lg" className="rounded-full font-semibold px-8 shadow-lg shadow-[var(--color-primary)]/20">
                  Start Your Journey
                </Button>
              </Link>
              <Link href="#features">
                <Button size="lg" variant="outline" className="rounded-full font-semibold px-8">
                  Learn More
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-24 bg-white">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold text-center mb-16">Why Choose FlyPermit?</h2>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  title: "Smart Checklists",
                  description: "Automatically generated document checklists tailored to your specific visa type and destination.",
                  icon: "✓"
                },
                {
                  title: "Progress Tracking",
                  description: "Visual dashboards to monitor your application progress and missing requirements.",
                  icon: "📊"
                },
                {
                  title: "Secure Storage",
                  description: "Safely organize and store your essential travel documents in one centralized location.",
                  icon: "🔒"
                }
              ].map((feature, i) => (
                <div key={i} className="rounded-2xl border border-[var(--color-border-custom)] p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                  <div className="w-12 h-12 rounded-lg bg-[var(--color-primary-light)] text-[var(--color-primary)] flex items-center justify-center text-2xl mb-6">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                  <p className="text-gray-600">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-[var(--color-border-custom)] bg-white py-12">
        <div className="container mx-auto px-4 text-center text-gray-500">
          <p>© {new Date().getFullYear()} FlyPermit. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
