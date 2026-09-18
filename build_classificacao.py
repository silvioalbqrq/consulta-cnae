import json, re, csv

base = json.load(open('simples-nacional-prototipo/cnaes.json', encoding='utf-8'))
byId = {b['id']: b for b in base}
anexo = json.load(open('simples-nacional-prototipo/anexo_subclasses23.json', encoding='utf-8'))

MAP = {
"0111301":{"a":["I"]},"4511101":{"a":["I"]},"4511102":{"a":["I"]},"4511103":{"a":["I"]},
"4512901":{"a":["V"],"fatorR":True},"4530702":{"a":["I"]},"4530703":{"a":["I"]},"4530704":{"a":["I"]},"4530705":{"a":["I"]},
"4530706":{"a":["V"],"fatorR":True},"4541202":{"a":["I"]},"4541206":{"a":["I"]},"4541207":{"a":["I"]},"4542101":{"a":["V"],"fatorR":True},
"4611700":{"a":["V"],"fatorR":True},"4612500":{"a":["V"],"fatorR":True},"4613300":{"a":["V"],"fatorR":True},"4614100":{"a":["V"],"fatorR":True},
"4615000":{"a":["V"],"fatorR":True},"4616800":{"a":["V"],"fatorR":True},"4617600":{"a":["V"],"fatorR":True},
"4618401":{"a":["V"],"fatorR":True},"4618402":{"a":["V"],"fatorR":True},"4619200":{"a":["V"],"fatorR":True},
"4711301":{"a":["I"]},"4711302":{"a":["I"]},"4721102":{"a":["I"]},
"4723700":{"a":["I"]},"4751201":{"a":["I"]},"4751202":{"a":["III"]},
"5611201":{"a":["I"]},"5611203":{"a":["I"]},"5611204":{"a":["I"]},"5620102":{"a":["III"]},
"5811500":{"a":["III"]},"5821200":{"a":["V"],"fatorR":True},"5911101":{"a":["III"]},
"6201501":{"a":["V"],"fatorR":True},"6202300":{"a":["III"]},"6203100":{"a":["V"],"fatorR":True},"6204000":{"a":["V"],"fatorR":True},
"6209100":{"a":["V"],"fatorR":True},"6311900":{"a":["V"],"fatorR":True},"6319400":{"a":["V"],"fatorR":True},
"6619302":{"a":["III"]},"6621501":{"a":["V"],"fatorR":True},"6622300":{"a":["III"]},
"6810201":{"a":["III"]},"6821801":{"a":["III"],"fatorR":True},"6911701":{"a":["IV"]},
"6920601":{"a":["III"]},"7020400":{"a":["V"],"fatorR":True},
"7111100":{"a":["III"],"fatorR":True},"7112000":{"a":["V"],"fatorR":True},"7311400":{"a":["V"],"fatorR":True},"7320300":{"a":["V"],"fatorR":True},
"7410202":{"a":["IV","V"],"fatorR":True},"7410203":{"a":["V"],"fatorR":True},"7420001":{"a":["V"],"fatorR":True},"7490101":{"a":["V"],"fatorR":True},
"7500100":{"a":["III"]},"7711000":{"a":["III"]},"7739099":{"a":["III"]},
"7810800":{"vedado":True},"7820500":{"vedado":True},"7830200":{"vedado":True},
"8011101":{"a":["IV"]},"8121400":{"a":["IV"]},"8111700":{"a":["IV"]},"8211300":{"a":["III"]},
"8299799":{"a":["V"],"fatorR":True},"8511200":{"a":["III"]},"8531700":{"a":["V"],"fatorR":True},
"8541400":{"a":["III"]},"8599604":{"a":["III"]},"8599699":{"a":["III"]},
"8610101":{"a":["III"]},"8630501":{"a":["III"]},"8630503":{"a":["III"]},"8630504":{"a":["III"],"fatorR":True},
"8640201":{"a":["V"],"fatorR":True},"8640202":{"a":["V"],"fatorR":True},"8640204":{"a":["V"],"fatorR":True},
"8640205":{"a":["V"],"fatorR":True},"8640206":{"a":["III","V"],"fatorR":True},"8640207":{"a":["III","V"],"fatorR":True},
"8640208":{"a":["III","V"],"fatorR":True},"8640209":{"a":["III","V"],"fatorR":True},"8640210":{"a":["III"],"fatorR":True},
"8650007":{"a":["V"],"fatorR":True},"8690901":{"a":["III"]},
"9001999":{"a":["III"]},"9313100":{"a":["III"]},"9329804":{"a":["III"]},
"9501180":{"a":["III"]},"9602501":{"a":["III"]},
"3513100":{"vedado":True},"3511500":{"vedado":True},"3512300":{"vedado":True},"3520400":{"vedado":True},
"6010100":{"vedado":True},"6021700":{"vedado":True},
"6410700":{"vedado":True},"6421200":{"vedado":True},"6422100":{"vedado":True},"6431000":{"vedado":True},
"6450600":{"vedado":True},"6470100":{"vedado":True},"6630400":{"vedado":True},
"1220401":{"vedado":True},"2092700":{"vedado":True},
"8411160":{"vedado":True},"9420100":{"vedado":True},"9491000":{"vedado":True},"9492800":{"vedado":True},
}
VED_PREFIX = ("6410","6421","6422","6423","6424","6431","6432","6433","6434","6435","6440","6450","6470","6630",
"8411","8412","8413","8421","8422","8423","8424","8425","9420","9430","9491","9492","9493","9499",
"1220","2092","6010","6021")

