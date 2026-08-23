"""NetSage AI: Deterministic Rule Verification Engine.
Executes pre-LLM regex static checks for known Cisco IOS anomalies.
"""
import re
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RuleViolation:
    rule_id: str
    osi_layer: str
    evidence: str
    suggested_action: str
    blast_radius: str
    confidence: float


def run_deterministic_checks(show_output: str) -> List[RuleViolation]:
    violations: List[RuleViolation] = []
    if not isinstance(show_output, str) or not show_output.strip():
        return violations

    # Rule 1: Administratively Down Interfaces (Layer 1 / Physical/Sub-interface)
    admin_down = re.finditer(
        r"(?P<iface>\S+)\s+is\s+administratively\s+down,\s+line\s+protocol\s+is\s+down|"
        r"(?P<iface2>\S+)\s+\S+\s+\S+\s+\S+\s+administratively\s+down\s+down",
        show_output,
        re.IGNORECASE
    )
    for match in admin_down:
        iface = match.group("iface") or match.group("iface2")
        violations.append(
            RuleViolation(
                rule_id="RULE-L1-ADMIN-DOWN",
                osi_layer="Layer 1",
                evidence=match.group(0),
                suggested_action=f"interface {iface}\n no shutdown",
                blast_radius="LOW",
                confidence=1.0
            )
        )

    # Rule 2: Missing NAT Overload Flag on Source Translation (Layer 4 / PAT)
    if re.search(
        r"ip\s+nat\s+inside\s+source\s+list\s+\d+\s+interface\s+\S+",
        show_output,
        re.IGNORECASE
    ) and not re.search(
        r"ip\s+nat\s+inside\s+source\s+list\s+\d+\s+interface\s+\S+\s+overload",
        show_output,
        re.IGNORECASE
    ):
        violations.append(
            RuleViolation(
                rule_id="RULE-L4-NAT-NO-OVERLOAD",
                osi_layer="Layer 4",
                evidence="NAT statement configured without PAT 'overload' flag",
                suggested_action="ip nat inside source list 1 interface Serial0/0/0 overload",
                blast_radius="MEDIUM",
                confidence=0.98
            )
        )

    # Rule 3: Access-List Explicit/Implicit Deny Drops Accumulation (Layer 4)
    acl_deny_match = re.search(
        r"(\d+)\s+matches.*deny\s+any|deny\s+ip\s+any\s+any\s+\((\d+)\s+matches\)",
        show_output,
        re.IGNORECASE
    )
    if acl_deny_match:
        violations.append(
            RuleViolation(
                rule_id="RULE-L4-ACL-IMPLICIT-DROP",
                osi_layer="Layer 4",
                evidence=f"Active packet drop counter in ACL: {acl_deny_match.group(0)}",
                suggested_action="Review permit statements for destination IP and service ports",
                blast_radius="HIGH",
                confidence=0.92
            )
        )

    # Rule 4: Native VLAN Mismatch / STP Inconsistency (Layer 2)
    if re.search(
        r"Native\s+VLAN\s+mismatch\s+discovered|blocking\s+FastEthernet\S+\s+on\s+VLAN\d+",
        show_output,
        re.IGNORECASE
    ):
        violations.append(
            RuleViolation(
                rule_id="RULE-L2-NATIVE-VLAN-MISMATCH",
                osi_layer="Layer 2",
                evidence="Spanning-Tree port inconsistent native VLAN unblock event",
                suggested_action="switchport trunk native vlan 1",
                blast_radius="MEDIUM",
                confidence=0.95
            )
        )

    return violations