# ERD: Ordering & Inventory Workflow (Simple Version)

## Focus: Ordering Process, Inventory Management, and User Roles

Simplified ERD showing the essential workflow between the three user roles.

```mermaid
erDiagram
    %% User Roles
    USER ||--o| SALESREPPROFILE : "has"
    USER ||--o| PHARMACISTADMINPROFILE : "has"
    
    %% Sales Rep: Ordering Process
    USER ||--o| CART : "has"
    CART ||--o{ CARTITEM : "contains"
    CARTITEM }o--|| MEDICINE : "selects"
    USER ||--o{ ORDER : "creates"
    ORDER ||--o{ ORDERITEM : "contains"
    ORDERITEM }o--|| MEDICINE : "orders"
    
    %% Pharmacist/Admin: Inventory & Fulfillment
    USER ||--o{ STOCKMOVEMENT : "manages"
    USER ||--o{ REORDERALERT : "processes"
    USER }o--o{ ORDER : "verifies/fulfills"
    MEDICINE ||--o{ STOCKMOVEMENT : "tracked_by"
    MEDICINE ||--o{ REORDERALERT : "generates"
    
    %% Medicine Catalog
    MEDICINE }o--|| CATEGORY : "belongs_to"
    MEDICINE }o--|| MANUFACTURER : "from"
    
    USER {
        int id PK
        string username
        string role "sales_rep|pharmacist_admin|admin"
        string email
    }
    
    SALESREPPROFILE {
        int id PK
        int user_id FK
        string employee_id
        string territory
    }
    
    PHARMACISTADMINPROFILE {
        int id PK
        int user_id FK
        string license_number
        date license_expiry
    }
    
    CART {
        int id PK
        int sales_rep_id FK
    }
    
    CARTITEM {
        int id PK
        int cart_id FK
        int medicine_id FK
        int quantity
    }
    
    ORDER {
        int id PK
        int sales_rep_id FK "created by"
        string order_number
        string status
        int verified_by_id FK "pharmacist/admin"
        decimal total_amount
    }
    
    ORDERITEM {
        int id PK
        int order_id FK
        int medicine_id FK
        int quantity
        decimal price
    }
    
    MEDICINE {
        int id PK
        string name
        decimal unit_price
        int current_stock
        int reorder_point
        int category_id FK
        int manufacturer_id FK
    }
    
    STOCKMOVEMENT {
        int id PK
        int medicine_id FK
        int created_by FK "pharmacist/admin"
        string movement_type
        int quantity
    }
    
    REORDERALERT {
        int id PK
        int medicine_id FK
        int processed_by FK "pharmacist/admin"
        string priority
        boolean is_processed
    }
    
    CATEGORY {
        int id PK
        string name
    }
    
    MANUFACTURER {
        int id PK
        string name
    }
```

---

## Process Flow Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    SALES REPRESENTATIVE                         │
│                    (Ordering Process)                           │
└─────────────────────────────────────────────────────────────────┘

    USER (sales_rep)
         │
         ├─→ CART (shopping cart)
         │    │
         │    └─→ CARTITEM → MEDICINE
         │
         └─→ ORDER (checkout)
              │
              └─→ ORDERITEM → MEDICINE


┌─────────────────────────────────────────────────────────────────┐
│                  PHARMACIST/ADMIN                               │
│              (Inventory Management & Order Fulfillment)          │
└─────────────────────────────────────────────────────────────────┘

    USER (pharmacist_admin)
         │
         ├─→ ORDER (verify & fulfill)
         │    │
         │    └─→ Updates status, verifies prescription
         │
         └─→ MEDICINE (inventory management)
              │
              ├─→ STOCKMOVEMENT (track stock changes)
              │
              └─→ REORDERALERT (manage low stock)


┌─────────────────────────────────────────────────────────────────┐
│                         MEDICINE CATALOG                        │
└─────────────────────────────────────────────────────────────────┘

    MEDICINE
         │
         ├─→ CATEGORY (organization)
         │
         └─→ MANUFACTURER (source)
```

---

## User Role Responsibilities

### 👤 Sales Representative
- **CART Management**: Add/remove medicines to cart
- **ORDER Creation**: Create orders from cart
- **Order Tracking**: View order status

### 👨‍⚕️ Pharmacist/Admin
- **Inventory Management**: 
  - Create STOCKMOVEMENT records
  - Process REORDERALERT
  - Update MEDICINE stock levels
- **Order Fulfillment**:
  - Verify orders (prescription verification)
  - Update ORDER status
  - Track order progress

### 👑 Admin
- **All Permissions**: Can do everything above
- **System Management**: User management, configuration

---

## Key Relationships Explained

### Ordering Flow
1. **Sales Rep** has **CART** → contains **CARTITEM** → references **MEDICINE**
2. **Sales Rep** creates **ORDER** → contains **ORDERITEM** → references **MEDICINE**
3. **Pharmacist/Admin** verifies/fulfills **ORDER**

### Inventory Flow
1. **MEDICINE** stock tracked by **STOCKMOVEMENT**
2. **MEDICINE** generates **REORDERALERT** when stock low
3. **Pharmacist/Admin** creates **STOCKMOVEMENT** and processes **REORDERALERT**

---

**Copy the Mermaid code above and paste it into [Mermaid Live Editor](https://mermaid.live/) to view the diagram!**