def enquadrar(cid, div, desc):
    m = MAP.get(cid)
    if m:
        if m.get("vedado"):
            return False, [], False, "Curadoria: vedação art.17", "curadoria"
        return True, m["a"], bool(m.get("fatorR")), "Curadoria tabela 2026", "curadoria"
    if any(cid.startswith(p) for p in VED_PREFIX):
        return False, [], False, "Prefixo com vedação típica art.17 (financeiro/adm.pública/associativo/fumo/explosivos/rádio/TV)", "regra"
    d2 = (div or "")[:2]
    U = (desc or "").upper()
    if d2 in ("49","50","51") and ("PASSAGEIR" in U or "COLETIVO" in U) and ("INTERMUNICIPAL" in U or "INTERESTADUAL" in U or "INTERNACIONAL" in U):
        return False, [], False, "Transporte intermunicipal/interestadual/internacional de passageiros — vedado", "regra"
    try:
        dn = int(d2)
    except:
        dn = 0
    if 1 <= dn <= 3:
        return True, ["I"], False, "Agro/pecuária/pesca — Anexo I (ou II se industrializar)", "regra"
    if 5 <= dn <= 33:
        if cid.startswith("25501") or cid.startswith("20924") or cid.startswith("12204") or cid.startswith("11119") or cid.startswith("11135"):
            return False, [], False, "Industrial com vedação potencial (armas/explosivos/fumo/bebidas em escala) — validar", "regra"
        return True, ["II"], False, "Indústria — Anexo II", "regra"
    if d2 == "35":
        return False, [], False, "Energia/gás — verificar vedação (ex: 3513-1/00 vedado)", "regra"
    if d2 in ("36","37","38","39"):
        return True, ["III"], False, "Saneamento/resíduos — Anexo III", "regra"
    if 41 <= dn <= 43:
        if cid.startswith("433") or cid.startswith("43991"):
            return True, ["III"], False, "Obras de acabamento/serviços — Anexo III", "regra"
        return True, ["IV"], False, "Construção — Anexo IV (CPP fora do DAS)", "regra"
    if 45 <= dn <= 47:
        if re.match(r"^(45129|4530706|4542101|461)", cid):
            return True, ["V"], True, "Representação/intermediação — Anexo V, pode ir ao III com Fator R", "regra"
        return True, ["I"], False, "Comércio — Anexo I", "regra"
    if 49 <= dn <= 53:
        return True, ["III"], False, "Transporte municipal/cargas/logística — Anexo III", "regra"
    if d2 == "55":
        return True, ["III"], False, "Alojamento — Anexo III", "regra"
    if d2 == "56":
        return True, ["I"], False, "Alimentação (bares/restaurantes) — Anexo I", "regra"
    if d2 in ("58","59","60","61","62","63"):
        if re.match(r"^(62015|62031|62040|62091|63119|63194|62012|58212)", cid):
            return True, ["V"], True, "TI/software — V (15,5%), pode ir ao III (6%) com Fator R", "regra"
        return True, ["III"], False, "Comunicação/TI operacional — Anexo III", "regra"
    if d2 in ("64","65","66"):
        return False, [], False, "Financeiro/seguros — em geral vedado, exceto 6619-3/02 e 6622-3/00", "regra"
    if d2 == "68":
        return True, ["III"], False, "Imobiliárias — Anexo III", "regra"
    if d2 == "69":
        if cid.startswith("69117"):
            return True, ["IV"], False, "Advocacia — Anexo IV", "regra"
        return True, ["III"], False, "Contabilidade e afins — Anexo III", "regra"
    if d2 in ("70","71","72","73","74","75"):
        return True, ["V"], True, "Serviço intelectual/técnico — V, pode ir ao III com Fator R", "regra"
    if d2 in ("77","78","79","80","81","82"):
        if re.match(r"^(78108|78205|78302)", cid):
            return False, [], False, "Cessão de mão de obra — vedado", "regra"
        if re.match(r"^(80111|81214|81117|81290)", cid):
            return True, ["IV"], False, "Vigilância/limpeza — Anexo IV", "regra"
        return True, ["III"], False, "Serviços de apoio — Anexo III", "regra"
    if d2 == "85":
        return True, ["III"], False, "Educação — Anexo III (superior pode cair em V, validar)", "regra"
    if d2 == "86":
        return True, ["V"], True, "Saúde — V com Fator R (pode ir ao III)", "regra"
    if d2 in ("87","88","90","91","92","93","95","96"):
        if d2 == "92":
            return False, [], False, "Jogos de azar/apostas — vedado na prática", "regra"
        return True, ["III"], False, "Serviços pessoais/cultura/esporte/reparação — Anexo III", "regra"
    if d2 == "94":
        return False, [], False, "Entidades associativas — vedado", "regra"
    if d2 in ("97","99"):
        return False, [], False, "Serviços domésticos/organismos internacionais — vedado", "regra"
    return True, ["?"], False, "Sem regra específica — validar art.17/18", "regra"

