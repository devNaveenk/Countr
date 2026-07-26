import Link from "next/link";

import { Footer } from "@/components/layout/Footer";
import { NavBar } from "@/components/layout/NavBar";
import { brand } from "@/lib/brand";

const features = [
  {
    title: "Fast checkout",
    body: "Scan a barcode, take payment, print a receipt. Built for a busy counter.",
    icon: "🧾",
  },
  {
    title: "Live inventory",
    body: "Stock counts update with every sale. Know what's running low before you sell out.",
    icon: "📦",
  },
  {
    title: "Clear reports",
    body: "See daily sales and best-sellers at a glance — no spreadsheets required.",
    icon: "📊",
  },
  {
    title: "Made for the US",
    body: "Sales tax, US payments, and QuickBooks — the things a US store actually needs.",
    icon: "🇺🇸",
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
        <section className="mx-auto max-w-6xl px-4 py-20 text-center sm:px-6 sm:py-28">
          <span className="inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
            For grocery &amp; convenience stores
          </span>
          <h1 className="mx-auto mt-6 max-w-3xl text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl">
            Run your store on <span className="text-emerald-600">{brand.name}</span>.
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-600">{brand.tagline}</p>
          <div className="mt-10 flex items-center justify-center gap-4">
            <Link
              href="/register"
              className="rounded-lg bg-emerald-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-emerald-700"
            >
              Get started free
            </Link>
            <Link
              href="/login"
              className="rounded-lg border border-slate-300 px-6 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
            >
              Sign in
            </Link>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="border-t border-slate-200 bg-slate-50">
          <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6">
            <h2 className="text-center text-3xl font-bold tracking-tight text-slate-900">
              Everything the counter needs
            </h2>
            <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {features.map((f) => (
                <div
                  key={f.title}
                  className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
                >
                  <div className="text-3xl" aria-hidden>
                    {f.icon}
                  </div>
                  <h3 className="mt-4 text-lg font-semibold text-slate-900">{f.title}</h3>
                  <p className="mt-2 text-sm text-slate-600">{f.body}</p>
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
                <div className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-emerald-600 text-lg font-bold text-white">
                  {s.n}
                </div>
                <h3 className="mt-4 text-lg font-semibold text-slate-900">{s.title}</h3>
                <p className="mt-2 text-sm text-slate-600">{s.body}</p>
              </div>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section id="pricing" className="border-t border-slate-200 bg-emerald-600">
          <div className="mx-auto max-w-4xl px-4 py-16 text-center sm:px-6">
            <h2 className="text-3xl font-bold tracking-tight text-white">
              Ready to simplify your store?
            </h2>
            <p className="mx-auto mt-3 max-w-xl text-emerald-50">{brand.shortPitch}</p>
            <Link
              href="/register"
              className="mt-8 inline-block rounded-lg bg-white px-6 py-3 text-sm font-semibold text-emerald-700 shadow-sm hover:bg-emerald-50"
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
