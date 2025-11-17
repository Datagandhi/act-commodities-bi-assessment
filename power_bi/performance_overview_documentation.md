# Performance Overview Dashboard - Power BI Report

## **Overview**

This Power BI report provides comprehensive trading performance overview for ACT Commodities, implementing a dimensional model based on the Kimball methodology. The report enables self-service analysis of P&L, trader performance, and trading activity across multiple dimensions.

---

## **Data Model Architecture**

### **Semantic Model Structure**

**Dimensional Tables (6):**
1. **DimDate** - Complete date dimension with fiscal hierarchy
2. **DimTrade** - Trade master attributes (status, type, direction)
3. **DimTrader** - Trader information with composite business key
4. **DimProduct** - Product hierarchy (4 levels) with UOM
5. **DimAccount** - Account hierarchy with country
6. **DimCurrency** - Currency dimension

**Fact Table (1):**
- **FactTrade** - Daily snapshot fact at grain: SnapshotDate + Trade + Trader

### **Composite Business Keys**

The model implements composite business keys to handle many-to-many relatonship:

| Dimension | Composite Key Pattern | Reason |
|-----------|----------------------|---------|
| DimTrader | TraderName + Department | Same trader works in multiple departments |
| DimProduct | ProductNumber + UnitOfMeasure | Same product traded in different UOMs (MT, BBL) |
| DimAccount | AccountName + AccountParent | Account names repeat under different parents |

### **Relationships**

```
FactTrade (Many) → (One) DimDate          [SnapshotDateKey → DateKey]
FactTrade (Many) → (One) DimTrade         [TradelineNumber → TradelineNumber]
FactTrade (Many) → (One) DimTrader        [TraderKey → TraderKey]
FactTrade (Many) → (One) DimProduct       [ProductKey → ProductKey]
FactTrade (Many) → (One) DimAccount       [AccountKey → AccountKey]
FactTrade (Many) → (One) DimCurrency      [Currency → Currency]
```

**Note:** DimTrade.ClosedDate and DimTrade.DealDate are stored as DATE attributes (not foreign keys) to avoid role-playing dimension complexity.

---

## **DAX Measures Documentation**

### **Base Measures**

#### **Total P&L**
```dax
Total P&L = SUM(FactTrade[PnL])
```
- **Purpose:** Aggregates realized + unrealized P&L
- **Format:** €# (millions)
- **Additivity:** Fully additive across all dimensions

#### **Total Revenue**
```dax
Total Revenue = COALESCE(SUM(FactTrade[Revenue]), 0)
```
- **Purpose:** Total revenue from sell trades
- **Format:** €# (millions)
- **Additivity:** Fully additive
- **Note:** Revenue is blank for buy trades (accounting convention)

#### **Profit %**
```dax
Profit % = DIVIDE([Total P&L], [Total Revenue], 0)
```
- **Purpose:** Profit margin calculation
- **Format:** Percentage
- **Calculation:** P&L ÷ Revenue
- **Additivity:** Non-additive (ratio measure, recalculate at each aggregation level)

#### **Unrealised PnL**
```dax
Unrealised PnL = 
COALESCE(
    SUMX(
        FILTER(
            FactTrade,
            ISBLANK(RELATED(DimTrade[ClosedDate]))
        ),
        (FactTrade[MtM Price] - FactTrade[Price]) * FactTrade[Volume]
    ),
    0
)
```
- **Purpose:** Mark-to-market gains/losses on open positions
- **Logic:** Filters trades where ClosedDate is NULL
- **Calculation:** (MtM Price - Execution Price) × Volume
- **Additivity:** Fully additive (calculated from additive measures: Price difference × Volume)

#### **Realised PnL**
```dax
Realised PnL = 
COALESCE(
    SUMX(
        FILTER(
            FactTrade,
            NOT ISBLANK(RELATED(DimTrade[ClosedDate]))
        ),
        FactTrade[PnL]
    ),
    0
)
```
- **Purpose:** Actual P&L from closed trades
- **Logic:** Filters trades where ClosedDate is populated
- **Additivity:** Fully additive (aggregates from FactTrade[PnL] which is fully additive)

---

### **Conditional Formatting Measures**

#### **MaxMin P&L Trader Bar BG**
```dax
MaxMin P&L Trader Bar BG = 
VAR ThisVal = [Total P&L]
VAR MaxVal = MAXX(ALLSELECTED(DimTrader[TraderName]), [Total P&L])
VAR MinVal = MINX(ALLSELECTED(DimTrader[TraderName]), [Total P&L])
RETURN
SWITCH(
    TRUE(),
    ThisVal = MaxVal, "#00C49A",   -- Green
    ThisVal = MinVal, "#F06543",   -- Red
    "#66C0ED"                       -- Default Blue
)
```
- **Purpose:** Color-code top/bottom performers in trader bar chart
- **Returns:** Hex color codes

