# Lab 3 — Spec-Driven Development

ไฟล์ในโฟลเดอร์นี้จัดตามโครงสร้างที่ใบงาน Lab 3 กำหนด และ source ปัจจุบันอยู่ใน `src/`.

## Deliverables
- `specs/spec.md`: user stories, acceptance criteria, scope, FR, NFR, design notes
- `.ai-rules.md`: context/code-generation rules
- `src/inventory.py`: Lab 2 baseline
- `src/inventory_no_context.py`: pre-context implementation retained for comparison
- `src/models.py`, `src/notifiers.py`, `src/service.py`: context-aligned implementation
- `AI_ITERATION_LOG.md`: before/after comparison and iteration evidence with provenance notes
- `diagrams/class.md`, `diagrams/sequence.md`: Mermaid based on current source
- `design_review.md`: AI-assisted SOLID review draft
- `tests/test_service.py`: added verification for acceptance criteria

## Validation
Run from this directory:

```bash
python -m pytest tests/ -v
```

The test file checks stock validation, threshold transition and no-repeat behavior, per-product channel selection, grouped stock value reports, empty reports, notifier creation, and rejects unconfigured notification channels. In this workspace, `python -m pytest tests/ -v` completed with 12 passed.

## Example setup

```python
from src.models import Category, Product
from src.notifiers import NotifierFactory
from src.service import InventoryService

email = NotifierFactory.create("email", email_destination)
sms = NotifierFactory.create("sms", sms_destination)
service = InventoryService({"email": email, "sms": sms})
product = Product("P-01", "สายไฟ", Category("งานไฟฟ้า"), 30,
                  quantity=20, threshold=15,
                  notification_channels=("email", "sms"))
service.add_product(product)
```

## Submission notes
The original team files at repository root remain unchanged. The review and AI log identify AI assistance and reconstructed historical prompts rather than presenting them as a student's personal analysis or verbatim historical record. Before submitting, the team should verify the AI platform is allowed as a free channel and each member should be able to explain the SOLID table.
