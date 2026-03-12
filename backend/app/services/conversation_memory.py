from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path

class ConversationMemory:
    """Track conversation history for follow-up questions"""
    
    def __init__(self, storage_path: str = "data/conversations"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.sessions = {}
    
    def create_session(self, session_id: str) -> Dict:
        """Create new conversation session"""
        self.sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "context_summary": ""
        }
        return self.sessions[session_id]
    
    def add_message(self, session_id: str, question: str, answer: str, 
                    citations: List[Dict], metadata: Dict = None):
        """Add Q&A to session history"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        self.sessions[session_id]["messages"].append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "citations": citations,
            "metadata": metadata or {}
        })
        
        self._save_session(session_id)
    
    def get_context(self, session_id: str, last_n: int = 3) -> str:
        """Get recent conversation context for follow-up questions"""
        if session_id not in self.sessions:
            return ""
        
        messages = self.sessions[session_id]["messages"][-last_n:]
        
        context = "Previous conversation:\n"
        for msg in messages:
            context += f"Q: {msg['question']}\nA: {msg['answer'][:200]}...\n\n"
        
        return context
    
    def resolve_followup(self, session_id: str, question: str) -> str:
        """Expand follow-up questions with context"""
        if session_id not in self.sessions or not self.sessions[session_id]["messages"]:
            return question
        
        # Check if question is a follow-up (contains pronouns, references)
        followup_indicators = ['it', 'this', 'that', 'they', 'these', 'those', 'also', 'additionally']
        
        if any(indicator in question.lower().split() for indicator in followup_indicators):
            last_msg = self.sessions[session_id]["messages"][-1]
            return f"Context: {last_msg['question']}\n\nFollow-up: {question}"
        
        return question
    
    def _save_session(self, session_id: str):
        """Persist session to disk"""
        session_file = self.storage_path / f"{session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(self.sessions[session_id], f, indent=2)
    
    def load_session(self, session_id: str) -> Optional[Dict]:
        """Load session from disk"""
        session_file = self.storage_path / f"{session_id}.json"
        if session_file.exists():
            with open(session_file, 'r') as f:
                self.sessions[session_id] = json.load(f)
            return self.sessions[session_id]
        return None
