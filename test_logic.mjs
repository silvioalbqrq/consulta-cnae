import test from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const L = require("./logic.js");

const row = (cnae, x) => ({ cnae, x });

test("extrai CNAE no formato com barra (padrão da tabela)", () => {
  assert.deepEqual(L.extractCnaes("6201-5/01").map(c => c.raw), ["6201501"]);
  assert.deepEqual(L.extractCnaes("47.11-3-01").map(c => c.raw), ["4711301"]);
  assert.deepEqual(L.extractCnaes("4711301").map(c => c.raw), ["4711301"]);
});

test("extrai vários códigos e ignora CNPJ/telefone", () => {
  const txt = "66.576.500/0001-84 60.035-130 (85) 8416-3096 45.30-7-05";
  assert.deepEqual(L.extractCnaes(txt).map(c => c.raw), ["4530705"]);
});

test("rateFor respeita o teto de R$ 4,8 mi e o piso zero", () => {
  assert.equal(L.rateFor("III", 5000000), null);
  assert.equal(L.rateFor("III", 0).ef, 0);
  assert.ok(Math.abs(L.rateFor("III", 4800000).ef - 19.5) < 0.01);
});

test("veredito de código desconhecido é inconclusivo", () => {
  const v = L.verdictFor([row("9999999", undefined)]);
  assert.equal(v.cls, "warn");
  assert.match(v.txt, /INCONCLUSIVO/);
  assert.match(v.meiTxt, /não confirmado/);
});

test("MEI só é confirmado com uma única atividade", () => {
  const mei = { status: "OPTANTE", anexos: "I", fatorR: "NAO", mei: "SIM" };
  const one = L.verdictFor([row("0121101", mei)]);
  assert.match(one.meiTxt, /PODE SER MEI/);
  const two = L.verdictFor([row("0121101", mei), row("0159801", mei)]);
  assert.doesNotMatch(two.meiTxt, /PODE SER MEI/);
  assert.match(two.meiTxt, /única ocupação/);
});

test("vedado impede a opção; vedado a validar pede confirmação", () => {
  const v = L.verdictFor([row("3513100", { status: "VEDADO", anexos: "", fatorR: "NAO", mei: "" })]);
  assert.equal(v.cls, "no");
  assert.match(v.txt, /IMPEDIDA/);
  const rev = L.verdictFor([row("3511500", { status: "VEDADO", anexos: "", fatorR: "NAO", mei: "", revisar: true })]);
  assert.equal(rev.cls, "warn");
  assert.match(rev.txt, /A CONFIRMAR/);
});

test("ambíguo sem anexo definido não vira Anexo V", () => {
  const v = L.verdictFor([row("8430200", { status: "AMBIGUO", anexos: "?", fatorR: "NAO", mei: "" })]);
  assert.equal(v.cls, "warn");
  assert.match(v.txt, /sem anexo definido/);
  assert.doesNotMatch(v.txt, /Anexo V/);
});

test("código 2.2 desativado e optante a validar pedem confirmação", () => {
  const des = L.verdictFor([row("1610201", { status: "DESATIVADA", anexos: "", fatorR: "NAO", mei: "" })]);
  assert.equal(des.cls, "warn");
  assert.match(des.txt, /DESATIVADO/);
  const rev = L.verdictFor([row("8512100", { status: "OPTANTE", anexos: "III", fatorR: "NAO", mei: "", revisar: true })]);
  assert.equal(rev.cls, "warn");
  assert.match(rev.txt, /VALIDAR/);
});
