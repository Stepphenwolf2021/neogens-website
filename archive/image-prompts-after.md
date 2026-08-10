# Prompt สำหรับสร้างภาพ "After" — Neo Gens

ใช้กับโมเดลสร้างภาพแนวสมจริง เช่น Midjourney, Google Imagen / Nano Banana, GPT Image, Flux

---

## อ่านก่อนหนึ่งข้อ สำคัญที่สุด

**อย่าให้ AI เขียนตัวหนังสือในภาพ** โดยเฉพาะภาษาไทย โมเดลสร้างภาพยังเขียนอักษรไทยไม่ถูก สระกับวรรณยุกต์จะเพี้ยนทุกครั้ง และคนไทยที่เข้าเว็บจะเห็นทันที ซึ่งทำลายความน่าเชื่อถือของเว็บที่ขายเรื่องความถูกต้องพอดี

**วิธีที่ได้ผลดีที่สุด แยกสองชั้น**

```
ชั้นล่าง   ภาพถ่ายจาก AI       ห้องจัดแสดง คน จอ วัตถุ แสง
ชั้นบน     SVG ที่เราคุมเอง     เส้นกราฟ ป้ายชื่อโหนด ป้ายที่มา
```

ได้ทั้งอารมณ์ภาพถ่ายและตัวหนังสือที่ถูกต้อง เปลี่ยนข้อความทีหลังได้ และยังสลับธีมสว่างมืดได้อยู่

ดังนั้น prompt ข้างล่างจึงสั่งให้ **ไม่มีตัวหนังสือใด ๆ ในภาพ** และเว้นที่ว่างฝั่งขวาไว้ให้เราวางกราฟทับ

---

## Master prompt (ภาพหลัก)

```
A quiet museum gallery at dusk, photographed on 35mm film. A single adult
visitor of Southeast Asian appearance stands with their back to the camera,
looking up at a large wall-mounted screen showing a deep-field star map and
the orbits of a solar system. To the right of the frame, an ancient stone
deity statue stands inside a low-lit glass vitrine. Extremely fine threads
of pale lime-green light arc through the air from the screen toward the
statue, like constellation lines drawn between two objects that were never
displayed together. The threads are thin, restrained and physical — as if
made of light, not graphics. Warm museum spotlights, cool screen glow,
visible dust in the beams. Shallow depth of field, natural film grain,
muted colour, no colour cast. Calm and reverent, not futuristic.
Photorealistic editorial photography.

Negative: no text, no letters, no typography, no captions, no UI, no HUD,
no holograms, no glowing hexagons, no circuit-board patterns, no blue neon,
no lens flare, no people facing camera, no crowds, no logos, no watermark.
```

**เว้นที่ให้ SVG** ถ้าจะเอาไปวางกราฟทับ ให้เติมท้าย prompt ว่า

```
Composition: subject and screen occupy the left two-thirds of the frame.
The right third is quiet negative space — dim wall, no detail.
```

---

## สามองค์ประกอบให้เลือก

**A · เต็มห้อง (แนะนำสำหรับหัวหน้าเพจ)**
มุมกว้าง เห็นทั้งคน จอ และตู้จัดแสดง ระยะห่างพอให้รู้สึกว่าเป็นพื้นที่จริง
เติมท้าย prompt: `wide establishing shot, 28mm lens, full room visible, low camera height`

**B · ข้ามไหล่ (แนะนำสำหรับภาพในเนื้อหา)**
กล้องอยู่หลังไหล่ผู้ชม เห็นสิ่งที่เขาเห็น ทำให้ผู้อ่านสวมบทบาทเป็นผู้ชม
เติมท้าย prompt: `over-the-shoulder shot from behind the visitor, 50mm lens,
the screen fills most of the frame, the statue visible at the frame edge`

**C · วัตถุเป็นตัวเอก**
โฟกัสที่เทวรูปในตู้ โดยมีจอเบลออยู่ไกล ๆ และมีเส้นแสงวิ่งมาจากทางนั้น
เติมท้าย prompt: `close shot of the stone statue in its vitrine, 85mm lens,
the screen a soft blurred glow far behind, threads of light arriving at the statue`

---

## สเปกที่ต้องใช้กับเว็บ

```
สัดส่วน      21:9 หรือ 2:1     ให้เข้ากับความกว้างของบล็อกภาพในเว็บ
ความละเอียด  อย่างน้อย 2400px กว้าง   แล้วย่อเหลือ 1600px ตอนขึ้นเว็บ
ไฟล์         .webp คุณภาพ 80    เล็กกว่า .jpg ราวครึ่งหนึ่งที่คุณภาพเท่ากัน
สีเน้น       #B8F04A            สีเดียวกับสีเน้นบนเว็บ ระบุตรง ๆ ใน prompt ได้
```

---

## พารามิเตอร์ตามโมเดล

**Midjourney**
```
[master prompt] --ar 21:9 --style raw --stylize 150 --no text, letters, hologram, neon blue
```
`--style raw` สำคัญ เพราะค่าเริ่มต้นของ Midjourney จะแต่งภาพให้ดูเป็นงานศิลป์เกินจริง

**Google Imagen / Nano Banana / GPT Image**
ใช้ prompt เป็นประโยคบรรยายได้เลย ไม่ต้องใส่พารามิเตอร์ ถ้าภาพออกมาเป็นงานกราฟิกเกินไป ให้เติมประโยคว่า
`Shot on Kodak Portra 400. Documentary photography, not illustration.`

**Flux**
ตอบสนองกับคำสั่งเรื่องแสงได้ดี เติม `soft practical lighting, no artificial rim light` เพื่อกันแสงขอบเทียม

---

## สิ่งที่ต้องตรวจก่อนเอาขึ้นเว็บ

- **ไม่มีตัวหนังสือหลงเหลือในภาพ** โมเดลชอบแอบใส่ป้ายบนผนังหรือบนตู้
- **มือและสัดส่วนคน** ถ้าเห็นมือ ให้ตรวจนิ้ว
- **เทวรูปต้องไม่เหมือนของจริงชิ้นใดชิ้นหนึ่ง** ถ้าคล้ายวัตถุที่มีเจ้าของ ให้สร้างใหม่
- **เส้นแสงต้องบางและน้อย** ถ้าหนาหรือเยอะ ภาพจะกลายเป็นภาพโฆษณาเทคโนโลยีทั่วไป ซึ่งเป็นสิ่งที่เว็บนี้พยายามไม่เป็น
- **เปิดดูทั้งธีมสว่างและมืด** ภาพมืดจัดจะดูเป็นรูตรงกลางหน้าเมื่ออยู่บนพื้นสว่าง

---

## ถ้าอยากได้ทั้งคู่ Before และ After

ใช้ prompt เดียวกันทุกอย่าง เปลี่ยนแค่ประโยคเรื่องเส้นแสง

**Before**
```
...no threads of light between them. The screen and the statue are lit
separately and share nothing. The gap between them is empty and dark.
```

**After**
```
...fine threads of pale lime-green light arc through the air from the
screen toward the statue.
```

การใช้ฉากเดิม มุมเดิม แสงเดิม แล้วเปลี่ยนแค่เส้น ทำให้ผู้อ่านเห็นความต่างในสิ่งเดียวที่เปลี่ยนจริง ซึ่งตรงกับข้อโต้แย้งของเว็บว่า **คอลเลกชันไม่ได้เปลี่ยน สิ่งที่เปลี่ยนคือเส้นทางผ่านมัน**
