import os
import PyPDF2
from io import BytesIO
from docx import Document

poppler_path = r"D:\软件安装包\poppler-24.08.0\Library\bin"  # 第一步2安装包的路径
# os.environ["PATH"] = f'{poppler_path};{os.environ["PATH"]}'

from pdf2image import convert_from_path
from pdf2docx import Converter


def pdf_to_images(pdfpath, output_folder):
    """pdf批量转JPEG图片

    Args:
        pdfpath (str|Path): pdf文件目录
        output_folder (str|Path): 图片输出位置
    """
    for name in os.listdir(pdfpath):
        images = convert_from_path(
            os.path.join(pdfpath, name), poppler_path=poppler_path
        )
        file_name = name.split(".")[0]
        for i, image in enumerate(images):
            image.save(f"{output_folder}\\{file_name}_{i}.jpg", "JPEG")


def pdf_to_word(pdf_file, docx_file):
    # 创建一个PDF到DOCX的转换器
    cv = Converter(pdf_file)

    # 执行转换
    cv.convert(docx_file, start=0, end=None)

    # 关闭转换器
    cv.close()


def pdf_to_word_bytes(pdf_file):
    # 创建一个PDF到DOCX的转换器
    cv = Converter(pdf_file)
    byte_stream = BytesIO()
    # 执行转换
    cv.convert(byte_stream, start=0, end=None)

    # 关闭转换器
    cv.close()

    # 将字节流指针移到开始位置
    byte_stream.seek(0)
    return byte_stream.getvalue()  # 返回字节流内容


def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


def text_to_word(text, word_path):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(word_path)


def convert_pdf_to_word(pdf_path, word_path):
    text = pdf_to_text(pdf_path)
    text_to_word(text, word_path)


if __name__ == "__main__":
    pdfpath1 = r"E:\工作文档\资料标准文件\201902-第三次全国国土调查技术规程.pdf"
    word = r"E:\工作文档\资料标准文件\303-自然资源监测培训ppt及材料\SZY材料\0808\02-技术规程及北京培训PPT\水资源基础调查技术规定与野外安全手册\水资源基础调查技术规定第2部分：地表液态水储存量调查.docx"
    res = pdf_to_word_bytes(pdfpath1)
    pass
