from docx import Document
from docxcompose.composer import Composer

doc = Document(
    r"C:\Users\Administrator\Desktop\关于印发重庆市第二批河流河道名录登记簿的通知.docx"
)
doc.save(r"E:\关于印发重庆市第二批河流河道名录登记簿的通知2.docx")
