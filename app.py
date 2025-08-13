import streamlit as st
import requests

st.set_page_config(page_title="وفرة - مساعد الادخار", layout="centered")
st.title("💰 وفرة - مساعدك الذكي للادخار")

# اختيار نوع الخدمة
option = st.radio("اختر نوع الخدمة:", ["🧾 الادخار التقليدي", "🤖 خدمات وفرة الذكية"])

if option == "🧾 الادخار التقليدي":
    st.subheader("🧾 الادخار التقليدي")
    monthly_income = st.number_input("📥 دخلك الشهري", min_value=0.0, step=100.0)
    saving_goal = st.number_input("🎯 هدفك الادخاري الكلي", min_value=0.0, step=100.0)
    duration_months = st.number_input("⏳ مدة الادخار (بالأشهر)", min_value=1, step=1)

    if st.button("احسب الخطة التقليدية"):
        try:
            url = "http://127.0.0.1:5000/traditional_saving"

            payload = {
                "monthly_income": monthly_income,
                "saving_goal": saving_goal,
                "duration_months": duration_months
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                if result["تحقق"]:
                    st.success(result["الرسالة"])
                else:
                    st.warning(result["الرسالة"])
            else:
                st.error("فشل الاتصال بالخدمة.")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")

elif option == "🤖 خدمات وفرة الذكية":
    st.subheader("🤖 نصيحة ادخار ذكية بناءً على مصروفاتك")
    if "advice_result" not in st.session_state:
        st.session_state.advice_result = None
    if "show_options" not in st.session_state:
        st.session_state.show_options = False

    monthly_income = st.number_input("📥 دخلك الشهري", min_value=0.0, step=100.0, key="smart_income")
    duration_months = st.number_input("⏳ مدة الادخار بالأشهر", min_value=1, step=1, key="smart_duration")

    if st.button("احصل على نصيحة ذكية"):
        try:
            url = "http://127.0.0.1:5000/saving_advice"
            payload = {
                "monthly_income": monthly_income,
                "duration_months": duration_months
            }
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                st.session_state.advice_result = response.json()
                st.session_state.show_options = True
            else:
                st.error("حدث خطأ في الاتصال بالخدمة.")
        except Exception as e:
            st.error(f"خطأ غير متوقع: {e}")

    if st.session_state.advice_result:
        result = st.session_state.advice_result
        st.subheader("📊 التفاصيل:")
        st.info(f"الدخل الشهري: {result['الدخل الشهري']} ريال")
        st.info(f"متوسط المصروفات الشهرية: {result['متوسط المصروفات الشهرية']} ريال")
        #st.success(f"💰 المبلغ الذي يمكن ادخاره خلال المدة: {result['المبلغ الذي يمكن ادخاره خلال المدة']} ريال")

        st.subheader("💡 النصائح المقترحة:")
        for suggestion in result["الاقتراحات"]:
            color = "✅" if suggestion["الأفضل"] else "🔹"
            st.write(f"{color} **{suggestion['الطريقة']}**: {suggestion['الشرح']}")
