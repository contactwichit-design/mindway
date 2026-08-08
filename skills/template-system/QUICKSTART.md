# Template System Quickstart

Status: REVIEW_READY

## Human usage
You do not need to name a template. Describe the work normally.

Examples:
- “ทำ memo ขออนุมัติเรื่องนี้”
- “วิเคราะห์ชีทนี้และสรุปสิ่งที่ต้องตัดสินใจ”
- “สร้างคลิป LMS M05”
- “ทำ status ของ routine รอบนี้”
- “งานนี้ติดตรงไหน ทำต่อได้อะไรบ้าง”

The AI should route automatically.

## AI fast path
1. Read `REGISTRY.md`.
2. Classify behavior.
3. Use `ROUTER.md` or `SYSTEM.json` to choose the minimum family set.
4. Read only selected sections in `FAMILIES.md` or `TEMPLATES.md`.
5. Resolve owner-system source truth.
6. Choose renderer separately.
7. Apply a design profile only if the output needs one.
8. Execute → verify → handoff.

## Common recipes
- Approval memo → T01+T09+T10+T07
- Research → T01+T02+T07 (+T10 if durable document)
- Plan → T01+T03+T17+T07
- Decision → T01+T02+T04+T07
- Status → T01+T05+T17+T07
- HOFF → T01+T06+T07
- Data dashboard → T01+T08+T04+T13+T07
- Graphic → T01+T11+T07
- Presentation → T01+T12+T11+T07
- Web/UI → T01+T13+T07+T06
- LMS lesson/video → T01+T14+T15+T11+T07+T06
- Automation → T01+T16+T05+T17+T07
- Evolution → T01+T18+T07+T06

## Non-negotiable behavior
- Do not load all families by default.
- Do not treat PDF/DOCX/PPTX as the work intent; they are renderers/output formats.
- Do not invent missing owner-system facts.
- Do not let a soft blocker stop independent safe work.
- Do not claim final when evidence/approval is still missing.
- Prefer updating an existing template/family over creating a new one.

## Personal design
For ZAFT personal functional surfaces, use `DESIGN_PROFILE_ZAFT_PERSONAL.md`. Project/corporate locked design systems override it when applicable.