import Link from "next/link";

import { brand } from "@/lib/brand";

const columns = [
  {
    title: "Product",
    links: [
      { label: "Features", href: "#features" },
      { label: "Pricing", href: "#pricing" },
      { label: "How it works", href: "#how" },
    ],
  },
  {
    title: "Company",
    links: [
      { label: "About", href: "#" },
      { label: "Contact", href: "#" },
      { label: "Blog", href: "#" },
    ],
  },
  {
    title: "Legal",
    links: [
      { label: "Privacy", href: "#" },
      { label: "Terms", href: "#" },
    ],
  },
];

export function Footer() {
  return (
    <footer className="mt-auto border-t border-slate-200 bg-slate-50">
      <div className="mx-auto grid max-w-6xl gap-8 px-4 py-12 sm:px-6 md:grid-cols-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="grid h-8 w-8 place-items-center rounded-lg bg-emerald-600 font-bold text-white">
              C
            </span>
            <span className="text-lg font-semibold text-slate-900">{brand.name}</span>
          </div>
          <p className="mt-3 max-w-xs text-sm text-slate-500">{brand.shortPitch}</p>
        </div>

        {columns.map((col) => (
          <div key={col.title}>
            <h3 className="text-sm font-semibold text-slate-900">{col.title}</h3>
            <ul className="mt-3 space-y-2 text-sm text-slate-500">
              {col.links.map((link) => (
                <li key={link.label}>
                  <Link href={link.href} className="hover:text-slate-900">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className="border-t border-slate-200">
        <div className="mx-auto max-w-6xl px-4 py-6 text-sm text-slate-500 sm:px-6">
          © {new Date().getFullYear()} {brand.name} — a {brand.vendor} product. All rights
          reserved.
        </div>
      </div>
    </footer>
  );
}
