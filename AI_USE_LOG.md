# Lab 5 AI use log

This records work produced in the current Codex task. It is not a claim about another student's prompts or a teammate's work history.

| Prompt / instruction | AI output | Review and decision |
|---|---|---|
| User: “ทำLab5 ต่อให้หน่อย” with the Lab 5 quickstart link. | Read the current assignment and the instructor handout; drafted the `low_stock_items` tests, sales rules, characterization suite, CI, and supporting notes. | Kept `low_stock_items` behavior to the written acceptance cases. The user/team should review the design and be able to explain it before submission. |
| Lab prompt: “ช่วยเขียน pytest unit test สำหรับเมธอด sell ของ class Inventory ให้หน่อย”. | A minimal test draft covers a normal sale and a sale exceeding stock. | Added boundary, invalid quantity, missing item, and type tests after identifying those gaps. The initial draft and added cases are identified in `test-gap.md`. |
| Lab prompt for refactoring: “ช่วยจัดโค้ดนี้ใหม่ให้อ่านง่ายขึ้น โดยพฤติกรรมทุกอย่างต้องเหมือนเดิมทุกกรณี ห้ามเปลี่ยนสูตรคิดราคา ห้ามเปลี่ยนลำดับการคิดส่วนลด และห้ามเปลี่ยนการปัดเศษ”. | Created `pricing_refactored.py` with small helpers and named policy constants. | Accepted only after the characterization test file, with its import changed to the new module, passed all cases including coupon dates, rounding, member points, and `LOG` side effects. The original file was retained unchanged. |

No separate paid AI service or personal data was used. The synthetic example URLs and member IDs in tests are non-personal placeholders. This log documents Codex assistance; each student should add any further prompts and their own review decisions before submitting.
