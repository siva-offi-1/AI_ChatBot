from app.retrieval import MarkdownRetriever

def test_indexes_multiple_markdown_files(tmp_path):
    (tmp_path / "attendance_policy.md").write_text("# Attendance\n\nOffice hours are 8 AM to 5 PM.", encoding="utf-8")
    (tmp_path / "leave_policy.md").write_text("# Leave\n\nAnnual leave is 24 days.", encoding="utf-8")
    r = MarkdownRetriever(tmp_path, top_k=3, threshold=0.0)
    assert r.load_documents() == 2
    assert r.search("office hours")[0]["source"] == "attendance_policy.md"
