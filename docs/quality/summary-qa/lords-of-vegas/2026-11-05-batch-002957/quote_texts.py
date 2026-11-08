"""Read actual quote payloads from the retained raw JSON schemas."""


def quote_texts(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [text for item in value for text in quote_texts(item)]
    if isinstance(value, dict):
        # A quote record can carry its text alongside heading/reference metadata.
        for key in ['text', 'quote', 'content', 'verbatim_quote']:
            if key in value:
                return quote_texts(value[key])
        # A heading-keyed dictionary stores the actual passages in its values.
        return [text for item in value.values() for text in quote_texts(item)]
    raise TypeError(f'Unsupported operative quote payload: {type(value).__name__}')
