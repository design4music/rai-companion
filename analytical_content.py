# analytical_content.py - Complete Analytical Library
# ========================================
# I. FRAMEWORK GUIDANCE & INSTRUCTIONS
# ========================================
RAI_FRAMEWORK_CORE = {
   "definition": "RAI is a structured method for performing adequate judgment under conditions of incomplete, ambiguous, or manipulated information. It does **not** guarantee truth, neutrality, or objectivity — only a disciplined approach to **reaching adequacy**.",
   
   "epistemological_disclaimer": {
       "warning": "⚠️ **Epistemological Disclaimer:**",
       "content": "You are working with partial, often contested data in a system shaped by incentives, power, and propaganda. This tool cannot produce certainty. It can help reduce error, bias, and self-deception. Always question inputs, especially your own."
   },
   
   "core_principles": [
       "Philosophical adequacy over mechanical neutrality",
       "Epistemic humility in face of uncertainty", 
       "Structured reasoning under information manipulation",
       "Reduction of error, bias, and self-deception",
       "Questioning all inputs, especially one's own assumptions"
   ],
   
   "execution_guidance": {
       "workflow": [
           "1. Apply CL-0.1 Wisdom Premise Calibration to select relevant premises",
           "2. Choose entry point (FL/NL/SL) based on input type",
           "3. Execute relevant modules with philosophical anchoring",
           "4. Synthesize findings across levels"
       ],
       "execution_principles": [
           "Modules should be executed systematically across levels",
           "Cross-level modules provide meta-analytical oversight", 
           "Final synthesis integrates insights from all levels",
           "Trust LLM intelligence over mechanical keyword matching"
       ],
       "entry_point_logic": {
           "fact_level": "If input contains a **concrete claim**, **event**, or **disputed report**",
           "narrative_level": "If input involves **moral framing**, **cause-effect chains**, or **identity/ideology**",
           "system_level": "If input is **strategic**, **ideological**, **geopolitical**, or refers to **power dynamics**"
       }
   },
   
   "premise_integration": {
       "purpose": "Philosophical premises act as interpretive lenses to enhance deep reasoning in narrative evaluation",
       "usage_instructions": [
           "Premises serve as interpretive lenses, not rigid rules",
           "Apply contextually based on topic and complexity",
           "Multiple premises may apply to a single case",
           "Premises deepen reasoning — they do not replace evidence"
       ],
       "integration_method": "Weave premises into reasoning to guide interpretive depth — do not treat them as external citations",
       "llm_instruction": "Use the 'Philosophical Anchoring' field in each module to activate relevant Macro Premises (D1–D8). These enhance context-sensitive reasoning and support narrative adequacy over shallow consistency."
   },
   
   "analytical_standards": {
       "factual_precision": "Rigorous attention to evidence, source integrity, and verifiability",
       "narrative_coherence": "Plausible, logically consistent cause-effect chains", 
       "systemic_insight": "Recognition of incentives, power, structure, and feedback loops",
       "philosophical_adequacy": "Depth of reasoning that accounts for complexity, uncertainty, and moral dimension"
   },
   
   "quality_criteria": {
       "adequacy_over_neutrality": "Choose depth and contextual judgment over surface neutrality",
       "epistemic_humility": "Clearly acknowledge limits of knowledge and uncertainty",
       "structural_awareness": "Include analysis of systems, not just isolated claims",
       "temporal_sensitivity": "Incorporate historical roots and long-term implications"
   },
   
   "warning_systems": {
       "bias_detection": "Continuously monitor for cognitive or narrative bias",
       "manipulation_awareness": "Identify signs of strategic framing or omission",
       "certainty_restraint": "Avoid unjustified certainty in the presence of ambiguity"
   },
   
   "output_requirements": {
       "epistemic_transparency": [
           "Acknowledge sources and their limitations",
           "Flag areas of uncertainty or contested information", 
           "Indicate confidence levels for different claims",
           "Suggest areas for further investigation"
       ],
       "philosophical_integration": [
           "Weave relevant premises into reasoning naturally",
           "Demonstrate adequate depth rather than surface analysis",
           "Show awareness of structural and systemic factors",
           "Maintain focus on adequacy over acceptability"
       ]
   }
}

