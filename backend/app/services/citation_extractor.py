from typing import List, Dict
import re

class CitationExtractor:
    """Extract and validate citations from generated answers"""
    
    def extract_citations(self, answer: str, retrieval_results: Dict) -> tuple[str, List[Dict]]:
        """
        Extract citations from answer and link to source chunks.
        Returns: (answer_with_links, citations_list)
        """
        
        citations = []
        citation_map = {}
        
        # Find citation patterns: [Source: filename] or [1]
        citation_pattern = r'\[(?:Source:\s*)?([^\]]+)\]'
        matches = re.finditer(citation_pattern, answer)
        
        for match in matches:
            citation_text = match.group(1)
            
            # Find matching source in retrieval results
            for query, results in retrieval_results.items():
                for result in results:
                    source = result["metadata"].get("source", "")
                    section = result["metadata"].get("section", "")
                    
                    if citation_text.lower() in source.lower():
                        citation_key = f"{source}_{section}"
                        
                        if citation_key not in citation_map:
                            citation_map[citation_key] = {
                                "id": len(citations) + 1,
                                "source": source,
                                "section": section,
                                "relevance": result["score"],
                                "text_preview": result["text"][:200] + "..."
                            }
                            citations.append(citation_map[citation_key])
        
        # Replace citations with numbered references
        def replace_citation(match):
            citation_text = match.group(1)
            for cit in citations:
                if citation_text.lower() in cit["source"].lower():
                    return f"[{cit['id']}]"
            return match.group(0)
        
        answer_with_refs = re.sub(citation_pattern, replace_citation, answer)
        
        return answer_with_refs, citations
    
    def validate_citations(self, answer: str, context: str) -> Dict:
        """Check if claims in answer are supported by context"""
        
        # Extract sentences from answer
        sentences = re.split(r'[.!?]+', answer)
        
        validation = {
            "total_claims": len(sentences),
            "supported_claims": 0,
            "unsupported_claims": []
        }
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short sentences
                continue
            
            # Simple check: are key terms from sentence in context?
            key_terms = self._extract_key_terms(sentence)
            terms_in_context = sum(1 for term in key_terms if term.lower() in context.lower())
            
            if terms_in_context >= len(key_terms) * 0.5:  # 50% threshold
                validation["supported_claims"] += 1
            else:
                validation["unsupported_claims"].append(sentence)
        
        validation["support_ratio"] = (
            validation["supported_claims"] / validation["total_claims"]
            if validation["total_claims"] > 0 else 0
        )
        
        return validation
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract important terms (simplified - use NLP in production)"""
        # Remove common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        words = re.findall(r'\b\w+\b', text.lower())
        return [w for w in words if w not in stopwords and len(w) > 3]
