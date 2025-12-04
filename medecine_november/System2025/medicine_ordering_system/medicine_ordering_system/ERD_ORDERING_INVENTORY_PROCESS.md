# ERD Diagram: Ordering Process & Inventory Management with User Roles

## Entity Relationship Diagram - Workflow Focused

This ERD focuses on the **ordering process**, **inventory management**, and the **three user roles** (Sales Representative, Pharmacist/Admin, and Admin) in the OnCare Medicine Ordering System.

```mermaid
erDiagram
    %% User Roles and Profiles
    USER ||--o| SALESREPPROFILE : "has (if sales_rep)"
    USER ||--o| PHARMACISTADMINPROFILE : "has (if pharmacist_admin)"
    
    %% Sales Rep Ordering Process
    USER ||--o| CART : "has (sales_rep only)"
    CART ||--o{ CARTITEM : "contains"
    CARTITEM }o--|| MEDICINE : "references"
    USER ||--o{ ORDER : "creates (sales_rep)"
    ORDER ||--o{ ORDERITEM : "contains"
    ORDERITEM }o--|| MEDICINE : "references"
    ORDER ||--o{ ORDERSTATUSHISTORY : "tracks"
    ORDER }o--o| USER : "verified_by (pharmacist/admin)"
    
    %% Inventory Management (Pharmacist/Admin)
    USER ||--o{ STOCKMOVEMENT : "creates (pharmacist/admin)"
    USER ||--o{ REORDERALERT : "processes (pharmacist/admin)"
    MEDICINE ||--o{ STOCKMOVEMENT : "has"
    MEDICINE ||--o{ REORDERALERT : "has"
    
    %% Medicine Catalog
    MEDICINE }o--|| CATEGORY : "belongs_to"
    MEDICINE }o--|| MANUFACTURER : "from"
    
    %% User Entity
    USER {
        int id PK
        string username
        string email
        string role "sales_rep|pharmacist_admin|admin"
        string phone_number
        datetime created_at
    }
    
    %% User Profiles
    SALESREPPROFILE {
        int id PK
        int user_id FK
        string employee_id UK
        string territory
        decimal commission_rate
        boolean is_active
    }
    
    PHARMACISTADMINPROFILE {
        int id PK
        int user_id FK
        string license_number UK
        date license_expiry
        string specialization
        boolean is_available
    }
    
    %% Ordering Process - Cart
    CART {
        int id PK
        int sales_rep_id FK
        datetime created_at
        datetime updated_at
    }
    
    CARTITEM {
        int id PK
        int cart_id FK
        int medicine_id FK
        int quantity
        datetime added_at
    }
    
    %% Ordering Process - Order
    ORDER {
        int id PK
        int sales_rep_id FK "created by"
        string order_number UK
        string customer_name
        string status "pending|confirmed|processing|delivered"
        string payment_status
        decimal total_amount
        boolean prescription_required
        int verified_by_id FK "pharmacist/admin"
        datetime created_at
        datetime confirmed_at
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
    
    %% Inventory Management
    MEDICINE {
        int id PK
        int category_id FK
        int manufacturer_id FK
        string name
        decimal unit_price
        int current_stock
        int reorder_point
        int minimum_stock_level
        boolean is_active
        boolean requires_prescription
    }
    
    STOCKMOVEMENT {
        int id PK
        int medicine_id FK
        int created_by FK "pharmacist/admin"
        string movement_type "in|out|adjustment|return"
        int quantity
        string reference_number
        text notes
        datetime created_at
    }
    
    REORDERALERT {
        int id PK
        int medicine_id FK
        int processed_by FK "pharmacist/admin"
        int current_stock
        string priority
        boolean is_processed
        datetime created_at
        datetime processed_at
    }
    
    %% Medicine Catalog
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
```

---

## Process Flow Explanation

### 1. Sales Representative Workflow

```
Sales Rep (USER with SALESREPPROFILE)
    │
    │ (1) Browsing & Shopping
    ▼
CART (one per sales rep)
    │
    │ (2) Adding items
    ▼
CARTITEM (multiple medicines)
    │
    │ (3) Checkout → Convert to Order
    ▼
ORDER (created by sales rep)
    │
    │ (4) Order contains
    ▼
ORDERITEM (references medicines from cart)
```

### 2. Pharmacist/Admin Workflow

