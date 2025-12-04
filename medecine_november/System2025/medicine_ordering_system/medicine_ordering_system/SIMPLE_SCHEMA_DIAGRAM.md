# Simple Database Schema Diagram - Level 0

## Essential Database Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                  ONCARE MEDICINE ORDERING SYSTEM                │
│                    Level 0 Database Schema                      │
└─────────────────────────────────────────────────────────────────┘

                     ┌──────────────┐
                     │    USER      │
                     │              │
                     │ • id (PK)    │
                     │ • username   │
                     │ • role       │
                     └──────┬───────┘
                            │
                            │ 1 creates
                            │
                            │ N
                            ▼
                     ┌──────────────┐
                     │    ORDER     │
                     │              │
                     │ • id (PK)    │
                     │ • sales_rep  │
                     │ • status     │
                     │ • total      │
                     └──────┬───────┘
                            │
                            │ 1 contains
                            │
                            │ N
                            ▼
        ┌──────────────────────────────────────┐
        │          ORDERITEM                   │
        │                                      │
        │ • id (PK)                            │
        │ • order_id (FK)                      │
        │ • medicine_id (FK) ────────┐         │
        │ • quantity                 │         │
        │ • price                    │         │
        └────────────────────────────│─────────┘
                                     │
                                     │ N references
                                     │
                                     │ 1
                                     ▼
                            ┌──────────────┐
                            │   MEDICINE   │
                            │              │
                            │ • id (PK)    │
                            │ • name       │
                            │ • price      │
                            │ • stock      │
                            │              │
                            │ category_id ─┼───┐
                            │ manufacturer ─┼───┼───┐
                            └──────────────┘   │   │
                                                │   │
                                    ┌───────────┘   │
                                    │               │
                                    ▼               ▼
                            ┌──────────────┐  ┌──────────────┐
                            │   CATEGORY   │  │ MANUFACTURER │
                            │              │  │              │
                            │ • id (PK)    │  │ • id (PK)    │
                            │ • name       │  │ • name       │
                            └──────────────┘  └──────────────┘
```

---

## Core Tables (6 Essential)

| # | Table | Purpose |
|---|-------|---------|
| 1 | **User** | System users (Sales Rep, Pharmacist, Admin) |
| 2 | **Order** | Customer orders/transactions |
| 3 | **OrderItem** | Items in each order |
| 4 | **Medicine** | Product catalog with inventory |
| 5 | **Category** | Medicine categorization |
| 6 | **Manufacturer** | Medicine suppliers |

---

## Relationships

```
USER (1) ─────── creates ────────> (N) ORDER
ORDER (1) ────── contains ───────> (N) ORDERITEM
ORDERITEM (N) ─── references ────> (1) MEDICINE
MEDICINE (N) ──── belongs_to ────> (1) CATEGORY
MEDICINE (N) ──── from ──────────> (1) MANUFACTURER
```

---

## Quick Reference

**Primary Keys (PK)**: Unique identifier for each record
**Foreign Keys (FK)**: Links between tables
**1:N**: One-to-Many relationship
**N:1**: Many-to-One relationship

---

## Simple Business Flow

```
Sales Rep (USER)
    │
    │ creates
    ▼
ORDER for Customer
    │
    │ contains
    ▼
Multiple MEDICINE items (ORDERITEM)
    │
    │ each references
    ▼
MEDICINE (from CATEGORY & MANUFACTURER)
```

---

**This diagram shows only the essential 6 tables that form the core of the system.**


