/**
 * Centralized brand config (see ADR-0007 / ADR-0008).
 *
 * Product name is provisional ("Countr") and lives in ONE place so a rename is cheap.
 * Countr has its own identity; BallotDA appears only as a light parent endorsement — we do
 * NOT reuse BallotDA's election branding here.
 */
export const brand = {
  name: "Countr",
  vendor: "BallotDA",
  tagline: "The point-of-sale and inventory system built for neighborhood stores.",
  shortPitch:
    "Ring up sales, track stock, and see how your store is doing — all in one simple app.",
} as const;
