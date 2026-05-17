"""Lazy LLM wrappers (framework-canonical).

Defers LLM construction until first attribute access so Lambda cold-start
does not pay for unused providers. Routes by user-supplied key prefix via
the provider adapter at chalicelib/llm/provider_adapter.py.
"""
# TODO: implement lazy proxies that pick the user-supplied provider per session
