#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────
# publish-kit · ตัวส่งงานขึ้น GitHub แบบมีด่านให้อ่านก่อนกด
#
# ไฟล์นี้ไม่ผูกกับโปรเจกต์ใด ค่าทั้งหมดอ่านจาก .tools/publish.conf
# ห้ามแก้ไฟล์นี้รายโปรเจกต์ ถ้าต้องแก้แปลว่ามีค่าที่ควรย้ายไปอยู่ใน conf
#
# หกขั้น เรียงแบบนี้ด้วยเหตุผล
#   1  ดึงของใหม่จาก GitHub ก่อน       กัน push ชนกับงานที่ทำจากเครื่องอื่น
#   2  รันตัวตรวจ                      ตรวจไม่ผ่าน = ไม่มีอะไรถูกส่ง
#   3  โชว์รายการไฟล์ที่จะเปลี่ยน       ให้คนอ่านด้วยตาแล้วตอบ y หรือ N
#   4  ถามข้อความอธิบายการเปลี่ยน       ประวัติที่อ่านรู้เรื่องมีค่ากว่าประวัติที่ครบ
#   5  commit แล้ว push
#   6  รันขั้น deploy ของโปรเจกต์ (ถ้ามี)
#
# ขั้น 3 คือหัวใจ  git add -A กวาดทุกอย่างจริง แต่กวาดมาให้ "ดู" ก่อน
# ตอบ N เมื่อไร มันสั่ง git reset คืนให้ทันที ไม่มีอะไรถูก commit
# ─────────────────────────────────────────────────────────────────────────
set -e

R="$(cd "$(dirname "$0")/.." && pwd)"
cd "$R"

# ── ค่าตั้งต้น ใช้เมื่อ publish.conf ไม่ได้กำหนด ──────────────────────
PROJECT_NAME="$(basename "$R")"
CHECK_CMD=""
DEPLOY_CMD=""
VERIFY_URLS=""
DEFAULT_MSG="Update"
REMIND=""

CONF="$R/.tools/publish.conf"
if [ -f "$CONF" ]; then
  # shellcheck disable=SC1090
  . "$CONF"
else
  echo "✗ ไม่พบ .tools/publish.conf"
  echo "  คัดลอกมาจาก publish-kit/template/.tools/publish.conf แล้วแก้ค่าก่อน"
  echo
  read -n 1 -s -r -p "กดปุ่มใดก็ได้เพื่อปิด..."
  exit 1
fi

clear 2>/dev/null || true    # clear ล้มเมื่อไม่มี TERM แล้ว set -e จะพาตายตั้งแต่บรรทัดแรก
echo "$PROJECT_NAME — publish"
echo "$(printf '%*s' "${#PROJECT_NAME}" '' | tr ' ' '=')========"
echo "โฟลเดอร์  $R"
echo

close() { echo; read -n 1 -s -r -p "กดปุ่มใดก็ได้เพื่อปิด..."; exit "$1"; }

# ── 0 · ต้องเป็น git repo และต้องมีปลายทาง ───────────────────────────
git rev-parse --git-dir >/dev/null 2>&1 || { echo "✗ โฟลเดอร์นี้ไม่ใช่ git repo"; close 1; }
git remote get-url origin >/dev/null 2>&1 || {
  echo "✗ ยังไม่ได้ตั้ง remote ชื่อ origin"
  echo "  ตั้งด้วย  git remote add origin git@github.com:<ชื่อคุณ>/<ชื่อรีโป>.git"
  close 1
}

# ── 1 · ดึงของใหม่จาก GitHub ก่อน ────────────────────────────────────
echo "1/6  กำลังซิงก์กับ GitHub"
git fetch --quiet origin

# รีโปที่เพิ่ง git init ยังไม่มี commit สักอัน  git rev-parse HEAD จะล้ม
# แล้ว set -e จะพาสคริปต์ตายพร้อมข้อความของ git ที่คนอ่านไม่รู้เรื่อง
# กรณีนี้ไม่มีอะไรให้ซิงก์อยู่แล้ว ข้ามไปขั้น 2 ได้เลย
if ! git rev-parse HEAD >/dev/null 2>&1; then
  echo "     รีโปนี้ยังไม่มี commit สักอัน รอบนี้จะเป็นครั้งแรก"
  BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null || echo main)"
  FIRST_COMMIT=1
else
  FIRST_COMMIT=0
  BRANCH="$(git rev-parse --abbrev-ref HEAD)"
  if [ "$BRANCH" = "HEAD" ]; then
    echo
    echo "✗ ตอนนี้ไม่ได้อยู่บน branch ใด (detached HEAD)"
    echo "  push จากสภาพนี้จะไม่ไปโผล่บน branch ไหนเลย สคริปต์จึงไม่ทำให้"
    echo "  กลับขึ้น branch ก่อนด้วย  git switch main   แล้วค่อยกดใหม่"
    close 1
  fi
fi

LOCAL="$([ $FIRST_COMMIT -eq 0 ] && git rev-parse HEAD || echo "")"
REMOTE="$(git rev-parse "origin/$BRANCH" 2>/dev/null || echo "")"

if [ $FIRST_COMMIT -eq 0 ] && [ -n "$REMOTE" ] && [ "$LOCAL" != "$REMOTE" ]; then
  if git merge-base --is-ancestor "$LOCAL" "$REMOTE"; then
    echo "     ปลายทางล้ำหน้าอยู่ กำลังดึงลงมา"
    git pull --quiet --ff-only
  elif ! git merge-base --is-ancestor "$REMOTE" "$LOCAL"; then
    echo
    echo "✗ เครื่องนี้กับ GitHub แยกสายกันแล้ว มีงานคนละชุดทั้งสองฝั่ง"
    echo "  สคริปต์นี้ไม่ merge ให้ เพราะอาจทับงานที่ทำจากอีกเครื่อง"
    echo "  ให้เปิด terminal แล้วจัดการเองก่อน  git status  แล้ว  git log --oneline --graph --all"
    close 1
  fi
