HOOK_TEMPLATE = """[Trigger]
Operation = Install
Operation = Upgrade
Type = Package
{targets}

[Action]
Description = [{name}] VSCodium installation hook
Exec = /usr/bin/{name} patch
When = PostTransaction
NeedsTargets
"""
HOOK_TARGET_TEMPLATE = "Target = {pkg}"
