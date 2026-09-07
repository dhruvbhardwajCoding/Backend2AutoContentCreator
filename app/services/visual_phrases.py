import re
import os
import numpy as np
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.models.schemas import VisualPhrasesRequest, VisualPhrasesResponse

# Load model once at module level
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    return _model

# Generic concepts to filter out
GENERIC_WORDS = {
    'person', 'people', 'thing', 'things', 'life', 'something', 'everything',
    'nothing', 'anyone', 'everyone', 'somebody', 'way', 'time', 'day', 'world',
    'stuff', 'lot', 'kind', 'sort', 'bit', 'part',
}

def _split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    # Filter out very short fragments
    return [s.strip() for s in sentences if len(s.strip()) > 15]

def _cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

def _to_visual_phrase(sentence: str) -> str:
    """Convert a sentence into a concise visual search phrase."""
    stop_words = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'shall', 'can', 'need', 'dare', 'ought',
        'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
        'as', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'between', 'out', 'off', 'over', 'under', 'again', 'further', 'then',
        'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'both',
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just',
        'because', 'but', 'and', 'or', 'if', 'while', 'about', 'that', 'this',
        'these', 'those', 'it', 'its', 'you', 'your', 'we', 'our', 'they',
        'their', 'i', 'me', 'my', 'he', 'him', 'his', 'she', 'her',
        "it's", "that's", "don't", "doesn't", "didn't", "won't", "can't",
        "isn't", "aren't", "wasn't", "weren't", "what's",
    }
    
    words = re.findall(r"[a-zA-Z']+", sentence.lower())
    meaningful = [w for w in words if w not in stop_words and w not in GENERIC_WORDS and len(w) > 2]
    
    phrase_words = meaningful[:6]
    if not phrase_words:
        return sentence[:50]
    
    return ' '.join(phrase_words)

def extract_visual_phrases(request_data: VisualPhrasesRequest) -> VisualPhrasesResponse:
    """Extract visually meaningful phrases from a script using semantic analysis."""
    model = _get_model()
    
    sentences = _split_sentences(request_data.script)
    
    if not sentences:
        return VisualPhrasesResponse(phrases=[request_data.topic])
    
    topic_embedding = model.embed_query(request_data.topic)
    sentence_embeddings = model.embed_documents(sentences)
    
    scored = []
    for i, (sent, emb) in enumerate(zip(sentences, sentence_embeddings)):
        similarity = _cosine_similarity(topic_embedding, emb)
        scored.append((i, sent, similarity, emb))
    
    scored.sort(key=lambda x: x[2], reverse=True)
    
    selected = []
    selected_embeddings = []
    
    for idx, sent, score, emb in scored:
        if len(selected) >= 6:
            break
        
        is_diverse = True
        for sel_emb in selected_embeddings:
            if _cosine_similarity(emb, sel_emb) > 0.85:
                is_diverse = False
                break
        
        if is_diverse:
            phrase = _to_visual_phrase(sent)
            if phrase and len(phrase) > 5:
                selected.append(phrase)
                selected_embeddings.append(emb)
    
    if len(selected) < 4:
        topic_phrase = _to_visual_phrase(request_data.topic)
        if topic_phrase not in selected:
            selected.append(topic_phrase)
    
    return VisualPhrasesResponse(phrases=selected[:6])
