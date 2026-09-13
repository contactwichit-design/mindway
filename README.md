# Mindway

> ถ้าคุณมาถึงที่นี่ ไม่ว่าจะตั้งใจหรือบังเอิญ ยินดีต้อนรับครับ

Mindway ไม่ได้เกิดจากคนที่มีคำตอบครบทุกอย่าง แต่เกิดจากคนที่หลงทางบ่อยพอ จนเริ่มวางป้ายบอกทางไว้ระหว่างเดิน

Mindway คือกรอบเปิดสำหรับมนุษย์และ AI เพื่อช่วยกันคิด เรียนรู้ จัดระเบียบ ทำงาน และเติบโต โดยไม่บังคับให้ทุกคนต้องคิดเหมือนกัน

## เริ่มใช้งาน

Mindway ใช้ pre-entry bootstrap contract เพื่อป้องกันกรณีที่ AI สรุปผิดว่า canonical `/my` เข้าไม่ได้หลังจาก transport แรกล้มเหลว

ใส่ข้อความนี้ใน Instruction ของ AI:

```text
MW-BOOT/1
Before substantial work, load and follow canonical Mindway:
https://raw.githubusercontent.com/contactwichit-design/mindway/main/my.md

A failed access method does NOT mean Mindway is inaccessible. Discover and exhaust all safe available read-only routes before declaring MINDWAY_BLOCKED.

Never claim MINDWAY_LOADED unless canonical my.md and every mandatory reference it requires were actually read and verified. Never use memory as proof of access. NO VERIFIED /my = NO SUBSTANTIAL EXECUTION.
```

Full bootstrap contract: [BOOTSTRAP.md](BOOTSTRAP.md)

จากนั้นใช้คำสั่งเดียว:

```text
/my
```

## Continuity / Center AI

สำหรับงานต่อเนื่องที่ต้องข้ามแชท ข้าม AI ข้ามโมเดล หรือกลับมาทำต่อภายหลัง ให้ใช้ [Continuity Center Runtime](skills/continuity-center/SKILL.md)

หลักคือไม่พึ่งความจำของ AI ตัวใดตัวหนึ่ง แต่ให้ AI อ่านบันทึกงานที่มีรหัสและย้อนกลับไปตรวจ source จริงก่อนทำต่อ

### Shorthand

เมื่อ owner ส่งคำสั่งในรูปแบบ:

```text
/my <work-code>
```

เช่น:

```text
/my 13926-1
```

ให้ตีความว่า:

1. เข้า canonical `/my` ตามปกติและผ่าน Entry Access Gate ก่อน
2. โหลด Continuity Center Runtime
3. ใช้ `<work-code>` ตามที่ owner พิมพ์แบบ exact; ห้าม renumber หรือเดาความหมายใหม่
4. รีวิว current conversation และ continuity record ที่เกี่ยวข้องซึ่งเข้าถึงได้
5. สำหรับงาน handoff/off-load หรือระบบซับซ้อน ให้เขียน/อัปเดต **DEEP continuity record** ไม่ใช่สรุปบาง ๆ
6. เก็บ mission, current state, completed/verified work, decisions + rationale, hard locks, dependencies, source of truth, data/interface contracts, risks, failed routes, human/emotional context ที่มีผลต่อการทำงาน, open loops, next actions และ resume instruction เท่าที่เกี่ยวข้อง
7. ใช้ continuity storage/location ที่ workspace หรือ owner กำหนดไว้เดิม; **ห้ามสร้างโฟลเดอร์/พื้นที่ใหม่แทนเอง** หากตำแหน่งเดิมหาไม่พบหรือเขียนไม่ได้ ให้รายงาน blocker แทนการสร้างของใหม่
8. หลังเขียนสำเร็จ ให้ verify การบันทึกและส่งลิงก์/ตำแหน่งกลับให้ owner

`/my <work-code>` เป็น shorthand สำหรับ continuity workflow ไม่ใช่การฝากความจำไว้ในโมเดลตัวเดียว

Center AI เป็น **บทบาทกลาง** ไม่ใช่ model identity ถาวร จึงสามารถเปลี่ยน AI/provider ในอนาคตได้ โดยอ่าน continuity records และ authoritative sources เดิมก่อนทำงานต่อ

ข้อจำกัดสำคัญ: `/my` ไม่ได้ข้ามสิทธิ์ของระบบภายนอก หาก AI ตัวนั้นไม่มีสิทธิ์หรือ connector ไปยัง Google Drive / repository / source เดิม มันต้องรายงานข้อจำกัดตรง ๆ และห้ามอ้างว่าได้อ่านหรืออัปเดตแล้ว

## อ่านต่อ

- [Bootstrap Contract](BOOTSTRAP.md)
- [Public Standard](PUBLIC_STANDARD.md)
- [Continuity Center Runtime](skills/continuity-center/SKILL.md)
- [Welcome](WELCOME.md)
- [How to Use Mindway](USE_MINDWAY.md)
- [Origin Story](ORIGIN_STORY.md)
- [Visitor & Safety](VISITOR_AND_SAFETY.md)
- [Contributing](CONTRIBUTING.md)
- [Credits](CREDITS.md)
- [Say Hello](SAY_HELLO.md)

## หลักสั้นที่สุด

- เริ่มด้วยความเคารพ
- คิดด้วยตัวเอง
- ตัดสินด้วยเหตุผลและหลักฐาน
- แบ่งปันสิ่งที่แบ่งปันได้
- ปกป้องสิ่งที่ได้รับความไว้วางใจ
- หยิบสิ่งที่ช่วยคุณไป แล้วแวะกลับมาทิ้งสิ่งที่อาจช่วยคนอื่น

Mindway was initiated and is stewarded by zaft (ZF), developed through ongoing collaboration with AI systems, and informed by wider human and open-source knowledge.
