from fastapi import FastAPI
from pydantic import BaseModel, Field
import pandas as pd
import math
import os

app = FastAPI()

# MCC code classification
mcc_categories = {
    5812: "entertainment",
    5411: "essential",
    5999: "entertainment",
    4900: "essential",
    4829: "essential",
    7011: "entertainment",
    5541: "essential",
    5732: "entertainment",
    5912: "entertainment",
    7832: "entertainment"
}

class UserInput(BaseModel):
    monthly_income: float = Field(..., title="الدخل الشهري")
    duration_months: int = Field(..., title="مدة الادخار بالأشهر")

class TraditionalSavingInput(BaseModel):
    monthly_income: float
    saving_goal: float
    duration_months: int

@app.post("/ادخار_تقليدي")
def traditional_saving(data: TraditionalSavingInput):
    income = data.monthly_income
    goal = data.saving_goal
    duration = data.duration_months

    monthly_required = round(goal / duration, 2)
    monthly_remaining = income - monthly_required

    if monthly_remaining < 0:
        return {
            "تحقق": False,
            "الرسالة": f"لا يمكنك ادخار {monthly_required} ريال شهريًا بدخلك الحالي. قلل من مصروفاتك لتحقيق الهدف."
        }
    else:
        return {
            "تحقق": True,
            "الرسالة": f"يمكنك تحقيق الهدف بادخار {monthly_required} ريال شهريًا. سيتم سحب المبلغ في بداية كل شهر."
        }

@app.post("/نصيحة_ادخار")
def saving_advice(data: UserInput):
    income = data.monthly_income
    duration = data.duration_months

    file_path = "MOCK_DATA.csv"
    if not os.path.exists(file_path):
        return {"error": "ملف العمليات غير موجود"}

    df = pd.read_csv(file_path, sep=",")
    df.columns = df.columns.str.strip()
    df.rename(columns={"Date": "date", "MCC_Code": "mcc", "Amount": "amount"}, inplace=True)

    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors='coerce')
    df = df.dropna(subset=["date"])
    df["category"] = df["mcc"].apply(lambda mcc: mcc_categories.get(mcc, "unknown"))

    latest_date = df["date"].max()
    three_months_ago = latest_date - pd.DateOffset(months=3)
    recent_df = df[df["date"] >= three_months_ago]

    recent_df["month"] = recent_df["date"].dt.to_period("M")
    monthly_expenses = recent_df.groupby("month")["amount"].sum()
    avg_expenses = monthly_expenses.mean()

    monthly_surplus = max(0, income - avg_expenses)
    saving_goal = monthly_surplus * duration

    # Hilalat Saving
    hilalat_saving = round(recent_df["amount"].apply(lambda x: math.ceil(x) - x).sum() / len(monthly_expenses) * duration, 2)

    # Entertainment Saving
    entertainment_df = recent_df[recent_df["category"] == "entertainment"]
    entertainment_saving = 0
    for amt in entertainment_df["amount"]:
        if amt < 100:
            entertainment_saving += amt * 0.01
        else:
            entertainment_saving += amt * 0.05
    entertainment_saving = round(entertainment_saving / len(monthly_expenses) * duration, 2)

    # Fixed Saving
    fixed_monthly_saving = round(0.25 * monthly_surplus, 2)
    fixed_total_saving = fixed_monthly_saving * duration

    max_saving = max(hilalat_saving, entertainment_saving, fixed_total_saving)

    methods = [
        {
            "الطريقة": "ادخار الهللات",
            "الشرح": f"تعتمد على تجميع الكسور المتبقية من عمليات الشراء، وبناء على بياناتك الماضية ستوفر تقريبًا {hilalat_saving} ريال خلال المدة المحددة.",
            "التوفير": hilalat_saving,
            "الأفضل": bool(hilalat_saving == max_saving)
        },
        {
            "الطريقة": "ادخار الترفيه",
            "الشرح": f"سحب 1% من أي مبلغ تحت 100 ريال على الترفيه و5% على ما فوق، سيوفر تقريبًا {entertainment_saving} ريال خلال المدة المحددة.",
            "التوفير": entertainment_saving,
            "الأفضل": bool(entertainment_saving == max_saving)
        },
        {
            "الطريقة": "ادخار ثابت",
            "الشرح": f"توفير 25% من الفرق بين الدخل والصرف شهريًا، وسيتم سحب {fixed_monthly_saving / 2} ريال مرتين شهريًا، لتوفير تقريبًا {fixed_total_saving} ريال خلال المدة المحددة.",
            "التوفير": fixed_total_saving,
            "الأفضل": bool(fixed_total_saving == max_saving)
        }
    ]

    return {
        "الدخل الشهري": income,
        "متوسط المصروفات الشهرية": round(avg_expenses, 2),
        "المبلغ الذي يمكن ادخاره خلال المدة": round(saving_goal, 2),
        "الاقتراحات": methods
    } 