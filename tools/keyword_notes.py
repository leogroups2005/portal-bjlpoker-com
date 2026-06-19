from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime

# Sample data associated with the configuration
EXAMPLE_URL = "https://portal-bjlpoker.com"
CORE_KEYWORD = "百家乐"

@dataclass
class KeywordNote:
    """Represents a structured note for a specific keyword."""
    keyword: str
    title: str
    content: str
    url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.url is None:
            self.url = EXAMPLE_URL

    def summary(self) -> str:
        """Return a short summary line."""
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.keyword}] {self.title} | Tags: {tag_str}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert the note to a dictionary for serialization."""
        return asdict(self)


@dataclass
class NoteCollection:
    """A collection of keyword notes with formatting utilities."""
    notes: List[KeywordNote] = field(default_factory=list)
    category: str = "General"

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        """Return notes whose keyword matches exactly."""
        return [n for n in self.notes if n.keyword == keyword]

    def format_notes_as_text(self) -> str:
        """Return a readable text representation of all notes."""
        lines = [f"Note Collection: {self.category}"]
        lines.append("=" * 50)
        for i, note in enumerate(self.notes, 1):
            lines.append(f"{i}. {note.summary()}")
            lines.append(f"   URL: {note.url}")
            lines.append(f"   Created: {note.created_at}")
            lines.append(f"   Content Preview: {note.content[:60]}...")
            lines.append("")
        return "\n".join(lines)

    def format_notes_as_html(self) -> str:
        """Return a basic HTML representation of the notes."""
        html_parts = [
            "<!DOCTYPE html>",
            "<html><head><meta charset='utf-8'><title>Keyword Notes</title></head><body>",
            f"<h1>Note Collection: {self.category}</h1>",
            "<ul>"
        ]
        for note in self.notes:
            safe_content = note.content.replace("<", "&lt;").replace(">", "&gt;")
            html_parts.append(
                f"<li><strong>{note.keyword}</strong>: {note.title} "
                f"(<a href='{note.url}'>link</a>) "
                f"<p>{safe_content[:100]}</p></li>"
            )
        html_parts.append("</ul></body></html>")
        return "\n".join(html_parts)


def demo_notes() -> NoteCollection:
    """Create a sample collection of keyword notes for demonstration."""
    collection = NoteCollection(category="Demo Notes")

    note1 = KeywordNote(
        keyword=CORE_KEYWORD,
        title="百家乐基础规则",
        content="百家乐是一种在亚洲非常流行的纸牌游戏。玩家可以选择庄家或闲家下注，目标是猜中哪一方牌点更接近9。",
        tags=["游戏", "规则", CORE_KEYWORD],
        url=EXAMPLE_URL
    )
    note2 = KeywordNote(
        keyword=CORE_KEYWORD,
        title="百家乐策略分析",
        content="虽然百家乐主要依赖运气，但一些玩家会使用趋势分析或下注模式来制定策略。",
        tags=["策略", "分析", CORE_KEYWORD]
    )
    note3 = KeywordNote(
        keyword="扑克",
        title="扑克与百家乐的区别",
        content="扑克需要更多技巧和读人能力，而百家乐更偏向随机性。",
        tags=["对比", "扑克", CORE_KEYWORD]
    )
    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)
    return collection


if __name__ == "__main__":
    # Run a quick demo
    demo = demo_notes()
    print(demo.format_notes_as_text())
    print("\n--- HTML Output ---\n")
    print(demo.format_notes_as_html())