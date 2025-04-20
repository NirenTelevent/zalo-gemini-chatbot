import os

from docx import Document


# === Đọc nội dung từ file Word (demo_data.docx trong thư mục /data) ===
def load_doc_knowledge(docx_path="data/demo_data.docx"):
    if not os.path.exists(docx_path):
        return ""
    doc = Document(docx_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

# Tải nội dung tài liệu nội bộ
DOC_KNOWLEDGE = load_doc_knowledge()

def agent_tracuu_tailieu(user_question: str):
    """
    Agent tra cứu thông tin trong DOC_KNOWLEDGE (nội dung từ tài liệu nội bộ).
    Nếu câu hỏi chứa từ khóa đặc thù → trả lại nội dung phù hợp.
    Nếu không liên quan → trả lại None.
    """
    keywords = [
        "ngành", "đào tạo", "điểm chuẩn", "học phí", "học bổng",
        "cơ sở vật chất", "thư viện", "ký túc xá", "khoa", "chuyên ngành"
    ]
    lower_q = user_question.lower()
    if any(kw in lower_q for kw in keywords):
        return f"(📘 Trích xuất từ tài liệu nội bộ)\n{DOC_KNOWLEDGE}"
    return None