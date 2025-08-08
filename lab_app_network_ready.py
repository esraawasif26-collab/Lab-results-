
import streamlit as st
import datetime

# إعداد واجهة البرنامج
st.set_page_config(page_title="Lab Reports", layout="centered")

# قاعدة بيانات بسيطة لتخزين المرضى
if "patients" not in st.session_state:
    st.session_state.patients = {}

st.title("🔬 Qurtor lab ")

# 🧾 إدخال بيانات المريض
st.subheader("بيانات المريض:")
name = st.text_input("الاسم", key="name")
date = st.date_input("التاريخ", value=datetime.date.today())
insurance_number = st.text_input("الرقم التأميني", key="insurance")

if st.button("📌 حفظ المريض"):
    if name and insurance_number:
        patient_id = f"{name}_{insurance_number}"
        st.session_state.patients[patient_id] = {
            "name": name,
            "date": date.strftime("%Y-%m-%d"),
            "insurance": insurance_number,
            "tests": {}
        }
        st.success("✅ تم حفظ المريض بنجاح.")
    else:
        st.warning("⚠️ من فضلك أدخل الاسم والرقم التأميني.")

# 📋 عرض المرضى السابقين
st.subheader("المرضى السابقين:")
for pid, pdata in st.session_state.patients.items():
    with st.expander(f"{pdata['name']} - {pdata['insurance']}"):
        st.write(f"📅 التاريخ: {pdata['date']}")
        st.write(f"🧪 التحاليل:")
        if pdata["tests"]:
            for test_name, result in pdata["tests"].items():
                st.write(f"- {test_name}: {result}")
        else:
            st.write("لا توجد تحاليل بعد.")

# ➕ اختيار تحاليل لمريض محدد
st.subheader("إضافة تحاليل:")
selected_pid = st.selectbox("اختر المريض", list(st.session_state.patients.keys()))
available_tests = ["CBC", "Blood Sugar", "Cholesterol", "Creatinine", "Urea", "SGPT", "SGOT", "Bilirubin"]
selected_tests = st.multiselect("اختر التحاليل", available_tests)

test_results = {}
for test in selected_tests:
    result = st.text_input(f"النتيجة لـ {test}")
    if result:
        test_results[test] = result

if st.button("💾 حفظ التحاليل"):
    if selected_pid and test_results:
        st.session_state.patients[selected_pid]["tests"].update(test_results)
        st.success("✅ تم حفظ نتائج التحاليل.")
    else:
        st.warning("⚠️ اختر مريض وأدخل نتائج التحاليل.")

# ✨ توليد التقرير
st.subheader("📤 طباعة التقرير:")
selected_report = st.selectbox("اختر مريض لطباعة تقريره", list(st.session_state.patients.keys()))

if st.button("📄 توليد التقرير"):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm

    patient = st.session_state.patients[selected_report]
    file_path = f"/mnt/data/Report_{patient['name']}.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("الهيئة العامة للتأمين الصحي - فرع الغربية<br/>عيادة قطور الشاملة", styles['Title']))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(f"الاسم: {patient['name']}", styles['Normal']))
    elements.append(Paragraph(f"التاريخ: {patient['date']}", styles['Normal']))
    elements.append(Paragraph(f"الرقم التأميني: {patient['insurance']}", styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))

    elements.append(Paragraph("التحاليل:", styles['Heading3']))
    for test, result in patient["tests"].items():
        elements.append(Paragraph(f"{test}: {result}", styles['Normal']))

    elements.append(Spacer(1, 2*cm))
    elements.append(Paragraph("Sign by", styles['Normal']))

    doc.build(elements)
    st.success("✅ تم إنشاء التقرير.")
    st.download_button("⬇️ تحميل التقرير", data=open(file_path, "rb"), file_name=file_path.split("/")[-1])
