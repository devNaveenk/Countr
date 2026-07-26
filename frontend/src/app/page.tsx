import Link from "next/link";
import type { SVGProps } from "react";

import { Footer } from "@/components/layout/Footer";
import { NavBar } from "@/components/layout/NavBar";
import {
  BarChartIcon,
  PackageIcon,
  ReceiptIcon,
  ShieldCheckIcon,
} from "@/components/ui/icons";
import { brand } from "@/lib/brand";

const features: {
  title: string;
  body: string;
  Icon: (p: SVGProps<SVGSVGElement>) => React.JSX.Element;
}[] = [
  {
    title: "Fast checkout",
    body: "Scan a barcode, take payment, print a receipt. Built for a busy counter.",
    Icon: ReceiptIcon,
  },
  {
    title: "Live inventory",
    body: "Stock counts update with every sale. Know what's running low before you sell out.",
    Icon: PackageIcon,
  },
  {
    title: "Clear reports",
    body: "See daily sales and best-sellers at a glance — no spreadsheets required.",
    Icon: BarChartIcon,
  },
  {
    title: "Made for the US",
    body: "Sales tax, US payments, and QuickBooks — the things a US store actually needs.",
    Icon: ShieldCheckIcon,
  },
];

const steps = [
  { n: 1, title: "Add your products", body: "Import or scan items into your catalog in minutes." },
  { n: 2, title: "Open the register", body: "Ring up sales on any device — desktop or tablet." },
  { n: 3, title: "Watch it add up", body: "Stock and reports update automatically as you sell." },
];

export default function LandingPage() {
  return (
    <>
      <NavBar />

      <main className="flex-1">
        {/* Hero */}
        <section className="relative overflow-hidden">
          <div
            aria-hidden
            className="pointer-events-none absolute inset-x-0 top-0 h-[420px] bg-gradient-to-b from-green-50 to-transparent"
          />
          <div className="relative mx-auto max-w-6xl px-4 py-20 text-center sm:px-6 sm:py-28">
            <span className="chip">For grocery &amp; convenience stores</span>
            <h1 className="mx-auto mt-6 max-w-3xl text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl">
              Run your store on{" "}
              <span className="text-primary">{brand.name}</span>.
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-600">{brand.tagline}</p>
            <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
              <Link href="/register" className="btn-primary px-6 py-3 text-base">
                Get started free
              </Link>
              <Link href="/login" className="btn-secondary px-6 py-3 text-base">
                Sign in
              </Link>
            </div>
            <p className="mt-4 text-sm text-slate-500">No card required · Set up in minutes</p>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="border-t border-slate-200 bg-white">
          <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6">
            <h2 className="text-center text-3xl font-bold tracking-tight text-slate-900">
              Everything the counter needs
            </h2>
            <p className="mx-auto mt-3 max-w-xl text-center text-slate-600">
              One simple app for the register, the stockroom, and the numbers.
            </p>
            <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {features.map(({ title, body, Icon }) => (
                <div key={title} className="card p-6 transition hover:shadow-md">
                  <span className="grid h-11 w-11 place-items-center rounded-xl bg-primary-soft text-primary">
                    <Icon className="h-6 w-6" />
                  </span>
                  <h3 className="mt-4 text-lg font-semibold text-slate-900">{title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-slate-600">{body}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* How it works */}
        <section id="how" className="mx-auto max-w-6xl px-4 py-20 sm:px-6">
          <h2 className="text-center text-3xl font-bold tracking-tight text-slate-900">
            Up and running in three steps
          </h2>
          <div className="mt-12 grid gap-8 md:grid-cols-3">
            {steps.map((s) => (
              <div key={s.n} className="text-center">
                <div className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-primary text-lg font-bold text-white">
                  {s.n}
                </div>
                <h3 className="mt-4 text-lg font-semibold text-slate-900">{s.title}</h3>
                <p className="mt-2 text-sm text-slate-600">{s.body}</p>
              </div>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section id="pricing" className="bg-primary">
          <div className="mx-auto max-w-4xl px-4 py-16 text-center sm:px-6">
            <h2 className="text-3xl font-bold tracking-tight text-white">
              Ready to simplify your store?
            </h2>
            <p className="mx-auto mt-3 max-w-xl text-green-50">{brand.shortPitch}</p>
            <Link
              href="/register"
              className="mt-8 inline-flex items-center justify-center rounded-lg bg-white px-6 py-3 text-sm font-semibold text-primary shadow-sm transition hover:bg-green-50"
            >
              Create your account
            </Link>
          </div>
        </section>
      </main>

      <Footer />
    </>
  );
}