```
Pharmacist/Admin (USER with PHARMACISTADMINPROFILE)
    │
    ├─→ (1) Receives ORDER (status: pending)
    │   │
    │   ├─→ Verify prescription (if required)
    │   │   └─→ Updates ORDER.verified_by
    │   │
    │   ├─→ Check stock availability (MEDICINE.current_stock)
    │   │
    │   └─→ Update ORDER status (processing → ready → delivered)
    │       └─→ Creates ORDERSTATUSHISTORY
    │
    └─→ (2) Inventory Management
        │
        ├─→ Creates STOCKMOVEMENT (stock in/out/adjustment)
        │   └─→ Updates MEDICINE.current_stock
        │
        └─→ Processes REORDERALERT
            └─→ When MEDICINE.current_stock <= reorder_point
```

### 3. Admin Workflow

```
Admin (USER with role='admin')
    │
    ├─→ Can do everything Pharmacist/Admin can do
    │
    └─→ Additional system management
        └─→ User management, system configuration
```

---

## Key Relationships

### Ordering Process Relationships

1. **USER (sales_rep) → CART** (1:1)
   - Each sales rep has one shopping cart

2. **CART → CARTITEM** (1:N)
   - Cart contains multiple items

3. **CARTITEM → MEDICINE** (N:1)
   - Each cart item references a medicine

4. **USER (sales_rep) → ORDER** (1:N)
   - Sales rep creates multiple orders

5. **ORDER → ORDERITEM** (1:N)
   - Order contains multiple items

6. **ORDERITEM → MEDICINE** (N:1)
   - Order items reference medicines

7. **ORDER → USER (pharmacist/admin)** (N:1, optional)
   - Orders can be verified by pharmacist/admin

### Inventory Management Relationships

8. **USER (pharmacist/admin) → STOCKMOVEMENT** (1:N)
   - Pharmacist/admin creates stock movements

9. **MEDICINE → STOCKMOVEMENT** (1:N)
   - Medicine has many stock movements

10. **USER (pharmacist/admin) → REORDERALERT** (1:N)
    - Pharmacist/admin processes reorder alerts

11. **MEDICINE → REORDERALERT** (1:N)
    - Medicine can have multiple reorder alerts

---

## Role-Based Access Summary

| Entity | Sales Rep | Pharmacist/Admin | Admin |
|--------|-----------|------------------|-------|
| **CART** | ✅ Create/View/Update | ❌ | ❌ |
| **ORDER** | ✅ Create | ✅ View/Update/Fulfill | ✅ All |
| **MEDICINE** | ✅ View | ✅ View/Manage | ✅ All |
| **STOCKMOVEMENT** | ❌ | ✅ Create | ✅ All |
| **REORDERALERT** | ❌ | ✅ View/Process | ✅ All |
| **Prescription Verification** | ❌ | ✅ Verify | ✅ All |

---

## Workflow Sequence

### Complete Order Lifecycle

```
1. Sales Rep logs in
   └─→ Creates/views CART

2. Sales Rep adds medicines to CART
   └─→ Creates CARTITEM records

3. Sales Rep checks out
   └─→ CART converts to ORDER
   └─→ CARTITEM converts to ORDERITEM
   └─→ ORDER status: "pending"

4. Pharmacist/Admin receives ORDER
   └─→ Reviews ORDER (prescription if needed)
   └─→ Updates ORDER.verified_by
   └─→ Checks MEDICINE.current_stock

5. Pharmacist/Admin fulfills ORDER
   └─→ Updates ORDER.status: "processing"
   └─→ Creates STOCKMOVEMENT (type: "out")
   └─→ Updates MEDICINE.current_stock (decreases)
   └─→ Creates ORDERSTATUSHISTORY

6. ORDER status: "ready_for_pickup" → "delivered"
   └─→ Creates ORDERSTATUSHISTORY for each status change

7. If MEDICINE.current_stock <= reorder_point
   └─→ System creates REORDERALERT
   └─→ Pharmacist/Admin processes alert
   └─→ Creates STOCKMOVEMENT (type: "in")
   └─→ Updates MEDICINE.current_stock (increases)
```

---

## Files Available

1. **ERD_ORDERING_INVENTORY_PROCESS.md** (this file) - Complete documentation
2. **ERD_ORDERING_PROCESS.mmd** - Mermaid source file
3. Copy the Mermaid code above to view in [Mermaid Live Editor](https://mermaid.live/)

---

**This diagram shows the complete workflow of how Sales Reps create orders and how Pharmacist/Admin manages inventory and fulfills orders.**


