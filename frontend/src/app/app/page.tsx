"use client";

import Link from "next/link";
import type { SVGProps } from "react";

import {
  BarChartIcon,
  CartIcon,
  InboxIcon,
  PackageIcon,
  ReceiptIcon,
} from "@/components/ui/icons";
import { useCurrentUser } from "@/features/auth/user-context";

type Module = {
  key: string;
  title: string;
  body: string;
  Icon: (p: SVGProps<SVGSVGElement>) => React.JSX.Element;
  href?: string; // set when the module is live
};

const modules: Module[] = [
  { key: "pos", title: "Point of Sale", body: "Ring up a sale", Icon: ReceiptIcon, href: "/app/pos" },
  {
    key: "catalog",
    title: "Products",
    body: "Manage your catalog",
    Icon: PackageIcon,
    href: "/app/products",
  },
  {
    key: "reports",
    title: "Reports",
    body: "Sales & best-sellers",
    Icon: BarChartIcon,
    href: "/app/reports",
  },
  { key: "buy", title: "Buy", body: "Purchase & receive stock", Icon: CartIcon, href: "/app/buy" },
  {
    key: "inventory",
    title: "Inventory",
    body: "Track stock levels",
    Icon: InboxIcon,
    href: "/app/inventory",
  },
];

function ModuleCard({ title, body, Icon, href }: Module) {
  const inner = (
    <>
      <span className="grid h-11 w-11 place-items-center rounded-xl bg-primary-soft text-primary">
        <Icon className="h-6 w-6" />
      </span>
      <h2 className="mt-4 font-semibold text-slate-900">{title}</h2>
      <p className="mt-1 text-sm text-slate-600">{body}</p>
      {href ? (
        <span className="mt-4 inline-block text-sm font-medium text-primary">Open →</span>
      ) : (
        <span className="mt-4 inline-block rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-500">
          Coming soon
        </span>
      )}
    </>
  );

  return href ? (
    <Link href={href} className="card p-6 transition hover:shadow-md">
      {inner}
    </Link>
  ) : (
    <div className="card p-6 opacity-90">{inner}</div>
  );
}

export default function AppPage() {
  const user = useCurrentUser();

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6">
      <h1 className="text-2xl font-bold tracking-tight text-slate-900">
        Welcome, {user?.full_name?.split(" ")[0]} 👋
      </h1>
      <p className="mt-1 text-slate-600">
        This is your store workspace. Start with Products, then Sell.
      </p>

      <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {modules.map(({ key, ...m }) => (
          <ModuleCard key={key} {...m} />
        ))}
      </div>
    </div>
  );
}
