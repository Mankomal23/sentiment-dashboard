import time
import hashlib
from transformers import pipeline as hf_pipeline

class SentimentPipeline:
    """
    3-class sentiment pipeline using Cardiff RoBERTa.
    Natively outputs positive / negative / neutral — no heuristic mapping needed.
    """

    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    # Model outputs these raw labels → map to clean names
    LABEL_MAP = {
        "positive": "positive",
        "negative": "negative",
        "neutral":  "neutral",
        # fallback for older label format
        "label_0": "negative",
        "label_1": "neutral",
        "label_2": "positive",
    }

    def __init__(self):
        print(f"Loading model: {self.model_name}")
        self._sentiment = hf_pipeline(
            "text-classification",
            model=self.model_name,
            truncation=True,
            max_length=512,
        )
        self._topics = {
            "product quality": ["quality", "build", "material", "durable", "broken", "defect"],
            "customer service": ["support", "service", "agent", "help", "response", "staff"],
            "delivery": ["shipping", "delivery", "arrived", "package", "fast", "slow", "delay"],
            "price & value": ["price", "worth", "expensive", "cheap", "value", "cost", "refund"],
            "user experience": ["easy", "use", "interface", "setup", "install", "intuitive"],
        }
        print("Pipeline ready.")

    def _detect_topics(self, text: str) -> list[str]:
        text_lower = text.lower()
        matched = [topic for topic, kws in self._topics.items() if any(kw in text_lower for kw in kws)]
        return matched if matched else ["general"]

    def analyze(self, text: str) -> dict:
        t0 = time.time()
        result = self._sentiment(text)[0]
        latency_ms = round((time.time() - t0) * 1000, 1)

        # raw_label = result["label"].lower()
        # sentiment = self.LABEL_MAP.get(raw_label, raw_label)
        raw_label = result["label"].lower()
        print(f"DEBUG: raw_label='{raw_label}' score={result['score']}")
        sentiment = self.LABEL_MAP.get(raw_label, raw_label)
        score = round(result["score"], 4)

        return {
            "id": hashlib.md5(f"{text}{time.time()}".encode()).hexdigest()[:8],
            "text": text[:300],
            "sentiment": sentiment,
            "score": score,
            "topics": self._detect_topics(text),
            "latency_ms": latency_ms,
            "timestamp": int(time.time() * 1000),
        }