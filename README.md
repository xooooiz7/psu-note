# PSU Note (Flask + PostgreSQL)

ระบบจดโน้ตพร้อมแท็ก (Tag) และ UI ทันสมัย รองรับ Select2, Bootstrap 5, Docker, PostgreSQL, pgAdmin และสามารถเพิ่มแท็กใหม่ขณะสร้าง/แก้ไขโน้ตได้

## โครงสร้างโปรเจกต์

- `psunote/` : โค้ดหลัก (Flask app, models, forms, templates)
- `requirements.txt` : รายการไลบรารี Python ที่ใช้
- `venv/` : (ไม่ต้อง commit) virtual environment
- `*.png`, `*.jpg` : รูปภาพประกอบ (5 รูป)
- `.gitignore` : ไฟล์สำหรับ ignore venv, ไฟล์ชั่วคราว, รูปภาพ ฯลฯ

### การสร้างโน้ตใหม่
![note-function-edit-note](/images/note-function-create.png)


### การแก้ไขโน้ต
![note-function-edit-note](/images/note-function-edit-note.png)

### การลบ/แก้ไขโน้ตจากรายการ
![note-function-del-edit](/images/note-function-del-edit.png)

### การสร้างแท็กใหม่
![tag-function-2-create](/images/tag-function-2-create.png)

### การแก้ไข/ลบแท็ก
![tag-function-1-edit_and_del](/images/tag-function-1-edit_and_del.png)

## วิธีติดตั้งและใช้งาน (Local)

1. สร้าง virtual environment และติดตั้ง dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. สร้างฐานข้อมูล PostgreSQL (เช่น ด้วย Docker หรือ local)

- ตัวอย่าง docker-compose (ถ้ามี)
- หรือสร้าง db/database/user ตาม connection string ใน `noteapp.py`

3. รันแอป

```bash
export FLASK_APP=psunote/noteapp.py
flask run
```

หรือรันตรงๆ

```bash
python psunote/noteapp.py
```

4. เปิดเบราว์เซอร์ที่ http://localhost:5000

## ฟีเจอร์ที่มี

- CRUD โน้ต (สร้าง/แก้ไข/ลบ/ดู)
- CRUD แท็ก (สร้าง/แก้ไข/ลบ/ดู)
- เลือกแท็กหลายอันขณะสร้าง/แก้ไขโน้ต (Select2)
- เพิ่มแท็กใหม่ได้ทันทีในหน้าโน้ต (modal)
- UI ทันสมัยด้วย Bootstrap 5
- รองรับ PostgreSQL, Docker, pgAdmin
- มีตัวอย่างรูปภาพการใช้งาน 5 รูป (ดูในโฟลเดอร์)

## อธิบายไฟล์ที่เพิ่ม/เปลี่ยนแปลง

- เพิ่ม `.gitignore` สำหรับ venv, ไฟล์ชั่วคราว, รูปภาพ ฯลฯ
- เพิ่ม/ปรับปรุง `README.md` พร้อมวิธีติดตั้งและใช้งาน
- เพิ่มรูปภาพตัวอย่าง 5 รูป (เช่น `img1.png` ถึง `img5.png`)
- ปรับปรุงโค้ดให้ robust, ไม่ error, รองรับ tag object เท่านั้น

## หมายเหตุ
- หากพบปัญหา AttributeError เกี่ยวกับ tag ให้ตรวจสอบว่าไม่ได้ assign string ให้กับ note.tags
- สามารถปรับ connection string PostgreSQL ได้ใน `noteapp.py`
- หากใช้ Docker สามารถเพิ่ม docker-compose.yml ได้เอง
# psu-note
