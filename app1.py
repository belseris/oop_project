import streamlit as st
import numpy as np
import base64
st.title("คำนวณภาษีบุคคลธรรมดา 2566")
st.markdown("---")
year = st.number_input("รายได้ต่อเดือน",step=1,format="%d")
years = year*12
newyear = st.number_input("รายได้อื่นๆต่อเดือน",step=1,format="%d")
if newyear > year :
    newyear = newyear*12
    newyear = (newyear-year)*0.005

reduce = 0
st. subheader("ค่าลดหย่อนภาษี")
with st.form("form 1"):
#ข้อมูลส่วนตัว
    st.subheader("ค่าลดหย่อนภาษีส่วนตัวเเละครอบครัว")
    status = st.selectbox("สถานะชีวิต", ["โสด", "คู่สมรส",])
    if status == "คู่สมรส" :
        reduce += 120000
    elif status == "โสด" :
        reduce += 60000
    col1,col2 = st.columns(2)
    babys = col1.number_input("บุตรกี่คน(ที่เกิดก่อน ปี พ.ศ 2561)",step=1,format="%d")
    babys = babys*30000
    reduce += babys
    babyss = col2.number_input("บุตรกี่คน(ที่เกิดหลัง ปี พ.ศ 2561)",step=1,format="%d")
    babyss = babyss*60000
    reduce += babyss
    st.markdown("---")
#ข้อมูลภายในบ้าน
    DM = st.selectbox("บิดามารดา", ["..","บิดา", "มารดา","บิดามารดา"])
    colDM1,colDM2 = st.columns(2)
    ageD = colDM1.number_input("อายุบิดา",step=1,format="%d")
    monthD = colDM2.number_input('รายได้ต่อเดือนบิดา',step=1,format="%d")
    ageM = colDM1.number_input("อายุมารดา",step=1,format="%d")
    monthM = colDM2.number_input('รายได้ต่อเดือนมารดา',step=1,format="%d")
    if (DM == "บิดา" or DM == "มารดา") and (ageD >= 60 and monthD < 30000) and (ageM >= 60 and monthM < 30000):
        reduce += 30000
    elif DM == "บิดามารดา" and (ageD >= 60 and monthD < 30000) and (ageM >= 60 and monthM < 30000):
        reduce += 60000
    DM1 = st.selectbox("บิดามารดาคู่สมรส", ["...","บิดาคู่สมรส", "มารดาคู่สมรส","บิดามารดาคู่สมรส"])
    colDM1,colDM2 = st.columns(2)
    ageD2 = colDM1.number_input("อายุบิดาคู่สมรส",step=1,format="%d")
    monthD2 = colDM2.number_input('รายได้ต่อเดือนบิดาคู่สมรส',step=1,format="%d")
    ageM2 = colDM1.number_input("อายุมารดาคู่สมรส",step=1,format="%d")
    monthM2 = colDM2.number_input('รายได้ต่อเดือนมารดาคู่สมรส',step=1,format="%d")
    if (DM1 == "บิดาคู่สมรส" or DM1 == "มารดาบิดาคู่สมรส") and (ageD2 >= 60 and monthD2 < 30000) or (ageM2 >= 60 and monthM2 < 30000):
        reduce += 30000
    elif DM1 == "บิดามารดาบิดาคู่สมรส" and (ageD2 >= 60 and monthD2 < 30000) or (ageM2 >= 60 and monthM2 < 30000):
        reduce += 60000
    disabled = st.number_input("จำนวนผู้พิการในครัวเรือน",step=1,format="%d")
    if disabled != 0 :
        reduce += disabled*60000

    st.markdown("---")

