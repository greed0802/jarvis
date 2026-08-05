# Document Completeness Model

Defines expected document checklists to score readiness.

## Completeness Scores
For a standard takeoff scope, the target checklist expected categories are:
1. **Architectural Drawing**
2. **Structural Drawing**
3. **Specification**
4. **BOQ**
5. **Checklist**

* **Score Calculation:** `Actual Present CategoriesCount / Total Expected CategoriesCount`.
* **Zero Items Warning:** Creates missing recommendations if count of items in any category is 0.