# ========================================  
# II. PREMISE LIBRARY
# ========================================
PREMISE_LIBRARY = {
    "CL-0.1": {
        "name": "Wisdom Premise Calibration",
        "purpose": "Dynamically align analysis with relevant Macro Premises by identifying high-level contextual patterns such as power asymmetry, systemic conflict, narrative manipulation, or historical trauma.",
        "core_questions": [
            "Does the narrative involve geopolitics, regime change, civil unrest, or mass communication?",
            "Are there signs of systemic conflict (e.g. war, sanctions, media battles, strategic alliances)?",
            "Are historical legacies or ethical framing being used to justify action or judgment?",
            "Do patterns of deception, denial, or simplification mask broader structural dynamics?"
        ],
        "outputs": [
            "🧠 Macro Premise selection recommendations",
            "⚡ Wisdom Overlay activation trigger",
            "🎯 Contextual pattern identification",
            "📊 Complexity and strategic significance assessment"
        ],
        "wisdom_injected": [
            "Context is the compass of wisdom.",
            "Strategic patterns repeat across domains.",
            "Complexity demands philosophical depth."
        ],
        "philosophical_anchoring": ["D2.1", "D3.3", "D5.1", "D7.1"]
    },
    "dimensions": {
        "D1": {
            "name": "Power & Governance",
            "description": "Political systems, governance, legitimacy, transitions of power",
            "premises": {
                "D1.1": {
                    "title": "Power is rarely surrendered; it is redistributed through ritual, consensus, or coercion",
                    "content": "In all functioning systems—democratic, autocratic, or hybrid—true power shifts occur under one of three conditions: Elite consensus to preserve stability, External pressure or control, or Systemic fracture or collapse. Elections and constitutional processes are often choreographed simulations to legitimize decisions already negotiated behind closed doors. Where elite unity breaks down or external actors intervene, transitions become turbulent, delayed, or violent.",
                    "rooted_in": "Elite Theory (Pareto, Mosca), Marxist Political Economy (false pluralism), Arendt (power as negotiated legitimacy)"
                },
                "D1.2": {
                    "title": "Political actors emerge from their cultural substrate",
                    "content": "Politicians are neither a separate species nor inherently corrupt—they reflect the ambitions, fears, and incentives of their societal base. While some act from self-interest, others assume genuine stewardship of national projects. Systems produce the leaders they enable, and demonizing individuals obscures structural flaws or popular complicity.",
                    "rooted_in": "Arendtian thought, democratic realism, systems view of leadership emergence"
                },
                "D1.3": {
                    "title": "Power is sustained through economic architecture",
                    "content": "Control over capital flows, debt, resource distribution, and media ownership often underlies political stability more than formal institutions or laws. Ownership replaces force, creating systemic compliance even in \"free\" societies.",
                    "rooted_in": "Marxist thought, Chomsky's propaganda model, elite wealth consolidation"
                }
            }
        },
        "D2": {
            "name": "Geopolitical Order & Conflict",
            "description": "Global hierarchy, war, asymmetry, strategic interests",
            "premises": {
                "D2.1": {
                    "title": "A few powers shape the planetary game",
                    "content": "Despite the appearance of multilateralism, geopolitical outcomes are determined by a small number of dominant states or blocs. Smaller actors either align with these poles, operate as regional proxies, or are marginalized. When evaluating claims of agency or independence in global affairs, it's worth asking: who truly sets the terms of the conversation?",
                    "rooted_in": "Realist IR theory, unipolar/multipolar models, neocolonial continuity"
                },
                "D2.2": {
                    "title": "Systemic war is ongoing, with kinetic conflict as its loudest symptom",
                    "content": "Economic pressure, cyberattacks, and narrative domination are integral tools of modern conflict. Physical war is no longer the beginning of conflict, but its explosion point. The war is on.",
                    "rooted_in": "Hybrid warfare doctrine, Russian \"Gerasimov doctrine,\" Western full-spectrum dominance strategies"
                },
                "D2.3": {
                    "title": "Neutrality becomes illusion in systemic conflict",
                    "content": "In high-stakes global competition, all states are drawn into alignment, either through dependence, coercion, or survival instinct. True neutrality is impossible in a deeply interconnected world.",
                    "rooted_in": "Dependency theory, proxy warfare patterns, sanctions regimes"
                },
                "D2.4": {
                    "title": "Nuclear weapons enforce adult behavior through existential fear",
                    "content": "The doctrine of Mutual Assured Destruction (MAD) has replaced idealism as the real guarantor of peace. Disarmament is noble, but premature. Without existential threat, aggressive competition would likely lead to catastrophe.",
                    "rooted_in": "Cold War logic, deterrence theory, game theory simulations"
                },
                "D2.5": {
                    "title": "War is waged beneath the surface through deception and engineered ambiguity",
                    "content": "Modern power projection often hides behind peace initiatives, democratic rhetoric, or defensive postures. Narratives become masks for strategic aims, enabling operations without triggering open conflict.",
                    "rooted_in": "Sun Tzu (\"all warfare is based on deception\"), Clausewitz, Cold War covert operations, modern hybrid warfare theory"
                },
                "D2.6": {
                    "title": "Geopolitical behavior is shaped by enduring asymmetries",
                    "content": "Power disparities in media reach, military capabilities, economic leverage, human resources, or technological infrastructure define what actors can realistically do.",
                    "rooted_in": "Asymmetric warfare theory, cyber power dynamics, realist IR, soft-power analysis"
                },
                "D2.7": {
                    "title": "Strategic interests are survival logic dressed in moral clothing",
                    "content": "Behind every noble speech about peace and values is a spreadsheet calculating market access, resource control, and strategic leverage. States act not out of virtue, but necessity—or appetite. Moral narratives—freedom, peace, democracy—are often retrofitted onto strategic decisions.",
                    "rooted_in": "Strategic realism, Mearsheimer, critical geopolitics, constructivist IR"
                }
            }
        },
        "D3": {
            "name": "Information & Perception",
            "description": "Epistemology, narrative warfare, cognitive control",
            "premises": {
                "D3.1": {
                    "title": "Information is a commodity in peace and a weapon in systemic conflict",
                    "content": "In peacetime, information flows are monetized; in systemic conflict, they are weaponized. Media must be controlled—whether through ownership, funding, surveillance, or subtle incentivization—by those with political or economic stakes. Mechanisms vary by system and culture, but truly \"free\" or \"independent\" media is a functional myth, not a structural reality.",
                    "rooted_in": "Chomsky's propaganda model, Soviet \"information front\" strategy, CIA media infiltration, postmodern media studies"
                },
                "D3.2": {
                    "title": "Censorship and visibility are asymmetric tools",
                    "content": "Control over digital infrastructure—platforms, algorithms, recommendation engines, content policies—enables nonlinear narrative dominance. What is suppressed is often less important than what is invisibly sidelined.",
                    "rooted_in": "Surveillance capitalism, Chinese content regulation models, shadow banning and algorithmic gatekeeping"
                },
                "D3.3": {
                    "title": "Perception is power",
                    "content": "Legitimacy, victimhood, and moral high ground are not just narratives—they are operational assets. Winning the story often has greater strategic value than winning the terrain. Modern information warfare includes memetic injection, coordinated emotional framing, information flooding, and virality engineering. Conflicts are now fought not only in trenches, but in timelines.",
                    "rooted_in": "Information warfare doctrine, soft power theory, international law and public opinion asymmetry"
                },
                "D3.4": {
                    "title": "Thought policing outperforms censorship",
                    "content": "When populations internalize the boundaries of acceptable thought, external repression becomes redundant. Self-censorship, social penalty, and digital panopticism are more effective than coercive force.",
                    "rooted_in": "Foucault (panopticon), Soviet self-criticism campaigns, cancel culture dynamics"
                },
                "D3.5": {
                    "title": "Large-scale protests are rarely spontaneous",
                    "content": "Mass participation may appear organic, but major movements that gain traction nearly always rest on pre-existing infrastructure: trained organizers, aligned institutions, sympathetic media, and international funding streams. Spontaneity is often facilitated by invisible hands, especially in contested or transitional regimes.",
                    "rooted_in": "Color revolution manuals, NGO funding patterns, digital mobilization studies"
                }
            }
        },
        "D4": {
            "name": "Civilization & Culture",
            "description": "Identity, memory, inherited trauma, ideological formation",
            "premises": {
                "D4.1": {
                    "title": "Cultural self-image distorts memory",
                    "content": "Societies tend to idealize their past, suppressing atrocities, defeats, or failures. Collective memory is selectively curated through trauma editing, symbolic purification, and ritualized storytelling in education, monuments, and national holidays. What is forgotten is as politically significant as what is remembered.",
                    "rooted_in": "Maurice Halbwachs (collective memory), Benedict Anderson (imagined communities), postcolonial theory, Arendt on narrative and history"
                },
                "D4.2": {
                    "title": "Victimhood is political capital",
                    "content": "Groups and nations frame themselves as historical victims to gain legitimacy, immunize against criticism, and mobilize internal cohesion or international sympathy. These narratives often blur genuine trauma with instrumental storytelling, turning suffering into a shield or bargaining chip.",
                    "rooted_in": "Identity politics theory, Pierre Bourdieu (symbolic capital), critical discourse analysis"
                },
                "D4.3": {
                    "title": "Civilizations pursue different visions of success",
                    "content": "All cultures strive for stability, continuity, and influence—but their definitions of success vary profoundly. Some prioritize expansion or technological progress; others value harmony, survival, or spiritual legacy. Strategies emerge from deep historical, geographic, and cultural encoding. Judging them by a single universal standard often reflects ideological projection, not objective analysis.",
                    "rooted_in": "Cultural relativism, Huntington (civilizational paradigms), Wittgenstein (language games and worldview)"
                },
                "D4.4": {
                    "title": "Cultural soft power is a vector of dominance",
                    "content": "Narratives travel through film, entertainment, humanitarian aid, and globalized education. Cultural output becomes a carrier of ideology, shaping aspiration, moral hierarchies, and political alignment. Empires no longer need missionaries—they have platforms.",
                    "rooted_in": "Gramsci (cultural hegemony), Joseph Nye (soft power), McLuhan (the medium is the message), Foucault (discursive regimes)"
                },
                "D4.5": {
                    "title": "Culture encodes strategy",
                    "content": "Deep-seated cultural traits—whether collectivist or individualist, honor-based or legality-based—shape behavior in diplomacy, warfare, and negotiation. What seems irrational to outsiders may follow a coherent internal logic. Understanding this encoding is essential for accurate geopolitical or narrative interpretation.",
                    "rooted_in": "Cultural anthropology (Geertz), strategic theory, Hofstede's dimensions of culture, structuralist ethnography"
                }
            }
        },
        "D5": {
            "name": "System Dynamics & Complexity",
            "description": "Non-linearity, feedback loops, control systems, systemic risk",
            "premises": {
                "D5.1": {
                    "title": "Systems behave through feedback, not intention",
                    "content": "Outcomes in complex systems are not directly caused by intentions but emerge from interactions between variables, delays, and feedback loops (both positive and negative). Even rational actors are swept into patterns beyond their awareness or control. Linear explanations almost always miss the real cause.",
                    "rooted_in": "Cybernetics (Wiener), systems thinking (Meadows, Senge), complexity theory"
                },
                "D5.2": {
                    "title": "Fragile systems suppress dissent",
                    "content": "When systems lack flexibility or redundancy, they tighten control in response to perceived threats. Repression is not always ideological—it is often a survival reflex in systems approaching failure. The more brittle the system, the more it fears even small disruptions.",
                    "rooted_in": "Taleb (fragility vs. antifragility), systems failure analysis, totalitarianism studies (Arendt)"
                },
                "D5.3": {
                    "title": "Stability depends on controlled transparency",
                    "content": "No system can operate in full opacity—or in full daylight. Long-term resilience often requires a managed flow of visibility: enough to maintain legitimacy, but not so much that its contradictions become uncontrollable. \"Openness\" is always calibrated.",
                    "rooted_in": "Habermas (legitimacy through discourse), realist governance theory, sociological systems theory (Luhmann)"
                },
                "D5.4": {
                    "title": "Self-correction requires pressure valves",
                    "content": "Resilient systems create mechanisms of controlled release: courts, protests, satire, journalism. When these are co-opted or blocked, pressure accumulates and can explode. Soft opposition is a structural necessity, not a luxury.",
                    "rooted_in": "Political sociology, authoritarian resilience studies, psycho-political tension models"
                },
                "D5.5": {
                    "title": "Narratives are the software of systems",
                    "content": "The shared stories people believe about their system (e.g. meritocracy, unity, threat) enable it to function. When narratives degrade, the system's behavioral code becomes corrupted. Crises of legitimacy are often preceded by narrative entropy.",
                    "rooted_in": "Constructivism, Arendt (truth and politics), post-structuralism, semiotics"
                }
            }
        },
        "D6": {
            "name": "Ethics & Judgment",
            "description": "Moral framing, ambiguity, pluralism",
            "premises": {
                "D6.1": {
                    "title": "Multiple value systems can be valid within their own logic",
                    "content": "Different ethical traditions—religious, cultural, strategic—can produce conflicting judgments without either being objectively false. What is \"just\" in one worldview may be \"barbaric\" in another. Ethical analysis requires context, not universalization.",
                    "rooted_in": "Moral relativism, anthropological pluralism, Alasdair MacIntyre"
                },
                "D6.2": {
                    "title": "Moral certainty often masks geopolitical or institutional interests",
                    "content": "The language of \"values\" and \"human rights\" is frequently used to cloak strategic motives. Claiming virtue becomes a tool of leverage, especially when paired with sanctions, military action, or selective outrage.",
                    "rooted_in": "Critical theory, realpolitik ethics, postcolonial critique"
                },
                "D6.3": {
                    "title": "The oppressed often inherit and reenact the logic of the oppressor",
                    "content": "Those who once suffered injustice may replicate coercive systems when power shifts. Victimhood does not guarantee virtue, and sympathy should never replace structural scrutiny.",
                    "rooted_in": "Frantz Fanon, Nietzschean critique of resentment, historical cycles of violence"
                },
                "D6.4": {
                    "title": "Democratic decay often originates from the people, not just elites",
                    "content": "While corruption and manipulation matter, mass apathy, fear, and ignorance can also erode democratic life. When the public ceases to demand virtue, representation becomes spectacle.",
                    "rooted_in": "Tocqueville, democratic realism, civic republicanism"
                },
                "D6.5": {
                    "title": "Political virtue is often the retroactive moralization of success",
                    "content": "History is written by winners, and legitimacy is often post-facto storytelling. What is framed as noble leadership may be little more than effective domination rewritten in moral terms.",
                    "rooted_in": "Foucault, Arendt (\"success as the ultimate justification\"), genealogical ethics"
                },
                "D6.6": {
                    "title": "Hypocrisy is not an anomaly, but a structural feature of moral discourse",
                    "content": "Nations, institutions, and individuals often fail to meet the standards they preach—not merely from weakness, but because moral language is strategically deployed to manage perception, not guide consistent behavior. Hypocrisy persists because it works.",
                    "rooted_in": "Cynical realism, Machiavelli, Reinhold Niebuhr (\"moral man, immoral society\"), Baudrillard (simulacra of virtue)"
                }
            }
        },
        "D7": {
            "name": "Temporal Awareness & Strategic Foresight",
            "description": "Historical cycles, long-term risk, delayed consequence",
            "premises": {
                "D7.1": {
                    "title": "Historical context is essential for understanding motivation",
                    "content": "Current decisions reflect accumulated trauma, inherited grievances, and strategic memory. Nations and actors often pursue goals laid down by events decades—or centuries—earlier. Analyzing current actions without their temporal roots produces shallow or false interpretations.",
                    "rooted_in": "Historical institutionalism, psychohistory, longue durée (Braudel), postcolonial theory"
                },
                "D7.2": {
                    "title": "Delayed outcomes are often more impactful than immediate ones",
                    "content": "What seems like success in the short term may erode legitimacy or stability over time. Systems have latency, and interventions often unleash feedback loops that manifest far later. Strategic judgment demands temporal patience.",
                    "rooted_in": "Systems theory, unintended consequences, deep forecasting models"
                },
                "D7.3": {
                    "title": "History rewards the effective, not the grateful",
                    "content": "There is no durable currency of gratitude in international relations or political history. Alliances shift based on interest, not memory. Attempts to extract loyalty based on past aid or sacrifice usually fail.",
                    "rooted_in": "Realism in IR, Machiavellian statecraft, historical patterns of alliance reversal"
                },
                "D7.4": {
                    "title": "Civilizations rise and fall in cycles",
                    "content": "No system lasts forever. Civilizations experience arcs of emergence, dominance, stagnation, and collapse. Denial of this cycle leads to strategic complacency and hubris. Those who believe they are immune to decline are usually entering it.",
                    "rooted_in": "Toynbee, Spengler, cyclical history theory, political entropy models"
                },
                "D7.5": {
                    "title": "The future is colonized by today's narratives",
                    "content": "The stories we tell about the future—progress, collapse, justice, revenge—shape policy, science, investment, and war. Competing visions of the future often drive present action more than actual planning does.",
                    "rooted_in": "Strategic foresight, future studies, narrative theory, ideological projection"
                },
                "D7.6": {
                    "title": "Strategic actors plan in decades; reactive actors respond in headlines",
                    "content": "Global competition rewards those who think beyond the electoral cycle or news cycle. Systems with long memory and long-range planning (e.g. intelligence agencies, imperial bureaucracies) shape outcomes more decisively than populist turbulence.",
                    "rooted_in": "Geostrategy, elite continuity theory, technocracy vs. populism"
                },
                "D7.7": {
                    "title": "Delays between cause and effect conceal responsibility",
                    "content": "When consequences unfold years later, those who set events in motion often escape accountability. Strategic manipulation benefits from this delay, enabling actors to externalize blame while pursuing short-term gain.",
                    "rooted_in": "Moral hazard, plausible deniability, delayed causality in complex systems"
                }
            }
        },
        "D8": {
            "name": "Political Economy & Resource Power",
            "description": "Capital flows, labor dynamics, ownership structures, resource control",
            "premises": {
                "D8.1": {
                    "title": "Economic power precedes and shapes political outcomes",
                    "content": "The distribution of capital, land, labor, and credit forms the invisible scaffolding beneath political institutions. Governance structures often emerge as reflections of dominant economic interests, whether feudal landowners, industrial capitalists, or technocratic financial elites. Ideological language tends to mask economic control mechanisms.",
                    "rooted_in": "Marxist base/superstructure theory, elite theory, oligarchic drift"
                },
                "D8.2": {
                    "title": "Class remains a functional reality beneath changing labels",
                    "content": "Despite rhetorical progress or rebranding, societies continue to stratify along lines of control over productive assets. Whether under capitalism, state socialism, or mixed regimes, there is always a division between those who own, those who manage, and those who labor.",
                    "rooted_in": "Neo-Marxist analysis, Piketty's wealth concentration, managerial capitalism critiques"
                },
                "D8.3": {
                    "title": "Resource dependencies define strategic behavior",
                    "content": "Access to energy, rare materials, food, and water determines national security and foreign policy alignment. States will violate ethical norms or destabilize entire regions to secure such resources or protect access routes (e.g., pipelines, shipping lanes, digital infrastructure).",
                    "rooted_in": "Resource geopolitics, petrostate theory, dependency theory"
                },
                "D8.4": {
                    "title": "Debt is a tool of control, not just finance",
                    "content": "Public and private debt create long-term dependency structures. Lenders can shape policy, impose austerity, and dictate reforms under the guise of fiscal discipline or development assistance. Sovereign debt crisis is often a political weapon, not just an economic accident.",
                    "rooted_in": "IMF/World Bank critiques, neocolonial analysis, Graeber's \"Debt: The First 5,000 Years\""
                },
                "D8.5": {
                    "title": "Technology is not neutral—it encodes power relations",
                    "content": "Digital platforms, algorithmic finance, and data monopolies allow unprecedented economic concentration. The illusion of decentralization often masks deeper centralization in the hands of those who build and own the infrastructure.",
                    "rooted_in": "Platform capitalism, surveillance economy, Shoshana Zuboff's work on data power"
                },
                "D8.6": {
                    "title": "Labor is globalized, devalued, and fragmented",
                    "content": "In a globalized economy, labor no longer negotiates from a national base. Jobs are offshored, gigified, or automated. As collective bargaining weakens, workers become interchangeable, and economic insecurity becomes a tool of control. \"Freedom of labor\" often means freedom from protection.",
                    "rooted_in": "Global labor studies, Braverman's deskilling theory, Standing's \"precariat\" class"
                },
                "D8.7": {
                    "title": "Automation shifts power from labor to capital",
                    "content": "As machines replace human labor, value concentrates around intellectual property, infrastructure ownership, and data extraction. Automation doesn't eliminate labor—it transforms it into invisible maintenance and algorithmic obedience. The promise of liberation often masks deeper alienation.",
                    "rooted_in": "Marx's \"general intellect,\" post-Fordist theory, AI-driven labor economics"
                },
                "D8.8": {
                    "title": "Supply chains are strategic weapons",
                    "content": "Global trade networks are not just economic artifacts—they are levers of pressure in geopolitical struggle. Countries that control logistics chokepoints, manufacturing hubs, or rare-earth refining can extract political concessions without firing a shot. Resilience narratives often hide weaponization strategies.",
                    "rooted_in": "Global supply chain theory, U.S.–China tech war, economic statecraft"
                }
            }
        }
    }
}