#ค่าลดหย่อนภาษีกลุ่มประกัน เงินออม และการลงทุน
    st.subheader("ค่าลดหย่อนภาษีกลุ่มประกัน เงินออม และการลงทุน")
    a = st.number_input("ประกันชีวิตเเละประกันสะสมทรัพย์ (ไม่เกิน 100000 บาท)",step=1,format="%d")
    if a  > 100000 :
        a = 100000
    b = st.number_input("ประกันสุขภาพ (ไม่เกิน 25000 บาท)",step=1,format="%d")
    if b  > 25000 :
        b = 25000
    c = st.number_input("ประกันสังคม (ไม่เกิน 9000 บาท)",step=1,format="%d")
    if c  > 9000 :
        c = 9000
    d = st.number_input("ประกันสุขภาพของบิดามารดา (ไม่เกิน 15000 บาท)",step=1,format="%d")
    if d  > 15000 :
        d = 15000
    e = st.number_input("เงินลงทุนะุรกิจ Social Enterprise (ไม่เกิน 100000 บาท)",step=1,format="%d")
    if e  > 100000 :
        e = 100000
    f = st.number_input("กองทุนไทยเพื่อความยังยื่น TESG (ไม่เกิน 100000 บาท)",step=1,format="%d")
    if f  > years / 100*30 :
        f = 100000
    if a+b+c+d+e+f > 100000 :
        reduce += 100000
    elif a+b+c+d+e+f < 100000 :
        reduce += a+b+c+d+e+f
    st.markdown("----")
#กองทุน RMF...
    g = st.number_input("กองทุนรวมเพื่อการเลี้ยงชีพ RMF (30% เงินได้ไม่เกิน 500,000 บาท )",step=1,format="%d")
    if g  > years/100*30 :
        g = 500000
    h = st.number_input("กองทุนรวมเพื่อการออม SSF (30% เงินได้ไม่เกิน 200,000 บาท )",step=1,format="%d")
    if h  > years/100*30 :
        h = 200000
    i = st.number_input("กองทุนสำรองเลี้ยงชีพ PVD (15% เงินได้ไม่เกิน 500,000 บาท )",step=1,format="%d")
    if i > years/100*15 :
        f = 500000
    j = st.number_input("กองทุนบำเหน็จบำนาญราชการ กบข (30% เงินได้ไม่เกิน 500,000 บาท )",step=1,format="%d")
    if j > years/100*30 :
        j = 500000
    k = st.number_input("กองทุนการออมแห่งชาติ กอช (ไม่เกิน 30,000 บาท )",step=1,format="%d")
    if k > 30000 :
        k = 300000
    l = st.number_input("เบี้ยประกันชีวิตแบบบำนาญ (15% เงินได้ไม่เกิน 200,000 บาท )",step=1,format="%d")
    if l > years/100*15 :
        l = 200000

    if g+h+i+j+k+l > 500000 :
        reduce += 500000
    elif a+b+c+d+e+f < 500000 :
        reduce += g+h+i+j+k+l
    st.markdown("---")
    Income = years-reduce
#ค่าลดหย่อนภาษีกลุ่มเงินบริจาค
    st.subheader("ค่าลดหย่อนภาษีกลุ่มเงินบริจาค")
    m = st.number_input("ทั่วไป",step=1,format="%d")
    if i < Income*0.1 :
        i = Income*0.1
    n = st.number_input("เงินบริจาคเพื่อการศึกษา การกีฬา การพัฒนาสังคม เพื่อประโยชน์สาธารณะ และบริจาคเพื่อสถานพยาบาลของรัฐ",step=1,format="%d")
    if n*2 < years*0.1 :
        n = years*0.1
    o = st.number_input("เงินบริจาคให้กับพรรคการเมือง ไม่เกิน 10,000 บาท",step=1,format="%d")
    if o > 10000 :
        o = 10000
    reduce += n +i +o
    st.markdown("---")
    st.subheader("ค่าลดหย่อนกลุ่มกระตุ้นเศรษฐกิจของรัฐ")
    p = st.number_input("โครงการช้อปดีมีคืน (ไม่เกิน 40,000 บาท)" ,step=1,format="%d")
    if p > 40000:
        p=40000
    q = st.number_input("ดอกเบี้ยกู้ยืมเพื่อซื้อหรือสร้างที่อยู่อาศัย (ไม่เกิน 100000 บาท)",step=1,format="%d")
    if q > 100000:
        q = 100000
    reduce += p+q
    froms = st.form_submit_button()
    if froms :
        st.warning(f"เงินได้สุธิของคุณเท่ากับ {reduce}")
    
