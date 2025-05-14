HOOK_TEMPLATE = """[Trigger]
Operation = Install
Operation = Upgrade
Type = Package
{targets}

[Action]
Description = [{name}] VSCodium installation hook
Exec = {bin} hook patch
When = PostTransaction
NeedsTargets
"""
HOOK_TARGET_TEMPLATE = "Target = {pkg}"