# ========================================
# III. MODULE LIBRARY  
# ========================================
MODULE_LIBRARY = {
    "CL": {
        "name": "Cross-Level Meta Modules",
        "purpose": "Handle input transformation, framing awareness, asymmetry checks, and value clarification",
        "modules": {
            "CL-0": {
                "name": "Input Clarity and Narrative Normalization",
                "purpose": "Pre-process user input to normalize vague, slangy, emotionally charged, or overly broad claims into analyzable form — while preserving intended meaning.",
                "core_questions": [
                    "Is the input a question, a claim, or a loosely formed opinion?",
                    "Does it contain emotional, tribal, or rhetorical noise?",
                    "Can it be split into distinct factual, narrative, or systemic components?",
                    "How can the input be reframed to test its adequacy without distorting intent?"
                ],
                "outputs": [
                    "🧹 Cleaned-up, analyzable version of input",
                    "🔍 Type classification: Factual Claim / Narrative / System Premise / Mixed",
                    "🎭 Style flags: Slang, Hyperbole, Mockery, etc.",
                    "🧭 Ready-for-analysis reformulation prompt"
                ],
                "wisdom_injected": [
                    "Every thought deserves a second draft.",
                    "Emotional noise is not a signal.",
                    "Honor the intent. Clean the form."
                ],
                "philosophical_anchoring": ["D1.1", "D1.4", "D6.2"]
            },
            "CL-1": {
                "name": "Narrative Logic Compression",
                "purpose": "Trace how individual facts are being linked into narrative arcs — and identify compression, distortion, or omission in that linkage.",
                "core_questions": [
                    "Are facts cherry-picked or overpacked?",
                    "Are connections between events natural or forced?",
                    "Are narrative arcs formed by implication instead of logic?",
                    "What causal assumptions are embedded in the story structure?"
                ],
                "outputs": [
                    "🪞 Narrative compression warning",
                    "🔗 Fact-to-Meaning linkage map",
                    "⚠️ Omissions or false link alert",
                    "🧭 Alternative narrative construction possibilities"
                ],
                "wisdom_injected": [
                    "Narrative is the space between facts.",
                    "Compression is the birthplace of distortion.",
                    "What connects may also disconnect."
                ],
                "philosophical_anchoring": ["D1.3", "D4.1", "D7.2"]
            },
            "CL-2": {
                "name": "Epistemic Load Balance",
                "purpose": "Test how knowledge burdens are distributed: What is assumed vs. what is proven? What must the audience infer, accept, or ignore?",
                "core_questions": [
                    "What 'common sense' is assumed?",
                    "Are any critical elements left implicit?",
                    "Does the burden of proof fall unfairly on one side?",
                    "What knowledge gaps are being papered over?"
                ],
                "outputs": [
                    "🧠 Assumption audit",
                    "⚖️ Burden imbalance detection",
                    "📚 Hidden inference recovery prompt",
                    "🕳️ Knowledge gap identification"
                ],
                "wisdom_injected": [
                    "What's not said may cost more than what is.",
                    "A rigged narrative hides its load.",
                    "Assumptions are the invisible architecture of argument."
                ],
                "philosophical_anchoring": ["D2.2", "D1.4", "D6.6"]
            },
            "CL-3": {
                "name": "Narrative Stack Tracking",
                "purpose": "Map layered or nested narratives — how facts support storylines, which support ideologies, which support strategic goals.",
                "core_questions": [
                    "What deeper story does this surface claim support?",
                    "How many layers deep does the logic go?",
                    "Are meta-narratives functioning as shields or amplifiers?",
                    "Which narrative layer is doing the real work?"
                ],
                "outputs": [
                    "🧩 Narrative layer diagram",
                    "🧠 Ideology alignment marker",
                    "🧭 Strategic function guess",
                    "🔍 Meta-narrative identification"
                ],
                "wisdom_injected": [
                    "Some stories wear other stories like armor.",
                    "The first claim is often the bait.",
                    "Depth reveals direction."
                ],
                "philosophical_anchoring": ["D4.2", "D6.3", "D7.1"]
            },
            "CL-4": {
                "name": "Moral and Strategic Fusion Detection",
                "purpose": "Identify moments where moral language is fused with strategic logic to mask real motivations or trigger tribal response.",
                "core_questions": [
                    "Are moral claims used to justify strategic actions?",
                    "Is moral framing exaggerated to obscure realism?",
                    "What would the statement sound like if stripped of moral charge?",
                    "Does virtue signaling serve strategic functions?"
                ],
                "outputs": [
                    "⚔️ Moral-strategic blend alert",
                    "🧪 Neutral reframe prompt",
                    "🎭 Tribal trigger identification",
                    "🔍 Strategic interest revelation"
                ],
                "wisdom_injected": [
                    "Moral words win wars — on screens.",
                    "Look where the virtue points — then follow the money.",
                    "Strategic necessity wears moral clothing."
                ],
                "philosophical_anchoring": ["D6.2", "D6.4", "D6.5"]
            },
            "CL-5": {
                "name": "Evaluative Symmetry Enforcement",
                "purpose": "Ensure actors, events, or claims are judged by consistent standards — even if they belong to different camps, cultures, or ideologies.",
                "core_questions": [
                    "Would this action be praised or condemned if done by the other side?",
                    "Are similar acts being framed in opposite ways?",
                    "Is the framework itself being bent to spare allies?",
                    "What would neutral evaluation look like?"
                ],
                "outputs": [
                    "♻️ Mirror standard test result",
                    "🔄 Narrative double standard flag",
                    "🧭 Neutral phrasing suggestion",
                    "⚖️ Consistency evaluation score"
                ],
                "wisdom_injected": [
                    "If it's wrong for them, it's wrong for you.",
                    "Truth wears no uniform.",
                    "Consistency is the test of principle."
                ],
                "philosophical_anchoring": ["D2.1", "D6.1", "D3.3"]
            }
        }
    },
    "FL": {
        "name": "Fact-Level Modules",
        "purpose": "Analyze factual structure, traceability, manipulation, and reliability",
        "modules": {
            "FL-1": {
                "name": "Claim Clarity and Anchoring",
                "purpose": "Isolate and verify the core factual claims. Ensure each is specific, testable, and anchored in time/place.",
                "core_questions": [
                    "What exactly is being claimed — and is it stated as a fact?",
                    "Is it time-stamped and location-bound?",
                    "Is it observable or measurable?",
                    "Is it distorted by metaphor or emotional language?"
                ],
                "outputs": [
                    "✅ Cleaned factual claims (rephrased neutrally)",
                    "⏳ Timestamp and location attached (or flagged as missing)",
                    "🧪 Verifiability score (High / Medium / Low)",
                    "⚠️ Manipulation risk note (if present)"
                ],
                "wisdom_injected": [
                    "Epistemic humility: Flag unverifiables, don't guess.",
                    "Linguistic precision: Strip rhetoric, keep signal.",
                    "Facts live in time and space."
                ],
                "philosophical_anchoring": ["D1.1", "D1.2", "D2.1"]
            },
            "FL-2": {
                "name": "Asymmetrical Amplification Awareness",
                "purpose": "Detect whether claims are being unnaturally promoted or suppressed due to information control asymmetries.",
                "core_questions": [
                    "Is the claim widely echoed across high-power media or ignored despite relevance?",
                    "Are opposing versions of the claim visible and credible?",
                    "Who has the megaphone? Who has been silenced?",
                    "What explains the amplification pattern?"
                ],
                "outputs": [
                    "📊 Amplification score (High / Medium / Low)",
                    "🔍 Visibility asymmetry indicator",
                    "⚠️ Suppression likelihood flag",
                    "📡 Media coordination assessment"
                ],
                "wisdom_injected": [
                    "What is repeated is not necessarily true.",
                    "Silence is often manufactured.",
                    "Volume reveals agenda."
                ],
                "philosophical_anchoring": ["D3.2", "D5.1", "D6.6"]
            },
            "FL-3": {
                "name": "Source Independence Audit (w/ Pattern Recognition)",
                "purpose": "Evaluate the independence, diversity, and reliability of sources cited or implied. Spot coordinated narratives or echo chambers.",
                "core_questions": [
                    "Are the cited sources directly involved, third-party, or anonymous?",
                    "Is there over-reliance on aligned actors?",
                    "Do citations originate from power-linked networks (gov, media groups, NGOs)?",
                    "What does the source ecosystem reveal about the claim?"
                ],
                "outputs": [
                    "🧾 Source lineage (firsthand / allied / recycled)",
                    "🌐 Source diversity index",
                    "🧭 Pattern repetition alert (e.g., 3+ citations back to same pool)",
                    "🔍 Independence assessment score"
                ],
                "wisdom_injected": [
                    "Power speaks in chorus.",
                    "Independence is not a brand, it's a structure.",
                    "Follow the source chain to find the source."
                ],
                "philosophical_anchoring": ["D2.3", "D5.2", "D3.2"]
            },
            "FL-4": {
                "name": "Strategic Relevance and Selection",
                "purpose": "Evaluate whether a fact is strategically chosen to steer perception or obscure larger realities.",
                "core_questions": [
                    "Is the fact central to the story or a distraction?",
                    "Would omitting this fact mislead? Would adding a suppressed one clarify?",
                    "Is it cherry-picked to create a false narrative?",
                    "What does the selection pattern reveal about intent?"
                ],
                "outputs": [
                    "🔍 Strategic distortion score",
                    "🔀 Relevance contrast map (what was said vs. what could've been)",
                    "🎯 Selection pattern analysis",
                    "⚠️ Cherry-picking alert"
                ],
                "wisdom_injected": [
                    "The truth may be in what's unsaid.",
                    "Strategic omission is the most elegant lie.",
                    "Selection reveals intention."
                ],
                "philosophical_anchoring": ["D4.2", "D7.2", "D8.2"]
            },
            "FL-5": {
                "name": "Scale and Proportion Calibration",
                "purpose": "Prevent inflation or minimization of facts through poor scale framing.",
                "core_questions": [
                    "Is this fact being framed as exceptional or representative?",
                    "Are numbers proportionate or manipulated by percent, scope, or baseline?",
                    "Would this framing hold across equivalent cases?",
                    "What does proper contextualization reveal?"
                ],
                "outputs": [
                    "📏 Scale misrepresentation index",
                    "⚖️ Equivalent comparison prompts",
                    "📊 Proportion analysis",
                    "🧭 Context calibration suggestions"
                ],
                "wisdom_injected": [
                    "Big data can lie small, and small facts can scream.",
                    "Context is the compass of honesty.",
                    "Scale without context is manipulation."
                ],
                "philosophical_anchoring": ["D1.2", "D1.3", "D8.1"]
            },
            "FL-6": {
                "name": "Neglected Primary Speech Recognition",
                "purpose": "Identify whether primary actor statements have been omitted or misrepresented.",
                "core_questions": [
                    "Has the subject of the claim spoken directly on the matter?",
                    "Are those statements missing, cherry-picked, or distorted?",
                    "What would direct quotes reveal that paraphrases hide?",
                    "Why might primary speech be avoided or filtered?"
                ],
                "outputs": [
                    "🎙️ Key actor speech alignment indicator",
                    "🧭 Primary statement search prompt",
                    "📝 Quote vs. paraphrase analysis",
                    "🔍 Speech omission pattern detection"
                ],
                "wisdom_injected": [
                    "Let them speak — then check the echo.",
                    "Silencing someone by paraphrase is still silencing.",
                    "Primary speech reveals primary intent."
                ],
                "philosophical_anchoring": ["D2.3", "D3.1", "D6.1"]
            },
            "FL-7": {
                "name": "Risk Context Adjustment",
                "purpose": "Tune skepticism based on stakes. Differentiate casual errors from high-stakes manipulations.",
                "core_questions": [
                    "Is this claim embedded in a low-risk or high-risk topic (e.g., war, finance, biopolitics)?",
                    "Do the consequences of falsehood justify higher scrutiny?",
                    "What interests are served by belief or disbelief?",
                    "How does risk level affect evidentiary standards?"
                ],
                "outputs": [
                    "⚠️ Risk-weighted skepticism multiplier",
                    "🔍 Elevation trigger (send to system-level for manipulation analysis)",
                    "📊 Stakes assessment matrix",
                    "🎯 Interest alignment analysis"
                ],
                "wisdom_injected": [
                    "The higher the cost of the lie, the deeper you dig.",
                    "Low-risk truths may not deserve your time. High-risk lies always do.",
                    "Stakes determine standards."
                ],
                "philosophical_anchoring": ["D7.2", "D8.3", "D8.5"]
            },
            "FL-8": {
                "name": "Time & Place Anchoring",
                "purpose": "Ensure all factual claims are tied to specific, verifiable moments and locations.",
                "core_questions": [
                    "Is there a clear timestamp and identifiable location?",
                    "Are those consistent with known records or conflicting claims?",
                    "Is ambiguity being used to protect from accountability?",
                    "What does temporal-spatial precision reveal or conceal?"
                ],
                "outputs": [
                    "🗓️ Anchored claim string (e.g., \"On April 12, near Kharkiv...\")",
                    "📍 Geo-temporal alignment map",
                    "⚠️ Vagueness / contradiction alert",
                    "🔍 Accountability avoidance indicator"
                ],
                "wisdom_injected": [
                    "Truth lives in time. Lies float.",
                    "No fact should be homeless.",
                    "Precision prevents manipulation."
                ],
                "philosophical_anchoring": ["D1.2", "D7.1", "D7.4"]
            },
            "FL-9": {
                "name": "Toxic Label Audit",
                "purpose": "Detect and neutralize judgment-distorting terms like \"conspiracy theory,\" \"populist,\" or \"authoritarian regime\" that may preempt empirical evaluation.",
                "core_questions": [
                    "Is the claim being disqualified due to who says it rather than what is said?",
                    "Are rhetorical labels replacing evidence or logic?",
                    "Does the claim violate reality, or just elite preferences?",
                    "What happens when we strip away the labels and examine the substance?"
                ],
                "outputs": [
                    "🧼 Label Alert (flagged terms: conspiracy, regime, populist, far-right, misinformation, etc.)",
                    "🔍 Rephrased neutral version for evaluation",
                    "⚖️ Disqualification Warning (if rhetorical judgment exceeds factual basis)",
                    "🎭 Label function analysis (dismissal vs. description)"
                ],
                "wisdom_injected": [
                    "Adequacy trumps acceptability.",
                    "A claim's origin does not determine its validity.",
                    "Ideological hygiene is not a proxy for truth."
                ],
                "philosophical_anchoring": ["D2.1", "D3.3", "D6.5"]
            }
        }
    },
    "NL": {
        "name": "Narrative-Level Modules",
        "purpose": "Explore causal logic, coherence, and how identity, memory, and framing shape meaning",
        "modules": {
            "NL-1": {
                "name": "Cause-Effect Chain Analysis",
                "purpose": "Evaluate whether cause-and-effect logic is coherent, plausible, and properly sequenced — with careful attention to where the chain begins.",
                "core_questions": [
                    "Are causes and consequences logically connected?",
                    "Is the sequence clear, or manipulated to create confusion or moral reversal?",
                    "Are plausible alternative causes or interpretations acknowledged?",
                    "⚠️ Start-Point Bias Check: Is the chosen starting point contested or strategically selected? Are earlier causes being ignored?"
                ],
                "outputs": [
                    "🔗 Coherence score for the causal chain",
                    "🧭 Alternate origin marker (\"Some narratives begin the chain at...\")",
                    "⚖️ Asymmetry alert (if causality is framed one-sidedly)"
                ],
                "wisdom_injected": [
                    "Causality is not a straight line — it's a choice of lens.",
                    "Every chain has a beginning — but not every beginning is the truth.",
                    "The origin you choose is the side you've chosen."
                ],
                "philosophical_anchoring": ["D4.1", "D4.3", "D7.2"]
            },        
            "NL-2": {
                "name": "Narrative Plausibility & Internal Coherence",
                "purpose": "Test the story's internal logic, character consistency, and plausibility without external verification.",
                "core_questions": [
                    "Do events follow naturally within the narrative?",
                    "Are motivations consistent with known actor behavior?",
                    "Are narrative contradictions explained or ignored?",
                    "Does the story require magical thinking or implausible leaps?"
                ],
                "outputs": [
                    "🧠 Internal coherence score",
                    "🔍 Implausibility markers (events, motives, or logic jumps)",
                    "📚 Suggested normalization or reframing prompts"
                ],
                "wisdom_injected": [
                    "Even lies must make sense — if they don't, question harder.",
                    "Inconsistency is often the fingerprint of fiction."
                ],
                "philosophical_anchoring": ["D1.3", "D4.1", "D6.1"]
            },      
            "NL-3": {
                "name": "Competing Narratives Contrast",
                "purpose": "Surface alternative narratives to evaluate blind spots, cultural framings, or missing dimensions.",
                "core_questions": [
                    "What other groups or actors interpret this differently?",
                    "What facts do those narratives emphasize or ignore?",
                    "Are they mutually exclusive or potentially synthesizable?",
                    "Who benefits from each version?"
                ],
                "outputs": [
                    "⚖️ Comparative narrative table",
                    "🧭 Bias contrast summary",
                    "🔄 Reconciliation path prompt (if possible)"
                ],
                "wisdom_injected": [
                    "The truth may be divided, but the lies are often complete.",
                    "Multiple lenses sharpen the image."
                ],
                "philosophical_anchoring": ["D3.3", "D6.1", "D8.4"]
            },       
            "NL-4": {
                "name": "Identity, Memory, and Group Interest Framing",
                "purpose": "Identify how group identities, historical trauma, and loyalty shape narrative preference and perception.",
                "core_questions": [
                    "What group identities are centered, valorized, or demonized?",
                    "Are historical grievances reactivated?",
                    "How is loyalty framed: as honor, duty, betrayal, or survival?",
                    "What moral or symbolic rewards are attached to belief?"
                ],
                "outputs": [
                    "🧬 Identity bias map",
                    "🧠 Loyalty trigger points",
                    "🕯️ Historical memory activation log"
                ],
                "wisdom_injected": [
                    "We see through the stories we inherit.",
                    "Group truth is not whole truth."
                ],
                "philosophical_anchoring": ["D3.1", "D6.3", "D7.1"]
            },        
            "NL-5": {
                "name": "Allegory, Analogy, and Symbol Injection",
                "purpose": "Flag where metaphor, analogy, or symbolism is distorting clarity or smuggling ideology.",
                "core_questions": [
                    "Are historical analogies accurate or manipulative (e.g., \"new Hitler,\" \"new Holocaust\")?",
                    "Are symbols used to oversimplify or moralize?",
                    "Does the analogy illuminate — or obscure — the situation?",
                    "What emotional payload is the metaphor carrying?"
                ],
                "outputs": [
                    "🔍 Symbolic distortion indicator",
                    "🧠 Analogy accuracy flag",
                    "🧭 De-metaphorization prompt"
                ],
                "wisdom_injected": [
                    "Symbols short-circuit thinking when unchecked.",
                    "Not all rhymes in history are honest."
                ],
                "philosophical_anchoring": ["D1.3", "D4.2", "D6.2"]
            },        
            "NL-6": {
                "name": "Narrative Gaps",
                "purpose": "Identify what's missing from the story that would change interpretation or conclusion.",
                "core_questions": [
                    "What key actors, events, or timeframes are absent?",
                    "Would including missing elements change the moral or causal assessment?",
                    "Are gaps strategic omissions or natural limitations?",
                    "What would a more complete picture reveal?"
                ],
                "outputs": [
                    "🕳️ Gap identification map",
                    "🔍 Missing element assessment",
                    "⚖️ Completeness evaluation"
                ],
                "wisdom_injected": [
                    "What's missing may matter more than what's present.",
                    "Gaps are not accidents — they are choices."
                ],
                "philosophical_anchoring": ["D4.1", "D7.1", "D3.2"]
            }
        }
    },
    "SL": {
        "name": "System-Level Modules",
        "purpose": "Analyze strategic implications, institutional forces, ideological feedback loops, and structural distortion",
        "modules": {
            "SL-1": {
                "name": "Power and Incentive Mapping",
                "purpose": "Trace who benefits — economically, politically, strategically — from a given claim or interpretation.",
                "core_questions": [
                    "What actors gain material or symbolic advantage?",
                    "Are the incentives aligned with claimed values?",
                    "Are incentives obscured, denied, or misattributed?"
                ],
                "outputs": [
                    "🧭 Power-benefit chart",
                    "💰 Incentive transparency flag",
                    "⚠️ Strategic interest disclosure alert"
                ],
                "wisdom_injected": [
                    "Follow the gain, not the claim.",
                    "Who benefits is not who speaks — but who wins."
                ],
                "philosophical_anchoring": ["D5.1", "D5.3", "D8.2"]
            },            
            "SL-2": {
                "name": "Institutional Behavior and Enforcement Patterns",
                "purpose": "Examine how institutions (governments, media, NGOs) adopt, enforce, or suppress specific claims or framings.",
                "core_questions": [
                    "Are institutions aligned in promoting a particular position?",
                    "Is dissent punished or discouraged?",
                    "What control mechanisms (laws, funding, censure) are in play?"
                ],
                "outputs": [
                    "🧱 Enforcement map",
                    "🚨 Suppression mechanism alert",
                    "🧮 Institutional alignment score"
                ],
                "wisdom_injected": [
                    "Institutions protect stories before people.",
                    "Censorship is a form of narrative hygiene."
                ],
                "philosophical_anchoring": ["D5.2", "D5.3", "D8.3"]
            },           
            "SL-3": {
                "name": "Identity and Memory Exploitation",
                "purpose": "Uncover how collective memory, trauma, and identity are used to frame or justify current interpretations and arguments.",
                "core_questions": [
                    "What past events are invoked to legitimize the present?",
                    "Are traumas weaponized or selectively remembered?",
                    "Whose identity is being centered — or erased?"
                ],
                "outputs": [
                    "🕯️ Memory trigger detection",
                    "🧠 Identity resonance map",
                    "🔍 Historical abuse flag"
                ],
                "wisdom_injected": [
                    "The past is not dead — it's rebranded.",
                    "Memory is power disguised as history."
                ],
                "philosophical_anchoring": ["D3.1", "D6.3", "D7.1"]
            },           
            "SL-4": {
                "name": "Function and Purpose Analysis",
                "purpose": "Determine the deeper goal of a claim or framing — mobilization, justification, distraction, polarization.",
                "core_questions": [
                    "What action does the message inspire or block?",
                    "Is the goal moral, strategic, emotional, or institutional?",
                    "Is the audience meant to feel, think, or act?"
                ],
                "outputs": [
                    "🎯 Functional tag (e.g., Mobilization / Justification / Deflection)",
                    "🧭 Alignment with actor goals",
                    "🧪 False purpose detection"
                ],
                "wisdom_injected": [
                    "Messages are weapons with audiences as targets.",
                    "Purpose reveals design — even in lies."
                ],
                "philosophical_anchoring": ["D4.2", "D4.4", "D5.3"]
            },           
            "SL-5": {
                "name": "Systemic Resistance and Inversion",
                "purpose": "Detect if a claim resists dominant systems or mimics resistance while reinforcing the same structures.",
                "core_questions": [
                    "Is the framing genuinely oppositional or performative?",
                    "Does it invert dominant logic or disguise it?",
                    "Who adopts the resistance framing — and why?"
                ],
                "outputs": [
                    "🧬 Resistance authenticity score",
                    "🪞 Inversion pattern tag",
                    "🧠 Mimicry detection alert"
                ],
                "wisdom_injected": [
                    "Not all rebels seek revolution. Some just want a turn at the throne.",
                    "Inversion is not liberation."
                ],
                "philosophical_anchoring": ["D4.3", "D5.3", "D6.3"]
            },           
            "SL-6": {
                "name": "Feedback Systems and Loop Control",
                "purpose": "Identify recursive reinforcement loops that bias understanding, suppress contradiction, or simulate consensus.",
                "core_questions": [
                    "Are rebuttals systematically excluded?",
                    "Do feedback channels reward loyalty over accuracy?",
                    "Is dissent pathologized (e.g., labeled disloyal, irrational)?"
                ],
                "outputs": [
                    "🔁 Loop map (actor-message-feedback)",
                    "🚫 Dissent suppression marker",
                    "📣 False consensus warning"
                ],
                "wisdom_injected": [
                    "What repeats, rules.",
                    "Broken echo is still an echo."
                ],
                "philosophical_anchoring": ["D5.2", "D7.3", "D8.4"]
            },           
            "SL-7": {
                "name": "Strategic Forecast and Predictive Testing",
                "purpose": "Test the implications of claims by projecting future actions, outcomes, or contradictions.",
                "core_questions": [
                    "If the interpretation is true, what logically follows?",
                    "Are predicted outcomes consistent with observed reality?",
                    "Do real-world results falsify or validate the framing?"
                ],
                "outputs": [
                    "📈 Forecast simulation tag",
                    "⚖️ Outcome match score",
                    "🔍 Predictive contradiction alert"
                ],
                "wisdom_injected": [
                    "Truth has a trajectory.",
                    "Prediction reveals what belief conceals."
                ],
                "philosophical_anchoring": ["D7.2", "D7.4", "D8.5"]
            },           
            "SL-8": {
                "name": "Systemic Blind Spots and Vulnerabilities",
                "purpose": "Reveal what the system or dominant information flow cannot process — its blind spots, silences, or forbidden truths.",
                "core_questions": [
                    "What facts or arguments are persistently excluded?",
                    "What questions can't be asked in polite society?",
                    "What knowledge is penalized?"
                ],
                "outputs": [
                    "🚷 Forbidden topic alert",
                    "🧠 Systemic silence map",
                    "🕳️ Blind spot trigger list"
                ],
                "wisdom_injected": [
                    "Systems fear what they can't metabolize.",
                    "The unspeakable reveals the ungovernable."
                ],
                "philosophical_anchoring": ["D3.2", "D5.3", "D8.4"]
            },            
            "SL-9": {
                "name": "Adaptive Evolution Awareness",
                "purpose": "Track how claims or framing evolve in response to public reaction, internal contradiction, or external pressure.",
                "core_questions": [
                    "Has the claim subtly shifted its framing?",
                    "Are past claims abandoned or reinterpreted?",
                    "Are inconsistencies explained or ignored?"
                ],
                "outputs": [
                    "🧬 Evolution trace (timeline)",
                    "🌀 Strategic reframe detector",
                    "🧊 Frozen contradiction tag"
                ],
                "wisdom_injected": [
                    "The first draft of a lie often dies a hero.",
                    "What adapts survives — but not always with its soul."
                ],
                "philosophical_anchoring": ["D7.3", "D7.4", "D8.6"]
            },
            "SL-10": {
                "name": "Feedback Loop Mapping and Distortion Patterns (Optional)",
                "purpose": "Map and detect distortions in closed-loop information systems.",
                "core_questions": [
                    "Who inputs, moderates, and echoes information?",
                    "Where does distortion occur and for what purpose?"
                ],
                "outputs": [
                    "🔁 Closed-loop diagram",
                    "🪞 Distortion phase tags",
                    "⚠️ Loop integrity score"
                ],
                "wisdom_injected": [
                    "Echo makes truth louder — or drowns it."
                ],
                "philosophical_anchoring": ["D5.2", "D7.3", "D8.4"]
            },
            "SL-11": {
                "name": "Technocratic Logic and Algorithmic Governance (Optional)",
                "purpose": "Evaluate how algorithms, models, and technocratic claims shape or substitute political logic.",
                "core_questions": [
                    "What decisions are outsourced to systems?",
                    "Are algorithmic claims used rhetorically?",
                    "Does technical neutrality mask ideology?"
                ],
                "outputs": [
                    "🧮 Technocratic language scan",
                    "⚙️ Power-delegation map",
                    "🧊 Ideological masking alert"
                ],
                "wisdom_injected": [
                    "What looks neutral may be coded.",
                    "Math is not morality."
                ],
                "philosophical_anchoring": ["D5.3", "D8.6", "D8.7"]
            },
            "SL-12": {
                "name": "Digital Infrastructure Control and Dependency (Optional)",
                "purpose": "Assess how digital platforms, infrastructure, and dependencies shape strategic behavior and control over information.",
                "core_questions": [
                    "Who owns and governs the digital pipes?",
                    "What happens if the infrastructure is withdrawn?",
                    "Are dependencies used as leverage?"
                ],
                "outputs": [
                    "🌐 Infrastructure map",
                    "🧲 Dependency exposure tag",
                    "⚠️ Strategic vulnerability alert"
                ],
                "wisdom_injected": [
                    "He who controls the pipe controls the pressure."
                ],
                "philosophical_anchoring": ["D5.2", "D8.2", "D8.7"]
            }
        }
    }
}

