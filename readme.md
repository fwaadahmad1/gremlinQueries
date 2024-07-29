# Gremlin Queries for Fraud Detection

This document provides Gremlin queries to detect potential fraudulent activities in a graph database. The queries are designed to work with a graph schema that includes nodes with labels: `Entity`, `Intermediary`, `Address`, and `Officer`, and edges with labels: `intermediary_of`, `registered_address`, and `officer_of`. Node properties start with `n.` and edge properties start with `r.`.

## 1. Identify Entities with Many Intermediaries

Detect entities that are connected to many intermediaries, which might indicate complex structures.

```gremlin
g.V().hasLabel('Entity').as('e')
  .in('intermediary_of').as('i')
  .select('e', 'i')
  .by('n.name')
  .by('n.name')
  .groupCount().by(select('e'))
  .order(local).by(values, desc)
```
