# ERD Diagram - Mermaid Format (Ready to Use)

## Complete ERD Diagram - All Tables

Copy the code below and paste it into [Mermaid Live Editor](https://mermaid.live/) or any markdown viewer that supports Mermaid:

```mermaid
erDiagram
    USER ||--o{ ORDER : "creates"
    USER ||--o| SALESREPPROFILE : "has"
    USER ||--o| PHARMACISTADMINPROFILE : "has"
    USER ||--o{ STOCKMOVEMENT : "creates"
    USER ||--o{ REORDERALERT : "processes"
    
    ORDER ||--o{ ORDERITEM : "contains"
    ORDER ||--o{ ORDERSTATUSHISTORY : "has"
    ORDER }o--|| USER : "created_by"
    ORDER }o--o| USER : "verified_by"
    
    ORDERITEM }o--|| MEDICINE : "references"
    ORDERITEM }o--|| ORDER : "belongs_to"
    
    MEDICINE }o--|| CATEGORY : "belongs_to"
    MEDICINE }o--|| MANUFACTURER : "from"
    MEDICINE ||--o{ STOCKMOVEMENT : "has"
    MEDICINE ||--o{ REORDERALERT : "has"
    MEDICINE ||--o{ MEDICINEIMAGE : "has"
    
    CATEGORY ||--o{ CATEGORY : "parent_category"
    
    USER {
        int id PK
        string username
        string email
        string role
        string phone_number
        datetime created_at
    }
    
    SALESREPPROFILE {
        int id PK
        int user_id FK
        string employee_id
        string territory
        decimal commission_rate
    }
    
    PHARMACISTADMINPROFILE {
        int id PK
        int user_id FK
        string license_number
        date license_expiry
        string specialization
    }
    
    ORDER {
        int id PK
        int sales_rep_id FK
        string order_number UK
        string customer_name
        string status
        string payment_status
        decimal total_amount
        datetime created_at
    }
    
    ORDERITEM {
        int id PK
        int order_id FK
        int medicine_id FK
        int quantity
        decimal unit_price
        decimal total_price
    }
    
    ORDERSTATUSHISTORY {
        int id PK
        int order_id FK
        int changed_by FK
        string old_status
        string new_status
        datetime changed_at
    }
    
    MEDICINE {
        int id PK
        int category_id FK
        int manufacturer_id FK
        string name
        string generic_name
        decimal unit_price
        int current_stock
        int reorder_point
        boolean is_active
    }
    
    CATEGORY {
        int id PK
        int parent_category_id FK
        string name UK
        text description
    }
    
    MANUFACTURER {
        int id PK
        string name UK
        string country
        string contact_email
    }
    
    STOCKMOVEMENT {
        int id PK
        int medicine_id FK
        int created_by FK
        string movement_type
        int quantity
        string reference_number
        datetime created_at
    }
    
    REORDERALERT {
        int id PK
        int medicine_id FK
        int processed_by FK
        int current_stock
        string priority
        boolean is_processed
    }
    
    MEDICINEIMAGE {
        int id PK
        int medicine_id FK
        string image
        boolean is_primary
    }
```

---

## Level 0 ERD - Essential Tables Only (6 Tables)

For a simplified view showing only the core business logic:

```mermaid
erDiagram
    USER ||--o{ ORDER : "creates"
    ORDER ||--o{ ORDERITEM : "contains"
    ORDERITEM }o--|| MEDICINE : "references"
    MEDICINE }o--|| CATEGORY : "belongs_to"
    MEDICINE }o--|| MANUFACTURER : "from"
    
    USER {
        int id PK
        string username
        string role
        string email
    }
    
    ORDER {
        int id PK
        int sales_rep_id FK
        string order_number UK
        string status
        decimal total_amount
    }
    
    ORDERITEM {
        int id PK
        int order_id FK
        int medicine_id FK
        int quantity
        decimal unit_price
    }
    
    MEDICINE {
        int id PK
        int category_id FK
        int manufacturer_id FK
        string name
        decimal unit_price
        int current_stock
    }
    
    CATEGORY {
        int id PK
        string name UK
    }
    
    MANUFACTURER {
        int id PK
        string name UK
    }
```

---

## How to Use

### Method 1: Mermaid Live Editor (Recommended)
1. Go to: **https://mermaid.live/**
2. Copy the Mermaid code above
3. Paste into the editor
4. View the interactive diagram
5. Export as PNG, SVG, or PDF

### Method 2: GitHub/GitLab
- These platforms automatically render Mermaid diagrams
- Just include the code block in your markdown file

### Method 3: VS Code
1. Install extension: **"Markdown Preview Mermaid Support"**
2. Open this file in VS Code
3. Preview will show the rendered diagram

### Method 4: Documentation Platforms
- **Notion**: Supports Mermaid
- **Confluence**: With Mermaid plugin
- **Docusaurus**: Built-in support
- **GitBook**: Built-in support

---

## Relationship Notation

| Symbol | Meaning | Example |
|--------|---------|---------|
| `||--o{` | One-to-Many | One user creates many orders |
| `}o--||` | Many-to-One | Many items belong to one order |
| `||--o\|` | One-to-One | One user has one profile |
| `}o--o\|` | Many-to-One (optional) | Order may have a verifier |

---

## Key Fields Legend

- **PK** = Primary Key (unique identifier)
- **FK** = Foreign Key (reference to another table)
- **UK** = Unique Key (unique constraint)

---

## Files Available

1. **ERD_MERMAID_READY.md** (this file) - Ready-to-use code
2. **ERD_DIAGRAM_COMPLETE.mmd** - Complete ERD as .mmd file
3. **ERD_DIAGRAM_SIMPLE.mmd** - Simple Level 0 ERD as .mmd file
4. **DATABASE_ERD_MERMAID.md** - Detailed documentation

---

**Ready to use!** Copy the code above and paste it into Mermaid Live Editor to generate your diagram.


