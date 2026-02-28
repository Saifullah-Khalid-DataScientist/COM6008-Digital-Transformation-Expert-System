# advisor_engine.py
# Small Business Digital Transformation Advisor - Expert Rule Engine
# Knowledge derived from McKinsey Digital Maturity Framework (2023),
# Gartner IT Maturity Model (2024), and EU SME Digital Index (2023)

class DigitalTransformationAdvisor:

    def __init__(self, answers):
        """
        answers: dict with keys from 8 business profile questions + 25 rule questions
        All values are 1 (Yes) or 0 (No)
        Profile keys: company_size, budget_level, industry, years_operating
        """
        self.answers = answers
        self.score = 0
        self.max_score = 100
        self.recommendations = []          # (priority, category, text)
        self.rule_log = []                 # fired rule descriptions
        self.category_scores = {}          # per-category breakdown
        self.risk_flags = []               # risk assessment findings
        self.critical_gaps = []            # must-fix items

    # ─────────────────────────────────────────────
    #  HELPER
    # ─────────────────────────────────────────────

    def _a(self, key):
        return bool(self.answers.get(key, 0))

    def _add_rule(self, rule_id, description, score_delta, category):
        self.score += score_delta
        self.category_scores[category] = self.category_scores.get(category, 0) + score_delta
        self.rule_log.append({
            "id": rule_id,
            "description": description,
            "points": score_delta,
            "category": category
        })

    def _add_rec(self, priority, category, text):
        """priority: Critical | Important | Optional"""
        self.recommendations.append({
            "priority": priority,
            "category": category,
            "text": text
        })

    # ─────────────────────────────────────────────
    #  25 EXPERT RULES
    # ─────────────────────────────────────────────

    def apply_rules(self):
        a = self._a

        # ── INFRASTRUCTURE (Rules 1–5) ──────────────────────────────────

        # Rule 1: Cloud adoption
        if a("cloud"):
            self._add_rule(1, "Cloud infrastructure adopted — scalability and remote access enabled.", 6, "Infrastructure")
        else:
            self._add_rule(1, "No cloud adoption — critical scalability gap identified.", 0, "Infrastructure")
            self._add_rec("Critical", "Infrastructure",
                "Migrate to cloud infrastructure (e.g. AWS, Azure, Google Cloud). "
                "Even a free-tier start reduces hardware costs and improves resilience.")
            self.critical_gaps.append("Cloud Infrastructure")

        # Rule 2: Cybersecurity practices
        if a("security"):
            self._add_rule(2, "Active cybersecurity measures — operational risk is controlled.", 6, "Infrastructure")
        else:
            self._add_rule(2, "No cybersecurity — high risk of data breach and legal liability.", 0, "Infrastructure")
            self._add_rec("Critical", "Infrastructure",
                "Implement cybersecurity baseline: firewall, endpoint protection, MFA, "
                "and regular security audits. GDPR non-compliance can result in heavy fines.")
            self.risk_flags.append("Cybersecurity Gap — HIGH RISK")
            self.critical_gaps.append("Cybersecurity")

        # Rule 3: Automated backup systems
        if a("backup"):
            self._add_rule(3, "Automated backups maintained — data loss risk minimised.", 4, "Infrastructure")
        else:
            self._add_rule(3, "No backup system — data loss risk is significant.", 0, "Infrastructure")
            self._add_rec("Critical", "Infrastructure",
                "Set up automated daily backups using cloud storage (e.g. Backblaze, AWS S3). "
                "Data loss can permanently cripple a small business.")
            self.risk_flags.append("No Backup System — DATA LOSS RISK")

        # Rule 4: Cloud + Security compound rule
        if a("cloud") and a("security"):
            self._add_rule(4, "Cloud AND Security active — infrastructure maturity is strong. Bonus awarded.", 4, "Infrastructure")
        elif not a("cloud") and not a("security"):
            self._add_rule(4, "Neither cloud nor security implemented — infrastructure critically underdeveloped.", 0, "Infrastructure")
            self.risk_flags.append("Infrastructure foundations completely absent")

        # Rule 5: Mobile access to systems
        if a("mobile_access"):
            self._add_rule(5, "Mobile-accessible systems — workforce flexibility supported.", 3, "Infrastructure")
        else:
            self._add_rule(5, "No mobile access — workforce agility is restricted.", 0, "Infrastructure")
            self._add_rec("Important", "Infrastructure",
                "Enable mobile access to key business systems. "
                "Remote and field teams require mobile-ready tools to remain productive.")

        # ── DATA & INTELLIGENCE (Rules 6–9) ─────────────────────────────

        # Rule 6: Data analytics usage
        if a("analytics"):
            self._add_rule(6, "Data analytics in use — decisions are evidence-based.", 5, "Data & Intelligence")
        else:
            self._add_rule(6, "No analytics — decisions are likely based on intuition, reducing accuracy.", 0, "Data & Intelligence")
            self._add_rec("Important", "Data & Intelligence",
                "Adopt business intelligence tools (e.g. Google Looker Studio, Power BI). "
                "Data-driven decisions improve revenue by up to 23% (McKinsey, 2023).")

        # Rule 7: Centralised data management
        if a("data_management"):
            self._add_rule(7, "Centralised data management — data accessibility and quality are ensured.", 4, "Data & Intelligence")
        else:
            self._add_rule(7, "Data is siloed — inconsistency and duplication likely.", 0, "Data & Intelligence")
            self._add_rec("Important", "Data & Intelligence",
                "Implement a centralised data warehouse or cloud database. "
                "Data silos prevent analytics and slow operational decisions.")

        # Rule 8: Performance tracking tools
        if a("performance_tracking"):
            self._add_rule(8, "Digital performance tracking active — KPIs are visible and actionable.", 3, "Data & Intelligence")
        else:
            self._add_rule(8, "No performance tracking — business health is not measurable.", 0, "Data & Intelligence")
            self._add_rec("Important", "Data & Intelligence",
                "Deploy KPI dashboards to track sales, customer satisfaction, and operational metrics in real time.")

        # Rule 9: Analytics + Data Management compound
        if a("analytics") and a("data_management"):
            self._add_rule(9, "Analytics AND centralised data both present — full data intelligence capability achieved.", 4, "Data & Intelligence")

        # ── AUTOMATION & AI (Rules 10–13) ────────────────────────────────

        # Rule 10: Business process automation
        if a("automation"):
            self._add_rule(10, "Process automation adopted — manual workload significantly reduced.", 5, "Automation & AI")
        else:
            self._add_rule(10, "No automation — staff are overloaded with repetitive tasks.", 0, "Automation & AI")
            self._add_rec("Important", "Automation & AI",
                "Automate repetitive workflows using tools like Zapier or Microsoft Power Automate. "
                "SMEs recover 20+ hours/week through basic automation.")

        # Rule 11: AI in operations
        if a("ai_tools"):
            self._add_rule(11, "AI tools in operations — predictive capability and efficiency enhanced.", 5, "Automation & AI")
        else:
            self._add_rule(11, "No AI adoption — competitive disadvantage growing as AI becomes standard.", 0, "Automation & AI")
            self._add_rec("Optional", "Automation & AI",
                "Explore AI tools for customer service (chatbots), inventory prediction, or marketing automation. "
                "Many are affordable for SMEs (e.g. HubSpot AI, Tidio).")

        # Rule 12: Automation + AI compound — high maturity signal
        if a("automation") and a("ai_tools"):
            self._add_rule(12, "Automation AND AI both implemented — highest operational efficiency tier reached.", 5, "Automation & AI")

        # Rule 13: Agile methodologies used
        if a("agile"):
            self._add_rule(13, "Agile methods adopted — adaptability and project delivery speed improved.", 3, "Automation & AI")
        else:
            self._add_rec("Optional", "Automation & AI",
                "Adopt agile project management (Scrum or Kanban) to improve team responsiveness and delivery cycles.")

        # ── CUSTOMER & MARKET (Rules 14–17) ──────────────────────────────

        # Rule 14: CRM system
        if a("crm"):
            self._add_rule(14, "CRM system in use — customer relationships are systematically managed.", 5, "Customer & Market")
        else:
            self._add_rule(14, "No CRM — customer data is likely scattered, losing revenue opportunities.", 0, "Customer & Market")
            self._add_rec("Critical", "Customer & Market",
                "Implement a CRM system (e.g. HubSpot Free, Zoho CRM). "
                "CRM adoption increases customer retention by up to 27% (Gartner, 2024).")
            self.critical_gaps.append("CRM System")

        # Rule 15: Digital customer platform/portal
        if a("customer_platform"):
            self._add_rule(15, "Digital customer platform active — customer accessibility enhanced.", 4, "Customer & Market")
        else:
            self._add_rule(15, "No digital customer channel — customer experience is limited to offline.", 0, "Customer & Market")
            self._add_rec("Important", "Customer & Market",
                "Build a customer-facing digital portal or website with self-service capability.")

        # Rule 16: Digital marketing
        if a("digital_marketing"):
            self._add_rule(16, "Digital marketing in use — customer reach is extended online.", 3, "Customer & Market")
        else:
            self._add_rule(16, "No digital marketing — growth potential is severely limited.", 0, "Customer & Market")
            self._add_rec("Important", "Customer & Market",
                "Invest in digital marketing: SEO, email campaigns, and social media. "
                "Cost-effective tools include Mailchimp and Google Ads.")

        # Rule 17: CRM + Digital Marketing compound — full customer lifecycle
        if a("crm") and a("digital_marketing"):
            self._add_rule(17, "CRM AND digital marketing combined — full customer acquisition-to-retention loop operational.", 4, "Customer & Market")

        # ── STRATEGY & GOVERNANCE (Rules 18–21) ──────────────────────────

        # Rule 18: Defined digital strategy
        if a("strategy"):
            self._add_rule(18, "Digital strategy defined — transformation has clear direction and milestones.", 5, "Strategy & Governance")
        else:
            self._add_rule(18, "No digital strategy — investment risks being wasted without direction.", 0, "Strategy & Governance")
            self._add_rec("Critical", "Strategy & Governance",
                "Develop a 12-month digital transformation roadmap. "
                "Define goals, budget allocation, and success metrics before investing in tools.")
            self.critical_gaps.append("Digital Strategy")

        # Rule 19: Leadership support
        if a("leadership"):
            self._add_rule(19, "Leadership actively supports digital transformation — organisational alignment ensured.", 4, "Strategy & Governance")
        else:
            self._add_rule(19, "No leadership buy-in — transformation initiatives are likely to stall.", 0, "Strategy & Governance")
            self._add_rec("Critical", "Strategy & Governance",
                "Secure executive sponsorship for digital transformation. "
                "Without leadership alignment, 70% of transformation programmes fail (McKinsey, 2023).")
            self.risk_flags.append("No Leadership Buy-In — TRANSFORMATION RISK")

        # Rule 20: IT governance defined
        if a("governance"):
            self._add_rule(20, "IT governance in place — technology investments are controlled and compliant.", 3, "Strategy & Governance")
        else:
            self._add_rec("Optional", "Strategy & Governance",
                "Establish basic IT governance policies covering data privacy, software licensing, and access control.")

        # Rule 21: Strategy + Leadership compound
        if a("strategy") and a("leadership"):
            self._add_rule(21, "Strategy AND leadership aligned — transformation success probability significantly elevated.", 4, "Strategy & Governance")

        # ── PEOPLE & COLLABORATION (Rules 22–25) ─────────────────────────

        # Rule 22: Employee digital training
        if a("training"):
            self._add_rule(22, "Digital training programme active — workforce capability continuously improving.", 4, "People & Collaboration")
        else:
            self._add_rule(22, "No digital training — tools adopted without skilled users will underperform.", 0, "People & Collaboration")
            self._add_rec("Important", "People & Collaboration",
                "Invest in structured digital skills training. "
                "Platforms like Google Digital Garage and LinkedIn Learning offer free SME-focused courses.")

        # Rule 23: Digital collaboration tools
        if a("collaboration"):
            self._add_rule(23, "Digital collaboration tools in use — team coordination and communication are efficient.", 3, "People & Collaboration")
        else:
            self._add_rule(23, "No collaboration tools — team efficiency is impaired.", 0, "People & Collaboration")
            self._add_rec("Important", "People & Collaboration",
                "Adopt collaboration platforms (e.g. Microsoft Teams, Slack, Notion) to improve team communication and productivity.")

        # Rule 24: Remote work capability
        if a("remote_work"):
            self._add_rule(24, "Remote work infrastructure in place — business continuity is protected.", 3, "People & Collaboration")
        else:
            self._add_rec("Optional", "People & Collaboration",
                "Enable remote working capability to attract talent and ensure business continuity during disruptions.")

        # Rule 25: Training + Collaboration + Leadership — triple maturity compound rule
        if a("training") and a("collaboration") and a("leadership"):
            self._add_rule(25, "Training, Collaboration AND Leadership all present — people-led digital culture fully established. Maximum people maturity bonus awarded.", 5, "People & Collaboration")
        elif a("training") and a("collaboration"):
            self._add_rule(25, "Training and Collaboration present — strong people capability, but leadership alignment is still needed.", 2, "People & Collaboration")

    # ─────────────────────────────────────────────
    #  RISK ASSESSMENT
    # ─────────────────────────────────────────────

    def assess_risk(self):
        critical_count = sum(1 for r in self.recommendations if r["priority"] == "Critical")

        if critical_count >= 4:
            risk_level = "HIGH"
            risk_description = "Multiple critical gaps identified. Immediate action required to avoid operational and competitive risk."
        elif critical_count >= 2:
            risk_level = "MEDIUM"
            risk_description = "Some critical weaknesses present. Address priority items within the next 6 months."
        else:
            risk_level = "LOW"
            risk_description = "Organisation shows solid digital foundations. Focus on optimisation and innovation."

        return risk_level, risk_description

    # ─────────────────────────────────────────────
    #  MATURITY LEVEL
    # ─────────────────────────────────────────────

    def get_maturity_level(self):
        if self.score >= 72:
            return "Advanced Digital Business", "#27ae60", 3
        elif self.score >= 42:
            return "Developing Digital Business", "#f39c12", 2
        else:
            return "Early Stage Digital Business", "#e74c3c", 1

    # ─────────────────────────────────────────────
    #  EVALUATE
    # ─────────────────────────────────────────────

    def evaluate(self):
        self.apply_rules()

        level, color, tier = self.get_maturity_level()
        risk_level, risk_description = self.assess_risk()

        # Normalise score to 100
        raw_possible = 100
        normalised = min(round((self.score / raw_possible) * 100), 100)

        sorted_recs = sorted(
            self.recommendations,
            key=lambda r: {"Critical": 0, "Important": 1, "Optional": 2}[r["priority"]]
        )

        return {
            "score": self.score,
            "score_pct": normalised,
            "level": level,
            "level_color": color,
            "tier": tier,
            "risk_level": risk_level,
            "risk_description": risk_description,
            "risk_flags": self.risk_flags,
            "critical_gaps": self.critical_gaps,
            "recommendations": sorted_recs,
            "rules_triggered": self.rule_log,
            "category_scores": self.category_scores
        }