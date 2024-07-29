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

## 2. Identify Circular Relationships

Find cycles involving entities and intermediaries, which might indicate circular ownership or involvement.

```
g.V().hasLabel('Entity').as('e')
  .repeat(bothE().otherV().simplePath()).until(hasId('e'))
  .path()
```

## 3. Detect Entities Connected via Multiple Intermediaries

Identify entities that are connected through multiple intermediaries or officers.

```
g.V().hasLabel('Entity').as('e1')
  .repeat(bothE('intermediary_of', 'officer_of').otherV().simplePath()).times(2)
  .emit()
  .hasLabel('Entity').as('e2')
  .where('e1', neq('e2'))
  .select('e1', 'e2')
  .by('n.name')
```

## 4. Find Entities Registered at the Same Address

Identify entities registered at the same address, which might indicate attempts to hide relationships.

```
g.V().hasLabel('Address').as('a')
  .in('registered_address').as('e')
  .select('a', 'e')
  .by('n.address')
  .by('n.name')
  .groupCount().by(select('a'))
  .order(local).by(values, desc)
```
