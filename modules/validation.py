"""

Input validation module and messages for AI Red Team Bot.
"""

MESSAGES = {
    "target_empty": "Target cannot be empty.",
    "target_bad_chars": "Target contains invalid characters: {target}",
}

def validate_target(target):
    """Validates and sanitizes the user-provided target."""
    target = target.strip()
    if not target:
        raise ValueError(MESSAGES["target_empty"])
    # Blocca caratteri pericolosi
    if any(c in target for c in [";", "&", "|", "`", "$", "(", ")", "{", "}", "<", ">", "\n", "\r"]):
        raise ValueError(MESSAGES["target_bad_chars"].format(target=target))
