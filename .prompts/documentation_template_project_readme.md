# Project README Documentation Template

**Purpose:** Generate comprehensive project-level README documentation for data engineering/BI projects using Gen AI.

---

## **Template Structure**

Use this template to create standardized project README files that provide:
- Project overview with single-sentence description
- Project component breakdown
- File organization with tree structure
- Component-specific details with technical setup
- Deliverables summary

---

## **Prompt Template**

```
Generate a README.md file following this EXACT structure:

# {project_name}

{project_description}

## Project Overview
This repository contains {component_count} core components for a {role_title} assessment:
{project_components_list}


## GenAI Documentation Automation

This project includes an automated documentation system that keeps project documentation synchronized with code changes. Instead of manually updating README files every time you modify SQL queries or data models, the system detects changes and generates updates automatically.

The workflow is simple: generate your initial documentation from templates, make code changes, and let the system detect what changed and update only the relevant sections. This saves time and ensures documentation never falls out of sync with your actual work.

Technical details and usage instructions are in `.prompts/USER_GUIDE.md` for anyone interested in the implementation.

## File Organization
```
{folder_structure_tree}
```

{file_descriptions_list}


## SQL Development (`{sql_file_name}`)

### Environment Setup
- **Target platform**: {sql_platform}
- **Testing platform**: {testing_url}

## Core Data Model
{data_model_description}

### Schema Notes
{schema_notes_list}

### Required Queries ({query_count} total)
{queries_list}

### Key Business Logic
{business_logic_list}

### SQL Patterns to Follow
{sql_patterns_list}

## Dimensional Modeling Exercise (`{model_file_path}`)

### Requirements
{modeling_requirements_list}

### Modeling Conventions
{modeling_conventions_list}

### Deliverable
{modeling_deliverable_details}

## Power BI Report (`{powerbi_report_name}`)

### Theme
- **Required theme**: `{theme_file_path}`
  
### Data Source
{data_source_details}

### Deliverable
{powerbi_deliverable_details}
  

## Deliverables Summary
{deliverables_summary_list}
```

**CRITICAL Style Rules:**
1. NO emoji anywhere
2. Use backticks for: filenames, code, table names, values
3. Use **bold** for: component names in bullets, key terms
4. Exact spacing: blank line before/after sections as shown
5. H2 sections: Project Overview, GenAI Documentation Automation, File Organization, SQL Development, Dimensional Modeling Exercise, Power BI Report, Deliverables Summary
6. GenAI section stays exactly as written above
7. Tree structure uses box-drawing characters: ├── └── │
8. File descriptions: `filename` - description format
9. Numbered lists for queries
10. Bulleted lists (dash) for everything else

---

## **Example Input Variables**