#### **MaxMin P&L Trader Datalabel**
```dax
MaxMin P&L Trader Datalabel = 
VAR ThisVal = [Total P&L]
VAR MaxVal = MAXX(ALLSELECTED(DimTrader[TraderName]), [Total P&L])
VAR MinVal = MINX(ALLSELECTED(DimTrader[TraderName]), [Total P&L])
RETURN
SWITCH(
    TRUE(),
    ThisVal = MaxVal || ThisVal = MinVal, ThisVal, BLANK()
)
```
- **Purpose:** Show data labels only for top/bottom performers
- **Returns:** P&L value or BLANK

---

### **Time Series Analysis Measures**

#### **Max P&L Timeseries Marker**
```dax
Max P&L Timeseries Marker = 
VAR ThisVal = [Total P&L]
VAR MaxVal = MAXX(ALLSELECTED(DimDate[Year], DimDate[MonthShortName]), [Total P&L])
RETURN
SWITCH(TRUE(), ThisVal = MaxVal, ThisVal, BLANK())
```
- **Purpose:** Highlight peak P&L month in line chart
- **Used in:** Monthly P&L visual

#### **Min P&L Timeseries Marker**
```dax
Min P&L Timeseries Marker = 
VAR ThisVal = [Total P&L]
VAR MinVal = MINX(ALLSELECTED(DimDate[Year], DimDate[MonthShortName]), [Total P&L])
RETURN
SWITCH(TRUE(), ThisVal = MinVal, ThisVal, BLANK())
```
- **Purpose:** Highlight lowest P&L month in line chart

#### **MaxMin P&L Timeseries Datalabel**
```dax
MaxMin P&L Timeseries Datalabel = 
VAR ThisVal = [Total P&L]
VAR MaxVal = MAXX(ALLSELECTED(DimDate[Year], DimDate[MonthShortName]), [Total P&L])
VAR MinVal = MINX(ALLSELECTED(DimDate[Year], DimDate[MonthShortName]), [Total P&L])
RETURN
SWITCH(TRUE(), ThisVal = MaxVal || ThisVal = MinVal, ThisVal, BLANK())
```
- **Purpose:** Show labels only at peak/trough points

---

## **Report Features**

### **Page: Performance Overview**

**KPI Cards (5):**
- Total P&L 
- Total Revenue 
- Unrealised PnL 
- Realised PnL 
- Profit % 

**Visuals:**

1. **Top 10 Traders by P&L** (Clustered Bar Chart)
   - X-axis: Total P&L
   - Y-axis: TraderName
   - Conditional formatting: Green (top), Red (bottom), Blue (others)
   - Data labels: Show only for max/min

2. **P&L by Trade Type and Direction** (Clustered Bar Chart)
   - **Field Parameter:** TradeType/ProductGroup Switch
   - Toggle between:
     - Trade Type breakdown (Spot, Forward, Future)
     - L1 Product Group breakdown
   - Split by Direction (Buy vs Sell)

3. **Monthly P&L** (Line Chart)
   - X-axis: Year + MonthShortName
   - Y-axis: Total P&L
   - Markers: Max P&L and Min P&L highlighted
   - Data labels: Only at peak/trough points

4. **Trade Level Details** (Table)
   - Columns: TradelineNumber, DealDate, Direction, TradeType, Price, P&L
   - Total row enabled
   - Sorted by P&L descending

**Slicers:**
- **Month Year:** Dropdown slicer (currently: 2024)

---

## **Advanced Features**

### **Field Parameters**

**TradeType/ProductGroup Switch:**
- Calculated table enabling dynamic axis switching
- Definition:
```dax
TradeType/ProductGroup Switch = 
{
    ("L1 Product Group", NAMEOF('DimProduct'[L1ProductGroup]), 0),
    ("Trade Type", NAMEOF('DimTrade'[TradeType]), 1)
}
```
- **Usage:** Radio button on P&L by Trade Type visual
- **Benefit:** Dual-perspective analysis without duplicating visuals

### **Date Intelligence**

- Auto-generated date hierarchies (Year → Quarter → Month → Day)
- LocalDateTable relationships for DealDate and ClosedDate variations
- Main date dimension relationship on SnapshotDateKey for time-series analysis

---

## **Data Transformation (Power Query)**

### **Source Table**
- **TradeInformationBase** - Loaded from trading_dataset.xlsx

### **Dimension Transformations**

**DimTrader:**
```m
1. Select columns: Trader, Job Position, Department
2. Remove duplicates
3. Rename: Trader → TraderName, Job Position → JobPosition
4. Add composite key: TraderName & "-" & Department
5. Reorder columns: TraderKey, TraderName, JobPosition, Department
```

