# 18 — Git & release workflow

trunk-based บน `main`; 7 commits ทั้งหมด, 1 ผ่าน PR (#1), ที่เหลือ direct push; ไม่มี tag/release; main ไม่มี branch protection

```mermaid
gitGraph
    commit id: "fe16925 feat"
    commit id: "05f510f docs"
    commit id: "ba70214 docs"
    commit id: "4dbb10d chore"
    commit id: "fceff08 chore"
    branch ci/devsecops-phase1
    commit id: "d733e7a ci"
    checkout main
    merge ci/devsecops-phase1 id: "ec1e2d6 PR 1"
    commit id: "0907a40 uv, mypy, tests"
```

```mermaid
flowchart LR
    Change["Change on branch or main"] --> CI["CI: sdk + security"]
    CI --> Main["main"]
    Main --> Copy["Manual re-copy into consumers"]
    Copy --> ConsCI["Consumer repo CI and its own deploy"]
```

หมายเหตุ: PR #1 ใน GitHub ถูก merge แล้วเป็น commit `ec1e2d6` บน main (first-parent) — gitGraph แสดงเป็น merge เพื่ออ่านง่าย; ไม่ได้ตรวจว่า merge แบบ squash หรือ merge commit

Sources: `git log --first-parent origin/main`, `gh pr list --state all`, `gh run list` (PR head `d733e7a`), `gh api .../branches/main/protection` (404), `git tag` (empty), `README.md`