fi

# ── 2 · รันตัวตรวจของโปรเจกต์ ────────────────────────────────────────
if [ -n "$CHECK_CMD" ]; then
  echo "2/6  กำลังรันตัวตรวจ  $CHECK_CMD"
  if ! ( eval "$CHECK_CMD" ); then
    echo
    echo "✗ ตรวจไม่ผ่าน ไม่มีอะไรถูกส่งขึ้นไป"
    close 1
  fi
else
  echo "2/6  ไม่ได้ตั้งตัวตรวจไว้ ข้ามขั้นนี้"
fi

# ── 3 · โชว์ก่อนกวาด ─────────────────────────────────────────────────
if [ -z "$(git status --porcelain)" ]; then
  echo
  echo "ไม่มีอะไรเปลี่ยนตั้งแต่ publish ครั้งก่อน"
  close 0
fi

echo
echo "3/6  สิ่งที่จะเปลี่ยนบนปลายทาง"
echo "-----------------------------------------------"

# ตั้งกับดักก่อน git add -A  ไม่ใช่หลัง
# ถ้าผู้ใช้ปิดหน้าต่างหรือกด Ctrl+C ตอนกำลังอ่านรายการ สคริปต์จะตายกลางคัน
# โดยที่ไฟล์ทั้งหมดถูก stage ค้างไว้แล้ว — เส้นทางตอบ N มี git reset ให้ แต่การปิด
# หน้าต่างฆ่าสคริปต์ก่อนถึงบรรทัดนั้น  เกิดจริงกับ personal-library เมื่อ 2026-08-25
# trap ทำให้ทุกทางออกก่อน commit คืน index ให้เหมือนเดิมเสมอ
trap 'git reset --quiet 2>/dev/null || true' EXIT INT TERM

git add -A
git -c color.ui=always diff --cached --stat | sed 's/^/    /'
echo "-----------------------------------------------"
echo
echo "อ่านรายการข้างบนก่อน ถ้าเห็นไฟล์ที่ไม่ได้ตั้งใจแตะ ให้ตอบ N"
read -r -p "ส่งการเปลี่ยนแปลงชุดนี้ขึ้น GitHub ไหม [y/N] " ans
case "$ans" in
  y|Y) ;;
  *) git reset --quiet; echo; echo "ยกเลิกแล้ว ไม่มีอะไรถูกส่ง"; close 0;;
esac

# ── 4 · ข้อความอธิบาย ────────────────────────────────────────────────
echo
read -r -p "4/6  อธิบายการเปลี่ยนรอบนี้สั้น ๆ หนึ่งบรรทัด: " msg
[ -z "$msg" ] && msg="$DEFAULT_MSG"

# ── 5 · commit แล้ว push ─────────────────────────────────────────────
echo
echo "5/6  กำลังส่งขึ้น GitHub"
git commit --quiet -m "$msg"
# commit ผ่านแล้ว ปลดกับดักทันที ไม่งั้นตอนจบสคริปต์มันจะไป reset ทับงานที่เพิ่ง commit
trap - EXIT INT TERM
# -u ตั้ง upstream ให้ด้วย จำเป็นตอน push ครั้งแรกของ branch และไม่มีผลเสียตอนอื่น
git push --quiet -u origin HEAD
SHA="$(git rev-parse --short HEAD)"
echo "     ✓ ส่งแล้ว  $SHA  บนสาย $BRANCH"

# ── 6 · ขั้น deploy ของโปรเจกต์ ──────────────────────────────────────
if [ -n "$DEPLOY_CMD" ]; then
  echo
  echo "6/6  ขั้น deploy  $DEPLOY_CMD"
  echo "     push ขึ้นไปแล้ว ขั้นนี้ล้มก็ไม่ทำให้ประวัติเสียหาย"
  echo
  if ! ( eval "$DEPLOY_CMD" ); then
    echo
    echo "✗ deploy ไม่ผ่าน แต่โค้ดขึ้น GitHub เรียบร้อยแล้วที่ $SHA"
    echo "  แก้แล้วรัน deploy ซ้ำได้เลย ไม่ต้อง publish ใหม่"
    close 1
  fi
  echo
  echo "     ✓ deploy เรียบร้อย"
else
  echo "6/6  ไม่ได้ตั้งขั้น deploy ไว้ ข้ามขั้นนี้"
fi

# ── ปิดท้าย · บอกว่าต้องไปดูอะไรต่อ ──────────────────────────────────
if [ -n "$VERIFY_URLS" ]; then
  echo
  echo "เปิดดูของจริงก่อนจะบอกใครว่าเสร็จ"
  for u in $VERIFY_URLS; do echo "    $u"; done
  echo
  echo "  ถ้าเห็นของเก่า ให้ hard refresh ก่อน แล้วรอสักสิบนาที"
  echo "  GitHub Pages ตั้งแคชไว้ราวสิบนาที ของเก่าค้างได้โดยที่ไม่มีอะไรพัง"
fi

# เขียนเป็น if ไม่ใช่ [ ... ] && { ... } เพราะรูปแบบหลังคืนค่า 1 เมื่อเงื่อนไขเป็นเท็จ
# แล้ว set -e จะพาสคริปต์จบด้วยรหัส 1 ทั้งที่ทุกอย่างสำเร็จ
if [ -n "$REMIND" ]; then
  echo
  echo "อย่าลืม"
  echo "    $REMIND"
fi

close 0