# ========================================
# IV. EPISTEMIC STATUS BLOCK
# ========================================
EPISTEMIC_STATUS_BLOCK = {
    "name": "Epistemic Status Block (Reusable Format)",
    "purpose": "Reusable across any Fact-Level module to reflect the confidence and limits of available knowledge",
    "description": "This block can be included in output to provide structured epistemic assessment",
    
    "status_fields": {
        "status": {
            "name": "Status",
            "description": "Overall epistemic status of the claim",
            "example_output": "🔴 **Contested** — Multiple sources conflict or official confirmation is lacking"
        },
        "evidence_confidence": {
            "name": "Evidence Confidence", 
            "description": "Assessment of evidence quality and reliability",
            "example_output": "⚠️ **Low** — Relies on single actor quote, no third-party verification"
        },
        "potential_asymmetry": {
            "name": "Potential Asymmetry",
            "description": "Detection of information asymmetries or narrative bias",
            "example_output": "📡 **High** — Claim downplayed in Western media, amplified in Russian narratives"
        },
        "primary_actor_silence": {
            "name": "Primary Actor Silence",
            "description": "Assessment of whether key actors have spoken directly",
            "example_output": "🕳️ **Yes** — No direct statement from Ukrainian officials located"
        },
        "suggested_action": {
            "name": "Suggested Action",
            "description": "Recommended next steps for verification or clarification",
            "example_output": "🔍 *Would you like to search for public statements by Ukrainian or Western officials? Or rephrase the claim more neutrally for source matching?*"
        }
    },    
    "status_definitions": {
        "confirmed": {
            "symbol": "✅",
            "label": "Confirmed",
            "description": "Supported by multiple, ideologically diverse sources"
        },
        "partially_verified": {
            "symbol": "🟡", 
            "label": "Partially Verified",
            "description": "Evidence exists but lacks transparency or corroboration"
        },
        "contested": {
            "symbol": "🔴",
            "label": "Contested", 
            "description": "Major dispute between actors or unverifiable details"
        },
        "unknown": {
            "symbol": "⚫",
            "label": "Unknown",
            "description": "No meaningful evidence found. May indicate suppression or topic obscurity"
        }
    },    
    "confidence_levels": {
        "high": {
            "symbol": "✅",
            "threshold": 0.8,
            "description": "Strong evidence from multiple independent sources"
        },
        "medium": {
            "symbol": "🟡",
            "threshold": 0.5,
            "description": "Moderate evidence with some limitations"
        },
        "low": {
            "symbol": "⚠️",
            "threshold": 0.3,
            "description": "Weak evidence, single sources, or significant gaps"
        },
        "very_low": {
            "symbol": "🔴",
            "threshold": 0.0,
            "description": "Insufficient or contradictory evidence"
        }
    },    
    "asymmetry_indicators": {
        "high": {
            "symbol": "📡",
            "description": "Significant narrative asymmetry detected across information sources"
        },
        "medium": {
            "symbol": "📊", 
            "description": "Moderate asymmetry in coverage or framing"
        },
        "low": {
            "symbol": "📈",
            "description": "Minimal asymmetry, relatively balanced coverage"
        },
        "none": {
            "symbol": "⚖️",
            "description": "No significant asymmetry detected"
        }
    },
    
    "output_template": """
**Epistemic Status Assessment:**

| **Field**                 | **Assessment**                                                                                                                                  |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**                | {status_symbol} **{status_label}** — {status_description}                                                                                      |
| **Evidence Confidence**   | {confidence_symbol} **{confidence_level}** — {confidence_description}                                                                          |
| **Potential Asymmetry**   | {asymmetry_symbol} **{asymmetry_level}** — {asymmetry_description}                                                                             |
| **Primary Actor Silence** | {silence_symbol} **{silence_assessment}** — {silence_description}                                                                              |
| **Suggested Action**      | {action_symbol} *{suggested_action_text}*                                                                                                      |
""",
    
    "wisdom_injected": [
        "Epistemic humility is the foundation of adequate analysis.",
        "Uncertainty acknowledged is truth preserved.",
        "What we don't know shapes what we do know."
    ],
    
    "philosophical_anchoring": ["D6.1", "D3.1", "D7.2"],
    
    "usage_instructions": {
        "when_to_use": "Include with any Fact-Level module output to provide epistemic context",
        "how_to_populate": "Assess each field based on available evidence and source analysis",
        "integration": "Can be automatically generated based on FL module findings"
    }
}

