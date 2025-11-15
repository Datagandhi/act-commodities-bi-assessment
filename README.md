# ACT Commodities BI Assessment

ACT Commodities BI take-home assessment focused on SQL, dimensional modeling, and Power BI reporting for commodities trading analytics.

## Project Overview
This repository contains three core components for a Senior BI Engineer role assessment:
- **SQL Analysis**: Trading data queries using MS SQL Server
- **Dimensional Modeling**: SCD Type 2 dimensions and periodic snapshot facts
- **Power BI Visualization**: Performance overview dashboard

## File Organization
```
.
├── README.md
└── project_documents/
    ├── act_power_bi_theme.json
    ├── senior_bi_engineer_assessment_details.md
    ├── sql_assignment.sql
    └── trading_dataset.xlsx
```

- `README.md` - Project Repository documentation
- `project_documents/act_power_bi_theme.json` - Power BI theme (required for reporting assessment)
- `project_documents/senior_bi_engineer_assessment_details.md` - Full requirements & assessment details
- `project_documents/sql_assignment.sql` - SQL schema + assignment placeholders
- `project_documents/trading_dataset.xlsx` - Trading dataset for dimensional modeling & Power BI


## SQL Development (`project_documents/sql_assignment.sql`)

### Environment Setup
- **Target platform**: MS SQL Server (T-SQL syntax)
- **Testing platform**: https://sqliteonline.com/ (MS SQL mode)

## Core Data Model
The dataset represents **commodities trading operations** with three main entities:
- **Trades**: Individual buy/sell transactions (T001-T010) linked to matched deals via `MatchId`
- **Deals**: Matched trade pairs (M1-M5) with execution dates and assigned traders
- **Traders**: Trader profiles with performance targets (AB=40, RA=20, CM=20)

### Schema Notes
- **Known typo**: `Deals.MatchedData` should be `MatchedDate` (column name inconsistency)
- Dates stored as `date` type with `YYYYMMDD` format (20230401, not 20250401)
- `TraderTarget` is `nvarchar(100)` but contains numeric values - requires casting in calculations

### Required Queries (7 total)
1. Total sold volume
2. Weighted average buy price
3. Profit per deal
4. Traders who reached targets
5. Second-highest profit trader
6. Daily profit for April 1-10
7. Cumulative profit for April 1-10

### Key Business Logic
- Trades are **paired by MatchId**: one Buy + one Sell = one Deal
- Profit calculation: `(Sell_Price - Buy_Price) * Volume` per deal
- Weighted average buy price: `SUM(Price * Volume) / SUM(Volume)` for buy-side trades only
- Target achievement: Trader's cumulative profit ≥ TraderTarget

### SQL Patterns to Follow
- Use explicit column lists in SELECT (avoid `SELECT *`)
- Join pattern: `Trades → Deals → Traders` via MatchId and TraderCode

## Dimensional Modeling Exercise

### Requirements
- Design **SCD Type 2** dimensions
- Create **periodical snapshot fact** tables 
- Output: Database diagram showing tables, attributes, PKs, FKs, relationships
- Source: "Trading Dataset.xlsx" (separate from SQL assignment data)

### Modeling Conventions
- Surrogate keys for dimension tables (e.g., `TraderKey`, not `TraderCode` as PK)
- Natural keys preserved as business keys
- Snapshot fact grain: Daily trader performance metrics
- Expected dimensions: DimTrader (SCD2), DimProduct/Commodity (SCD2) and DimDate
- Expected facts: FactTraderPerformance (periodic snapshots)

## Power BI Report (`Performance Overview`)

### Theme
- **Required theme**: `project_documents/act_power_bi_theme.json`
  
### Data Source
- Use "Trading Dataset.xlsx" (NOT the SQL assignment sample data)
- May require data transformation in Power Query to align with dimensional model
  

## Deliverables
- **SQL**: Commented queries added to `sql_assignment.sql` under each requirement
- **Modeling**: Database diagram (image or .pdf) showing SCD2 dimensions and snapshot fact with PK, FK and relationships between tables captured.
- **Power BI**: `.pbix` file named "Performance Overview" with given theme