```yaml
project_name: "ACT Commodities BI Assessment"
project_description: "ACT Commodities BI take-home assessment focused on SQL, dimensional modeling, and Power BI reporting for commodities trading analytics."
component_count: "three"
role_title: "Senior BI Engineer role"

project_components_list: |
  - **SQL Analysis**: Trading data queries using MS SQL Server
  - **Dimensional Modeling**: SCD Type 2 dimensions and periodic snapshot facts
  - **Power BI Visualization**: Performance overview dashboard

folder_structure_tree: |
  .
  ├── README.md
  ├── completed_sql_queries.sql
  ├── dimensional_model/
  │   ├── model.md
  │   └── act_dimensional_model_erd.png
  ├── power_bi/
  │   ├── Performance Overview.pbip
  │   └── performance_overview_documentation.md
  ├── project_documents/
  │   ├── act_power_bi_theme.json
  │   ├── senior_bi_engineer_assessment_details.md
  │   ├── sql_assignment.sql
  │   └── trading_dataset.xlsx
  └── .prompts/
      ├── USER_GUIDE.md
      └── documentation_*.py

file_descriptions_list: |
  - `README.md` - Project repository documentation
  - `completed_sql_queries.sql` - SQL solutions with detailed thought process (8 queries)
  - `dimensional_model/model.md` - Complete dimensional model specification
  - `dimensional_model/act_dimensional_model_erd.png` - Entity relationship diagram
  - `power_bi/Performance Overview.pbip` - Power BI project file (PBIP format)
  - `power_bi/performance_overview_documentation.md` - DAX measures and report documentation
  - `project_documents/act_power_bi_theme.json` - Power BI theme (required for reporting assessment)
  - `project_documents/senior_bi_engineer_assessment_details.md` - Full requirements & assessment details
  - `project_documents/sql_assignment.sql` - SQL schema + assignment placeholders
  - `project_documents/trading_dataset.xlsx` - Trading dataset for dimensional modeling & Power BI
  - `.prompts/` - GenAI documentation automation system

sql_file_name: "completed_sql_queries.sql"
sql_platform: "MS SQL Server (T-SQL syntax)"
testing_url: "https://sqliteonline.com/ (MS SQL mode)"

data_model_description: |
  The dataset represents **commodities trading operations** with three main entities:
  - **Trades**: Individual buy/sell transactions (T001-T010) linked to matched deals via `MatchId`
  - **Deals**: Matched trade pairs (M1-M5) with execution dates and assigned traders
  - **Traders**: Trader profiles with performance targets (AB=40, RA=20, CM=20)

schema_notes_list: |
  - **Known typo**: `Deals.MatchedData` should be `MatchedDate` (column name inconsistency)
  - Dates stored as `date` type with `YYYYMMDD` format (20230401, not 20250401)
  - `TraderTarget` is `nvarchar(100)` but contains numeric values - requires casting in calculations

query_count: "8"
queries_list: |
  1. Total sold volume
  2. Weighted average buy price
  3. Profit per deal
  4. Traders who reached targets
  5. Second-highest profit trader
  6. Daily profit for April 1-10
  7. Cumulative profit for April 1-10
  8. Top 3 most profitable commodities (bonus query)

business_logic_list: |
  - Trades are **paired by MatchId**: one Buy + one Sell = one Deal
  - Profit calculation: `(Sell_Price - Buy_Price) * Volume` per deal
  - Weighted average buy price: `SUM(Price * Volume) / SUM(Volume)` for buy-side trades only
  - Target achievement: Trader's cumulative profit ≥ TraderTarget

sql_patterns_list: |
  - Use explicit column lists in SELECT (avoid `SELECT *`)
  - Join pattern: `Trades → Deals → Traders` via MatchId and TraderCode

model_file_path: "dimensional_model/model.md"

modeling_requirements_list: |
  - Design **SCD Type 2** dimensions
  - Create **periodical snapshot fact** tables 
  - Output: Database diagram showing tables, attributes, PKs, FKs, relationships
  - Source: "Trading Dataset.xlsx" (separate from SQL assignment data)

modeling_conventions_list: |
  - Surrogate keys for dimension tables (e.g., `TraderKey`, not `TraderCode` as PK)
  - Natural keys preserved as business keys
  - Snapshot fact grain: Daily trader performance metrics
  - Expected dimensions: DimTrader (SCD2), DimProduct/Commodity (SCD2) and DimDate
  - Expected facts: FactTraderPerformance (periodic snapshots)

modeling_deliverable_details: |
  - **Model Specification**: `dimensional_model/model.md` - Complete star schema with 6 dimensions, 1 fact table, composite business keys
  - **ERD Diagram**: `dimensional_model/act_dimensional_model_erd.png` - Visual representation of relationships

powerbi_report_name: "Performance Overview"
theme_file_path: "project_documents/act_power_bi_theme.json"

data_source_details: |
  - Use "Trading Dataset.xlsx" (NOT the SQL assignment sample data)
  - May require data transformation in Power Query to align with dimensional model

powerbi_deliverable_details: |
  - **Report File**: `power_bi/Performance Overview.pbip` - Power BI project format
  - **Documentation**: `power_bi/performance_overview_documentation.md` - DAX measures, visuals, data model architecture

deliverables_summary_list: |
  - **SQL**: `completed_sql_queries.sql` - 8 commented queries with thought process
  - **Modeling**: `dimensional_model/model.md` + ERD diagram with SCD2 dimensions and snapshot fact
  - **Power BI**: `power_bi/Performance Overview.pbip` with ACT theme applied
```

---

## **Usage with Gen AI Agent**

### **Invoke from Code:**

```python
from genai_agent import DocumentationAgent

agent = DocumentationAgent()
readme_content = agent.generate_from_template(
    template_path=".prompts/documentation_template_project_readme.md",
    variables={
        "project_name": "ACT Commodities BI Assessment",
        "project_description": "Technical assessment for Senior BI Engineer...",
        "technologies_list": ["SQL Server", "Power BI", "Excel"],
        # ... other variables
    }
)

with open("README.md", "w") as f:
    f.write(readme_content)
```

### **Invoke from VS Code Copilot:**

```
@workspace /new using template .prompts/documentation_template_project_readme.md 
generate README for project "ACT Commodities BI Assessment" with SQL, Power BI, and dimensional modeling deliverables
```

---


## **Version History**

- **v1.0** (Nov 2025): Initial template for project README generation
