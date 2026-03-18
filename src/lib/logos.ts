export interface LogoRect {
  x: number;
  y: number;
  w: number;
  h: number;
  role: "body" | "face" | "dark";
}

export interface ColorScheme {
  name: string;
  description: string;
  body: string;
  face: string;
  dark: string;
  glow: string;
}

// Toro shape — 16x16 viewBox, ~20 rects
export const toroShape: LogoRect[] = [
  // Corna
  { x: 0, y: 2, w: 2, h: 2, role: "body" },
  { x: 2, y: 4, w: 2, h: 2, role: "body" },
  { x: 14, y: 2, w: 2, h: 2, role: "body" },
  { x: 12, y: 4, w: 2, h: 2, role: "body" },
  // Guance
  { x: 2, y: 6, w: 2, h: 2, role: "body" },
  { x: 12, y: 6, w: 2, h: 2, role: "body" },
  // Fronte
  { x: 4, y: 4, w: 8, h: 2, role: "body" },
  // Lati occhi
  { x: 4, y: 6, w: 2, h: 4, role: "body" },
  { x: 10, y: 6, w: 2, h: 4, role: "body" },
  // Faccia
  { x: 6, y: 6, w: 4, h: 4, role: "face" },
  // Occhi
  { x: 5, y: 7, w: 2, h: 2, role: "dark" },
  { x: 9, y: 7, w: 2, h: 2, role: "dark" },
  // Mascella
  { x: 4, y: 10, w: 8, h: 2, role: "body" },
  // Muso
  { x: 6, y: 12, w: 4, h: 2, role: "body" },
  // Naso
  { x: 7, y: 13, w: 2, h: 1, role: "body" },
  // Mento
  { x: 6, y: 14, w: 1, h: 1, role: "body" },
  { x: 9, y: 14, w: 1, h: 1, role: "body" },
];

// Indices in toroShape of the eye rects (for blink)
export const eyeIndices: number[] = [10, 11];

// Brand terracotta palette
export const brandScheme: ColorScheme = {
  name: "brand",
  description: "Terracotta — palette principale",
  body: "#c47a5a",
  face: "#9a5030",
  dark: "#2a1a12",
  glow: "#c47a5a",
};

// Green retro palette
export const greenScheme: ColorScheme = {
  name: "green",
  description: "Green retro — terminale fosforescente",
  body: "#33FF33",
  face: "#1a8c1a",
  dark: "#0a0a0a",
  glow: "#33FF33",
};

export const allSchemes: ColorScheme[] = [brandScheme, greenScheme];

// Semantic build groups — anatomical entrance order
export const buildGroups: number[][] = [
  [0, 1, 2, 3],        // Corna
  [4, 5, 6],           // Guance + Fronte
  [7, 8, 9],           // Lati occhi + Faccia
  [10, 11],            // Occhi
  [12, 13],            // Mascella + Muso
  [14, 15, 16],        // Naso + Mento
];