#คำนวณภาษีด้วยเปอร์เซ็น 
reduce = years - reduce  
tax = 0
if reduce < 150001 :
    tex = reduce
if 150001 <= reduce <= 300000:
    tax = (reduce - 150000) * 0.05
elif 300001 <= reduce <= 500000:
    tax = ((reduce - 300000) * 0.1) + 7500
elif 500001 <= reduce <= 750000:
    tax = ((reduce - 500000) * 0.15) + 27500
elif 750001 <= reduce <= 1000000:
    tax = ((reduce - 750000) * 0.2) + 65000
elif 1000001 <= reduce <= 2000000:
    tax = ((reduce - 1000000) * 0.25) + 115000
elif 2000001 <= reduce <= 5000000:
    tax = ((reduce - 2000000) * 0.3) + 365000
else:
    tax = ((reduce - 5000000) * 0.35) + 1265000

colDM1,colDM2,colDM3 = st.columns(3)
sum = colDM2.button("คำนวณภาษี")
if sum :
    st.write('<span style="color: red;">สรุป</span>', unsafe_allow_html=True)
    if newyear > tax :
        st.markdown(f"คุณต้องเสียภาษีเเบบเหมาเนื่องจากมีรายได้ช่องทางอื่นๆมากกว่ารายได้จากเงินเดือนปกติโดยเมื่อเทียบกันระหว่างคำนวณภาษีเเบบปกติเเล้วภาษีเเบบเหมาได้มากกว่าดังนั้นจึงต้องใช่วิธีคิดหาภาษีเเบบเหมานั้นเอง")
        st.markdown(f"ภาษีที่ต้องจ่าย {newyear} บาท")
        if newyear < 5000 :
            st.markdown("ยกเว้นการจ่ายภาษี เนื่องจากด้วยวิธีคิดแบบเหมาแล้ว มีภาษีที่ต้องเสียทั้งสิ้นไม่เกิน 5,000 บาท จะได้รับการยกเว้นภาษีในวิธีนี้")
        st.markdown("คำนวณได้จากสูตรการหาภาษีโดย")
        st.write('<span style="color: green;">ภาษีแบบเหมา = (เงินได้ทุกประเภท - เงินเดือน) x 0.005</span>', unsafe_allow_html=True)
    elif tax > newyear :
        st.markdown("ภาษีบุคคลธรรมดาที่คุณต้องเสียโดยคิดอัตราภาษีเเบบขั้นบันไดซึ่งผ่านจากการคำนวณเงินได้ลบค่าลดหย่อนเเละค่าใช่จ่ายเเล้ว จึงได้เงินสุธิ")
        st.markdown(f"เงินสุธิของคุณ  {reduce}  บาท")
        st.markdown(f"ภาษีที่ต้องจ่าย  {tax}  บาท")
        st.write('<span style="color: green;">ภาษีที่ต้องจ่าย = เงินได้สุธิ * อัตราภาษี</span>', unsafe_allow_html=True)
    elif reduce < 150000 :
        st.markdown(f"เงินสุธิของคุณ  {reduce}  บาท")
        st.markdown("ได้รับการยกเว้นภาษีภาษีเนื่องจากเงินได้สุธิไม่เกินไปกว่าที่รัฐกำหนด")  
    # st.write('<span style="color: red;">สรุป</span>', unsafe_allow_html=True)
    # st.markdown(f"เงินสุธิ {reduce}")
    # st.markdown(f"ภาษีที่ต้องจ่าย {tax} บาท")
    # st.markdown("คำนวณได้จากสูตรการหาภาษีโดย")
    # st.write('<span style="color: green;">ภาษีที่ต้องจ่าย = เงินได้สุธิ * อัตราภาษี</span>', unsafe_allow_html=True)
#รูปพื้นหลัง
def add_bg_from_local(image_file, footer_link):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/png;base64,{encoded_string}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            position: relative;
        }}
        .custom-footer {{
            position: absolute;
            bottom: 10px;
            font-size: 14px;
            color: white;
        }}
        .custom-footer a {{
            color: white;
            text-decoration: underline;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_local('bel2.jpg','http://localhost:8502/')




