#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二批英文技术文章（由 build_insights.py 合并进 ARTICLES）"""

ARTICLES_EXTRA = [
{
 "slug": "5crnimo-vs-5crni2mov-vs-h13",
 "title": "5CrNiMo vs 5CrNi2MoV vs H13: Choosing a Die Material",
 "seo_title": "5CrNiMo vs 5CrNi2MoV vs H13 | Die Material Selection",
 "desc": "How to choose between 5CrNiMo (DIN 1.2713 / JIS SKT4), 5CrNi2MoV and H13 for hammer dies, die blocks and inserts — toughness, hardenability and cost.",
 "h1": "5CrNiMo vs 5CrNi2MoV vs H13: Choosing a Hot-Work Die Material",
 "lead": "Three steels appear on almost every hot-forging die drawing: 5CrNiMo, 5CrNi2MoV and H13. They are not interchangeable, and the wrong choice shows up as either cracked dies or a die that softens after a few thousand strokes. This note explains what each one is good at, and how to write the requirement so the die behaves as designed.",
 "body": """
<h2>The three families in one sentence each</h2>
<ul>
<li><strong>5CrNiMo</strong> (DIN 1.2713 / JIS SKT4 / ASTM L6) — a low-alloy, high-toughness hot-work steel for hammer dies and large blocks. Moderate hot strength, excellent resistance to cracking under impact.</li>
<li><strong>5CrNi2MoV</strong> (near DIN 1.2714) — the same idea with more nickel and a vanadium addition: deeper hardening and better toughness in large sections, which is why it is used for very large die blocks.</li>
<li><strong>H13 / 4Cr5MoSiV1</strong> (DIN 1.2344 / JIS SKD61) — a 5 % Cr hot-work steel with much higher hot strength and temper resistance, used for die inserts, extrusion tooling and die casting dies.</li>
</ul>

<h2>Composition comparison</h2>
<table class="art-table">
<thead><tr><th>Element (%)</th><th>5CrNiMo</th><th>5CrNi2MoV</th><th>H13 / 4Cr5MoSiV1</th></tr></thead>
<tbody>
<tr><td>C</td><td>0.50–0.60</td><td>0.50–0.60</td><td>0.32–0.42</td></tr>
<tr><td>Cr</td><td>0.50–0.80</td><td>0.60–0.90</td><td>4.75–5.50</td></tr>
<tr><td>Ni</td><td>1.40–1.80</td><td>1.60–2.20</td><td>—</td></tr>
<tr><td>Mo</td><td>0.15–0.30</td><td>0.30–0.50</td><td>1.10–1.75</td></tr>
<tr><td>V</td><td>≤0.20</td><td>0.05–0.15</td><td>0.80–1.20</td></tr>
</tbody>
</table>
<p class="art-note">Typical ranges; confirm against the mill certificate rather than the grade name.</p>

<h2>What actually separates them in service</h2>
<h3>Hot strength and temper resistance</h3>
<p>This is the H13 advantage. The 5 % chromium and molybdenum content, with vanadium, gives a steel that keeps its hardness at 500–600 °C. A 5CrNiMo die in the same hot-forging application will soften faster at the die face and lose dimensional control sooner. If the die surface runs hot — thin sections, short cycle times, poor cooling — H13 is the default answer.</p>

<h3>Toughness and crack resistance</h3>
<p>Reverse the argument for impact. Hammer dies see violent, repeated blows; the failure mode is cracking, not softening. 5CrNiMo and 5CrNi2MoV have the lower carbon and higher nickel that make them tolerant of impact. Putting an H13 insert into a hammer die application, with the wrong hardness, is a common cause of early cracking.</p>

<h3>Hardenability in large sections</h3>
<p>Die blocks are thick. A steel that hardens well in a 100 mm section may not harden through a 400 mm block, and a soft core under a hard surface is a fatigue crack waiting to happen. The nickel addition in 5CrNi2MoV exists precisely for this: it lets large blocks through-harden and stay tough.</p>

<h3>Cost</h3>
<p>H13 costs more than 5CrNiMo, and 5CrNi2MoV sits in between. Choosing H13 for a die that only needs toughness means paying for hot strength you do not use; choosing 5CrNiMo for a die that runs hot means replacing dies more often.</p>

<h2>Selection guide</h2>
<table class="art-table">
<thead><tr><th>Application</th><th>Typical choice</th><th>Why</th></tr></thead>
<tbody>
<tr><td>Hammer die inserts, small to medium</td><td>5CrNiMo</td><td>Impact toughness, forgiving heat treatment</td></tr>
<tr><td>Very large hammer die blocks</td><td>5CrNi2MoV</td><td>Hardenability through thick sections</td></tr>
<tr><td>Hot forging dies, press dies, die inserts</td><td>H13</td><td>Hot strength and temper resistance</td></tr>
<tr><td>Extrusion tooling, container liners</td><td>H13 (or higher-Mo 1.2367)</td><td>Sustained high temperature</td></tr>
<tr><td>Die casting dies</td><td>H13, ESR for critical</td><td>Thermal fatigue resistance</td></tr>
</tbody>
</table>

<h2>How to specify it on the drawing</h2>
<ul>
<li>Grade plus standard: <em>5CrNiMo per GB/T 1299, or 1.2713 / SKT4 equivalent</em>.</li>
<li>Delivery condition and hardness range — annealed blocks are typically 197–241 HBW; state the range you want.</li>
<li>For H13, state whether ESR is required and which micro-cleanliness rating applies (NADCA #207 or SEP 1614).</li>
<li>Ultrasonic quality class for blocks, with the standard and acceptance level named — see our <a href="ut-acceptance-criteria-forgings.html">UT specification guide</a>.</li>
<li>Grain flow direction relative to the working face, if the die is directional.</li>
</ul>

<h2>What we supply</h2>
<p>We forge and machine hot-work die steels and die forgings in these grades: H13 / 4Cr5MoSiV1, 5CrNiMo, 5CrNi2MoV, plus customer-specified grades. Blocks, inserts and near-net die blanks are supplied spheroidize annealed, with chemical, mechanical and UT reports per shipment, and metallographic examination to NADCA #207, SEP 1614 or VDG ASA on request. Our <a href="../products.html#grades">grade cross reference</a> lists every grade with its DIN, JIS and AISI equivalents.</p>
""",
 "faq": [
   ("Can H13 replace 5CrNiMo for hammer dies?",
    "Not directly. H13 has higher hot strength but lower toughness at the hardness levels used for hammer dies, and it is more sensitive to heat treatment. If a hammer die is being upgraded, the geometry, hardness and preheating practice usually need to change as well."),
   ("What is 5CrNi2MoV equivalent to in European standards?",
    "It is closest to DIN 1.2714 (55NiCrMoV7), which is the large-block variant of the 5CrNiMo family. The two are near-equivalent rather than identical; for critical blocks, specify the properties you need — hardenability, toughness at the core, UT class — rather than relying on the grade name alone."),
   ("Which grade gives the longest die life?",
    "It depends on the failure mode. For thermal fatigue and softening, H13. For impact cracking in hammer dies, 5CrNiMo or 5CrNi2MoV. Die life is usually decided by matching the grade to the failure mechanism, then controlling inclusion content and heat treatment."),
 ],
},
{
 "slug": "hydraulic-cylinder-barrel-forging-materials",
 "title": "Hydraulic Cylinder Barrel Forgings: 27SiMn vs E355 vs 42CrMo",
 "seo_title": "Hydraulic Cylinder Barrel Material | 27SiMn vs E355",
 "desc": "Material selection for large-diameter hydraulic cylinder barrels: 27SiMn, E355 and 42CrMo compared on strength, weldability, machinability and wall thickness.",
 "h1": "Hydraulic Cylinder Barrel Forgings: 27SiMn, E355 or 42CrMo?",
 "lead": "A cylinder barrel looks like a simple tube, but the material choice fixes the pressure rating, the welding procedure, the honing behaviour and the inspection plan. This note compares the three grades most often specified for large-diameter barrels, and explains when a forging beats a seamless tube.",
 "body": """
<h2>The three common choices</h2>
<table class="art-table">
<thead><tr><th>Grade</th><th>Equivalents</th><th>Typical use</th></tr></thead>
<tbody>
<tr><td><strong>27SiMn</strong></td><td>Chinese GB grade; no direct DIN/JIS equivalent</td><td>Standard hydraulic cylinder barrels in the Chinese market</td></tr>
<tr><td><strong>E355</strong></td><td>EN E355 (1.0580)</td><td>European drawings, welded and honed barrels</td></tr>
<tr><td><strong>42CrMo</strong></td><td>DIN 1.7225 / JIS SCM440 / AISI 4140</td><td>High-pressure barrels, rods, heavy-duty cylinders</td></tr>
</tbody>
</table>

<h2>What each one is good for</h2>
<h3>27SiMn — the domestic workhorse</h3>
<p>27SiMn is a manganese-silicon steel developed for hydraulic supports and cylinder barrels. It offers good strength after quenching and tempering, reasonable machinability and low cost, and it is widely available in China. Its weakness is weldability: the relatively high carbon and manganese content makes it crack-sensitive in welding, so preheat and post-weld heat treatment are not optional. If a barrel is to be welded to a flange or a port block, that matters.</p>

<h3>E355 — the European default</h3>
<p>E355 is a structural steel specified for hollow sections and tubes, and it appears on European cylinder drawings because the barrel is often made from a honed tube rather than a forging. It welds well and machines predictably, but its strength as supplied is lower than a quenched and tempered 27SiMn or 42CrMo. For high pressure, the wall thickness has to grow — which then costs weight and material.</p>

<h3>42CrMo — for pressure and duty cycle</h3>
<p>42CrMo (AISI 4140 family) gives the highest strength of the three after quenching and tempering, with good toughness and fatigue resistance. It is the choice for high-pressure barrels, large bore cylinders and applications with pressure cycling. It costs more and needs proper heat treatment control, and like 27SiMn it requires care in welding.</p>

<h2>Forged barrel or honed tube?</h2>
<p>Both routes are legitimate, and the choice is usually made on diameter and wall thickness:</p>
<ul>
<li><strong>Seamless tube</strong> — economical for standard diameters, readily available in E355 and equivalent grades, and convenient when the barrel is short and the pressure moderate.</li>
<li><strong>Forged barrel</strong> — better where the diameter is large, the wall is thick, or the barrel carries ports, flanges or a closed end. Forging gives a continuous grain flow around the section, closes internal porosity and allows UT of the full volume before machining.</li>
</ul>
<p>For thick-wall, high-pressure barrels, a forged and quenched-and-tempered shell with a bored and honed bore is often the more reliable route than a tube, because the internal quality can be verified and the mechanical properties are uniform through the wall.</p>

<h2>Points that decide whether the barrel works</h2>
<ol>
<li><strong>Wall thickness uniformity.</strong> An eccentric wall means uneven stress and a bore that cannot be honed true. This is a forging and machining discipline, not a material property.</li>
<li><strong>Heat treatment through the wall.</strong> A barrel that is hard on the outside and soft at the bore will not hold pressure as designed. Specify quench and temper with hardness checked at the bore, not only at the surface.</li>
<li><strong>UT before boring.</strong> Internal defects are cheapest to find before the bore is finished. Specify the standard and acceptance level — GB/T 6402, ASTM A388 or EN 10228-3.</li>
<li><strong>Weldability, if welding follows.</strong> If the barrel will be welded, say so at enquiry stage. It changes the material recommendation and the heat treatment sequence.</li>
<li><strong>Bore finish and tolerance.</strong> Honing, skiving and roller burnishing all have different starting requirements; the barrel supplier needs to know which follows.</li>
</ol>

<h2>What to write on the enquiry</h2>
<ul>
<li>Bore diameter, wall thickness and overall length, with the drawing.</li>
<li>Working pressure and whether it is static or cycling.</li>
<li>Material preference and the standard it must meet.</li>
<li>Whether the barrel will be welded, and to what.</li>
<li>UT standard and acceptance level; hardness check position.</li>
<li>Delivery condition: as-forged, rough machined, or bored and honed.</li>
</ul>

<h2>What we supply</h2>
<p>We forge large-diameter hydraulic cylinder barrel forgings in 27SiMn, 35CrMo, 42CrMo and 45#, quenched and tempered for dense structure and uniform wall thickness, with chemical, mechanical and UT reports per lot. Barrels can be supplied as-forged, rough machined, or bored and honed to drawing. Details on our <a href="../cylinder-barrel.html">hydraulic cylinder barrel page</a>.</p>
""",
 "faq": [
   ("Is 27SiMn equivalent to E355?",
    "No. They are used for similar products but are different steels: 27SiMn is a Chinese grade with higher carbon and manganese, quenched and tempered for strength; E355 is a European structural steel supplied in the as-rolled or normalized condition. A drawing written for E355 will not be satisfied by 27SiMn without a review of strength, weldability and heat treatment."),
   ("Can you supply the barrel already honed?",
    "We supply as-forged, rough machined or bored and honed barrels depending on the requirement. For honed supply, please state the bore tolerance, surface finish and the honing allowance expected, so the pre-honing bore can be prepared correctly."),
   ("Why is a forging preferred over a tube for thick walls?",
    "Because the full volume can be inspected by UT before machining, the grain flow follows the section, and the mechanical properties can be made uniform through a thick wall by quenching and tempering. Thick-wall tubes are limited by what the tube mill can produce and by the inspection coverage available on the tube."),
 ],
},
{
 "slug": "forging-ratio-and-internal-quality",
 "title": "Forging Ratio: Why Reduction Decides Internal Quality",
 "seo_title": "Forging Ratio Explained | Reduction and Internal Quality",
 "desc": "What forging ratio controls, how it relates to ingot segregation and UT results, and what to specify on a purchase order for critical shaft and rotor forgings.",
 "h1": "Forging Ratio: Why Reduction Decides Internal Quality",
 "lead": "Two forgings can carry the same grade, the same heat number and the same certificate, and still behave differently — because one was forged from a small bloom and the other from a large ingot with barely enough reduction to shape it. Forging ratio is the number that describes that difference, and it is one of the few process parameters a buyer can specify and verify.",
 "body": """
<h2>What forging ratio means</h2>
<p>Forging ratio compares the cross-section before and after forging:</p>
<p class="art-note">Forging ratio = original cross-sectional area ÷ final cross-sectional area</p>
<p>An ingot or bloom of 100 000 mm² forged down to 25 000 mm² has a ratio of 4:1. The same figure is sometimes quoted as a reduction in height during a specific operation, so when a supplier states a ratio, ask which definition is being used and whether it is the total ratio or the ratio of a single step.</p>

<h2>What reduction actually does</h2>
<ul>
<li><strong>Closes internal porosity.</strong> Ingot centreline shrinkage and gas porosity weld shut under sufficient reduction, provided the stress state is compressive and the temperature is right.</li>
<li><strong>Breaks up segregation and coarse carbides.</strong> Alloying elements segregate during solidification; forging deforms and disperses those bands.</li>
<li><strong>Refines grain structure</strong> when the deformation and temperature sequence is controlled, which raises both strength and toughness.</li>
<li><strong>Creates directional grain flow</strong> that can be aligned with the service stress — the main reason a shaft is forged rather than machined from bar.</li>
</ul>

<h2>Why the centre is the difficult part</h2>
<p>Reduction applied at the surface does not automatically reach the core. In a poorly sequenced operation, the outer layers deform while the centre barely moves — the ratio looks acceptable on paper, but the centreline remains porous and segregated. That is exactly where a rotating shaft carries maximum stress and where fatigue initiates.</p>
<p>The practical consequences: die design and pass sequence matter as much as the headline ratio, and inspection must target the centre. This is why ultrasonic testing is performed on the finished forging volume rather than on the surface, and why rotor specifications often call for fatigue specimens taken from the centre position.</p>

<h2>Typical requirements</h2>
<table class="art-table">
<thead><tr><th>Application</th><th>Common minimum forging ratio</th><th>Comment</th></tr></thead>
<tbody>
<tr><td>General industrial forgings</td><td>3:1</td><td>Commercial baseline</td></tr>
<tr><td>Shafts and rotating parts</td><td>4:1 or higher</td><td>Centre soundness matters</td></tr>
<tr><td>Rotor and safety-critical forgings</td><td>4:1 to 6:1, agreed</td><td>Often with centre test specimens</td></tr>
<tr><td>Die blocks and thick sections</td><td>3:1 to 4:1 with upsetting</td><td>Upsetting first improves centre consolidation</td></tr>
</tbody>
</table>
<p class="art-note">Values are typical rather than universal; the applicable figure should be taken from the product standard or agreed with the customer.</p>

<h2>How a buyer can verify it</h2>
<ol>
<li><strong>Ask for the ingot or bloom size</strong> and the finished dimensions — the ratio follows arithmetically. If a supplier cannot state the input size, the ratio cannot be verified.</li>
<li><strong>Ask for the process route</strong>: upsetting and drawing sequence, number of passes, and the forging temperature range.</li>
<li><strong>Ask where the test specimens come from</strong> — end prolongation, mid-radius or centre. A certificate that does not state the position cannot be compared with another.</li>
<li><strong>Use UT as the evidence.</strong> Reduction shows up in ultrasonic results; a forging with inadequate centre reduction is difficult to pass a demanding UT class consistently.</li>
</ol>

<h2>Common ways the number gets diluted</h2>
<ul>
<li>Quoting the ratio of the largest single step rather than the total reduction.</li>
<li>Forging from a size that is already close to the final section, so the nominal ratio is met but the centre never consolidates.</li>
<li>Finishing below the recommended temperature, which reduces the effective deformation without changing the arithmetic.</li>
<li>Relying on a ratio figure while skipping ultrasonic inspection of the centre region.</li>
</ul>

<h2>How we handle it</h2>
<p>Forgings are produced from a recorded input size with a documented pass sequence, and the achieved ratio is stated on the process documentation rather than assumed. Rotor and other critical parts are ultrasonically inspected piece by piece after final heat treatment, and fatigue verification is taken from the centre position. See the <a href="forged-vs-cast-flywheel-rotor.html">forged versus cast rotor note</a> for why that sampling position decides the result.</p>
""",
 "faq": [
   ("Is a higher forging ratio always better?",
    "Not unconditionally. Beyond a point the benefit plateaus, and excessive working at low temperature can introduce its own problems. What matters is that the ratio is sufficient for the centre of the section to consolidate, and that the deformation reaches the core — which is a matter of pass sequence, not only of arithmetic."),
   ("Can I verify the forging ratio from the certificate?",
    "Usually not from a standard mill certificate, which reports composition and properties. The ratio lives in the process documentation: input size, pass sequence and finished dimensions. Ask for it at enquiry stage, and confirm the definition being used."),
   ("How does forging ratio relate to ultrasonic acceptance?",
    "Adequately reduced forgings pass demanding UT classes more consistently, because porosity and segregation have been consolidated rather than redistributed. A supplier who cannot state the input size often cannot state the ratio either, and that is a reasonable signal to ask more questions."),
 ],
},
{
 "slug": "sour-service-forgings-nace-mr0175",
 "title": "Sour Service Forgings: NACE MR0175 and 4130 / 30CrMo",
 "seo_title": "Sour Service Forgings | NACE MR0175 Requirements",
 "desc": "What NACE MR0175 / ISO 15156 requires of forged manifold parts: hardness limits, chemistry control, heat treatment, and what to specify for H2S service.",
 "h1": "Sour Service Forgings: What NACE MR0175 Changes for 4130 and 30CrMo",
 "lead": "An oil and gas manifold forging ordered to the same drawing behaves differently depending on whether the service is sweet or sour. Hydrogen sulphide changes the failure mechanism from overload to cracking at stresses well below yield. That is why NACE MR0175 exists, and why it constrains hardness, chemistry and heat treatment rather than just test results.",
 "body": """
<h2>What sour service means</h2>
<p>Sour service means the process stream contains hydrogen sulphide. In wet H2S, atomic hydrogen can enter the steel and cause sulphide stress cracking (SSC) or hydrogen-induced cracking (HIC). The failure can occur at stresses far below the yield strength, sometimes within days, and it usually starts at a hard spot, a segregated band or an inclusion stringer rather than at a gross defect.</p>
<p>NACE MR0175 / ISO 15156 is the standard that defines what materials and conditions are acceptable in these environments. It is a materials standard, not a design code: it constrains the material state, and the designer remains responsible for stresses.</p>

<h2>What MR0175 actually constrains</h2>
<h3>Hardness</h3>
<p>The best-known requirement: carbon and low-alloy steels for sour service are limited to <strong>22 HRC maximum</strong> (approximately 250 HV). Hardness is used as a proxy because hard regions are more susceptible to cracking, and because hardness can be measured on the finished part. This has a direct consequence for 4130 and 42CrMo-type grades — they can meet 22 HRC comfortably, but only if the tempering treatment is controlled and the hardness is checked, not assumed.</p>

<h3>Chemistry</h3>
<p>Composition limits exist for elements that promote cracking or degrade cracking resistance. Sulphur and phosphorus are held low to limit inclusion stringers; nickel content is restricted in some material groups; and for carbon steels the carbon equivalent influences what hardness is achievable after heat treatment.</p>

<h3>Heat treatment</h3>
<p>Sour service parts are normally supplied quenched and tempered, with the tempering temperature high enough to reach the hardness limit. A part that reaches 22 HRC by rapid cooling rather than by tempering is not the same material as one that is properly tempered to that hardness, even though the number matches.</p>

<h3>Documentation</h3>
<p>The standard is verified through the certificate: chemistry, heat treatment record, hardness survey (including the location of readings), and — where required — specific HIC or SSC testing.</p>

<h2>Where 4130 and 30CrMo stand</h2>
<table class="art-table">
<thead><tr><th>Item</th><th>Typical position for 4130 / 30CrMo</th></tr></thead>
<tbody>
<tr><td>Hardness capability</td><td>Meets 22 HRC limit when quenched and tempered correctly</td></tr>
<tr><td>Strength level</td><td>High — which is exactly why hardness control must be explicit</td></tr>
<tr><td>Common forgings</td><td>Adapters, square tees, square crosses, valve bodies</td></tr>
<tr><td>Risk</td><td>Unauthorised substitution at higher strength, or hardness checked only at the surface</td></tr>
</tbody>
</table>
<p>Both grades are widely used for sour service manifold components. The failure mode to guard against is not the grade, it is the process: a heat treated to 26 HRC and certified with a single surface reading will look acceptable on the paperwork and unacceptable in the standard.</p>

<h2>What to write on the purchase order</h2>
<ul>
<li>Service condition: sour, with H2S partial pressure and the applicable MR0175 / ISO 15156 material group.</li>
<li>Hardness limit and inspection method, including the number and location of readings — surface, mid-wall, and at the bore for hollow parts.</li>
<li>Heat treatment: quenched and tempered, with the tempering temperature range stated on the record.</li>
<li>Chemistry limits for S, P, and any element restricted by the material group.</li>
<li>Supplementary testing where applicable: hardness survey, and HIC testing to NACE TM0284 if the application calls for it.</li>
<li>Ultrasonic inspection to a named standard and class — internal soundness and sour service are separate requirements, and both are needed.</li>
<li>Marking and traceability: heat number, and where required the MR0175 marking.</li>
</ul>

<h2>Two mistakes that recur</h2>
<p><strong>First: treating MR0175 as a certificate checkbox.</strong> A supplier who writes MR0175 compliant on the certificate without a hardness survey and heat treatment record has not demonstrated compliance, only asserted it.</p>
<p><strong>Second: checking hardness at the wrong place.</strong> Surface readings on a quenched and tempered forging can miss a harder sub-surface zone. For thick parts, readings should be taken through the section or at agreed locations, and stated in the report.</p>

<h2>What we supply</h2>
<p>We forge oil and gas manifold parts in 4130 / 30CrMo and related grades — adapters, square tees and square crosses for high-pressure service — quenched and tempered, with chemical, mechanical and UT reports per lot, and hardness readings at agreed locations on request. Where a customer specifies sour service, the hardness limit, chemistry and heat treatment record are documented in the certificate package. See our <a href="../oil-forgings.html">oil and gas forgings page</a>.</p>
""",
 "faq": [
   ("Is 4130 suitable for sour service?",
    "Yes, provided it is quenched and tempered to meet the hardness limit required by NACE MR0175 / ISO 15156 — typically 22 HRC maximum for carbon and low-alloy steels — and that hardness is actually verified at agreed locations. The grade is not the issue; the delivered condition is."),
   ("What hardness limit applies in sour service?",
    "For carbon and low-alloy steels the widely applied limit in MR0175 / ISO 15156 is 22 HRC maximum. Some material groups and conditions carry additional restrictions, so the applicable requirement should be taken from the standard for your specific environment and confirmed on the order."),
   ("Do I need HIC testing as well as UT?",
    "They answer different questions. Ultrasonic testing finds volumetric defects; HIC testing evaluates the steel's resistance to hydrogen-induced cracking in the specified environment. Whether HIC testing is required depends on the application and should be stated in the purchase order."),
 ],
},
]