**DimProduct:**
```m
1. Select columns: ProductNumber2, L1_ProductGroup...L4_SubCategory, UnitOfMeasure
2. Remove duplicates
3. Rename columns (remove underscores)
4. Add composite key: ProductNumber & "-" & UnitOfMeasure
5. Reorder columns
```

**DimAccount:**
```m
1. Select columns: AccountName, Inter Company Account, Account Parent, Account Country
2. Remove duplicates
3. Rename (remove spaces)
4. Add composite key: AccountName & "-" & AccountParent
5. Reorder columns
```

**DimTrade:**
```m
1. Select columns: TradelineNumber, CompanyCode, Type, RecordSource, TradeType, 
                   TradelineStatus, Direction, MatchIndicator, DealDate, Closed Date
2. Rename: Type → TradeTypeCategory, Closed Date → ClosedDate
3. Remove duplicates (one row per TradelineNumber)
```

**FactTrade:**
```m
1. Select all measure columns + foreign key columns
2. Add SnapshotDateKey: DATE(YEAR([SnapshotDate]), MONTH([SnapshotDate]), DAY([SnapshotDate]))
3. Add composite keys:
   - TraderKey = Trader & "-" & Department
   - AccountKey = AccountName & "-" & Account Parent
   - ProductKey = ProductNumber2 & "-" & UnitOfMeasure
4. Remove natural key columns
5. Keep: SnapshotDateKey, TraderKey, AccountKey, ProductKey, TradelineNumber, 
         PnlSplitPercentage, Volume, Price, MtM Price, COGS, Revenue, PnL, Currency
```

---

---

## **Performance Optimizations**

1. **Hidden Columns:** TraderKey, ProductKey, AccountKey marked as hidden (surrogate keys)
2. **Column Summarization:** Text columns set to "Do Not Summarize"
3. **Date Hierarchies:** Auto-date/time disabled, manual hierarchies only
4. **Relationships:** All many-to-one with single-direction cross-filter
5. **Measure Organization:** Grouped in "BaseMeasures" display folder
6. **Measure Additivity Rules:** 
   - **Fully Additive Measures:** Volume, COGS, Revenue, PnL, Unrealised PnL, Realised PnL (sum across all dimensions including time)
   - **Non-Additive Measures:** Price, MtM Price (use weighted average or last value over time), PnlSplitPercentage (use weighted average), Profit % (ratio measure, recalculate at each level)

---

## **Theme Configuration**

**Applied Theme:** ACT_PBI_Theme (act_power_bi_theme.json)

**Brand Colors:**
- Primary Purple: #64334D (table headers, slicer headers)
- Accent Teal: #0096E1 (line charts, highlights)
- Success Green: #00C49A (max values)
- Alert Red: #F06543 (min values)
- Default Blue: #66C0ED (standard bars)

**Typography:**
- Font Family: Arial
- Header Font Color: #FFFFFF (white on purple)
- Axis Label Color: #252423 (dark gray)

---
---

## **File Structure**

```
Performance Overview.pbip
├── Performance Overview.Report/
│   ├── definition/
│   │   ├── pages/
│   │   │   └── c9b46a871cae85be99b9.json     # Performance Overview page
│   │   └── report.json                        # Report metadata
│   ├── StaticResources/
│   │   └── RegisteredResources/
│   │       └── ACT_PBI_Theme.json            # Custom theme
│   └── definition.pbir                        # Report definition
│
└── Performance Overview.SemanticModel/
    ├── definition.pbism                       # Semantic model definition
    ├── model.bim                              # Tabular model (13K lines)
    └── diagramLayout.json                     # Model diagram layout
```

---



## **Usage Guidelines**

### **For End Users:**

1. **Filter by Year:** Use Month Year slicer to analyze specific periods
2. **Compare Perspectives:** Toggle between Trade Type and Product Group on P&L chart
3. **Identify Outliers:** Top/bottom performers highlighted automatically
4. **Track Trends:** Monthly P&L shows peak (€0.98M in 202410) and trough (€0.04M in 202406)
5. **Drill into Details:** Use Trade Level Details table for transaction-level analysis

### **For Developers:**

1. **Extend Dimensions:** Add new attributes to dimension tables via Power Query
2. **Create Measures:** Use _Measures table, organize in display folders
3. **Modify Theme:** Edit act_power_bi_theme.json for branding changes
4. **Add Slicers:** Connect to existing dimensions (DimProduct, DimAccount not yet sliced)
5. **Version Control:** .pbip format enables Git-friendly source control

---

## **Contact & Version**

**Report Name:** Performance Overview Dashboard  
**Version:** 1.0  
**Created:** November 2025  
**Power BI Desktop Version:** Compatible with PBIP format (2023+)  
**Assessment:** ACT Commodities Senior BI Engineer Technical Assessment  

**Model Compatibility Level:** 1567 (SQL Server 2019 / Power BI)  
**Culture:** en-GB  
**Source Query Culture:** en-001  

---
