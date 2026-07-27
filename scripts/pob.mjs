#!/usr/bin/env node
/**
 * Drive pob-mcp over stdio and run a sequence of tool calls.
 *
 * Usage: node scripts/pob.mjs calls.json
 * calls.json = [{ "name": "lua_start", "arguments": {} }, ...]
 */
import { spawn } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const calls = JSON.parse(readFileSync(process.argv[2], "utf8"));

const proc = spawn("node", [`${root}/vendor/pob-mcp/build/index.js`], {
  env: {
    ...process.env,
    PATH: `${process.env.HOME}/.local/bin:${process.env.PATH}`,
    POB_DIRECTORY: `${root}/builds`,
    POB_LUA_ENABLED: "true",
    POB_PATH: `${root}/vendor/PathOfBuilding/src`,
    POB_CMD: `${process.env.HOME}/.local/bin/luajit`,
    POB_TIMEOUT_MS: "120000",
    POE_TRADE_ENABLED: "true",
    // PoB's pure-Lua deps live in runtime/lua; luautf8 is a locally built C module.
    LUA_PATH: [
      `${root}/vendor/PathOfBuilding/runtime/lua/?.lua`,
      `${root}/vendor/PathOfBuilding/runtime/lua/?/init.lua`,
      `${root}/vendor/PathOfBuilding/src/?.lua`,
      "",
      "",
    ].join(";"),
    LUA_CPATH: `${process.env.HOME}/.local/lib/?.so;;`,
  },
  stdio: ["pipe", "pipe", "pipe"],
});

let buffer = "";
const pending = new Map();

proc.stdout.on("data", (chunk) => {
  buffer += chunk;
  let idx;
  while ((idx = buffer.indexOf("\n")) >= 0) {
    const line = buffer.slice(0, idx).trim();
    buffer = buffer.slice(idx + 1);
    if (!line) continue;
    let msg;
    try {
      msg = JSON.parse(line);
    } catch {
      continue;
    }
    const resolver = pending.get(msg.id);
    if (resolver) {
      pending.delete(msg.id);
      resolver(msg);
    }
  }
});
proc.stderr.on("data", (d) => process.stderr.write(`[pob] ${d}`));

let nextId = 1;
function send(method, params) {
  const id = nextId++;
  return new Promise((res, rej) => {
    pending.set(id, res);
    proc.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", id, method, params })}\n`);
    setTimeout(() => rej(new Error(`timeout: ${method} ${params?.name ?? ""}`)), 180000);
  });
}

await send("initialize", {
  protocolVersion: "2024-11-05",
  capabilities: {},
  clientInfo: { name: "pob-driver", version: "1.0" },
});

for (const call of calls) {
  const label = `=== ${call.name} ${JSON.stringify(call.arguments ?? {}).slice(0, 160)}`;
  console.log(`\n${label}`);
  try {
    const res = await send("tools/call", { name: call.name, arguments: call.arguments ?? {} });
    const text = res.result?.content?.map((c) => c.text).join("\n") ?? JSON.stringify(res.error ?? res);
    console.log(text);
  } catch (err) {
    console.log(`ERROR: ${err.message}`);
  }
}

proc.kill();
process.exit(0);
