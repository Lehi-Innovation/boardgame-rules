import { describe, it, expect } from "vitest";
import worker from "../src/index";
import { fakeEnv, FakeKV } from "./helpers";

function adminReq(path: string, token?: string, init?: RequestInit): Request {
  return new Request(`https://worker.test${path}`, {
    ...init,
    headers: {
      ...(init?.headers ?? {}),
      ...(token ? { authorization: `Bearer ${token}` } : {}),
    },
  });
}

describe("admin API", () => {
  it("is disabled without ADMIN_TOKEN", async () => {
    const res = await worker.fetch(adminReq("/admin/export"), fakeEnv({ RULINGS: new FakeKV() }));
    expect(res.status).toBe(503);
  });

  it("rejects bad tokens", async () => {
    const env = fakeEnv({ RULINGS: new FakeKV(), ADMIN_TOKEN: "secret" });
    const res = await worker.fetch(adminReq("/admin/export", "wrong"), env);
    expect(res.status).toBe(401);
  });

  it("501s without the KV binding", async () => {
    const env = fakeEnv({ ADMIN_TOKEN: "secret" });
    const res = await worker.fetch(adminReq("/admin/export", "secret"), env);
    expect(res.status).toBe(501);
  });

  it("exports queued rulings and acks them", async () => {
    const kv = new FakeKV();
    await kv.put("q:2026-08-05T00:00:00.000Z:abc", JSON.stringify({ type: "ruling", slug: "catan" }));
    await kv.put("miss:2026-08-05T00:00:00.000Z:def", JSON.stringify({ query: "Carcassonne" }));
    const env = fakeEnv({ RULINGS: kv, ADMIN_TOKEN: "secret" });

    const res = await worker.fetch(adminReq("/admin/export?kind=rulings", "secret"), env);
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.items.length).toBe(1);
    expect(body.items[0].value.slug).toBe("catan");
    expect(body.complete).toBe(true);

    const misses = await worker.fetch(adminReq("/admin/export?kind=misses", "secret"), env);
    expect((await misses.json()).items[0].value.query).toBe("Carcassonne");

    const ack = await worker.fetch(
      adminReq("/admin/ack", "secret", {
        method: "POST",
        body: JSON.stringify({ keys: [body.items[0].key, "evil:key"] }),
      }),
      env,
    );
    const ackBody = await ack.json();
    expect(ackBody.deleted).toBe(1);
    expect(ackBody.ignored).toBe(1);
    expect(kv.keysWithPrefix("q:").length).toBe(0);
    expect(kv.keysWithPrefix("miss:").length).toBe(1);
  });

  it("rejects unknown export kinds", async () => {
    const env = fakeEnv({ RULINGS: new FakeKV(), ADMIN_TOKEN: "secret" });
    const res = await worker.fetch(adminReq("/admin/export?kind=everything", "secret"), env);
    expect(res.status).toBe(400);
  });
});