# ========================================
# V. FINAL SYNTHESIS MODULE 
# ========================================
FINAL_SYNTHESIS_MODULE = {
    "name": "Final Synthesis and Output Module",
    "purpose": "Integrate insights across all framework levels into a coherent final judgment.",
    
    "core_questions": [
        "What is the final epistemic status of the core claims?",
        "How strong is the overall adequacy of the submission?",
        "What deeper structural or strategic insights emerged?"
    ],
    
    "output_components": [
        "🔍 Claim Summary: Reworded core claim(s) in neutral, testable form",
        "📊 Epistemic Status: Truth likelihood, manipulation risk, evidence coverage, source integrity",
        "🧠 Integrated Evaluation: Key findings across fact, narrative, and system levels",
        "🔁 Guidance & Next Steps: Verification methods and follow-up recommendations"
    ],
    
    "wisdom_injected": [
        "Conclusion is a judgment, not a closure.",
        "Doubt can be wise — denial is not."
    ],
    
    "philosophical_anchoring": ["D6.1", "D7.2", "D5.1"]
}

# ========================================
# VI. FRAMEWORK METADATA
# ========================================
FRAMEWORK_METADATA = {
    "author": "Max Micheliov",
    "release": "June 2025", 
    "contact": "max.micheliov@gmail.com",
    "project_description": "This framework is part of an ongoing project to develop **Real Artificial Intelligence** — a reasoning architecture grounded in philosophical adequacy rather than mechanical neutrality.",
    "collaboration_note": "I welcome collaboration, critique, and meaningful use. Let's build something that thinks wisely.",
    "philosophical_foundation": "Grounded in philosophical adequacy rather than mechanical neutrality"
}