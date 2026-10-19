#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成英文技术文章（Insights）

目的：覆盖海外工程师/采购的长尾搜索词（材质等效、探伤标准、锻造 vs 铸造等），
这是 B2B 站点获取自然流量的主力方式。

产出：
  en/insights.html                 文章列表页
  en/insights/*.html               4 篇技术文章
并在 en/products.html、en/tech.html 注入「Further Reading」内链区块。
"""
import os, io, re, json
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
EN = os.path.join(HERE, "en")
OUT = os.path.join(EN, "insights")
SITE = "https://www.lxshengda.com"
TODAY = "2026-10-18"

ARTICLES = [
{
 "slug": "h13-vs-1-2344-vs-skd61",
 "title": "H13 vs 1.2344 vs SKD61: One Steel, Three Names",
 "seo_title": "H13 vs 1.2344 vs SKD61 | Grade Equivalence Guide",
 "desc": "H13, 1.2344 (X40CrMoV5-1) and SKD61 are the same hot-work die steel family — but not identical. Composition ranges, delivery hardness and how to specify on a PO.",
 "h1": "H13 vs 1.2344 vs SKD61: One Steel, Three Names — and Where They Differ",
 "lead": "A buyer in Germany writes 1.2344 on the drawing, a toolmaker in Japan writes SKD61, and a Chinese mill quotes H13. All three are the same chromium-molybdenum-vanadium hot-work die steel family. That does not mean the certificates will match. Here is what actually differs, and how to write the requirement so nobody argues after delivery.",
 "body": """
<h2>Why three names for one steel</h2>
<p>Each standard system names tool steels by its own logic. The American AISI system uses a letter group plus a number — H for hot-work, 13 for the specific grade. The German DIN/EN system uses a material number plus a short symbol: <strong>1.2344</strong>, symbol X40CrMoV5-1, which spells out roughly 0.40 % carbon, chromium, molybdenum, vanadium, 5 % chromium, 1 % vanadium. The Japanese JIS system uses SKD61 for the same family. China's GB/T 1299 calls it <strong>4Cr5MoSiV1</strong>.</p>
<p>They all sit in the 5 % Cr hot-work family, hardened and tempered to roughly 48–52 HRC in service, and used for die casting dies, hot forging dies, extrusion tooling and mandrels. In day-to-day trade the names are used interchangeably. Technically, they are <em>near-equivalent</em>, not identical.</p>

<h2>Typical composition ranges side by side</h2>
<table class="art-table">
<thead><tr><th>Element (%)</th><th>AISI H13</th><th>DIN 1.2344</th><th>JIS SKD61</th><th>GB 4Cr5MoSiV1</th></tr></thead>
<tbody>
<tr><td>C</td><td>0.32–0.45</td><td>0.35–0.42</td><td>0.35–0.42</td><td>0.32–0.42</td></tr>
<tr><td>Si</td><td>0.80–1.25</td><td>0.80–1.20</td><td>0.80–1.20</td><td>0.80–1.20</td></tr>
<tr><td>Mn</td><td>0.20–0.60</td><td>0.25–0.50</td><td>0.30–0.50</td><td>0.20–0.50</td></tr>
<tr><td>Cr</td><td>4.75–5.50</td><td>4.80–5.50</td><td>4.80–5.50</td><td>4.75–5.50</td></tr>
<tr><td>Mo</td><td>1.10–1.75</td><td>1.20–1.50</td><td>1.00–1.50</td><td>1.10–1.75</td></tr>
<tr><td>V</td><td>0.80–1.20</td><td>0.85–1.15</td><td>0.80–1.20</td><td>0.80–1.20</td></tr>
</tbody>
</table>
<p class="art-note">Ranges are typical values from the respective standards; always compare against the actual mill certificate rather than the grade designation.</p>
<p>Read the table carefully and you see the point: the ranges overlap heavily but the windows are not the same. A heat at 0.45 % C sits inside AISI H13 but outside 1.2344. A heat at 1.70 % Mo is legal H13 and legal 4Cr5MoSiV1, but outside the 1.2344 window. Both differences are small in service, and both are enough to fail an incoming inspection written against the wrong standard.</p>

<h2>What actually differs in practice</h2>
<h3>1. Delivery condition</h3>
<p>The grade name says nothing about how the steel arrives. H13 is normally supplied annealed at 180–235 HBW, but pre-hardened stock (around 38–42 HRC) is also sold under the same name. If your machining plan assumes annealed stock, write the hardness range on the purchase order, not just the grade.</p>

<h3>2. Micro-cleanliness and microstructure</h3>
<p>Two heats of identical chemistry can behave completely differently in a die cavity. What matters is inclusion content, banding, carbide distribution and grain size. These are controlled by melting route (EAF + VD, or ESR for critical tooling) and by the rating standard you specify — for tool steels the usual ones are <strong>NADCA #207</strong> (North American Die Casting Association), <strong>SEP 1614</strong> (German, microscopic inclusion rating) and <strong>VDG ASA</strong> (German foundry guideline for die casting dies). A mill certificate that shows chemistry and hardness but no micro-cleanliness rating is only telling you half the story.</p>

<h3>3. Ultrasonic quality class</h3>
<p>For large blocks and die holders, internal soundness matters as much as chemistry. UT is specified separately — see our <a href="ut-acceptance-criteria-forgings.html">guide to specifying UT acceptance criteria</a>, where GB/T 6402, ASTM A388 and EN 10228-3 are compared.</p>

<h3>4. Which "H13" you are actually buying</h3>
<p>In China, "H13" is used loosely for both the GB/T 1299 grade 4Cr5MoSiV1 and for the Baosteel / Baowu Special Metallurgy product that carries the H13 trade name with tighter internal control. If brand and origin matter to your process — and for high-pressure die casting they usually do — specify the mill and ask for the mill's own certificate, not a trading company's declaration.</p>

<h2>How to write it on a drawing or PO</h2>
<p>Instead of "material: H13", write something a supplier can be measured against:</p>
<ul>
<li><strong>Grade and standard:</strong> "Hot-work tool steel 1.2344 per DIN EN ISO 4957, or equivalent H13 per ASTM A681 — mill certificate required."</li>
<li><strong>Delivery condition:</strong> "Annealed, 180–220 HBW."</li>
<li><strong>Microstructure:</strong> "Inclusion rating to SEP 1614, class not worse than …; microstructure rating to NADCA #207."</li>
<li><strong>Internal soundness:</strong> "UT to EN 10228-3, quality class 3, 100 % coverage."</li>
<li><strong>Traceability:</strong> "Heat number stamped on each piece, matching the certificate."</li>
</ul>
<p>Four extra lines on the drawing remove almost every dispute that arises from grade equivalence.</p>

<h2>What we supply</h2>
<p>We forge and machine H13 / 4Cr5MoSiV1 hot-work die steel and die forgings, supplied as annealed bars, forged blocks or heat-treated parts, with chemical composition, mechanical property and ultrasonic reports per shipment. As an authorised round-bar user of Baowu Special Metallurgy, we can supply certified Baosteel H13 with complete documentation. Metallographic examination is available to NADCA #207, SEP 1614 and VDG ASA on request.</p>
<p>Our published <a href="../products.html#grades">steel grade cross reference</a> maps every GB grade we offer to its DIN/EN, JIS and AISI/ASTM equivalents.</p>
""",
 "faq": [
   ("Is 1.2344 exactly the same as H13?",
    "They are near-equivalent, not identical. Both are 5 % Cr-Mo-V hot-work steels, but the specified composition windows differ slightly — for example AISI H13 allows up to 0.45 % C and up to 1.75 % Mo, while DIN 1.2344 is limited to 0.42 % C and 1.50 % Mo. For most tooling the difference is negligible; for incoming inspection written against one standard only, it can cause a rejection."),
   ("Can you supply H13 as ESR material?",
    "Yes. For die casting dies and other critical tooling, specify ESR (electroslag remelting) on the order. It improves micro-cleanliness and reduces the scatter in fatigue life, at a higher cost than conventional EAF + VD material."),
   ("Which standard should I write on my drawing, H13 or 1.2344?",
    "Write whichever your own quality system uses, and add 'or equivalent' plus the properties that matter to you — hardness, micro-cleanliness and UT class. Specifying properties rather than names is what actually controls the delivered part."),
 ],
},
{
 "slug": "ut-acceptance-criteria-forgings",
 "title": "Specifying UT for Forgings: GB/T 6402 vs ASTM A388 vs EN 10228-3",
 "seo_title": "UT Acceptance Criteria for Forgings | GB/T 6402 vs ASTM A388",
 "desc": "Why 'UT passed' is not enough on a forging certificate. How GB/T 6402, ASTM A388/A388M, EN 10228-3 and JIS G 0587 differ, and what to write on the purchase order.",
 "h1": "Specifying Ultrasonic Testing for Forgings: GB/T 6402, ASTM A388, EN 10228-3 and JIS G 0587 Compared",
 "lead": "A certificate that says 'UT: OK' tells you almost nothing. Ultrasonic testing of forgings is defined by a standard, a calibration reflector, a scanning coverage and an acceptance level — and those four things decide whether your forging is actually acceptable. This is how the main standards differ, and what to write on the order.",
 "body": """
<h2>The four standards buyers meet most often</h2>
<p>Forging suppliers in China quote UT against <strong>GB/T 6402</strong>. European drawings usually call for <strong>EN 10228-3</strong> (ferritic and martensitic steel forgings). North American drawings call <strong>ASTM A388/A388M</strong>. Japanese drawings call <strong>JIS G 0587</strong>. All four use the pulse-echo method and all four will find laminations, inclusions, shrinkage and cracks. They are still not interchangeable, for reasons that are administrative as much as technical.</p>

<h2>Where they differ</h2>
<table class="art-table">
<thead><tr><th></th><th>GB/T 6402</th><th>ASTM A388/A388M</th><th>EN 10228-3</th><th>JIS G 0587</th></tr></thead>
<tbody>
<tr><td>Reference reflector</td><td>Flat-bottom hole (FBH) blocks</td><td>Side-drilled hole (SDH) or FBH, by agreement; DGS permitted</td><td>FBH or DGS technique</td><td>FBH blocks</td></tr>
<tr><td>Acceptance level</td><td>Quality grades defined in the standard</td><td><strong>Not defined</strong> — the purchaser states the limits</td><td>Quality classes 1–4</td><td>Defined classes</td></tr>
<tr><td>Default coverage</td><td>Radial and axial scanning, with overlap</td><td>As agreed; typically 100 % of the specified volume</td><td>Specified in the inquiry</td><td>Per agreement</td></tr>
<tr><td>Typical use</td><td>Chinese domestic supply, widely quoted</td><td>North America, oil &amp; gas, heavy equipment</td><td>Europe, pressure and machinery parts</td><td>Japan</td></tr>
</tbody>
</table>
<p class="art-note">Simplified from the standards for procurement purposes. For acceptance decisions, work from the official text.</p>

<p>Two consequences follow. First, <em>ASTM A388 has no built-in acceptance level</em> — if your PO does not state one, the supplier can pass anything that produces a clean report. Second, GB/T 6402 and EN 10228-3 use different reference reflectors by default, so a report written to one is not automatically acceptable to an inspector holding the other. Additional testing or re-evaluation is usually required.</p>

<h2>Five things a UT specification must state</h2>
<ol>
<li><strong>Standard and revision</strong> — "EN 10228-3:2016", not "EN 10228".</li>
<li><strong>Acceptance level</strong> — quality class 3, or a stated maximum equivalent reflector size at a stated depth.</li>
<li><strong>Coverage</strong> — 100 % of the specified volume, or the surfaces and directions required. For thick sections, angle-beam scanning for radial defects should be explicit.</li>
<li><strong>Test surface and timing</strong> — ultrasonics is normally performed after final heat treatment and after rough machining, when the surface finish allows good coupling. Testing an as-forged, scaled surface produces a report that means very little.</li>
<li><strong>Reporting</strong> — defect location, depth, equivalent size and a plot for any indication above the recording level; operator certification level (ISO 9712 / ASNT Level II or above).</li>
</ol>

<h2>Common failure modes in Chinese certificates</h2>
<ul>
<li>Test performed <strong>before final heat treatment</strong>. Heat treatment can open up internal defects, so the report no longer describes the delivered part.</li>
<li>Report quotes a standard but no <strong>acceptance class</strong>.</li>
<li><strong>As-forged surface</strong> tested, with heavy coupling loss and no mention of it.</li>
<li>Only straight-beam scanning used on a thick section where radial defects are the main risk.</li>
<li>"Equivalent to ASTM A388" claimed without any statement of reference reflector — the two are not equivalent in that sense.</li>
</ul>

<h2>How we run UT</h2>
<p>Every forging is inspected piece by piece — no sampling. The default standard is GB/T 6402, and ASTM A388/A388M, EN 10228-3 or JIS G 0587 are performed on request, with the acceptance level agreed in the order. Testing is carried out after final heat treatment; where required we test again after rough machining. Reports carry defect location and size, and third-party witnessing (SGS, BV, TUV) can be arranged.</p>
<p>See also our published <a href="../products.html#grades">NDT and test standards cross reference</a>, which lists the Chinese standard alongside the ASTM, EN/ISO and JIS counterparts for UT, tensile, impact, fatigue and metallography.</p>
""",
 "faq": [
   ("Is GB/T 6402 the same as ASTM A388?",
    "No. Both are ultrasonic test-method standards for steel forgings and both use pulse-echo technique, but they differ in reference reflector type, default frequency range, minimum thickness and — most importantly — acceptance criteria. GB/T 6402 defines quality grades inside the standard; ASTM A388 leaves acceptance limits to the purchaser. Reports are generally mutually recognisable only after additional evaluation."),
   ("Do you test every forging or sample them?",
    "Every forging is tested individually. For rotor and other safety-critical parts this is non-negotiable, and we apply the same practice to standard forgings unless the customer specifies sampling."),
   ("Can you arrange SGS / BV / TUV witnessing?",
    "Yes. Third-party inspection can be arranged at the customer's cost, either witnessing our in-house testing or performing independent testing. Please state the requirement in the order so it can be scheduled with production."),
 ],
},
{
 "slug": "forged-vs-cast-flywheel-rotor",
 "title": "Forged vs Cast Flywheel Rotor: Why Fatigue Decides",
 "seo_title": "Forged vs Cast Flywheel Rotor | Fatigue Life Comparison",
 "desc": "Why flywheel energy storage rotors are forged rather than cast: internal soundness, metal flow lines, and 10-million-cycle fatigue verification at the rotor centre.",
 "h1": "Forged vs Cast Flywheel Rotor: Why Fatigue Life Decides the Choice",
 "lead": "A flywheel energy storage rotor spins continuously for years, at high tip speed, with stress cycling every revolution. The design driver is not static strength — it is high-cycle fatigue and the consequence of internal defects. That is why the rotor is forged, and why the fatigue test position matters as much as the test result.",
 "body": """
<h2>The duty cycle is the specification</h2>
<p>A rotor in a flywheel energy storage system accumulates cycles fast. At a few thousand revolutions per minute, one hour of operation is already a few hundred thousand stress cycles; a year is in the billions of load reversals at the stress-concentration features — the bore, the stepped shaft transition, keyways and fits. Under those conditions the rotor does not fail by yielding. It fails, if it fails, by fatigue initiating at an internal or surface defect.</p>
<p>That single sentence determines the manufacturing route: the material must be dense, homogeneous and free of the defect types that act as fatigue initiators.</p>

<h2>What casting gives you, and what it costs you</h2>
<p>Casting is attractive for shape freedom and cost. Its weakness is exactly where a rotor is most sensitive:</p>
<ul>
<li><strong>Shrinkage porosity</strong> in the thermal centre — which for a disc-type rotor is precisely the highest-stressed region.</li>
<li><strong>Non-metallic inclusions</strong> and slag entrapment, acting as initiation sites.</li>
<li><strong>Coarse, dendritic as-cast structure</strong> with segregation of alloying elements.</li>
<li><strong>No grain flow</strong> to follow the stress pattern — the material is isotropic in the worst sense.</li>
</ul>
<p>Cast rotors do exist, and for low-speed, low-energy applications they can be adequate. For high tip speed they are used rarely, and when they are, they tend to be heavily derated.</p>

<h2>What forging does</h2>
<p>Forging works on the same steel mechanically rather than thermally:</p>
<ul>
<li><strong>Closes internal porosity.</strong> Adequate reduction ratio welds shut internal voids, which is why forging ratio is a controlled parameter and not a casual one.</li>
<li><strong>Refines grain size and breaks up carbides</strong>, raising both strength and toughness at the same time — a combination castings cannot offer.</li>
<li><strong>Creates continuous metal flow lines</strong> that follow the part contour, improving fatigue resistance at fillets and transitions where cracks start.</li>
<li><strong>Makes internal quality verifiable.</strong> A forged and heat-treated rotor can be fully inspected by ultrasonic testing after final heat treatment, which is not equally true for a casting.</li>
</ul>

<h2>Why the fatigue specimen position matters</h2>
<p>Fatigue data quoted from a specimen taken near the surface says little about a rotor. The critical region is the centre of the section, where solidification effects and forging reduction are least favourable, and where the stress state is complex. A fatigue verification that is worth the paper it is printed on samples the <strong>centre</strong>, at the mid-length of the forging.</p>
<p>Our rotor forgings are fatigue tested at the centre position to <strong>10 million cycles</strong>, alongside piece-by-piece ultrasonic inspection and full chemical and mechanical testing. That is the level of evidence a flywheel OEM needs before putting a rotor into a series product.</p>

<h2>Buyer's checklist for a flywheel rotor forging</h2>
<ol>
<li><strong>Melting route</strong> — vacuum degassing at minimum; ESR or VAR for higher-duty rotors.</li>
<li><strong>Forging ratio</strong> and reduction sequence, not just "forged".</li>
<li><strong>Heat treatment record</strong> — full cycle with temperatures, holding times and cooling method, traceable to the heat number.</li>
<li><strong>UT after final heat treatment</strong>, to a named standard and acceptance level, piece by piece.</li>
<li><strong>Fatigue verification at the centre position</strong>, with the specimen location stated in the report.</li>
<li><strong>Mechanical properties at the specified sampling position</strong> — tensile, yield, elongation, reduction of area and impact energy.</li>
<li><strong>Traceability</strong> — heat number on the part, matching certificate, heat treatment record and test reports.</li>
</ol>

<h2>Where we fit</h2>
<p>We forge high-strength, high-purity flywheel energy storage rotor forgings, fatigue tested at the centre to 10 million cycles and ultrasonically inspected piece by piece, supplied in series production to leading Chinese flywheel energy storage manufacturers. Rotor bodies and rotor assemblies with stepped shafts are both available, built to drawing.</p>
<p>Details are on our <a href="../flywheel-rotor.html">flywheel rotor forging page</a>. If you are evaluating a new rotor design, send the drawing and duty cycle and we will come back on manufacturability and inspection plan.</p>
""",
 "faq": [
   ("Why not just cast the rotor and derate it?",
    "Derating a casting for a high-tip-speed rotor offsets most of the cost advantage, because the mass and diameter have to grow to carry the same energy at lower stress — and the resulting inertia often does not fit the application envelope. Forging lets you use the material closer to its fatigue capability."),
   ("At what point in production is UT performed?",
    "After final heat treatment, and again after rough machining where the customer requires it. Testing before final heat treatment is not accepted as evidence for the delivered part, because heat treatment can open internal defects."),
   ("Can you supply the rotor as an assembly with the shaft?",
    "Yes. We supply rotor bodies, and rotor assemblies including the stepped shaft, machined to drawing. Both configurations ship with chemical, mechanical, UT and fatigue documentation."),
 ],
},
{
 "slug": "reading-chinese-mill-certificate",
 "title": "Reading a Chinese Mill Certificate: GB Grades to DIN / JIS / AISI",
 "seo_title": "Chinese Mill Certificate Guide | GB to DIN JIS AISI",
 "desc": "How to read a Chinese mill certificate for forgings: GB grade naming, equivalent DIN/JIS/AISI grades, and the five checks that catch most problems before delivery.",
 "h1": "Reading a Chinese Mill Certificate: Mapping GB Grades to DIN, JIS and AISI",
 "lead": "Chinese mill certificates are not hard to read once you know how the GB system names steel — but they are easy to misread, because a grade name tells you less than you think and 'equivalent' is a word with a wide meaning. Here is the naming logic, the common grade mappings, and five checks that catch most problems.",
 "body": """
<h2>How the GB naming system works</h2>
<p>Most Chinese structural and alloy grades are built the same way: <strong>carbon content in hundredths of a percent, followed by the main alloying elements</strong>.</p>
<ul>
<li><strong>45#</strong> — nominal 0.45 % carbon. Plain carbon steel, roughly AISI 1045, DIN C45, JIS S45C.</li>
<li><strong>40Cr</strong> — 0.40 % carbon with chromium. Roughly AISI 5140, DIN 41Cr4 (1.7035), JIS SCr440.</li>
<li><strong>42CrMo</strong> — 0.42 % carbon, chromium and molybdenum. Roughly AISI 4140, DIN 42CrMo4 (1.7225), JIS SCM440.</li>
<li><strong>35CrMo</strong> — 0.35 % carbon Cr-Mo. Roughly AISI 4135, DIN 34CrMo4 (1.7220), JIS SCM435.</li>
<li><strong>30CrMo</strong> — 0.30 % carbon Cr-Mo, commonly treated as the Chinese counterpart of AISI 4130. Roughly DIN 25CrMo4 (1.7218), JIS SCM430.</li>
<li><strong>2Cr13</strong> — about 0.2 % carbon, 13 % chromium martensitic stainless. Roughly AISI 420, DIN X20Cr13 (1.4021), JIS SUS420J1.</li>
</ul>
<p>Understanding this pattern lets you sanity-check a certificate at a glance. If a heat claimed as 42CrMo shows 0.28 % C, something is wrong — regardless of what the grade column says.</p>

<h2>The classic stumbling blocks</h2>
<h3>"Equivalent" does not mean identical</h3>
<p>A 30CrMo heat is not a 4130 heat certified to ASTM A29. They are close enough that both are used for the same applications, and different enough that a certificate written against one may fail an audit written against the other. Where the application is safety-relevant — pressure-containing parts, rotating equipment — specify the standard, not the equivalent.</p>

<h3>Tool steel names travel badly</h3>
<p>In tool steels, a Chinese supplier may write H13 and mean the GB/T 1299 grade 4Cr5MoSiV1, or the Baosteel product sold under the H13 name, or a generic 5 % Cr hot-work steel. All three are sold as "H13". See <a href="h13-vs-1-2344-vs-skd61.html">H13 vs 1.2344 vs SKD61</a> for the composition windows and how to write the requirement.</p>

<h3>Test standards are also in a different language</h3>
<p>A Chinese certificate will cite GB/T 228.1 for tensile and GB/T 6402 for UT. Those map to ASTM E8/E8M and ASTM A388 respectively, but as <em>near</em>-equivalents with different acceptance definitions. Our <a href="ut-acceptance-criteria-forgings.html">UT specification guide</a> covers the differences that matter.</p>

<h2>Five checks that catch most problems</h2>
<ol>
<li><strong>Grade versus composition.</strong> Compare carbon and main alloy content against the grade name logic above. This one check catches transcription errors and grade substitution.</li>
<li><strong>Hardness units.</strong> HBW and HRC are not interchangeable and conversion is not linear. A certificate that says "hardness 220" without a unit is incomplete.</li>
<li><strong>Impact test temperature.</strong> Charpy values at +20 °C look far better than at −20 °C or −40 °C. Check that the test temperature on the certificate matches the one on your specification.</li>
<li><strong>Sampling position and orientation.</strong> Properties taken from a prolongation at the end of the forging differ from those at mid-radius or at the centre. For critical parts the position must be stated.</li>
<li><strong>Heat treatment record.</strong> A property certificate without the heat treatment cycle cannot be verified and cannot be reproduced. Ask for the cycle: temperatures, holding times, quench medium, tempering temperature.</li>
</ol>

<h2>What a complete documentation package looks like</h2>
<p>For each lot, expect: chemical composition report, mechanical property report, ultrasonic inspection report (with standard and acceptance level), heat treatment record, and — for tool steels — a metallographic report. All of them traceable to the same heat number, which is stamped on the parts.</p>
<p>Our own cross-reference tables are published so that this comparison can be done before ordering rather than after delivery: the <a href="../products.html#grades">steel grade cross reference</a> (GB / DIN-EN / JIS / AISI) and the NDT and test standards table on the same page.</p>

<h2>If you have a certificate and want a second opinion</h2>
<p>Send us the certificate and the drawing. We will tell you whether the grade and test standards on it actually meet the drawing, and what to add to the purchase order if they do not. There is no charge for this and no obligation — it is the same check we run on our own suppliers.</p>
""",
 "faq": [
   ("Is 30CrMo the same as 4130?",
    "It is the closest Chinese equivalent and is used interchangeably in many applications, but they are certified to different standards (GB/T 3077 versus ASTM A29/A29M) with slightly different composition windows. For pressure-containing or safety-relevant parts, specify the standard you need certified."),
   ("What does the '#' in 45# mean?",
    "It simply marks a plain carbon steel grade, read as '45 steel' — nominal 0.45 % carbon. It is not a special symbol beyond that."),
   ("Can you supply certificates in English?",
    "Yes. Chemical composition, mechanical property, UT and metallographic reports are issued in English (with Chinese originals where required), and third-party inspection reports from SGS, BV or TUV can be arranged."),
 ],
},
]

# 第二批文章（材质选型 / 油缸 / 锻造比 / 酸性工况）
try:
    from articles_extra import ARTICLES_EXTRA
    ARTICLES.extend(ARTICLES_EXTRA)
except Exception as _e:  # pragma: no cover
    print("  [!] 第二批文章加载失败:", _e)


def load_shell():
    """从现有英文页提取 header / footer / lightbox / scripts，保证导航与页脚一致"""
    src = io.open(os.path.join(EN, "tech.html"), encoding="utf-8").read()
    header = re.search(r"<header class=\"site-header\">.*?</header>", src, re.S).group(0)
    footer = re.search(r"<footer class=\"site-footer\">.*?</footer>", src, re.S).group(0)
    lightbox = re.search(r"<div class=\"lightbox\" id=\"certLightbox\".*?</div>\s*</div>", src, re.S)
    lightbox = lightbox.group(0) if lightbox else ""
    scripts = re.search(r"<script>window\.LX_FORCE_LANG.*?</script>\s*<script src=\"\.\./assets/main\.js\"></script>", src, re.S).group(0)

    # 文章位于 en/insights/ 子目录，页头页脚中的同级链接需要上提一级
    import re as _re
    def up(frag):
        frag = _re.sub(r'href="(?!#|https?:|mailto:|tel:|\.\./)([^"]+)"', r'href="../\1"', frag)
        frag = _re.sub(r'src="(?!#|https?:|\.\./)([^"]+)"', r'src="../\1"', frag)
        return frag
    header, footer, lightbox = up(header), up(footer), up(lightbox)
    return header, footer, lightbox, scripts


def faq_json(faqs):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    }, ensure_ascii=False, indent=2)


def article_json(a):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": a["h1"],
        "description": a["desc"],
        "datePublished": TODAY,
        "dateModified": TODAY,
        "inLanguage": "en",
        "author": {"@type": "Organization", "name": "Langxi Shengda Forging Co., Ltd."},
        "publisher": {"@type": "Organization", "name": "Langxi Shengda Forging Co., Ltd.",
                      "logo": {"@type": "ImageObject", "url": f"{SITE}/logo.webp"}},
        "mainEntityOfPage": f"{SITE}/en/insights/{a['slug']}.html",
    }, ensure_ascii=False, indent=2)


def breadcrumb_json(a):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/en/"},
            {"@type": "ListItem", "position": 2, "name": "Insights", "item": f"{SITE}/en/insights.html"},
            {"@type": "ListItem", "position": 3, "name": a["title"], "item": f"{SITE}/en/insights/{a['slug']}.html"},
        ]
    }, ensure_ascii=False, indent=2)


def build_article(a, header, footer, lightbox, scripts):
    faq_html = "".join(
        f'<div class="faq-item"><div class="q">{q}</div><div class="a-body"><p>{ans}</p></div></div>'
        for q, ans in a["faq"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" type="image/png" href="../../favicon.png">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{a['seo_title']}</title>
<meta name="description" content="{a['desc']}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{SITE}/en/insights/{a['slug']}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{a['seo_title']}">
<meta property="og:description" content="{a['desc']}">
<meta property="og:url" content="{SITE}/en/insights/{a['slug']}.html">
<meta property="og:locale" content="en_US">
<link rel="alternate" hreflang="en" href="{SITE}/en/insights/{a['slug']}.html">
<link rel="alternate" hreflang="x-default" href="{SITE}/en/insights/{a['slug']}.html">
<link rel="stylesheet" href="../../assets/style.css">
<script type="application/ld+json">
{article_json(a)}
</script>
<script type="application/ld+json">
{breadcrumb_json(a)}
</script>
<script type="application/ld+json">
{faq_json(a['faq'])}
</script>
</head>
<body>
{header}
<section class="art-band">
<div class="container art-body">
<div class="art-meta"><a href="../insights.html">Insights</a> · Technical note · {TODAY}</div>
<h1>{a['h1']}</h1>
<p class="art-lead">{a['lead']}</p>
{a['body']}
<h2>Frequently asked</h2>
<div class="faq-list">
{faq_html}
</div>
<div class="art-cta">
<h3>Need a quotation or a document check?</h3>
<p>Send your drawing, grade and test requirements — we will confirm manufacturability, inspection plan and lead time.</p>
<p><a class="btn btn-primary" href="../contact.html">Contact us</a> <a class="btn btn-ghost" href="../products.html">View products</a></p>
</div>
</div>
</section>
{footer}
{lightbox}
{scripts}
</body>
</html>
"""


def build_hub(header, footer, lightbox, scripts):
    cards = ""
    for a in ARTICLES:
        cards += f"""<a class="ins-card" href="insights/{a['slug']}.html">
<h3>{a['title']}</h3>
<p>{a['desc']}</p>
<span>Read the note →</span>
</a>
"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" type="image/png" href="../favicon.png">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Technical Insights | Forging Standards &amp; Grades</title>
<meta name="description" content="Technical notes for forging buyers: grade equivalence (H13 / 1.2344 / SKD61), UT acceptance criteria, forged versus cast rotors, and reading a Chinese mill certificate.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{SITE}/en/insights.html">
<meta property="og:type" content="website">
<meta property="og:title" content="Technical Insights | Langxi Shengda Forging">
<meta property="og:description" content="Technical notes on forging grades, standards and inspection for buyers.">
<meta property="og:url" content="{SITE}/en/insights.html">
<meta property="og:locale" content="en_US">
<link rel="alternate" hreflang="en" href="{SITE}/en/insights.html">
<link rel="alternate" hreflang="x-default" href="{SITE}/en/insights.html">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
{header}
<section class="art-band">
<div class="container">
<div class="sec-head">
<div class="en">Insights</div>
<h1>Technical Insights for Forging Buyers</h1>
<p>Short technical notes on the questions that come up most often when sourcing forgings from China — grade equivalence, inspection standards and the difference between similar-looking specifications.</p>
</div>
<div class="ins-grid">
{cards}
</div>
</div>
</section>
{footer}
{lightbox}
{scripts}
</body>
</html>
"""


def inject_further_reading():
    """在 en/products.html 与 en/tech.html 注入内链区块（幂等）"""
    links = "".join(f'<li><a href="insights/{a["slug"]}.html">{a["title"]}</a></li>\n' for a in ARTICLES)
    block = f"""<div class="further-reading">
<h3>Further reading</h3>
<ul>
{links}</ul>
</div>
"""
    for page, anchor in [("products.html", "</div>\n</section>\n\n<section class=\"catalog-band\""),
                         ("tech.html", None)]:
        p = os.path.join(EN, page)
        if not os.path.exists(p):
            continue
        s = io.open(p, encoding="utf-8").read()
        if "further-reading" in s:
            s = re.sub(r'<div class="further-reading">.*?</div>\s*', "", s, flags=re.S)
        if anchor and anchor in s:
            s = s.replace(anchor, block + "</div>\n</section>\n\n<section class=\"catalog-band\"", 1)
            io.open(p, "w", encoding="utf-8", newline="").write(s)
            print(f"  注入内链: {page}")
            continue
        # tech.html：插在 footer 之前
        if "<footer class=\"site-footer\">" in s:
            s = s.replace("<footer class=\"site-footer\">", block + "<footer class=\"site-footer\">", 1)
            io.open(p, "w", encoding="utf-8", newline="").write(s)
            print(f"  注入内链: {page}")


def update_sitemap():
    p = os.path.join(HERE, "sitemap_en.xml")
    s = io.open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<url>\s*<loc>[^<]*/en/insights[^<]*</loc>.*?</url>", "", s, flags=re.S)
    entries = [f"{SITE}/en/insights.html"] + [f"{SITE}/en/insights/{a['slug']}.html" for a in ARTICLES]
    add = ""
    for loc in entries:
        add += f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n"
    s = s.replace("</urlset>", add + "</urlset>")
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print(f"  sitemap_en.xml 更新: +{len(entries)} 条")


def main():
    os.makedirs(OUT, exist_ok=True)
    header, footer, lightbox, scripts = load_shell()
    for a in ARTICLES:
        html = build_article(a, header, footer, lightbox, scripts)
        io.open(os.path.join(OUT, a["slug"] + ".html"), "w", encoding="utf-8", newline="").write(html)
        print(f"  文章: insights/{a['slug']}.html  ({len(html)} 字节)")
    hub = build_hub(header, footer, lightbox, scripts)
    io.open(os.path.join(EN, "insights.html"), "w", encoding="utf-8", newline="").write(hub)
    print(f"  列表页: insights.html ({len(hub)} 字节)")
    inject_further_reading()
    update_sitemap()


if __name__ == "__main__":
    main()