def digits(s):
    return re.sub(r"\D", "", s)

out = []
for a in anexo:
    cid = digits(a["cnae"])
    b = byId.get(cid, {})
    div = b.get("div", "")
    desc = a["desc"]
    perm, anexos, fr, motivo, origem = enquadrar(cid, div, desc)
    if not perm:
        status = "VEDADO"
    elif fr or len(anexos) > 1 or "?" in anexos:
        status = "AMBIGUO"
    else:
        status = "OPTANTE"
    out.append({
        "cnae": a["cnae"], "id": cid, "descricao": desc, "divisao": div,
        "status": status, "anexos": ",".join(anexos),
        "fatorR": "SIM" if fr else "NAO",
        "motivo": motivo, "origem": origem,
    })

json.dump(out, open("simples-nacional-prototipo/classificacao_simples_23.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open("simples-nacional-prototipo/classificacao_simples_23.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["cnae","id","descricao","divisao","status","anexos","fatorR","motivo","origem"])
    w.writeheader()
    w.writerows(out)

from collections import Counter
c = Counter(x["status"] for x in out)
print("TOTAL", len(out), dict(c))
print("VEDADOS:", sum(1 for x in out if x["status"]=="VEDADO"))
print("AMBIGUOS:", sum(1 for x in out if x["status"]=="AMBIGUO"))
# top divisoes vedadas
vd = Counter(x["divisao"] for x in out if x["status"]=="VEDADO")
print("ved por divisao", vd.most_common(12))
am = Counter(x["divisao"] for x in out if x["status"]=="AMBIGUO")
print("amb por divisao", am.most_common(12))
# exemplos
for x in out:
    if x["cnae"] in ("4723-7/00","6201-5/01","6911-7/01","3513-1/00","7810-8/00"):
        print(x)
