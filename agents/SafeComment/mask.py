from dataclasses import dataclass

from loguru import logger

@dataclass
class SafeCommentAgent:
    """Safe Comment Agent"""
    banned_words = ["fuck", "doggy"]
    filter_text = '[MASKED]'

    def masking_text(self, input_comment: str) -> tuple[str, bool, bool]:
        """
        Masks the input comment by replacing banned words with a filter text.
        Args:
            input_comment (str): The comment to be processed.
        Returns:
            tuple[str, bool, bool]: A tuple containing:
                - masked_comment (str): The comment with banned words replaced by the filter text.
                - has_toxic_word (bool): True if the comment contains any banned words, False otherwise.
                - is_safe (bool): True if the comment does not contain any banned words, False otherwise.
        """
        words = input_comment.split()
        has_toxic_word = any(word in self.banned_words for word in words)
        
        masked_comment = ' '.join(
            self.filter_text if word in self.banned_words else word
            for word in words
        )
        
        return masked_comment, has_toxic_word, not has_toxic_word
