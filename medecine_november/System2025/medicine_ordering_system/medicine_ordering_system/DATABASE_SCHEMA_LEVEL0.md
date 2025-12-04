# Database Schema - Level 0 (Essential Tables Only)

## Simple Entity Relationship Diagram

```
┌─────────────────────┐
│       User          │
│─────────────────────│
│ • id (PK)           │
│ • username          │
│ • role              │
│ • email             │
└──────────┬──────────┘
           │
           │ (1:N)
           │
           ▼
┌─────────────────────┐
│       Order         │
│─────────────────────│
│ • id (PK)           │
│ • order_number      │
│ • sales_rep_id (FK) │
│ • status            │
│ • total_amount      │
└──────────┬──────────┘
           │
           │ (1:N)
           │
           ▼
┌─────────────────────┐      ┌─────────────────────┐
│     OrderItem       │─────▶│      Medicine       │
│─────────────────────│  N:1 │─────────────────────│
│ • id (PK)           │      │ • id (PK)           │
│ • order_id (FK)     │      │ • name              │
│ • medicine_id (FK)  │      │ • unit_price        │
│ • quantity          │      │ • current_stock     │
│ • unit_price        │      │ • category_id (FK)  │
└─────────────────────┘      │ • manufacturer_id(FK)│
                             └──────────┬──────────┘
                                        │
                          ┌─────────────┴──────────────┐
                          │                            │
                          ▼                            ▼
                  ┌──────────────┐         ┌─────────────────────┐
                  │   Category   │         │    Manufacturer     │
                  │──────────────│         │─────────────────────│
                  │ • id (PK)    │         │ • id (PK)           │
                  │ • name       │         │ • name              │
                  └──────────────┘         └─────────────────────┘
```

---

## Core Tables Overview

### 1. **User** (Users/Authentication)
- Primary entity for all system users
- Roles: Sales Rep, Pharmacist/Admin, Admin
- Links to orders and other user-related activities

### 2. **Medicine** (Product Catalog)
- Core product entity
- Contains inventory levels, pricing, and product details
- Links to Category and Manufacturer

### 3. **Category** (Medicine Organization)
- Organizes medicines into categories
- Supports hierarchical categories (parent-child)

### 4. **Manufacturer** (Medicine Source)
- Tracks medicine manufacturers/suppliers

### 5. **Order** (Sales Transactions)
- Main transaction entity
- Links Sales Rep (User) to customer orders
- Tracks order status and payment

### 6. **OrderItem** (Order Details)
- Individual items within an order
- Links Order to Medicine with quantity and pricing

---

## Key Relationships

1. **User → Order** (1:N)
   - One user (sales rep) can create many orders

2. **Order → OrderItem** (1:N)
   - One order contains many order items

3. **OrderItem → Medicine** (N:1)
   - Many order items can reference the same medicine

4. **Medicine → Category** (N:1)
   - Many medicines belong to one category

5. **Medicine → Manufacturer** (N:1)
   - Many medicines come from one manufacturer

---

## Essential Attributes Per Table

### User
- `id` (Primary Key)
- `username`, `email`
- `role` (sales_rep, pharmacist_admin, admin)

### Medicine
- `id` (Primary Key)
- `name`, `description`
- `unit_price`, `cost_price`
- `current_stock`, `reorder_point`
- `category_id` (Foreign Key)
- `manufacturer_id` (Foreign Key)

### Category
- `id` (Primary Key)
- `name`

### Manufacturer
- `id` (Primary Key)
- `name`

### Order
- `id` (Primary Key)
- `order_number` (Unique)
- `sales_rep_id` (Foreign Key → User)
- `status`, `payment_status`
- `total_amount`

### OrderItem
- `id` (Primary Key)
- `order_id` (Foreign Key → Order)
- `medicine_id` (Foreign Key → Medicine)
- `quantity`, `unit_price`, `total_price`

---

## Simplified Data Flow

```
User (Sales Rep)
    │
    │ creates
    ▼
Order
    │
    │ contains
    ▼
OrderItem(s)
    │
    │ references
    ▼
Medicine ← Category
    │         │
    │         Manufacturer
    │
    │ (inventory tracking)
    └──→ Stock Levels
```

---

## Table Summary

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **User** | System users | id, username, role |
| **Medicine** | Product catalog | id, name, price, stock |
| **Category** | Product grouping | id, name |
| **Manufacturer** | Product source | id, name |
| **Order** | Sales transactions | id, order_number, status |
| **OrderItem** | Order details | id, order_id, medicine_id, quantity |

**Total Essential Tables: 6**

---

## Notes

- This is a **Level 0** (high-level) diagram showing only core entities
- Additional tables exist for:
  - Stock movements tracking
  - Analytics/forecasting
  - Audit logs
  - User profiles
  - Transactions/payments
  - System administration

- All relationships use Foreign Keys (FK) for data integrity
- Primary Keys (PK) are auto-generated IDs
- This simplified view focuses on the core business logic: **Users create Orders containing Medicines**


