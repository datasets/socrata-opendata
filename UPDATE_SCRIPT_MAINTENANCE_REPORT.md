## Update Script Maintenance Report

Date: 2026-03-04

- Ran updater: `python main.py`.
- Root cause: no workflow automation and minor script compatibility issue (`is` vs `==` for string comparison).
- Fixes made:
  - Corrected string comparison and hardened optional HTML attribute handling.
  - Added first monthly + manual workflow with dependency install and `contents: write`.
- Validation summary: updater runs and generates dataset outputs; broad full refresh can be long-running due scrape volume.
