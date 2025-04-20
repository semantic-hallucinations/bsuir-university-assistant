class BatchedTexts:
    """Represents batched grouping of texts."""

    def __init__(self, texts: list[str], batch_size: int):
        self._texts = texts
        self._batch_size = batch_size

    def __iter__(self):
        batch = []
        for text in self._texts:
            batch.append(text)
            if len(batch) == self._batch_size:
                yield batch
                batch = []

        if batch:
            yield batch

    def as_list(self):
        return [
            self._texts[begin : begin + self._batch_size]
            for begin in range(0, len(self._texts), self._batch_size)
        ]
