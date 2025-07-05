"""
RAI Premise Engine - Intelligent Premise Selection and Injection
Real Artificial Intelligence Framework Implementation

This module analyzes input context and selects relevant macro premises from the
RAI Premise Library to enhance analytical depth and interpretive adequacy.
"""

import json
import logging
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import re
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PremiseRelevance(Enum):
    """Relevance levels for premise selection"""
    HIGH = "high"      # Core to understanding the topic
    MEDIUM = "medium"  # Contextually relevant
    LOW = "low"        # Tangentially related
    NONE = "none"      # Not applicable

@dataclass
class PremiseMatch:
    """Individual premise matching result"""
    premise_id: str
    relevance: PremiseRelevance
    confidence: float  # 0-1 scale
    trigger_keywords: List[str]
    contextual_factors: List[str]
    
@dataclass
class PremiseSelection:
    """Complete premise selection result"""
    primary_premises: List[str]    # Core premises (3-5)
    secondary_premises: List[str]  # Supporting premises (2-3)
    wisdom_overlay: bool           # Whether to activate wisdom overlay
    total_relevance_score: float   # Overall relevance assessment
    selection_rationale: str       # Why these premises were chosen

class PremiseEngine:
    """
    Intelligent Premise Selection Engine
    
    Analyzes input context and selects relevant macro premises based on:
    1. Topic domain mapping
    2. Keyword density analysis
    3. Contextual pattern recognition
    4. Geopolitical/strategic indicators
    5. Temporal and complexity factors
    """
    
    def __init__(self, premise_library_path: str = "premise_library.json"):
        """Initialize premise engine with premise library"""
        self.premise_library = self._load_premise_library()
        self.premise_index = self._build_premise_index()
        self.contextual_patterns = self._load_contextual_patterns()
        self.geopolitical_indicators = self._load_geopolitical_indicators()
        
    def _load_premise_library(self) -> Dict:
        """Load and structure the premise library"""
        # Full premise library with detailed content
        return {
            "dimensions": {
                "D1": {
                    "name": "Power & Governance",
                    "description": "Political systems, governance, legitimacy, transitions of power",
                    "premises": {
                        "D1.1": {
                            "title": "Power is rarely surrendered; it is redistributed through ritual, consensus, or coercion",
                            "content": "In all functioning systems—democratic, autocratic, or hybrid—true power shifts occur under one of three conditions: Elite consensus to preserve stability, External pressure or control, or Systemic fracture or collapse.",
                            "keywords": ["power", "elections", "transition", "elite", "consensus", "coercion", "legitimacy", "democracy", "autocracy"],
                            "contexts": ["political_transition", "electoral_analysis", "regime_change", "power_struggle"],
                            "weight": 0.9
                        },
                        "D1.2": {
                            "title": "Political actors emerge from their cultural substrate",
                            "content": "Politicians are neither a separate species nor inherently corrupt—they reflect the ambitions, fears, and incentives of their societal base.",
                            "keywords": ["politicians", "corruption", "society", "culture", "leadership", "representation"],
                            "contexts": ["political_analysis", "leadership_evaluation", "democratic_theory"],
                            "weight": 0.7
                        },
                        "D1.3": {
                            "title": "Power is sustained through economic architecture",
                            "content": "Control over capital flows, debt, resource distribution, and media ownership often underlies political stability more than formal institutions or laws.",
                            "keywords": ["economic", "capital", "debt", "media", "ownership", "stability", "institutions"],
                            "contexts": ["economic_power", "media_control", "institutional_analysis"],
                            "weight": 0.8
                        }
                    }
                },
                "D2": {
                    "name": "Geopolitical Order & Conflict",
                    "description": "Global hierarchy, war, asymmetry, strategic interests",
                    "premises": {
                        "D2.1": {
                            "title": "A few powers shape the planetary game",
                            "content": "Despite the appearance of multilateralism, geopolitical outcomes are determined by a small number of dominant states or blocs.",
                            "keywords": ["geopolitical", "powers", "multilateral", "dominant", "states", "blocs", "global", "hierarchy"],
                            "contexts": ["international_relations", "global_power", "geopolitics", "hegemony"],
                            "weight": 0.9
                        },
                        "D2.2": {
                            "title": "Systemic war is ongoing, with kinetic conflict as its loudest symptom",
                            "content": "Economic pressure, cyberattacks, and narrative domination are integral tools of modern conflict. Physical war is no longer the beginning of conflict, but its explosion point.",
                            "keywords": ["war", "conflict", "cyber", "economic", "narrative", "hybrid", "warfare", "systemic"],
                            "contexts": ["modern_warfare", "hybrid_conflict", "economic_warfare", "information_warfare"],
                            "weight": 0.9
                        },
                        "D2.3": {
                            "title": "Neutrality becomes illusion in systemic conflict",
                            "content": "In high-stakes global competition, all states are drawn into alignment, either through dependence, coercion, or survival instinct.",
                            "keywords": ["neutrality", "alignment", "dependence", "coercion", "survival", "competition"],
                            "contexts": ["neutral_states", "alliance_systems", "proxy_conflicts"],
                            "weight": 0.8
                        },
                        "D2.4": {
                            "title": "Nuclear weapons enforce adult behavior through existential fear",
                            "content": "The doctrine of Mutual Assured Destruction (MAD) has replaced idealism as the real guarantor of peace.",
                            "keywords": ["nuclear", "weapons", "MAD", "deterrence", "peace", "existential", "threat"],
                            "contexts": ["nuclear_policy", "deterrence_theory", "great_power_conflict"],
                            "weight": 0.8
                        },
                        "D2.5": {
                            "title": "War is waged beneath the surface through deception and engineered ambiguity",
                            "content": "Modern power projection often hides behind peace initiatives, democratic rhetoric, or defensive postures.",
                            "keywords": ["deception", "ambiguity", "peace", "rhetoric", "defensive", "covert", "hidden"],
                            "contexts": ["covert_operations", "diplomatic_deception", "strategic_ambiguity"],
                            "weight": 0.8
                        },
                        "D2.6": {
                            "title": "Geopolitical behavior is shaped by enduring asymmetries",
                            "content": "Power disparities in media reach, military capabilities, economic leverage, human resources, or technological infrastructure define what actors can realistically do.",
                            "keywords": ["asymmetry", "capabilities", "leverage", "infrastructure", "military", "economic", "technology"],
                            "contexts": ["power_imbalance", "capability_analysis", "strategic_resources"],
                            "weight": 0.8
                        },
                        "D2.7": {
                            "title": "Strategic interests are survival logic dressed in moral clothing",
                            "content": "Behind every noble speech about peace and values is a spreadsheet calculating market access, resource control, and strategic leverage.",
                            "keywords": ["strategic", "interests", "moral", "survival", "resources", "leverage", "values", "market"],
                            "contexts": ["realpolitik", "strategic_analysis", "moral_rhetoric"],
                            "weight": 0.9
                        }
                    }
                },
                "D3": {
                    "name": "Information & Perception",
                    "description": "Epistemology, narrative warfare, cognitive control",
                    "premises": {
                        "D3.1": {
                            "title": "Information is a commodity in peace and a weapon in systemic conflict",
                            "content": "In peacetime, information flows are monetized; in systemic conflict, they are weaponized. Media must be controlled by those with political or economic stakes.",
                            "keywords": ["information", "media", "control", "weaponized", "monetized", "conflict", "propaganda"],
                            "contexts": ["media_analysis", "information_warfare", "propaganda", "narrative_control"],
                            "weight": 0.9
                        },
                        "D3.2": {
                            "title": "Censorship and visibility are asymmetric tools",
                            "content": "Control over digital infrastructure—platforms, algorithms, recommendation engines, content policies—enables nonlinear narrative dominance.",
                            "keywords": ["censorship", "algorithms", "platforms", "content", "digital", "infrastructure", "narrative"],
                            "contexts": ["social_media", "algorithmic_control", "content_moderation", "digital_censorship"],
                            "weight": 0.8
                        },
                        "D3.3": {
                            "title": "Perception is power",
                            "content": "Legitimacy, victimhood, and moral high ground are not just narratives—they are operational assets. Winning the story often has greater strategic value than winning the terrain.",
                            "keywords": ["perception", "legitimacy", "victimhood", "moral", "narrative", "story", "strategic"],
                            "contexts": ["narrative_warfare", "perception_management", "soft_power", "legitimacy_battles"],
                            "weight": 0.9
                        },
                        "D3.4": {
                            "title": "Thought policing outperforms censorship",
                            "content": "When populations internalize the boundaries of acceptable thought, external repression becomes redundant. Self-censorship, social penalty, and digital panopticism are more effective than coercive force.",
                            "keywords": ["thought", "policing", "censorship", "self-censorship", "social", "penalty", "panopticon"],
                            "contexts": ["social_control", "self_censorship", "cancel_culture", "thought_control"],
                            "weight": 0.8
                        },
                        "D3.5": {
                            "title": "Large-scale protests are rarely spontaneous",
                            "content": "Mass participation may appear organic, but major movements that gain traction nearly always rest on pre-existing infrastructure: trained organizers, aligned institutions, sympathetic media, and international funding streams.",
                            "keywords": ["protests", "spontaneous", "organizers", "infrastructure", "funding", "movements", "organic"],
                            "contexts": ["protest_movements", "color_revolutions", "social_movements", "astroturfing"],
                            "weight": 0.8
                        }
                    }
                },
                "D4": {
                    "name": "Civilization & Culture",
                    "description": "Identity, memory, inherited trauma, ideological formation",
                    "premises": {
                        "D4.1": {
                            "title": "Cultural self-image distorts memory",
                            "content": "Societies tend to idealize their past, suppressing atrocities, defeats, or failures. Collective memory is selectively curated through trauma editing, symbolic purification, and ritualized storytelling.",
                            "keywords": ["culture", "memory", "trauma", "history", "collective", "narrative", "identity"],
                            "contexts": ["historical_memory", "cultural_identity", "collective_trauma", "historical_revisionism"],
                            "weight": 0.8
                        },
                        "D4.2": {
                            "title": "Victimhood is political capital",
                            "content": "Groups and nations frame themselves as historical victims to gain legitimacy, immunize against criticism, and mobilize internal cohesion or international sympathy.",
                            "keywords": ["victimhood", "capital", "legitimacy", "criticism", "sympathy", "mobilization", "identity"],
                            "contexts": ["victim_narrative", "identity_politics", "historical_grievance", "legitimacy_claims"],
                            "weight": 0.8
                        },
                        "D4.3": {
                            "title": "Civilizations pursue different visions of success",
                            "content": "All cultures strive for stability, continuity, and influence—but their definitions of success vary profoundly. Some prioritize expansion or technological progress; others value harmony, survival, or spiritual legacy.",
                            "keywords": ["civilization", "success", "stability", "continuity", "influence", "progress", "harmony"],
                            "contexts": ["civilizational_analysis", "cultural_values", "development_models"],
                            "weight": 0.7
                        },
                        "D4.4": {
                            "title": "Cultural soft power is a vector of dominance",
                            "content": "Narratives travel through film, entertainment, humanitarian aid, and globalized education. Cultural output becomes a carrier of ideology, shaping aspiration, moral hierarchies, and political alignment.",
                            "keywords": ["soft", "power", "culture", "entertainment", "education", "ideology", "dominance"],
                            "contexts": ["cultural_hegemony", "soft_power", "cultural_influence", "ideological_transmission"],
                            "weight": 0.8
                        },
                        "D4.5": {
                            "title": "Culture encodes strategy",
                            "content": "Deep-seated cultural traits—whether collectivist or individualist, honor-based or legality-based—shape behavior in diplomacy, warfare, and negotiation.",
                            "keywords": ["culture", "strategy", "collectivist", "individualist", "honor", "legal", "diplomacy"],
                            "contexts": ["cultural_strategy", "diplomatic_behavior", "negotiation_styles"],
                            "weight": 0.7
                        }
                    }
                },
                "D5": {
                    "name": "System Dynamics & Complexity",
                    "description": "Non-linearity, feedback loops, control systems, systemic risk",
                    "premises": {
                        "D5.1": {
                            "title": "Systems behave through feedback, not intention",
                            "content": "Outcomes in complex systems are not directly caused by intentions but emerge from interactions between variables, delays, and feedback loops.",
                            "keywords": ["systems", "feedback", "complexity", "nonlinear", "emergence", "loops", "variables"],
                            "contexts": ["systems_analysis", "complexity_theory", "unintended_consequences"],
                            "weight": 0.8
                        },
                        "D5.2": {
                            "title": "Fragile systems suppress dissent",
                            "content": "When systems lack flexibility or redundancy, they tighten control in response to perceived threats. Repression is not always ideological—it is often a survival reflex.",
                            "keywords": ["fragile", "systems", "dissent", "control", "repression", "survival", "flexibility"],
                            "contexts": ["system_fragility", "authoritarian_response", "social_control"],
                            "weight": 0.8
                        },
                        "D5.3": {
                            "title": "Stability depends on controlled transparency",
                            "content": "No system can operate in full opacity—or in full daylight. Long-term resilience often requires a managed flow of visibility: enough to maintain legitimacy, but not so much that its contradictions become uncontrollable.",
                            "keywords": ["stability", "transparency", "opacity", "legitimacy", "contradictions", "visibility", "managed"],
                            "contexts": ["transparency_management", "legitimacy_maintenance", "information_control"],
                            "weight": 0.7
                        },
                        "D5.4": {
                            "title": "Self-correction requires pressure valves",
                            "content": "Resilient systems create mechanisms of controlled release: courts, protests, satire, journalism. When these are co-opted or blocked, pressure accumulates and can explode.",
                            "keywords": ["self-correction", "pressure", "valves", "courts", "protests", "journalism", "resilient"],
                            "contexts": ["system_resilience", "social_pressure", "institutional_safety_valves"],
                            "weight": 0.7
                        },
                        "D5.5": {
                            "title": "Narratives are the software of systems",
                            "content": "The shared stories people believe about their system enable it to function. When narratives degrade, the system's behavioral code becomes corrupted.",
                            "keywords": ["narratives", "software", "systems", "stories", "behavioral", "code", "legitimacy"],
                            "contexts": ["narrative_legitimacy", "system_narratives", "ideological_software"],
                            "weight": 0.8
                        }
                    }
                },
                "D6": {
                    "name": "Ethics & Judgment",
                    "description": "Moral framing, ambiguity, pluralism",
                    "premises": {
                        "D6.1": {
                            "title": "Multiple value systems can be valid within their own logic",
                            "content": "Different ethical traditions can produce conflicting judgments without either being objectively false. Ethical analysis requires context, not universalization.",
                            "keywords": ["ethics", "values", "moral", "traditions", "context", "relativism", "judgment"],
                            "contexts": ["ethical_analysis", "moral_relativism", "value_conflicts"],
                            "weight": 0.7
                        },
                        "D6.2": {
                            "title": "Moral certainty often masks geopolitical or institutional interests",
                            "content": "The language of 'values' and 'human rights' is frequently used to cloak strategic motives. Claiming virtue becomes a tool of leverage.",
                            "keywords": ["moral", "certainty", "values", "human", "rights", "strategic", "virtue", "leverage"],
                            "contexts": ["moral_rhetoric", "strategic_morality", "humanitarian_intervention"],
                            "weight": 0.8
                        },
                        "D6.3": {
                            "title": "The oppressed often inherit and reenact the logic of the oppressor",
                            "content": "Those who once suffered injustice may replicate coercive systems when power shifts. Victimhood does not guarantee virtue.",
                            "keywords": ["oppressed", "oppressor", "injustice", "power", "shifts", "victimhood", "virtue"],
                            "contexts": ["power_transitions", "victim_perpetrator_cycles", "revolutionary_dynamics"],
                            "weight": 0.8
                        },
                        "D6.4": {
                            "title": "Democratic decay often originates from the people, not just elites",
                            "content": "While corruption and manipulation matter, mass apathy, fear, and ignorance can also erode democratic life. When the public ceases to demand virtue, representation becomes spectacle.",
                            "keywords": ["democratic", "decay", "people", "elites", "apathy", "fear", "ignorance", "virtue"],
                            "contexts": ["democratic_erosion", "civic_engagement", "political_apathy"],
                            "weight": 0.7
                        },
                        "D6.5": {
                            "title": "Political virtue is often the retroactive moralization of success",
                            "content": "History is written by winners, and legitimacy is often post-facto storytelling. What is framed as noble leadership may be little more than effective domination rewritten in moral terms.",
                            "keywords": ["virtue", "success", "history", "winners", "legitimacy", "leadership", "domination"],
                            "contexts": ["historical_narrative", "winner_history", "legitimacy_construction"],
                            "weight": 0.8
                        },
                        "D6.6": {
                            "title": "Hypocrisy is not an anomaly, but a structural feature of moral discourse",
                            "content": "Nations, institutions, and individuals often fail to meet the standards they preach—not merely from weakness, but because moral language is strategically deployed to manage perception, not guide consistent behavior.",
                            "keywords": ["hypocrisy", "moral", "discourse", "standards", "strategic", "perception", "behavior"],
                            "contexts": ["moral_hypocrisy", "strategic_morality", "performative_ethics"],
                            "weight": 0.8
                        }
                    }
                },
                "D7": {
                    "name": "Temporal Awareness & Strategic Foresight",
                    "description": "Historical cycles, long-term risk, delayed consequence",
                    "premises": {
                        "D7.1": {
                            "title": "Historical context is essential for understanding motivation",
                            "content": "Current decisions reflect accumulated trauma, inherited grievances, and strategic memory. Nations and actors often pursue goals laid down by events decades—or centuries—earlier.",
                            "keywords": ["historical", "context", "trauma", "grievances", "memory", "decisions", "motivation"],
                            "contexts": ["historical_analysis", "long_term_strategy", "inherited_conflict"],
                            "weight": 0.8
                        },
                        "D7.2": {
                            "title": "Delayed outcomes are often more impactful than immediate ones",
                            "content": "What seems like success in the short term may erode legitimacy or stability over time. Systems have latency, and interventions often unleash feedback loops that manifest far later.",
                            "keywords": ["delayed", "outcomes", "impact", "short", "term", "latency", "feedback", "loops"],
                            "contexts": ["long_term_consequences", "systemic_delay", "strategic_patience"],
                            "weight": 0.7
                        },
                        "D7.3": {
                            "title": "History rewards the effective, not the grateful",
                            "content": "There is no durable currency of gratitude in international relations or political history. Alliances shift based on interest, not memory.",
                            "keywords": ["history", "effective", "grateful", "gratitude", "alliances", "interest", "memory"],
                            "contexts": ["alliance_dynamics", "strategic_interest", "historical_patterns"],
                            "weight": 0.7
                        },
                        "D7.4": {
                            "title": "Civilizations rise and fall in cycles",
                            "content": "No system lasts forever. Civilizations experience arcs of emergence, dominance, stagnation, and collapse. Those who believe they are immune to decline are usually entering it.",
                            "keywords": ["civilizations", "cycles", "rise", "fall", "decline", "collapse", "dominance"],
                            "contexts": ["civilizational_cycles", "imperial_decline", "historical_patterns"],
                            "weight": 0.7
                        },
                        "D7.5": {
                            "title": "The future is colonized by today's narratives",
                            "content": "The stories we tell about the future—progress, collapse, justice, revenge—shape policy, science, investment, and war. Competing visions of the future often drive present action more than actual planning does.",
                            "keywords": ["future", "narratives", "stories", "progress", "collapse", "justice", "policy"],
                            "contexts": ["future_narratives", "strategic_vision", "ideological_projection"],
                            "weight": 0.8
                        },
                        "D7.6": {
                            "title": "Strategic actors plan in decades; reactive actors respond in headlines",
                            "content": "Global competition rewards those who think beyond the electoral cycle or news cycle. Systems with long memory and long-range planning shape outcomes more decisively than populist turbulence.",
                            "keywords": ["strategic", "actors", "decades", "reactive", "headlines", "planning", "memory"],
                            "contexts": ["strategic_planning", "long_term_thinking", "electoral_cycles"],
                            "weight": 0.8
                        },
                        "D7.7": {
                            "title": "Delays between cause and effect conceal responsibility",
                            "content": "When consequences unfold years later, those who set events in motion often escape accountability. Strategic manipulation benefits from this delay.",
                            "keywords": ["delays", "cause", "effect", "responsibility", "consequences", "accountability", "manipulation"],
                            "contexts": ["accountability_gaps", "delayed_consequences", "strategic_manipulation"],
                            "weight": 0.7
                        }
                    }
                },
                "D8": {
                    "name": "Political Economy & Resource Power",
                    "description": "Capital flows, labor dynamics, ownership structures, resource control",
                    "premises": {
                        "D8.1": {
                            "title": "Economic power precedes and shapes political outcomes",
                            "content": "The distribution of capital, land, labor, and credit forms the invisible scaffolding beneath political institutions. Governance structures often emerge as reflections of dominant economic interests.",
                            "keywords": ["economic", "power", "capital", "labor", "credit", "political", "governance", "institutions"],
                            "contexts": ["political_economy", "economic_influence", "class_analysis"],
                            "weight": 0.9
                        },
                        "D8.2": {
                            "title": "Class remains a functional reality beneath changing labels",
                            "content": "Despite rhetorical progress or rebranding, societies continue to stratify along lines of control over productive assets. Whether under capitalism, state socialism, or mixed regimes, there is always a division between those who own, those who manage, and those who labor.",
                            "keywords": ["class", "stratification", "assets", "capitalism", "socialism", "ownership", "labor"],
                            "contexts": ["class_analysis", "economic_stratification", "ownership_structures"],
                            "weight": 0.8
                        },
                        "D8.3": {
                            "title": "Resource dependencies define strategic behavior",
                            "content": "Access to energy, rare materials, food, and water determines national security and foreign policy alignment. States will violate ethical norms or destabilize entire regions to secure such resources.",
                            "keywords": ["resources", "dependencies", "energy", "materials", "food", "water", "security", "foreign"],
                            "contexts": ["resource_geopolitics", "energy_security", "strategic_resources"],
                            "weight": 0.9
                        },
                        "D8.4": {
                            "title": "Debt is a tool of control, not just finance",
                            "content": "Public and private debt create long-term dependency structures. Lenders can shape policy, impose austerity, and dictate reforms under the guise of fiscal discipline or development assistance.",
                            "keywords": ["debt", "control", "finance", "dependency", "austerity", "reforms", "fiscal"],
                            "contexts": ["debt_control", "economic_dependency", "financial_leverage"],
                            "weight": 0.8
                        },
                        "D8.5": {
                            "title": "Technology is not neutral—it encodes power relations",
                            "content": "Digital platforms, algorithmic finance, and data monopolies allow unprecedented economic concentration. The illusion of decentralization often masks deeper centralization in the hands of those who build and own the infrastructure.",
                            "keywords": ["technology", "neutral", "power", "digital", "platforms", "algorithms", "data", "monopolies"],
                            "contexts": ["tech_power", "digital_economy", "platform_capitalism"],
                            "weight": 0.8
                        },
                        "D8.6": {
                            "title": "Labor is globalized, devalued, and fragmented",
                            "content": "In a globalized economy, labor no longer negotiates from a national base. Jobs are offshored, gigified, or automated. As collective bargaining weakens, workers become interchangeable.",
                            "keywords": ["labor", "globalized", "devalued", "fragmented", "offshored", "automated", "bargaining"],
                            "contexts": ["labor_economics", "globalization", "worker_rights"],
                            "weight": 0.7
                        },
                        "D8.7": {
                            "title": "Automation shifts power from labor to capital",
                            "content": "As machines replace human labor, value concentrates around intellectual property, infrastructure ownership, and data extraction. Automation doesn't eliminate labor—it transforms it into invisible maintenance and algorithmic obedience.",
                            "keywords": ["automation", "labor", "capital", "machines", "property", "infrastructure", "data"],
                            "contexts": ["automation_economics", "tech_displacement", "digital_labor"],
                            "weight": 0.7
                        },
                        "D8.8": {
                            "title": "Supply chains are strategic weapons",
                            "content": "Global trade networks are not just economic artifacts—they are levers of pressure in geopolitical struggle. Countries that control logistics chokepoints, manufacturing hubs, or rare-earth refining can extract political concessions without firing a shot.",
                            "keywords": ["supply", "chains", "strategic", "weapons", "trade", "logistics", "manufacturing", "geopolitical"],
                            "contexts": ["supply_chain_warfare", "economic_statecraft", "trade_dependencies"],
                            "weight": 0.8
                        }
                    }
                }
            }
        }
    
    def _build_premise_index(self) -> Dict[str, List[str]]:
        """Build keyword index for fast premise lookup"""
        index = defaultdict(list)
        
        for dim_id, dimension in self.premise_library["dimensions"].items():
            for prem_id, premise in dimension["premises"].items():
                # Index by keywords
                for keyword in premise["keywords"]:
                    index[keyword.lower()].append(prem_id)
                
                # Index by context
                for context in premise["contexts"]:
                    index[context.lower()].append(prem_id)
        
        return dict(index)
    
    def _load_contextual_patterns(self) -> Dict[str, List[str]]:
        """Load contextual patterns for advanced matching"""
        return {
            "regime_change": [
                "election", "transition", "coup", "revolution", "protest", "uprising",
                "democracy", "autocracy", "legitimacy", "power", "government"
            ],
            "information_warfare": [
                "media", "propaganda", "narrative", "censorship", "bias", "fake",
                "news", "disinformation", "misinformation", "platform", "algorithm"
            ],
            "geopolitical_conflict": [
                "war", "conflict", "military", "sanctions", "alliance", "nuclear",
                "deterrence", "strategy", "security", "threat", "defense"
            ],
            "economic_control": [
                "debt", "capital", "finance", "trade", "resources", "energy",
                "supply", "chain", "economic", "market", "wealth", "class"
            ],
            "cultural_hegemony": [
                "culture", "identity", "values", "ideology", "soft", "power",
                "narrative", "memory", "trauma", "civilization", "heritage"
            ],
            "systemic_analysis": [
                "system", "complexity", "feedback", "control", "stability",
                "fragility", "resilience", "transparency", "pressure", "valve"
            ],
            "temporal_dynamics": [
                "history", "historical", "time", "cycles", "future", "past",
                "memory", "legacy", "evolution", "change", "development"
            ],
            "moral_framework": [
                "ethics", "moral", "values", "virtue", "justice", "rights",
                "good", "evil", "responsibility", "hypocrisy", "legitimacy"
            ]
        }
    
    def _load_geopolitical_indicators(self) -> Dict[str, float]:
        """Load geopolitical complexity indicators"""
        return {
            # High-stakes terms
            "nuclear": 0.95,
            "war": 0.9,
            "sanctions": 0.85,
            "military": 0.8,
            "conflict": 0.8,
            "geopolitical": 0.9,
            "strategic": 0.85,
            "alliance": 0.8,
            "deterrence": 0.8,
            
            # Power dynamics
            "power": 0.8,
            "control": 0.75,
            "dominance": 0.8,
            "hegemony": 0.85,
            "elite": 0.75,
            "regime": 0.8,
            
            # Information warfare
            "propaganda": 0.8,
            "narrative": 0.7,
            "media": 0.6,
            "censorship": 0.8,
            "disinformation": 0.85,
            "algorithm": 0.7,
            
            # Economic leverage
            "debt": 0.7,
            "capital": 0.6,
            "resources": 0.7,
            "energy": 0.75,
            "trade": 0.6,
            "supply chain": 0.8,
            
            # System indicators
            "systemic": 0.8,
            "complexity": 0.7,
            "feedback": 0.6,
            "stability": 0.6,
            "fragility": 0.7,
            
            # Temporal factors
            "historical": 0.6,
            "legacy": 0.6,
            "memory": 0.6,
            "cycles": 0.7
        }
    
    def select_premises(self, rai_input, max_primary: int = 5, max_secondary: int = 3) -> PremiseSelection:
        """
        Main premise selection function
        
        Args:
            rai_input: RAIInput object from wrapper
            max_primary: Maximum primary premises to select
            max_secondary: Maximum secondary premises to select
            
        Returns:
            PremiseSelection object with selected premises and rationale
        """
        try:
            # Step 1: Generate premise matches
            matches = self._generate_premise_matches(rai_input)
            
            # Step 2: Score and rank premises
            scored_premises = self._score_premises(matches, rai_input)
            
            # Step 3: Select primary and secondary premises
            primary, secondary = self._select_premise_tiers(
                scored_premises, max_primary, max_secondary
            )
            
            # Step 4: Determine wisdom overlay
            wisdom_overlay = self._should_activate_wisdom_overlay(
                rai_input, scored_premises
            )
            
            # Step 5: Calculate total relevance
            total_relevance = self._calculate_total_relevance(scored_premises)
            
            # Step 6: Generate selection rationale
            rationale = self._generate_selection_rationale(
                rai_input, primary, secondary, wisdom_overlay
            )
            
            return PremiseSelection(
                primary_premises=primary,
                secondary_premises=secondary,
                wisdom_overlay=wisdom_overlay,
                total_relevance_score=total_relevance,
                selection_rationale=rationale
            )
            
        except Exception as e:
            logger.error(f"Error in premise selection: {str(e)}")
            return self._fallback_selection(rai_input)
    
    def _generate_premise_matches(self, rai_input) -> List[PremiseMatch]:
        """Generate premise matches based on input analysis"""
        matches = []
        
        # Get input text for analysis
        text = rai_input.cleaned_input.lower()
        words = set(text.split())
        
        # Analyze each premise
        for dim_id, dimension in self.premise_library["dimensions"].items():
            for prem_id, premise in dimension["premises"].items():
                match = self._analyze_premise_match(
                    prem_id, premise, text, words, rai_input
                )
                if match.relevance != PremiseRelevance.NONE:
                    matches.append(match)
        
        return matches
    
    def _analyze_premise_match(self, prem_id: str, premise: Dict, 
                              text: str, words: Set[str], rai_input) -> PremiseMatch:
        """Analyze how well a premise matches the input"""
        
        # Keyword matching
        keyword_matches = []
        for keyword in premise["keywords"]:
            if keyword.lower() in text:
                keyword_matches.append(keyword)
        
        # Context matching
        context_matches = []
        for context in premise["contexts"]:
            if self._matches_context(context, text, rai_input):
                context_matches.append(context)
        
        # Calculate base relevance score
        keyword_score = len(keyword_matches) / len(premise["keywords"])
        context_score = len(context_matches) / len(premise["contexts"])
        
        # Weight by premise importance
        weighted_score = (keyword_score * 0.6 + context_score * 0.4) * premise["weight"]
        
        # Apply input-specific modifiers
        modified_score = self._apply_input_modifiers(
            weighted_score, prem_id, rai_input, keyword_matches
        )
        
        # Determine relevance level
        if modified_score >= 0.7:
            relevance = PremiseRelevance.HIGH
        elif modified_score >= 0.4:
            relevance = PremiseRelevance.MEDIUM
        elif modified_score >= 0.2:
            relevance = PremiseRelevance.LOW
        else:
            relevance = PremiseRelevance.NONE
        
        # Identify contextual factors
        contextual_factors = self._identify_contextual_factors(rai_input, prem_id)
        
        return PremiseMatch(
            premise_id=prem_id,
            relevance=relevance,
            confidence=modified_score,
            trigger_keywords=keyword_matches,
            contextual_factors=contextual_factors
        )
    
    def _matches_context(self, context: str, text: str, rai_input) -> bool:
        """Check if input matches a contextual pattern"""
        if context in self.contextual_patterns:
            pattern_words = self.contextual_patterns[context]
            return any(word in text for word in pattern_words)
        return False
    
    def _apply_input_modifiers(self, base_score: float, prem_id: str, 
                              rai_input, keyword_matches: List[str]) -> float:
        """Apply input-specific modifiers to premise score"""
        score = base_score
        
        # Boost for high emotional charge in relevant domains
        if rai_input.emotional_charge >= 4:
            if prem_id.startswith(("D3", "D6")):  # Information/Ethics domains
                score *= 1.2
        
        # Boost for high complexity
        if rai_input.complexity_score >= 4:
            if prem_id.startswith(("D5", "D7")):  # System/Temporal domains
                score *= 1.15
        
        # Boost for geopolitical indicators
        geopolitical_boost = 0
        for keyword in keyword_matches:
            if keyword.lower() in self.geopolitical_indicators:
                geopolitical_boost += self.geopolitical_indicators[keyword.lower()]
        
        if geopolitical_boost > 0:
            score *= (1 + geopolitical_boost / 10)
        
        # Boost for input type alignment
        if rai_input.input_type.value == "system_premise" and prem_id.startswith(("D1", "D2", "D5")):
            score *= 1.3
        elif rai_input.input_type.value == "narrative" and prem_id.startswith(("D3", "D4", "D6")):
            score *= 1.2
        elif rai_input.input_type.value == "factual_claim" and prem_id.startswith(("D2", "D3", "D8")):
            score *= 1.1
        
        # Topic-specific boosts
        for topic in rai_input.detected_topics:
            if topic == "geopolitical" and prem_id.startswith("D2"):
                score *= 1.25
            elif topic == "information" and prem_id.startswith("D3"):
                score *= 1.25
            elif topic == "power_governance" and prem_id.startswith("D1"):
                score *= 1.25
            elif topic == "economy" and prem_id.startswith("D8"):
                score *= 1.25
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _identify_contextual_factors(self, rai_input, prem_id: str) -> List[str]:
        """Identify why this premise is contextually relevant"""
        factors = []
        
        # Input type factors
        if rai_input.input_type.value == "system_premise":
            factors.append("system_level_input")
        
        # Emotional factors
        if rai_input.emotional_charge >= 4:
            factors.append("high_emotional_charge")
        
        # Complexity factors
        if rai_input.complexity_score >= 4:
            factors.append("high_complexity")
        
        # Style factors
        for flag in rai_input.style_flags:
            if flag in ["hyperbole", "emotional"]:
                factors.append(f"style_{flag}")
        
        # Topic factors
        for topic in rai_input.detected_topics:
            factors.append(f"topic_{topic}")
        
        return factors
    
    def _score_premises(self, matches: List[PremiseMatch], rai_input) -> List[Tuple[str, float]]:
        """Score and rank premise matches"""
        scored = []
        
        for match in matches:
            # Base score from confidence
            score = match.confidence
            
            # Boost for multiple trigger keywords
            if len(match.trigger_keywords) > 2:
                score *= 1.1
            
            # Boost for multiple contextual factors
            if len(match.contextual_factors) > 2:
                score *= 1.05
            
            # Domain synergy bonuses
            score = self._apply_domain_synergy(score, match.premise_id, matches)
            
            scored.append((match.premise_id, score))
        
        # Sort by score (descending)
        return sorted(scored, key=lambda x: x[1], reverse=True)
    
    def _apply_domain_synergy(self, score: float, prem_id: str, 
                             all_matches: List[PremiseMatch]) -> float:
        """Apply bonuses for domain synergy"""
        domain = prem_id.split('.')[0]  # e.g., "D2" from "D2.1"
        
        # Count matches in same domain
        same_domain_count = sum(
            1 for match in all_matches 
            if match.premise_id.startswith(domain) and match.relevance != PremiseRelevance.NONE
        )
        
        # Boost if multiple premises from same domain are relevant
        if same_domain_count >= 2:
            score *= 1.1
        if same_domain_count >= 3:
            score *= 1.15
        
        # Cross-domain synergies
        synergy_map = {
            "D1": ["D2", "D8"],  # Power & Geopolitics & Economy
            "D2": ["D1", "D3", "D8"],  # Geopolitics & Power & Information & Economy
            "D3": ["D2", "D4", "D6"],  # Information & Geopolitics & Culture & Ethics
            "D4": ["D3", "D6", "D7"],  # Culture & Information & Ethics & Temporal
            "D5": ["D1", "D7", "D8"],  # Systems & Power & Temporal & Economy
            "D6": ["D3", "D4", "D7"],  # Ethics & Information & Culture & Temporal
            "D7": ["D4", "D5", "D6"],  # Temporal & Culture & Systems & Ethics
            "D8": ["D1", "D2", "D5"]   # Economy & Power & Geopolitics & Systems
        }
        
        if domain in synergy_map:
            synergy_domains = synergy_map[domain]
            synergy_count = sum(
                1 for match in all_matches
                for syn_domain in synergy_domains
                if match.premise_id.startswith(syn_domain) and match.relevance != PremiseRelevance.NONE
            )
            
            if synergy_count >= 1:
                score *= 1.05
            if synergy_count >= 2:
                score *= 1.1
        
        return score
    
    def _select_premise_tiers(self, scored_premises: List[Tuple[str, float]], 
                             max_primary: int, max_secondary: int) -> Tuple[List[str], List[str]]:
        """Select primary and secondary premise tiers"""
        
        if not scored_premises:
            return [], []
        
        # Ensure diversity across domains
        primary = []
        secondary = []
        used_domains = set()
        
        # First pass: select top premises ensuring domain diversity
        for prem_id, score in scored_premises:
            domain = prem_id.split('.')[0]
            
            if len(primary) < max_primary:
                if score >= 0.6:  # High threshold for primary
                    primary.append(prem_id)
                    used_domains.add(domain)
                elif len(primary) < max_primary // 2:  # Fill at least half
                    primary.append(prem_id)
                    used_domains.add(domain)
            elif len(secondary) < max_secondary:
                if score >= 0.3 and domain not in used_domains:  # Ensure diversity
                    secondary.append(prem_id)
                    used_domains.add(domain)
        
        # Second pass: fill remaining slots with best scores
        for prem_id, score in scored_premises:
            if prem_id not in primary and prem_id not in secondary:
                if len(primary) < max_primary and score >= 0.4:
                    primary.append(prem_id)
                elif len(secondary) < max_secondary and score >= 0.2:
                    secondary.append(prem_id)
        
        return primary, secondary
    
    def _should_activate_wisdom_overlay(self, rai_input, scored_premises: List[Tuple[str, float]]) -> bool:
        """Determine if wisdom overlay should be activated"""
        
        # High complexity or emotional charge
        if rai_input.complexity_score >= 4 or rai_input.emotional_charge >= 4:
            return True
        
        # Multiple high-scoring premises
        high_score_count = sum(1 for _, score in scored_premises if score >= 0.7)
        if high_score_count >= 3:
            return True
        
        # Geopolitical or system-level content
        if rai_input.input_type.value == "system_premise":
            return True
        
        # Multiple detected topics
        if len(rai_input.detected_topics) >= 3:
            return True
        
        # High geopolitical indicator presence
        text = rai_input.cleaned_input.lower()
        geopolitical_score = sum(
            self.geopolitical_indicators.get(word, 0)
            for word in text.split()
            if word in self.geopolitical_indicators
        )
        
        if geopolitical_score >= 2.0:
            return True
        
        return False
    
    def _calculate_total_relevance(self, scored_premises: List[Tuple[str, float]]) -> float:
        """Calculate overall relevance score"""
        if not scored_premises:
            return 0.0
        
        # Weight by position (top premises matter more)
        weighted_sum = 0.0
        weight_sum = 0.0
        
        for i, (_, score) in enumerate(scored_premises[:10]):  # Top 10
            weight = 1.0 / (i + 1)  # Decreasing weight
            weighted_sum += score * weight
            weight_sum += weight
        
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0
    
    def _generate_selection_rationale(self, rai_input, primary: List[str], 
                                    secondary: List[str], wisdom_overlay: bool) -> str:
        """Generate explanation for premise selection"""
        
        rationale_parts = []
        
        # Input characteristics
        rationale_parts.append(
            f"Input classified as {rai_input.input_type.value} with "
            f"complexity {rai_input.complexity_score}/5 and "
            f"emotional charge {rai_input.emotional_charge}/5."
        )
        
        # Detected topics
        if rai_input.detected_topics:
            rationale_parts.append(
                f"Detected topic domains: {', '.join(rai_input.detected_topics)}."
            )
        
        # Primary premises reasoning
        if primary:
            primary_domains = list(set(p.split('.')[0] for p in primary))
            rationale_parts.append(
                f"Selected {len(primary)} primary premises from domains: "
                f"{', '.join(primary_domains)} based on keyword matching and contextual relevance."
            )
        
        # Secondary premises reasoning
        if secondary:
            secondary_domains = list(set(p.split('.')[0] for p in secondary))
            rationale_parts.append(
                f"Added {len(secondary)} secondary premises from domains: "
                f"{', '.join(secondary_domains)} for broader contextual support."
            )
        
        # Wisdom overlay reasoning
        if wisdom_overlay:
            rationale_parts.append(
                "Wisdom overlay activated due to high complexity, emotional charge, "
                "or geopolitical significance."
            )
        
        return " ".join(rationale_parts)
    
    def _fallback_selection(self, rai_input) -> PremiseSelection:
        """Fallback selection when main algorithm fails"""
        
        # Basic selection based on input type
        fallback_premises = {
            "factual_claim": ["D3.1", "D2.2"],
            "narrative": ["D4.1", "D6.1"],
            "system_premise": ["D1.1", "D2.1", "D5.1"],
            "mixed": ["D1.1", "D3.1"],
            "question": ["D6.1", "D7.1"]
        }
        
        input_type = rai_input.input_type.value
        primary = fallback_premises.get(input_type, ["D1.1", "D3.1"])
        
        return PremiseSelection(
            primary_premises=primary,
            secondary_premises=[],
            wisdom_overlay=False,
            total_relevance_score=0.3,
            selection_rationale="Fallback selection due to processing error."
        )
    
    def format_premises_for_prompt(self, selection: PremiseSelection) -> str:
        """Format selected premises for inclusion in RAI prompt"""
        
        if not selection.primary_premises:
            return ""
        
        formatted_parts = []
        
        # Header
        formatted_parts.append("**RELEVANT MACRO PREMISES:**")
        formatted_parts.append("")
        
        # Primary premises
        formatted_parts.append("**Primary Interpretive Lenses:**")
        for prem_id in selection.primary_premises:
            premise_data = self._get_premise_data(prem_id)
            if premise_data:
                formatted_parts.append(f"• **{prem_id}**: {premise_data['title']}")
                formatted_parts.append(f"  {premise_data['content'][:200]}...")
                formatted_parts.append("")
        
        # Secondary premises (if any)
        if selection.secondary_premises:
            formatted_parts.append("**Supporting Context:**")
            for prem_id in selection.secondary_premises:
                premise_data = self._get_premise_data(prem_id)
                if premise_data:
                    formatted_parts.append(f"• **{prem_id}**: {premise_data['title']}")
                    formatted_parts.append("")
        
        # Wisdom overlay note
        if selection.wisdom_overlay:
            formatted_parts.append("**⚡ WISDOM OVERLAY ACTIVATED ⚡**")
            formatted_parts.append("Apply these premises as deep interpretive lenses, not surface constraints.")
            formatted_parts.append("")
        
        # Selection rationale
        formatted_parts.append(f"**Selection Rationale:** {selection.selection_rationale}")
        formatted_parts.append("")
        
        return "\n".join(formatted_parts)
    
    def _get_premise_data(self, prem_id: str) -> Optional[Dict]:
        """Get premise data by ID"""
        domain_id = prem_id.split('.')[0]
        
        if domain_id in self.premise_library["dimensions"]:
            dimension = self.premise_library["dimensions"][domain_id]
            return dimension["premises"].get(prem_id)
        
        return None
    
    def get_premise_summary(self, prem_id: str) -> str:
        """Get a brief summary of a premise"""
        premise_data = self._get_premise_data(prem_id)
        if premise_data:
            return f"{prem_id}: {premise_data['title']}"
        return f"{prem_id}: Unknown premise"


# Integration example
if __name__ == "__main__":
    from rai_wrapper import RAIWrapper, RAIInput, InputType
    
    # Initialize engines
    rai_wrapper = RAIWrapper()
    premise_engine = PremiseEngine()
    
    # Test input
    test_input = "The Western media's coverage of the Ukraine conflict shows clear bias and this proves information warfare is real and ongoing."
    
    # Process with RAI wrapper
    rai_result = rai_wrapper.process_input(test_input)
    rai_input = rai_result['input']
    
    # Select premises
    premise_selection = premise_engine.select_premises(rai_input)
    
    print("=== PREMISE SELECTION RESULT ===")
    print(f"Primary Premises: {premise_selection.primary_premises}")
    print(f"Secondary Premises: {premise_selection.secondary_premises}")
    print(f"Wisdom Overlay: {premise_selection.wisdom_overlay}")
    print(f"Total Relevance: {premise_selection.total_relevance_score:.3f}")
    print(f"Rationale: {premise_selection.selection_rationale}")
    print("\n=== FORMATTED FOR PROMPT ===")
    print(premise_engine.format_premises_for_prompt(premise_selection))
