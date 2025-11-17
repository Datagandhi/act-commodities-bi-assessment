# Dimensional Model Documentation Template

**Purpose:** Generate comprehensive dimensional model documentation using Kimball methodology with Gen AI.

---

## **Template Structure**

Use this template to create standardized dimensional model documentation that includes:
- Star schema design with relationships
- Dimension table specifications
- Fact table grain and measures
- Business rules and conventions
- SCD Type 2 implementation details
- Composite business key justifications

---

## **Prompt Template**

```
Generate dimensional model documentation following this EXACT structure:

# {project_name} - Dimensional Model Specification


---

## 📋 **MODEL OVERVIEW**

**Purpose:** {model_purpose}
**Architecture:** {architecture_type}
**Grain:** {fact_grain}
**Author:** {author_name}
**Date:** {date}

---

## ⚠️ **IMPORTANT NOTE: Composite Business Keys**

**{composite_keys_title}:**  
{composite_keys_explanation}

For this reason, I use composite business keys:
{composite_keys_list}

{composite_keys_implementation_note}

---

## 🎯 **BUSINESS REQUIREMENTS**

### **Key Business Questions:**
{business_questions_list}

### **Design Rationale:**
{design_rationale_list}

---

## 📊 **FACT TABLE**

### **{fact_table_name}**

**THOUGHT PROCESS:**
{fact_thought_process}

{fact_table_schema}

---

## 📅 **DIMENSION 1: DimDate**

**THOUGHT PROCESS:**
{dimdate_thought_process}

**PURPOSE:** {dimdate_purpose}
**TYPE:** {dimdate_type}

{dimdate_schema}

---

## 📈 **DIMENSION 2: {dim2_name} ({dim2_scd_type})**

**THOUGHT PROCESS:**
{dim2_thought_process}

**PURPOSE:** {dim2_purpose}
**TYPE:** {dim2_type}
**BUSINESS KEY:** {dim2_business_key}

{dim2_schema}

---

## 👤 **DIMENSION 3: {dim3_name} ({dim3_scd_type})**

**THOUGHT PROCESS:**
{dim3_thought_process}

**PURPOSE:** {dim3_purpose}
**TYPE:** {dim3_type}
**BUSINESS KEY:** {dim3_business_key}

{dim3_schema}

---

## 🏷️ **DIMENSION 4: {dim4_name}**

**THOUGHT PROCESS:**
{dim4_thought_process}

**PURPOSE:** {dim4_purpose}
**TYPE:** {dim4_type}
**BUSINESS KEY:** {dim4_business_key}

{dim4_schema}

{dim4_hierarchy}

---

## 🏢 **DIMENSION 5: {dim5_name}**

**THOUGHT PROCESS:**
{dim5_thought_process}

**PURPOSE:** {dim5_purpose}
**TYPE:** {dim5_type}
**BUSINESS KEY:** {dim5_business_key}

{dim5_schema}

---

## 💱 **DIMENSION 6: {dim6_name}**

**THOUGHT PROCESS:**
{dim6_thought_process}

**PURPOSE:** {dim6_purpose}
**TYPE:** {dim6_type}
**STANDARD:** {dim6_standard}

{dim6_schema}

---

## 🔗 **RELATIONSHIPS**

### **Star Schema Relationships ({relationship_count} Total):**

#### **From {fact_table_name}:**
{relationships_list}

{relationships_notes}

---

## 📐 **SCD TYPE 2 LOGIC**

### **Implementation Details:**

**AFFECTED DIMENSIONS:**
{scd2_dimensions_list}

**SCD TYPE 2 FIELDS:**
{scd2_fields_list}

**FACT-TO-DIMENSION LOOKUP LOGIC:**
{scd2_lookup_sql}

**CHANGE TRACKING PROCESS:**
{scd2_change_process}

**EXAMPLE:**
{scd2_example}

---

## 🎯 **BUSINESS RULES**

### **Fact Table Grain:**
{fact_grain_rule}

### **Measure Additivity:**
{measure_additivity_rules}

### **Date Handling:**
{date_handling_rules}

### **Surrogate Keys:**
{surrogate_keys_rules}

---

## ✅ **MODEL VALIDATION CHECKLIST**

{validation_checklist}

---

**Model Version:** {model_version}
**Last Updated:** {last_updated}
**For:** {project_context}
**Author:** {author_name}
```

