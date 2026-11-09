"""
NOIZYVOX Project Manager
========================

Voice work projects, contracts, and assignments.

Professional voice work, professionally managed.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4


class ProjectStatus(Enum):
    """Status of a project."""
    DRAFT = "draft"
    CASTING = "casting"
    ACTIVE = "active"
    RECORDING = "recording"
    POST_PRODUCTION = "post_production"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


class ProjectType(Enum):
    """Types of voice projects."""
    AUDIOBOOK = "audiobook"
    COMMERCIAL = "commercial"
    ANIMATION = "animation"
    VIDEO_GAME = "video_game"
    DOCUMENTARY = "documentary"
    E_LEARNING = "e_learning"
    PODCAST = "podcast"
    IVR = "ivr"
    FILM_DUBBING = "film_dubbing"
    CORPORATE = "corporate"
    PROMO = "promo"
    RADIO = "radio"


class ContractStatus(Enum):
    """Status of a contract."""
    DRAFT = "draft"
    SENT = "sent"
    SIGNED = "signed"
    ACTIVE = "active"
    COMPLETED = "completed"
    TERMINATED = "terminated"


@dataclass
class VoiceRole:
    """A voice role within a project."""
    role_id: str = field(default_factory=lambda: str(uuid4()))

    # Role details
    name: str = ""
    description: str = ""
    character_type: str = ""  # protagonist, villain, narrator, etc.

    # Requirements
    gender: str = "any"
    age_range: str = ""
    accent_required: str = ""
    language: str = "English"
    special_requirements: List[str] = field(default_factory=list)

    # Assignment
    assigned_member_id: Optional[str] = None
    assigned_member_name: Optional[str] = None

    # Compensation
    flat_fee: float = 0.0
    per_hour_rate: float = 0.0
    estimated_hours: float = 0.0

    # Status
    audition_required: bool = True
    audition_deadline: Optional[datetime] = None
    filled: bool = False

    # Lines/Pages
    estimated_lines: int = 0
    estimated_pages: float = 0.0


@dataclass
class Contract:
    """A contract for voice work."""
    contract_id: str = field(default_factory=lambda: str(uuid4()))

    # Parties
    project_id: str = ""
    member_id: str = ""
    member_name: str = ""
    client_id: str = ""
    client_name: str = ""

    # Role
    role_id: str = ""
    role_name: str = ""

    # Status
    status: ContractStatus = ContractStatus.DRAFT

    # Terms
    compensation_total: float = 0.0
    payment_schedule: str = "on_completion"
    usage_rights: List[str] = field(default_factory=list)
    usage_term: str = "1 year"
    usage_territory: str = "worldwide"

    # AI & Consent
    ai_training_allowed: bool = False
    synthetic_voice_allowed: bool = False
    consent_id: Optional[str] = None

    # Deliverables
    recording_deadline: Optional[datetime] = None
    revision_rounds: int = 2

    # Signatures
    member_signed: bool = False
    member_signed_date: Optional[datetime] = None
    client_signed: bool = False
    client_signed_date: Optional[datetime] = None

    # Dates
    created_date: datetime = field(default_factory=datetime.utcnow)

    @property
    def fully_signed(self) -> bool:
        """Check if contract is fully signed."""
        return self.member_signed and self.client_signed

    def sign_member(self):
        """Sign as member."""
        self.member_signed = True
        self.member_signed_date = datetime.utcnow()
        if self.fully_signed:
            self.status = ContractStatus.ACTIVE

    def sign_client(self):
        """Sign as client."""
        self.client_signed = True
        self.client_signed_date = datetime.utcnow()
        if self.fully_signed:
            self.status = ContractStatus.ACTIVE


@dataclass
class Project:
    """A voice work project."""
    project_id: str = field(default_factory=lambda: str(uuid4()))

    # Identity
    title: str = ""
    description: str = ""
    project_type: ProjectType = ProjectType.COMMERCIAL

    # Client
    client_id: str = ""
    client_name: str = ""
    client_contact: str = ""

    # Status
    status: ProjectStatus = ProjectStatus.DRAFT

    # Roles
    roles: List[VoiceRole] = field(default_factory=list)
    contracts: List[str] = field(default_factory=list)  # Contract IDs

    # Budget
    total_budget: float = 0.0
    budget_allocated: float = 0.0
    budget_spent: float = 0.0

    # Timeline
    created_date: datetime = field(default_factory=datetime.utcnow)
    casting_deadline: Optional[datetime] = None
    recording_start: Optional[datetime] = None
    recording_end: Optional[datetime] = None
    delivery_date: Optional[datetime] = None

    # Specifications
    audio_format: str = "WAV 48kHz/24bit"
    delivery_format: str = "WAV"
    style_guide: str = ""

    # Files
    script_url: Optional[str] = None
    reference_audio: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)

    # Notes
    notes: str = ""

    @property
    def roles_filled(self) -> int:
        """Number of roles filled."""
        return sum(1 for r in self.roles if r.filled)

    @property
    def total_roles(self) -> int:
        """Total number of roles."""
        return len(self.roles)

    @property
    def is_fully_cast(self) -> bool:
        """Check if all roles are filled."""
        return all(r.filled for r in self.roles)

    def add_role(self, role: VoiceRole):
        """Add a role to the project."""
        self.roles.append(role)

    def assign_role(self, role_id: str, member_id: str, member_name: str) -> bool:
        """Assign a member to a role."""
        for role in self.roles:
            if role.role_id == role_id:
                role.assigned_member_id = member_id
                role.assigned_member_name = member_name
                role.filled = True
                return True
        return False

    def start_casting(self):
        """Begin casting phase."""
        self.status = ProjectStatus.CASTING

    def start_recording(self):
        """Begin recording phase."""
        self.status = ProjectStatus.RECORDING
        self.recording_start = datetime.utcnow()

    def complete(self):
        """Mark project as completed."""
        self.status = ProjectStatus.COMPLETED


class ProjectManager:
    """
    The Project Manager.

    Manages all voice work projects.
    """

    def __init__(self):
        self.manager_id = str(uuid4())
        self.projects: Dict[str, Project] = {}
        self.contracts: Dict[str, Contract] = {}
        self.created = datetime.utcnow()

    # ─────────────────────────────────────────────────────────────────────────
    # Projects
    # ─────────────────────────────────────────────────────────────────────────

    def create_project(
        self,
        title: str,
        project_type: ProjectType,
        client_id: str,
        client_name: str,
        description: str = ""
    ) -> Project:
        """Create a new project."""
        project = Project(
            title=title,
            description=description,
            project_type=project_type,
            client_id=client_id,
            client_name=client_name
        )
        self.projects[project.project_id] = project
        return project

    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID."""
        return self.projects.get(project_id)

    def add_role_to_project(self, project_id: str, role: VoiceRole) -> bool:
        """Add a role to a project."""
        project = self.projects.get(project_id)
        if not project:
            return False

        project.add_role(role)
        return True

    # ─────────────────────────────────────────────────────────────────────────
    # Contracts
    # ─────────────────────────────────────────────────────────────────────────

    def create_contract(
        self,
        project_id: str,
        role_id: str,
        member_id: str,
        member_name: str
    ) -> Optional[Contract]:
        """Create a contract for a role assignment."""
        project = self.projects.get(project_id)
        if not project:
            return None

        # Find role
        role = None
        for r in project.roles:
            if r.role_id == role_id:
                role = r
                break

        if not role:
            return None

        contract = Contract(
            project_id=project_id,
            member_id=member_id,
            member_name=member_name,
            client_id=project.client_id,
            client_name=project.client_name,
            role_id=role_id,
            role_name=role.name,
            compensation_total=role.flat_fee or (role.per_hour_rate * role.estimated_hours)
        )

        self.contracts[contract.contract_id] = contract
        project.contracts.append(contract.contract_id)

        return contract

    def sign_contract(self, contract_id: str, signer: str) -> bool:
        """Sign a contract."""
        contract = self.contracts.get(contract_id)
        if not contract:
            return False

        if signer == "member":
            contract.sign_member()
        elif signer == "client":
            contract.sign_client()
        else:
            return False

        # If fully signed, assign the role
        if contract.fully_signed:
            project = self.projects.get(contract.project_id)
            if project:
                project.assign_role(
                    contract.role_id,
                    contract.member_id,
                    contract.member_name
                )

        return True

    # ─────────────────────────────────────────────────────────────────────────
    # Queries
    # ─────────────────────────────────────────────────────────────────────────

    def get_casting_projects(self) -> List[Project]:
        """Get projects currently casting."""
        return [p for p in self.projects.values() if p.status == ProjectStatus.CASTING]

    def get_member_projects(self, member_id: str) -> List[Project]:
        """Get projects a member is assigned to."""
        result = []
        for project in self.projects.values():
            for role in project.roles:
                if role.assigned_member_id == member_id:
                    result.append(project)
                    break
        return result

    def get_open_roles(self, project_type: ProjectType = None) -> List[Dict]:
        """Get unfilled roles, optionally by project type."""
        roles = []
        for project in self.projects.values():
            if project.status != ProjectStatus.CASTING:
                continue
            if project_type and project.project_type != project_type:
                continue

            for role in project.roles:
                if not role.filled:
                    roles.append({
                        "project_id": project.project_id,
                        "project_title": project.title,
                        "project_type": project.project_type.value,
                        "role": role
                    })

        return roles

    # ─────────────────────────────────────────────────────────────────────────
    # Statistics
    # ─────────────────────────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """Get project manager statistics."""
        all_projects = list(self.projects.values())

        status_counts = {}
        for status in ProjectStatus:
            status_counts[status.value] = len([p for p in all_projects if p.status == status])

        type_counts = {}
        for ptype in ProjectType:
            type_counts[ptype.value] = len([p for p in all_projects if p.project_type == ptype])

        total_roles = sum(p.total_roles for p in all_projects)
        filled_roles = sum(p.roles_filled for p in all_projects)

        return {
            "total_projects": len(all_projects),
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "total_roles": total_roles,
            "filled_roles": filled_roles,
            "open_roles": total_roles - filled_roles,
            "total_contracts": len(self.contracts),
            "signed_contracts": len([c for c in self.contracts.values() if c.fully_signed]),
            "total_budget": sum(p.total_budget for p in all_projects)
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the Project Manager."""
    print("\n" + "=" * 70)
    print("NOIZYVOX PROJECT MANAGER — DEMO")
    print("Professional voice work, professionally managed")
    print("=" * 70)

    manager = ProjectManager()

    # Create project
    print("\n" + "─" * 50)
    print("  CREATING PROJECT")
    print("─" * 50)

    project = manager.create_project(
        title="Epic Fantasy Audiobook",
        project_type=ProjectType.AUDIOBOOK,
        client_id="publisher_001",
        client_name="Grand Publishing House",
        description="Full-cast audiobook, 15 hours estimated"
    )
    project.total_budget = 25000.0
    project.delivery_date = datetime.utcnow() + timedelta(days=90)

    print(f"  Project: {project.title}")
    print(f"  Type: {project.project_type.value}")
    print(f"  Client: {project.client_name}")
    print(f"  Budget: ${project.total_budget:,.2f}")

    # Add roles
    print("\n" + "─" * 50)
    print("  ADDING ROLES")
    print("─" * 50)

    roles = [
        VoiceRole(
            name="Narrator",
            description="Main narrator for the entire book",
            character_type="narrator",
            age_range="35-55",
            flat_fee=8000.0,
            estimated_hours=25
        ),
        VoiceRole(
            name="King Aldric",
            description="The wise but troubled king",
            character_type="protagonist",
            gender="male",
            age_range="50-65",
            accent_required="British",
            flat_fee=3000.0,
            estimated_hours=5
        ),
        VoiceRole(
            name="Princess Elara",
            description="The rebellious princess",
            character_type="protagonist",
            gender="female",
            age_range="18-25",
            flat_fee=3000.0,
            estimated_hours=5
        ),
        VoiceRole(
            name="Dark Sorcerer",
            description="The main antagonist",
            character_type="villain",
            gender="any",
            age_range="40-60",
            special_requirements=["Can do menacing whisper", "Deep voice preferred"],
            flat_fee=2500.0,
            estimated_hours=3
        )
    ]

    for role in roles:
        manager.add_role_to_project(project.project_id, role)
        print(f"  ✓ {role.name} — ${role.flat_fee:,.2f}")

    # Start casting
    project.start_casting()
    print(f"\n  Status: {project.status.value}")
    print(f"  Total roles: {project.total_roles}")

    # Create and sign contract
    print("\n" + "─" * 50)
    print("  CREATING CONTRACT")
    print("─" * 50)

    narrator_role = roles[0]
    contract = manager.create_contract(
        project_id=project.project_id,
        role_id=narrator_role.role_id,
        member_id="member_123",
        member_name="Marcus Williams"
    )

    if contract:
        print(f"  Contract: {contract.contract_id[:8]}...")
        print(f"  Role: {contract.role_name}")
        print(f"  Compensation: ${contract.compensation_total:,.2f}")

        # Sign contract
        manager.sign_contract(contract.contract_id, "member")
        print(f"  ✓ Member signed")

        manager.sign_contract(contract.contract_id, "client")
        print(f"  ✓ Client signed")

        print(f"  Status: {contract.status.value}")

    # Check casting status
    print("\n" + "─" * 50)
    print("  CASTING STATUS")
    print("─" * 50)

    print(f"  Roles filled: {project.roles_filled}/{project.total_roles}")
    print(f"  Fully cast: {project.is_fully_cast}")

    # Open roles
    open_roles = manager.get_open_roles()
    print(f"\n  Open roles: {len(open_roles)}")
    for item in open_roles:
        print(f"    • {item['role'].name} — {item['project_title']}")

    # Stats
    print("\n" + "─" * 50)
    print("  MANAGER STATISTICS")
    print("─" * 50)

    stats = manager.get_stats()
    print(f"  Total projects: {stats['total_projects']}")
    print(f"  Total roles: {stats['total_roles']}")
    print(f"  Open roles: {stats['open_roles']}")
    print(f"  Signed contracts: {stats['signed_contracts']}")

    print("\n" + "=" * 70)
    print("Professional voice work, professionally managed.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
