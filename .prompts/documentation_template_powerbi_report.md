# Power BI Report Documentation Template

**Purpose:** Generate comprehensive Power BI report documentation using Gen AI for semantic models, DAX measures, and report design.

---

## **Template Structure**

Use this template to create standardized Power BI report documentation that includes:
- Data model architecture
- DAX measure definitions
- Report page layouts
- Visual configurations
- Power Query transformations
- Theme and branding details

---

## **Prompt Template**

```
Generate Power BI report documentation following this EXACT structure:

# {report_title} - Power BI Report

## **Overview**

{report_overview_paragraph}

---

## **Data Model Architecture**

### **Semantic Model Structure**

**Dimensional Tables ({dim_count}):**
{dimensional_tables_list}

**Fact Table ({fact_count}):**
{fact_table_description}

### **Composite Business Keys**

{composite_keys_explanation}

{composite_keys_table}

### **Relationships**

```
{relationships_diagram}
```

{relationships_notes}

---

## **DAX Measures Documentation**

### **Base Measures**

{base_measures_sections}

---

### **Conditional Formatting Measures**

{conditional_formatting_measures}

---

### **Time Series Analysis Measures**

{time_series_measures}

---

## **Report Features**

### **Page: {page_name}**

**KPI Cards ({kpi_count}):**
{kpi_cards_list}

**Visuals:**

{visuals_list}

**Slicers:**
{slicers_list}

---

## **Advanced Features**

### **Field Parameters**

{field_parameters_details}

### **Date Intelligence**

{date_intelligence_details}

---

## **Data Transformation (Power Query)**

### **Source Table**
{source_table_info}

### **Dimension Transformations**

{dimension_transformations}

---

---

## **Performance Optimizations**

{performance_optimizations_list}

---

## **Theme Configuration**

**Applied Theme:** {theme_name}

**Brand Colors:**
{brand_colors_list}

**Typography:**
{typography_settings}

---
---

## **File Structure**

```
{file_structure_tree}
```

---



## **Usage Guidelines**

### **For End Users:**

{end_user_guidelines}

### **For Developers:**

{developer_guidelines}

---

## **Contact & Version**

**Report Name:** {report_name}
**Version:** {version}
**Created:** {created_date}
**Power BI Desktop Version:** {powerbi_version}
**Assessment:** {assessment_context}

**Model Compatibility Level:** {compatibility_level}
**Culture:** {culture}
**Source Query Culture:** {source_culture}

---
```

**CRITICAL Style Rules:**
1. Use **bold** for section labels: **Purpose**, **Format**, **Additivity**, **Logic**
2. DAX code blocks with ```dax language identifier
3. M code blocks with ```m language identifier
4. Tables use markdown format with | separators
5. H2 sections with ** formatting: ## **Overview**
6. H3 sections without bold: ### **Base Measures**
7. H4 sections for individual measures: #### **Total P&L**
8. Bullet lists after DAX blocks for metadata
9. Separator lines: --- between major sections
10. Double --- before File Structure
11. File tree uses ASCII box-drawing characters
12. Hex color codes in format: #RRGGBB
13. Emoji: none
14. Spacing: blank line before/after sections

---

## **Example Input Variables**

```yaml
report_name: "Performance Overview Dashboard"
business_purpose: "Track trading performance, trader P&L, product trends, trade lifecycle"
target_audience: "Trading managers, risk analysts, executive leadership"

tables_list:
  dimensions:
    - DimDate: "Calendar dimension with fiscal hierarchies"
    - DimTrade: "Trade master attributes (SCD Type 2)"
    - DimTrader: "Trader information with composite key"
    - DimProduct: "Product 4-level hierarchy"
    - DimAccount: "Account hierarchy with parent"
    - DimCurrency: "Currency lookup"
  facts:
    - FactTradeDaily: "Daily snapshot at grain: SnapshotDate + Trade + Trader"

measure_definitions:
  base_measures:
    - name: "Total P&L"
      dax: "SUM(FactTradeDaily[PnL])"
      format: "€#,0"
    - name: "Unrealised PnL"
      dax: "SUMX(FILTER(FactTrade, ISBLANK(RELATED(DimTrade[ClosedDate]))), ...)"
      format: "€#,0.00"
  conditional_formatting:
    - name: "MaxMin P&L Trader Bar BG"
      dax: "SWITCH(TRUE(), ThisVal = MaxVal, \"#00C49A\", ...)"
      purpose: "Color-code top/bottom performers"

page_layouts:
  - page_name: "Performance Overview"
    visuals:
      - type: "KPI Cards"
        count: 5
        metrics: ["Total P&L", "Revenue", "Unrealised PnL", "Realised PnL", "Profit %"]
      - type: "Clustered Bar Chart"
        name: "Top 10 Traders by P&L"
        axis: "TraderName"
        values: "Total P&L"
      - type: "Line Chart"
        name: "Monthly P&L"
        axis: "Year-Month"
        values: "Total P&L"
        markers: "Max/Min P&L"

field_parameters:
  - name: "TradeType/ProductGroup Switch"
    fields: ["DimTrade[TradeType]", "DimProduct[L1ProductGroup]"]
    usage: "Dynamic axis on P&L by Trade Type visual"

theme_file: "act_power_bi_theme.json"
brand_colors:
  primary: "#64334D"
  accent: "#0096E1"
  success: "#00C49A"
  alert: "#F06543"
```

---

## **Usage with Gen AI Agent**

### **Invoke from Code:**

```python
from genai_agent import DocumentationAgent

agent = DocumentationAgent()
report_doc = agent.generate_from_template(
    template_path=".prompts/documentation_template_powerbi_report.md",
    variables={
        "report_name": "Performance Overview Dashboard",
        "tables_list": {...},
        "measure_definitions": {...},
        # ... other variables
    }
)

with open("power_bi/performance_overview_documentation.md", "w") as f:
    f.write(report_doc)
```

### **Invoke from VS Code Copilot:**

```
@workspace /new using template .prompts/documentation_template_powerbi_report.md 
generate Power BI documentation for Performance Overview with 10 DAX measures and field parameters
```

---

## **Customization Points**

**For Different Report Types:**

- **Executive Dashboard:** Focus on KPIs, trends, high-level summaries
- **Operational Report:** Detailed tables, drill-through, real-time data
- **Analytical Workbook:** Many slicers, cross-filtering, what-if parameters
- **Mobile Report:** Simplified layout, phone-optimized visuals

**For Different Data Models:**

- **Star Schema:** Classic dimensional model
- **Snowflake Schema:** Normalized dimensions
- **Composite Model:** Import + DirectQuery hybrid
- **Live Connection:** Analysis Services connection

---

## **Quality Checklist**

Before finalizing generated Power BI documentation:

- [ ] All DAX measures documented with code
- [ ] Power Query steps explained
- [ ] Relationships mapped with cardinality
- [ ] Visual configurations detailed
- [ ] Theme colors specified (hex codes)
- [ ] Field parameters explained
- [ ] Performance optimizations noted
- [ ] Usage guidelines clear for end users
- [ ] File structure (PBIP) documented
- [ ] Known issues listed
- [ ] Future enhancements outlined

---

## **Version History**

- **v1.0** (Nov 2025): Initial template for Power BI report documentation generation