**CRITICAL Style Rules:**
1. Use emoji in H2 headers: 📋 📊 📅 📈 👤 🏷️ 🏢 💱 🔗 📐 🎯 ✅ ⚠️
2. THOUGHT PROCESS sections in natural, conversational language ("I realized", "That's why")
3. Bold keywords: **Purpose**, **Architecture**, **Grain**, **TYPE**, **BUSINESS KEY**
4. Tables use markdown format with | separators
5. SQL code blocks with triple backticks
6. Hierarchical spacing: --- separator between major sections
7. Lists use dash - format
8. Inline code with backticks for field names, values
9. Bold for emphasis on key design decisions
10. Date format: Month DD, YYYY

---

## **Example Input Variables**

```yaml
business_domain: "Commodities Trading Performance Analytics"
reporting_requirements: "Track trader P&L, volume, trade lifecycle, product performance across time"
source_systems: "trading_dataset.xlsx (Commodities CRM, Mifid CRM)"

fact_tables:
  - name: "FactTradeDaily"
    grain: "One row per SnapshotDate + Trade + Trader"
    measures:
      - PnL (fully additive)
      - Volume (fully additive)
      - Price (non-additive)
      - MtMPrice (non-additive)
      - Revenue (fully additive)
      - COGS (fully additive)

dimension_tables:
  - name: "DimDate"
    scd_type: "Type 1"
    business_key: "DateKey (YYYYMMDD)"
  - name: "DimTrade"
    scd_type: "Type 2"
    business_key: "TradelineNumber"
    reason: "Trade status changes over time (Open → Invoiced → Paid)"
  - name: "DimTrader"
    scd_type: "Type 2 (optional)"
    business_key: "TraderName + Department (composite)"
    reason: "Same trader can work in multiple departments"
  - name: "DimProduct"
    scd_type: "Type 1"
    business_key: "ProductNumber + UnitOfMeasure (composite)"
    reason: "Same product traded in different UOMs (MT, BBL)"

composite_keys:
  - dimension: "DimTrader"
    pattern: "TraderName-Department"
    justification: "Trader 18 exists in both Coal and Gas departments"
  - dimension: "DimProduct"
    pattern: "ProductNumber-UnitOfMeasure"
    justification: "Product NGO003 traded as MT and BBL"
```

---

## **Usage with Gen AI Agent**

### **Invoke from Code:**

```python
from genai_agent import DocumentationAgent

agent = DocumentationAgent()
model_doc = agent.generate_from_template(
    template_path=".prompts/documentation_template_dimensional_model.md",
    variables={
        "business_domain": "Commodities Trading",
        "fact_tables": [...],
        "dimension_tables": [...],
        # ... other variables
    }
)

with open("dimensional_model/model.md", "w") as f:
    f.write(model_doc)
```

### **Invoke from VS Code Copilot:**

```
@workspace /new using template .prompts/documentation_template_dimensional_model.md 
generate dimensional model documentation for commodities trading with SCD Type 2 on DimTrade
```

---

## **Customization Points**

**For Different Kimball Patterns:**

- **Transaction Fact:** Atomic grain (one row per transaction)
- **Periodic Snapshot:** Time-series grain (one row per period + entity)
- **Accumulating Snapshot:** Process grain (one row per workflow instance)
- **Factless Fact:** Event tracking (attendance, eligibility)

**For Different Industries:**

- **Retail:** Product, Store, Customer, Time dimensions
- **Healthcare:** Patient, Provider, Diagnosis, Time dimensions
- **Finance:** Account, Transaction, Customer, Time dimensions
- **Manufacturing:** Product, Plant, Order, Time dimensions

---

## **Quality Checklist**

Before finalizing generated model documentation:

- [ ] Fact grain explicitly stated
- [ ] All measures classified by additivity
- [ ] SCD Type 2 logic explained with examples
- [ ] Composite keys justified with data evidence
- [ ] Business rules documented
- [ ] SQL examples provided for ETL
- [ ] Star schema relationships clear
- [ ] Foreign keys mapped to primary keys
- [ ] Sign conventions explained
- [ ] Data validation rules specified

---

## **Version History**

- **v1.0** (Nov 2025): Initial template for dimensional model documentation generation
