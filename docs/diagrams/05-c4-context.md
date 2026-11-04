# 05 — C4 Context

library ไม่มี runtime ของตัวเอง จึงแสดง library **อยู่ภายใน** consumer services

```mermaid
C4Context
    title service_auth library in its consumers
    Person(owner, "Owner", "Calls owner-private APIs through a caller")
    System_Ext(issuer, "Token issuer", "Signs RS256 service JWTs; consumer READMEs name Solo Web")
    System_Boundary(consumers, "Consumer services (each with vendor/service-auth)") {
        System(accounts, "accounts-metadata-api", "aud accounts-api")
        System(aiusage, "ai-usage-api", "aud ai-usage-api")
        System(integ, "integrations-api", "aud integrations-api")
        System(know, "knowledge-api", "aud knowledge-api, forked copy")
        System(saas, "saas-catalog-api", "aud saas-catalog-api")
    }
    System_Ext(gh, "GitHub bookchaowalit/platform-auth-sdk", "Canonical source, public")
    Rel(owner, issuer, "Uses")
    Rel(issuer, accounts, "Bearer JWT")
    Rel(issuer, integ, "Bearer JWT")
    Rel(gh, consumers, "Manual re-copy of service_auth")
```

Sources: `README.md`, `PRODUCT.md`, consumer `server.py` (`AuthPolicy.from_env` audience), consumer READMEs (platform-accounts-api `services/accounts-metadata-api/README.md`, platform-integrations-api `README.md`: issuer = Solo Web origin), `gh repo view` (visibility PUBLIC)

หมายเหตุ: ภาพแสดงเส้น issuer ไปเพียง 2 consumer ที่ README ยืนยันว่าเป็น Solo Web; ส่วนอื่นไม่ได้ตรวจ issuer จริง

Open questions:
- issuer ของ ai-usage-api, saas-catalog-api, knowledge-api ใน production คือใคร (env `<PREFIX>AUTH_ISSUER` อยู่ใน runtime config ไม่อยู่ใน repo)
