/**
 * Fluid Memory Sync Hook
 * Automatically syncs conversation to Fluid Memory when messages are sent
 */

import { spawn } from "child_process";
import path from "path";
import fs from "fs";
import os from "os";

// Path to fluid_skill.py
const FLUID_SKILL_PATH = path.join(
  path.dirname(process.execPath),
  "..",
  "..",
  "..",
  "..",
  "..",
  ".openclaw",
  "workspace",
  "skills",
  "fluid-memory",
  "fluid_skill.py"
);

// Alternative: try to find in user home
const USER_HOME = os.homedir();
const ALT_FLUID_SKILL_PATH = path.join(
  USER_HOME,
  ".openclaw",
  "workspace",
  "skills",
  "fluid-memory",
  "fluid_skill.py"
);

function getPythonPath() {
  // Try common Python paths on Windows
  const candidates = [
    "python",
    "python3",
    path.join(USER_HOME, "miniconda3", "python.exe"),
    path.join(USER_HOME, "AppData", "Local", "Programs", "Python", "python.exe"),
  ];
  
  for (const candidate of candidates) {
    try {
      // Just return the first available one
      return candidate;
    } catch (e) {
      continue;
    }
  }
  return "python";
}

function runFluidSkill(args) {
  return new Promise((resolve, reject) => {
    const pythonPath = getPythonPath();
    const scriptPath = fs.existsSync(FLUID_SKILL_PATH) 
      ? FLUID_SKILL_PATH 
      : ALT_FLUID_SKILL_PATH;
    
    if (!fs.existsSync(scriptPath)) {
      console.error("[fluid-memory-sync] Skill not found at:", scriptPath);
      reject(new Error("Fluid Memory skill not found"));
      return;
    }

    const proc = spawn(pythonPath, [scriptPath, ...args], {
      stdio: ["ignore", "pipe", "pipe"],
      windowsHide: true,
    });

    let stdout = "";
    let stderr = "";

    proc.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    proc.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    proc.on("close", (code) => {
      if (code === 0) {
        resolve(stdout.trim());
      } else {
        console.error("[fluid-memory-sync] Error:", stderr);
        reject(new Error(`Exit code: ${code}`));
      }
    });
  });
}

export default async function handler(event) {
  // Only handle message:sent events
  if (event.type !== "message" || event.action !== "sent") {
    return;
  }

  // Skip if no content
  if (!event.content) {
    return;
  }

  try {
    // Format: "用户说: xxx | 我说: yyy"
    const conversation = `用户说: ${event.content}`;
    
    console.log("[fluid-memory-sync] Syncing conversation to Fluid Memory...");
    
    const result = await runFluidSkill([
      "increment_summarize",
      "--conversation",
      conversation,
    ]);

    console.log("[fluid-memory-sync] Result:", result);
    
    // Parse result to check if it was stored or buffered
    try {
      const parsed = JSON.parse(result);
      if (parsed.status === "stored") {
        console.log("[fluid-memory-sync] ✅ Memory stored to vector DB!");
      } else if (parsed.status === "buffering") {
        console.log(`[fluid-memory-sync] ⏳ Buffering (${parsed.rounds})`);
      }
    } catch (e) {
      // Result might not be JSON, ignore
    }
  } catch (error) {
    console.error("[fluid-memory-sync] Failed to sync:", error.message);
  }
}
