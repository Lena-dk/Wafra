# Wafra
A banking feature that helps users save through three tailored methods: rounding up spare change, saving 25% of the monthly surplus in two installments, and diverting a portion of entertainment expenses to savings — promoting consistent and effortless saving habits.


# **What is Waffra?**

A banking feature that helps users save money automatically through three customizable methods, designed to build consistent saving habits with minimal effort.

---

## **Core Data Sources**

* **Monthly income** (salary + fixed income sources).
* **Essential expenses** (housing, transport, food, bills, etc.).
* **Entertainment expenses** (restaurants, cinema, subscriptions, etc.).
* **Salary date** and automatic deduction dates.

---

## **The Three Saving Methods**

### **1) Spare Change Saving (Round-Up)**

* Every card purchase is **rounded up** to the nearest chosen amount (e.g., nearest 1, 5 SAR).
* The **difference** between the actual amount and the rounded amount is transferred to savings.

**Example:** Purchase = 18.20 SAR, 0.80 SAR goes to savings.

---

### **2) Fixed Saving**

**Concept:** Deduct **25% of the monthly surplus** in **two installments** — one at the start of the month and one in the middle.

* **Monthly surplus:**

  $$
  \text{Surplus} = \text{Monthly income} - \text{Essential expenses}
  $$

* **Monthly saving amount:**

  $$
  \text{Saving} = 0.25 \times \text{Surplus}
  $$

* **Schedule:**

  * **1st installment:** Start of the month (or salary date).
  * **2nd installment:** Mid-month.
  * Each installment = **half** of the monthly saving amount.

**Example:**
Income = 8,000 SAR
Essential expenses = 6,200 SAR
Surplus = 1,800 SAR
Monthly saving = 25% × 1,800 = **450 SAR**
Two installments = **225 SAR** at the start, **225 SAR** mid-month.

---

## **3) Entertainment Saving**
Automatically saves a percentage from every entertainment-related purchase.
If the purchase amount is 100 SAR or less → save 1% of that amount.
If the purchase amount is more than 100 SAR → save 5% of that amount.
The saving happens instantly after each qualifying transaction.

---

## **User Journey**

1. **Setup:** Link accounts/cards, set salary date, enter essential expenses, configure limits.
2. **Automation:** Run selected methods on schedule (Round-Up instantly, Fixed twice monthly, Entertainment monthly/weekly).
3. **Notifications:** Before each scheduled deduction + weekly/monthly saving summary.
4. **Reports:** Dashboard with breakdown per method, growth over time, and goal tracking.

---



